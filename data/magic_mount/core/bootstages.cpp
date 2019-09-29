#include <sys/mount.h>
#include <sys/wait.h>
#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>
#include <fcntl.h>
#include <string.h>
#include <dirent.h>
#include <vector>
#include <string>
 

#include "logging.h"
#include "stream.h"
#include "defs.h"


using namespace std;

static char buf[PATH_MAX], buf2[PATH_MAX];

static int bind_mount(const char *from, const char *to, bool log = true);

/***************
 * Magic Mount *
 ***************/

 
#define VLOGI(tag, from, to) printf(" Magic Mount %s %s: %s\n", tag, from, to)

// Precedence: MODULE > SKEL > INTER > DUMMY
#define IS_DUMMY   0x01    /* mount from mirror */
#define IS_INTER   0x02    /* intermediate node */
#define IS_SKEL    0x04    /* replace with tmpfs */
#define IS_MODULE  0x08    /* mount from module */

#define IS_DIR(n)  ((n)->type == DT_DIR)
#define IS_LNK(n)  ((n)->type == DT_LNK)
#define IS_REG(n)  ((n)->type == DT_REG)

class node_entry {
public:
	explicit node_entry(const char *name, uint8_t type = DT_DIR, uint8_t status = IS_INTER)
			: module(nullptr), name(name), type(type), status(status), parent(nullptr) {}
	~node_entry();
	void create_module_tree(const char *module);
	void magic_mount();
	node_entry *extract(const char *name);

	static bool vendor_root;
	static bool product_root;

private:
	const char *module;    /* Only used when IS_MODULE */
	const string name;
	uint8_t type;
	uint8_t status;
	node_entry *parent;
	vector<node_entry *> children;

	node_entry(node_entry *parent, const char *module, const char *name, uint8_t type)
			: module(module), name(name), type(type), status(0), parent(parent) {}
	bool is_special();
	bool is_root();
	string get_path();
	void insert(node_entry *&);
	void clone_skeleton();
	int get_path(char *path);
};

bool node_entry::vendor_root = false;
bool node_entry::product_root = false;

node_entry::~node_entry() {
	for (auto &node : children)
		delete node;
}

#define SPECIAL_NODE (parent->parent ? false : \
((vendor_root && name == "vendor") || (product_root && name == "product")))

bool node_entry::is_special() {
	return parent ? SPECIAL_NODE : false;
}

bool node_entry::is_root() {
	return parent ? SPECIAL_NODE : true;
}

string node_entry::get_path() {
	get_path(buf);
	return buf;
}

int node_entry::get_path(char *path) {
	int len = 0;
	if (parent)
		len = parent->get_path(path);
	len += sprintf(path + len, "/%s", name.c_str());
	return len;
}

void node_entry::insert(node_entry *&node) {
	node->parent = this;
	for (auto &child : children) {
		if (child->name == node->name) {
			if (node->status > child->status) {
				// The new node has higher precedence
				delete child;
				child = node;
			} else {
				delete node;
				node = child;
			}
			return;
		}
	}
	children.push_back(node);
}


