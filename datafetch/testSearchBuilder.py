#!/usr/bin/python

import sys
import searchbuilder

cache = searchbuilder.Search("test","other")
cache.build_cache()
print cache.get_cache().to_json()
