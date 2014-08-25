from settings import config
from content import dbconnect

db_table_logs = config.variables.get("db_table_log")
db_user = config.variables.get("db_user")
db_password = config.variables.get("db_password")
db_server = config.variables.get("db_server")
def db_insert_log_entry(ID, search, category):
	database = dbconnect.Connect(db_server,db_user,db_password,db_table_logs)
	try:	
		database.run_query('INSERT INTO searches.search_log ' + 'VALUES('+'"'+ID+'"'+','+'"'+search+'"'+','+'"'+category+'"'+')')
	except:
		return 
