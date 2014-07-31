from settings import config
import os

cache = config.variables.get("search_cache")
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
