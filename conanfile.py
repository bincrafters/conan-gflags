from conans import ConanFile, CMake, tools


class GflagsConan(ConanFile):
    name = "gflags"
    version = "v2.2.1"
    license = "MIT License"
    url = "gflags"
    description = "The gflags package contains a C++ library that implements commandline flags processing. "
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=False"
    generators = "cmake"

    def source(self):
        self.run("git clone https://github.com/gflags/gflags.git")
        self.run("cd gflags && git checkout -b v2.2.1-conan v2.2.1")
        #self.run("git checkout -b v2.2.1-conan v2.2.1")
        # This small hack might be useful to guarantee proper /MT /MD linkage in MSVC
        # if the packaged project doesn't have variables to set it properly
        tools.replace_in_file("gflags/CMakeLists.txt", "include (CheckCXXSymbolExists)", '''include (CheckCXXSymbolExists)
include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()''')

    def build(self):
        cmake = CMake(self)
        self.run('cmake gflags %s' % cmake.command_line)
        self.run("cmake --build . %s" % cmake.build_config)

    def package(self):
        self.copy("*.h", dst="include/gflags", src="include/gflags")
        self.copy("*.dll", dst="bin", keep_path=False)
        self.copy("*.so", dst="lib", keep_path=False)
        self.copy("*.dylib", dst="lib", keep_path=False)
        self.copy("*.a", dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ["gflags"]
