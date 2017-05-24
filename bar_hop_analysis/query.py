import sqlite3
#from pyspatialite import dbapi2 as db

def print_results(data, limiter_on=True):
	limiter = 10
	with open('result_viewer.txt','w') as fp:
		if limiter_on:
			for d in data:
				if limiter < 0:
					return 0
				fp.write(",".join(str(item) for item in d))
				fp.write('\n')
				limiter -= 1
		else:
			for d in data:
				fp.write(",".join(str(item) for item in d))
				fp.write('\n')

def query1():
	lat, lon  = 47.614259, -122.316579
	con = sqlite3.connect("../sqlite_dbs/CustomSeattle.db")
	cur = con.cursor()
	
	sql_cmd = """
	
	SELECT T1.id, T1.value, T2.value, 
		(nodes.lat-47.614259)*(nodes.lat-47.614259)+(nodes.lon+122.316579)*(nodes.lon+122.316579)
		As dist_score
	FROM nodes_tags AS T1                                      
	JOIN (
		SELECT * FROM nodes_tags
		WHERE key = 'amenity' 
		AND value LIKE '%bar%'
		) AS T2
	JOIN nodes
	ON T1.id = T2.id
	WHERE T1.key = 'name'
	AND T1.id = nodes.id
	ORDER BY dist_score
	"""
	
	data = cur.execute(sql_cmd)
	print_results(data, False)	
	con.close()

if __name__ == "__main__":
	query1()