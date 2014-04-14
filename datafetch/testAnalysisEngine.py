#!/usr/bin/python

from analysis import SearchAnalysis

analysis = SearchAnalysis("resultCacheHolder")
#print analysis._unpack_list("good phrases", True)
analysis.analyze_comment("incredable! awsome! this is so great! Thank you so much for this amzing upload!")
