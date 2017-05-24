import sqlite3

def print_results(data):
	limiter = 10
	with open('result_viewer.txt','w') as fp:
		for d in data:		
			if limiter < 0:
				break
			fp.write(",".join(str(item) for item in d))
			fp.write('\n')
			limiter -= 1

def query1():
	con = sqlite3.connect("../sqlite_dbs/nodes_tags.db")
	cur = con.cursor()
	
	sql_cmd = """.tables
	"""
	
	data = cur.execute(sql_cmd)
	print_results(data)	
	con.close()

if __name__ == "__main__":
	query1()
