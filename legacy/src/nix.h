#include <cerrno> 
#include <cstdio> 
#include <cstring> 
#include <string> 
#include <vector>


static const char USAGE[] = R"***(
A su wrapper for termux. 

Usage: tsu
    tsu -h | --help | --version
    
Options: 
    -h --help Show this screen. 
    --version Show version.  
)***";

namespace nix {

int execvpe(const std::string &path, const std::vector<std::string> &argv);

int execvpe(const std::vector<std::string> &argv); 

}