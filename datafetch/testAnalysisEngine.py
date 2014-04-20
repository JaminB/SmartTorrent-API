#!/usr/bin/python

from analysis import CommentAnalysis
from analysis import Signatures
analysis = CommentAnalysis("this is a good copy virus")
#print analysis._unpack_list("good phrases", True)
analysis.build_cache()
#print analysis.get_cache()
signatures = Signatures(analysis.get_cache())
#print signatures.sig_cease_and_decist()
#print signatures.sig_good_quality()
print signatures.sig_malware()
