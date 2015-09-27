include_directories (${libmpong_DIR}/include)
add_executable (libmpongtest ball_test.cpp)
target_link_libraries (libmpongtest libmpong gtest gtest_main pthread)