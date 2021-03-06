from settings import config
from content import dbconnect
import MySQLdb
import os

cache = config.variables.get("search_cache")
db_table_cache = config.variables.get("db_table_cache")
db_user = config.variables.get("db_user")
db_password = config.variables.get("db_password")
db_server = config.variables.get("db_server")

searches = []
def _list_searches_in_cache():
	files = []
	files = os.listdir(cache)
	for file in files:
		if len(file) == 32:
			searches.append(file)
	return searches

def check_exists_by_hash(hash):
	_list_searches_in_cache()
	if hash in searches:	
		return True
	return False

def open_search_by_hash(hash):
	try:
		search = open(cache+hash, "r")
		return search.read()
	except Exception,e:
		print str(e)
		return "No result cached"

def get_size_by_hash(hash):
	try:
		return os.path.getsize(cache+hash)
	except Exception, e:
		return "Could not derive size of cached search"
#Database Cache Operations

def db_open_search_by_hash(hash):
	database = dbconnect.Connect(db_server,db_user,db_password,db_table_cache)
	query = database.run_query('SELECT data FROM cache.searches WHERE id=' +'"'+hash+'"'+ ';')
	output = ''
	for row in query:
		output+=row[0]
	return output

def db_get_size_by_hash(hash):
	database = dbconnect.Connect(db_server,db_user,db_password,db_table_cache)
	try:
		return database.run_query('SELECT LENGTH(data) FROM cache.searches WHERE id=' +'"'+hash+'"'+ ';')[0][0]
	except:
		return 0

def db_check_exists_by_hash(hash):
	return bool(db_get_size_by_hash(hash))

def db_persist_search(hash,data):
	database = dbconnect.Connect(db_server,db_user,db_password,db_table_cache)
	if db_check_exists_by_hash(hash):
		#database.run_query('UPDATE cache.searches SET data='+'"'+data+'"'+' WHERE id=' +'"'+str(MySQLdb.escape_string(hash))+'"'+";")
		database.run_query('DELETE from cache.searches WHERE id='+'"'+hash+'"'+";")
		database.run_query('INSERT INTO cache.searches VALUES('+'"'+hash+'"'+","+'"'+str(MySQLdb.escape_string(data))+'"' +');')
	else:
		database.run_query('INSERT INTO cache.searches VALUES('+'"'+hash+'"'+","+'"'+str(MySQLdb.escape_string(data))+'"' +');')

