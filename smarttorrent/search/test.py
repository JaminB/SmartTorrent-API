import searchcache
from settings import config
from analysis import Wordlist
from analysis import CommentAnalysis
#wordlist = Wordlist()
#print wordlist.get_negators()
commentText = "Meech! You're the best mate. Awesome quality. Reasonable size too. Believe me, I've not bellied 10, 4 TB hard drives and it's time to care more about quality-compressed stuff."
commentAnalysis = CommentAnalysis(commentText)
commentAnalysis.build_cache()
comment = commentAnalysis.get_cache()
print comment.get_signatures()
#print comment.get_negator_words()
#print config.variables.get("db_password")
#print config.variables.get("db_user")
#print config.variables.get("db_server")
#print config.variables.get("db_table_cache")
#print "UPDATE COMMAND"
#searchcache.db_persist_search("test2", "tasdasdflk;asdfkl;asdfl\nThis is a test")
#print searchcache.db_open_search_by_hash("f069baa731d8e94fb814321ab05f1a1e")
