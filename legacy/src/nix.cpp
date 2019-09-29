#include <cerrno>
#include <string>
#include <vector> 
#include <unistd.h>


#include "nix.h"

using namespace nix; 

int nix::execvpe(const std::string &path, const std::vector<std::string> &argv) { 
/* Convert arguments to C-style and call execv. If it returns * (fails), clean up and pass return value to caller. */


if (argv.size() == 0) { 
errno = EINVAL; 
return -1; }

 std::vector<char *> vec_cp; vec_cp.reserve(argv.size() + 1);
  for (auto s : argv) vec_cp.push_back(strdup(s.c_str()));
  
   vec_cp.push_back(NULL); 
   
   int retval = execv(path.c_str(), vec_cp.data()); 
   int save_errno = errno; 
   
   for (auto p : vec_cp) free(p); 
   errno = save_errno; 
   return retval; 
   
  }
  
  
 
 