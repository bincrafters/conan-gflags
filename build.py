#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bincrafters import build_template_default
from copy import deepcopy


if __name__ == "__main__":

    builder = build_template_default.get_builder(pure_c=False)
    builds = list(builder.items)
    thread_builds = deepcopy(builds)
    for build in thread_builds:
        build.options['gflags:nothreads'] = False
    builder.items.extend(thread_builds)
    builder.run()
