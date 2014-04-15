#!/usr/bin/python

from analysis import CommentAnalysis

analysis = CommentAnalysis("This is awsome, really like it!, huge fan.")
#print analysis._unpack_list("good phrases", True)
analysis.build_cache()
