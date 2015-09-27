include(ExternalProject)

add_subdirectory(libmpong)

ExternalProject_Add(
	gtest 
	URL https://googletest.googlecode.com/files/gtest-1.7.0.zip 
	INSTALL_COMMAND ""
)
