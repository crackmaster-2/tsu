cmake_minimum_required(VERSION 3.8)

project (tsu VERSION 3.0.1)

set (TERMUX /data/data/com.termux/files/usr) 


find_package(docopt  REQUIRED)

 
add_executable(tsu libtsu.cpp nix.cpp)
target_link_libraries(tsu  docopt )
 
 install(TARGETS tsu DESTINATION bin)


 