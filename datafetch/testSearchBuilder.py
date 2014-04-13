#!/usr/bin/python

import sys
import searchbuilder

cacheBuilder = searchbuilder.Search("Woodkid","music")
cacheBuilder.build_cache()
cache = cacheBuilder.get_cache()
cache.de_duplicate_cache()
print cache.to_json()
