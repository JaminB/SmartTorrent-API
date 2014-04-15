#!/usr/bin/python

import sys
import searchbuilder

cacheBuilder = searchbuilder.Search("game of thrones","movie")
cacheBuilder.build_cache()
cache = cacheBuilder.get_cache()
cache.de_duplicate_cache()
cache.analyze_comments()
print cache.to_json()
