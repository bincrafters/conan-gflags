#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, CMake, tools
import os

class GflagsConan(ConanFile):
    name = "gflags"
    version = "2.2.1"
    license = 'BSD 3-clause "New" or "Revised" License'
    url = "gflags"
    description = "The gflags package contains a C++ library that implements commandline flags processing. "
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "fPIC": [True, False], "nothreads": [True, False]}
    default_options = "shared=True", "fPIC=True", "nothreads=True"
    generators = "cmake"
    exports_sources = ["CMakeLists.txt", "Findgflags.cmake"]

    def configure(self):

        if not self.options.shared:
            raise tools.ConanException("Static builds are not supported for the gflags package for the time being.")
        
        del self.settings.compiler.libcxx
        
        if self.settings.os == "Windows":
            self.options.remove("fPIC")

    def source(self):
        source_url = "https://github.com/gflags/gflags"
        tools.get("{0}/archive/v{1}.tar.gz".format(source_url, self.version))
        os.rename("%s-%s" % (self.name, self.version), "sources")

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
        
        if self.settings.os != "Windows":
            cmake.definitions['CMAKE_POSITION_INDEPENDENT_CODE'] = self.options.fPIC
        cmake.configure()
        cmake.build()
        cmake.install()

    def package(self):
        self.copy("Findgflags.cmake", ".", ".")
        self.copy("sources/copying*", dst="licenses",  ignore_case=True, keep_path=False)

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)

