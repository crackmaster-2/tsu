
#include <iostream>
#include <string>
#include <vector> 
#include <map>
#include <iterator>

#include "docopt.h"
#include "nix.h"


int main (int argc, const char* argv[]) {

// std::cout << USAGE;

std::vector<std::string> vargv;

for (int i = 1; i < argc; ++i) {
std::cout << argv[i] << std::endl; 
  vargv.push_back( 
  std::string(
  argv[i])); 
}
for (auto i: vargv) std::cout << i << ' ';

//std::map<std::string, docopt::value> args = docopt::docopt(USAGE,vargv, true,  "3.0");

// Defaults in Termux and Android
std::string TERMUX_FS="/data/data/com.termux/files/" ; 
std::string TERMUX_PREFIX=TERMUX_FS + "/usr" ;
std::string TERMUX_PATHS=TERMUX_PREFIX + "/bin:" + TERMUX_PREFIX + "/bin/applets" ;
std::string ROOT_HOME="/data/data/com.termux/files/root" ;
std::string ANDROIDSYSTEM_PATHS="/system/bin:/system/xbin" ;

std::string MAGISK_LOCATION = "/sbin/magisk";
std::string SU_LOCATION[] = { "/system,/xbin/su" };


std::cout << MAGISK_LOCATION;

std::vector<std::string> cmdx;
cmdx.push_back("su") ; 

nix::execvpe( MAGISK_LOCATION , cmdx) ;

return 0;
}
 
 