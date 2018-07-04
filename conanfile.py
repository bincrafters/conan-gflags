#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, CMake, tools
import os


class GflagsConan(ConanFile):
    name = "gflags"
    version = "2.2.1"
    description = "The gflags package contains a C++ library that implements commandline flags processing. "
    url = "https://github.com/bincrafters/conan-gflags"
    license = 'BSD 3-clause'
    exports = ["LICENSE.md"]
    exports_sources = ["CMakeLists.txt", "Findgflags.cmake"]
    source_subfolder = "source_subfolder"
    generators = "cmake"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "fPIC": [True, False], "nothreads": [True, False], "namespace": "ANY"}
    default_options = "shared=False", "fPIC=True", "nothreads=True", "namespace=gflags"

    def configure(self):
        if self.settings.os == "Windows":
            self.options.remove("fPIC")

    def source(self):
        source_url = "https://github.com/gflags/gflags"
        tools.get("{0}/archive/v{1}.tar.gz".format(source_url, self.version))
        os.rename("%s-%s" % (self.name, self.version), self.source_subfolder)

    def build(self):
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

        if self.settings.os != "Windows":
            cmake.definitions['CMAKE_POSITION_INDEPENDENT_CODE'] = self.options.fPIC
        cmake.configure()
        cmake.build()
        cmake.install()

    def package(self):
        self.copy("Findgflags.cmake", ".", ".")
        self.copy("COPYING.txt", dst="licenses", src=self.source_subfolder)

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
        if self.settings.os == "Windows":
            self.cpp_info.libs.extend(['shlwapi'])
        else:
            self.cpp_info.libs.extend(["pthread"])
