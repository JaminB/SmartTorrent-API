#!/usr/bin/python

import sys
from search import searchbuilder

cacheBuilder = searchbuilder.Search("test","movie")
cacheBuilder.build_cache()
cache = cacheBuilder.get_cache()
cache.de_duplicate_cache()
cache.analyze_comments()
print cache.to_json()
