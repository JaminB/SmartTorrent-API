#!/usr/bin/python

import sys
import searchbuilder

cache = searchbuilder.Search("captain america","movie")
cache.build_cache()
print cache.get_cache().to_json()
