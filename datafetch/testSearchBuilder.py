#!/usr/bin/python

import sys
import searchbuilder

cache = searchbuilder.Search("Woodkid","music")
cache.build_cache()
print cache.get_cache()
