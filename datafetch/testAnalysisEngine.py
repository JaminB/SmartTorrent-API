#!/usr/bin/python

from analysis import CommentAnalysis

analysis = CommentAnalysis("Audio: 10, Video: 10")
#print analysis._unpack_list("good phrases", True)
analysis.build_cache()
print analysis.get_cache()
