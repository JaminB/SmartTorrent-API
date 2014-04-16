#!/usr/bin/python

from analysis import CommentAnalysis

analysis = CommentAnalysis("This is a test, thanks!")
#print analysis._unpack_list("good phrases", True)
analysis.build_cache()
print analysis.get_cache()
