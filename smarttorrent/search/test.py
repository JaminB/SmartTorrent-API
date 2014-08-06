import searchcache
from settings import config

print config.variables.get("db_password")
print config.variables.get("db_user")
print config.variables.get("db_server")
print config.variables.get("db_table_cache")
#print "UPDATE COMMAND"
#searchcache.db_persist_search("test2", "tasdasdflk;asdfkl;asdfl\nThis is a test")
#print searchcache.db_open_search_by_hash("f069baa731d8e94fb814321ab05f1a1e")
