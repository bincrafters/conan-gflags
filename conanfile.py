from conans import ConanFile, CMake, tools


class GflagsConan(ConanFile):
    name = "gflags"
    version = "2.2.1"
    license = "MIT License"
    url = "gflags"
    description = "The gflags package contains a C++ library that implements commandline flags processing. "
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = "shared=True", "fPIC=True"
    generators = "cmake"

    def source(self):
        source_url = "https://github.com/gflags/gflags"
        tools.get("{0}/archive/v{1}.tar.gz".format(source_url, self.version))

        # This small hack might be useful to guarantee proper /MT /MD linkage in MSVC
        # if the packaged project doesn't have variables to set it properly
        tools.replace_in_file("{0}-{1}/CMakeLists.txt".format(self.name, self.version),
                              "include (CheckCXXSymbolExists)", '''include (CheckCXXSymbolExists)
include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()''')

    def build(self):
        cmake = CMake(self)
        flags = []

        compiler = str(self.settings.compiler)
        if compiler in ("gcc", "clang", "apple-clang"):
            if self.settings.arch == 'x86':
                flags.append("-m32")
            else:
                flags.append("-m64")

            if self.options.fPIC:
                flags.append("-fPIC")

        self.output.info("arch: {0} flags {1}".format(self.settings.arch, flags))
        if compiler in ("clang", "apple-clang"):
            # without the following, compilation gets stuck indefinitely
            flags.append("-Wno-deprecated-declarations")

        cmake.definitions["CMAKE_C_FLAGS"] = " ".join(flags)
        cmake.definitions["CMAKE_CXX_FLAGS"] = cmake.definitions["CMAKE_C_FLAGS"]

        cmake.definitions["BUILD_SHARED_LIBS"] = self.options.shared

        cmake.configure(source_dir="{0}-{1}".format(self.name, self.version))
        cmake.build()
        cmake.install()


    def package(self):
        self.copy("*.h", dst="include/gflags", src="include/gflags")
        self.copy("*.dll", dst="bin", keep_path=False)
        self.copy("*.so", dst="lib", keep_path=False)
        self.copy("*.dylib", dst="lib", keep_path=False)
        self.copy("*.a", dst="lib", keep_path=False)
        self.copy("*.lib", dst="lib", keep_path=False)
        
    def package_info(self):
        if self.options.shared:
            self.cpp_info.libs = ["gflags"]
        else:
            self.cpp_info.libs = ["gflags_static"]
