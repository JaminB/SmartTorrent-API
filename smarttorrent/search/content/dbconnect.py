import MySQLdb

class Connect:
	
	def __init__(self, host, user, passwd, database):
		db = MySQLdb.connect(host=host, passwd=passwd, user=user, db=database)
		self.query = db.cursor()
	
	def run_query(self, query):
		self.query.execute(query)
		self.query.connection.commit()
		return self.query.fetchall()