void node_entry::clone_skeleton() {
	DIR *dir;
	struct dirent *entry;

	// Clone the structure
	auto full_path = get_path();
	snprintf(buf, PATH_MAX, "%s%s", MIRRDIR, full_path.c_str());
	if (!(dir = xopendir(buf)))
		return;
	while ((entry = xreaddir(dir))) {
		if (entry->d_name == "."sv || entry->d_name == ".."sv)
			continue;
		// Create dummy node
		auto dummy = new node_entry(entry->d_name, entry->d_type, IS_DUMMY);
		insert(dummy);
	}
	closedir(dir);

	if (status & IS_SKEL) {
		file_attr attr;
		getattr(full_path.c_str(), &attr);
		LOGI("mnt_tmpfs : %s\n", full_path.c_str());
		xmount("tmpfs", full_path.c_str(), "tmpfs", 0, nullptr);
		setattr(full_path.c_str(), &attr);
	}

	for (auto &child : children) {
		snprintf(buf, PATH_MAX, "%s/%s", full_path.c_str(), child->name.c_str());

		// Create the dummy file/directory
		if (IS_DIR(child))
			xmkdir(buf, 0755);
		else if (IS_REG(child))
			close(creat(buf, 0644));
		// Links will be handled later
 if (child->status & (IS_SKEL | IS_INTER)) {
			// It's an intermediate folder, recursive clone
			child->clone_skeleton();
			continue;
		} else if (child->status & IS_DUMMY) {
			// Mount from mirror to dummy file
			snprintf(buf2, PATH_MAX, "%s%s/%s", MIRRDIR, full_path.c_str(), child->name.c_str());
		}

		if (IS_LNK(child)) {
			// Copy symlinks directly
			cp_afc(buf2, buf);
			VLOGI("copy_link ", buf2, buf);
		} else {
			snprintf(buf, PATH_MAX, "%s/%s", full_path.c_str(), child->name.c_str());
			bind_mount(buf2, buf);
		}
	}
}

void node_entry::magic_mount() {
	 if (status & IS_SKEL) {
		// The node is labeled to be cloned with skeleton, lets do it
		clone_skeleton();
	} else if (status & IS_INTER) {
		// It's an intermediate node, travel deeper
		for (auto &child : children)
			child->magic_mount();
	}
}

node_entry *node_entry::extract(const char *name) {
	node_entry *node = nullptr;
	// Extract the node out of the tree
	for (auto it = children.begin(); it != children.end(); ++it) {
		if ((*it)->name == name) {
			node = *it;
			node->parent = nullptr;
			children.erase(it);
			break;
		}
	}
	return node;
}

/*****************
 * Miscellaneous *
 *****************/

static int bind_mount(const char *from, const char *to, bool log) {
	int ret = xmount(from, to, nullptr, MS_BIND, nullptr);
	if (log) VLOGI("bind_mount", from, to);
	return ret;
}

#define MIRRMNT(part)   MIRRDIR "/" #part
#define PARTBLK(part)   BLOCKDIR "/" #part
#define DIR_IS(part)    (me->mnt_dir == "/" #part ""sv)

#define mount_mirror(part, flag) { \
	xstat(me->mnt_fsname, &st); \
	mknod(PARTBLK(part), (st.st_mode & S_IFMT) | 0600, st.st_rdev); \
	xmkdir(MIRRMNT(part), 0755); \
	xmount(PARTBLK(part), MIRRMNT(part), me->mnt_type, flag, nullptr); \
	VLOGI("mount", PARTBLK(part), MIRRMNT(part)); \
}

  

void unlock_blocks() {
	DIR *dir;
	struct dirent *entry;
	int fd, dev, OFF = 0;

	if (!(dir = xopendir("/dev/block")))
		return;
	dev = dirfd(dir);

	while((entry = readdir(dir))) {
		if (entry->d_type == DT_BLK) {
			if ((fd = openat(dev, entry->d_name, O_RDONLY | O_CLOEXEC)) < 0)
				continue;
			if (ioctl(fd, BLKROSET, &OFF) < 0)
				PLOGE("unlock %s", entry->d_name);
			close(fd);
		}
	}
	closedir(dir);
}

static bool log_dump = false;
static void dump_logs() {
	if (log_dump)
		return; 
}

/****************
 * Entry points *
 ****************/


 int   main(int argc, char const *argv[])
{
	/* code */
	
	printf("mm - magic mounter \n");
	
	auto sys_root = new node_entry("system");


		sys_root->magic_mount();
		
		// Directories in tmpfs overlay
	xmkdir(MAGISKTMP,0);
	xmkdir(MIRRDIR, 0);
	xmkdir(BLOCKDIR, 0);
	
	
	bool system_as_root = false;
	struct stat st;
	parse_mnt("/proc/mounts", [&](mntent *me) {
		
		 if ( DIR_IS(system)) {
			
		mount_mirror(system, MS_RDONLY);}
		return true;
	
		
		});
	
    
	// Cleanup memory
	
	return 0;
}
