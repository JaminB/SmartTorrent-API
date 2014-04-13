#!/usr/bin/python

from analysis import SearchAnalysis

analysis = SearchAnalysis("resultCacheHolder")
print analysis._unpack_list("good phrases", True)
