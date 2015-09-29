include_directories (${libmpong_DIR}/include ${GTEST_ROOT}/include)
add_executable (libmpongtest ball_test.cpp)

target_link_libraries (
	libmpongtest
	libmpong
	gtest_main
	gtest
	pthread
    )