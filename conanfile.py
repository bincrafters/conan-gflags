#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, CMake, tools
import os


class GflagsConan(ConanFile):
    name = "gflags"
    version = "2.2.1"
    description = "The gflags package contains a C++ library that implements commandline flags processing"
    topics = ("conan", "gflags", "cli", "flags")
    url = "https://github.com/bincrafters/conan-gflags"
    homepage = "https://github.com/gflags/gflags"
    license = 'BSD-3-Clause'
    exports = ["LICENSE.md"]
    exports_sources = ["CMakeLists.txt", "Findgflags.cmake"]
    generators = "cmake"

    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "fPIC": [True, False], "nothreads": [True, False], "namespace": "ANY"}
    default_options = {'shared': False, 'fPIC': True, 'nothreads': True, 'namespace': 'gflags'}

    _source_subfolder = "source_subfolder"
    _build_subfolder = "build_subfolder"

    def configure(self):
        if self.settings.os == "Windows":
            self.options.remove("fPIC")

    def source(self):
        sha256 = "ae27cdbcd6a2f935baa78e4f21f675649271634c092b1be01469440495609d0e"
        tools.get("{0}/archive/v{1}.tar.gz".format(self.homepage, self.version), sha256=sha256)
        os.rename("%s-%s" % (self.name, self.version), self._source_subfolder)

    def _configure_cmake(self):
        cmake = CMake(self)
        cmake.definitions["BUILD_SHARED_LIBS"] = self.options.shared
        cmake.definitions["BUILD_STATIC_LIBS"] = not self.options.shared
        cmake.definitions["BUILD_gflags_LIB"] = not self.options.nothreads
        cmake.definitions["BUILD_gflags_nothreads_LIB"] = self.options.nothreads
        cmake.definitions["BUILD_PACKAGING"] = False
        cmake.definitions["BUILD_TESTING"] = False
        cmake.definitions["INSTALL_HEADERS"] = True
        cmake.definitions["INSTALL_SHARED_LIBS"] = self.options.shared
        cmake.definitions["INSTALL_STATIC_LIBS"] = not self.options.shared
        cmake.definitions["REGISTER_BUILD_DIR"] = False
        cmake.definitions["REGISTER_INSTALL_PREFIX"] = False
        cmake.definitions["GFLAGS_NAMESPACE"] = self.options.namespace
        cmake.configure(build_folder=self._build_subfolder)
        return cmake

    def build(self):
        cmake = self._configure_cmake()
        cmake.build()


    def package(self):
        self.copy(pattern="LICENSE", dst="licenses", src=self._source_subfolder)
        cmake = self._configure_cmake()
        cmake.install()

        self.copy("Findgflags.cmake", ".", ".")
        self.copy("COPYING.txt", dst="licenses", src=self._source_subfolder)

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
        if self.settings.os == "Windows":
            self.cpp_info.libs.extend(['shlwapi'])
        else:
            self.cpp_info.libs.extend(["pthread"])
