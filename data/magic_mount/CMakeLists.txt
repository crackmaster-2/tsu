cmake_minimum_required (VERSION 3.6)


set (CMAKE_CXX_STANDARD 17)


project (mm)
# The version number.
set (Tutorial_VERSION_MAJOR 1)
set (Tutorial_VERSION_MINOR 0)
 
include_directories(include)
include_directories(utils/include)
 
# add the binary tree to the search path for include files
# so that we will find TutorialConfig.h
include_directories("${PROJECT_BINARY_DIR}")
 
# add the executable
add_executable(mm core/bootstages.cpp utils/xwrap.cpp utils/logging.cpp utils/file.cpp utils/missing.cpp utils/selinux.cpp)

target_link_libraries(mm log)