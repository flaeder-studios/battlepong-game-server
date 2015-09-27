cmake_minimum_required (VERSION 2.8)
project (multipong)

# The version number.
set (Tutorial_VERSION_MAJOR 1)
set (Tutorial_VERSION_MINOR 0)
set (CXX_EXTENSIONS_FLAGS "-std=c++11" )

enable_testing()

add_definitions(${CXX_EXTENSIONS_FLAGS})

add_subdirectory (libmpong)
# add_subdirectory (server)
# add_subdirectory (multipong)
add_subdirectory (test)
