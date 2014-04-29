#!/usr/bin/python
from analysis import CommentAnalysis
from analysis import Signatures
from analysis import Wordlist

analysis = CommentAnalysis("AWESOME for a cam !!")
#print analysis._unpack_list("good phrases", True)
analysis.build_cache()
analysis.get_cache()
signatures = Signatures(analysis.get_cache())
#print signatures.sig_rated_content()
#print signatures.create_signature("Malware Detected", signatures.get_custom_words_in_comment(["malware", "virus"]))
wordlist = Wordlist()
print analysis.get_cache()
#print wordlist.get_good_words_weighted()
#print signatures.sig_cease_and_decist()
#print signatures.sig_good_quality()
#print signatures.sig_bad_quality()
#print signatures.sig_malware()
#print signatures.sig_rated_content()
