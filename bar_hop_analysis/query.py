import sqlite3

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

	def dist_score(lat1, lon1, lat2, lon2):
		return (lat1-lat2)**2 + (lon1-lon2)**2
	
	ilat, ilon  = 47.614259, -122.316579
	con = sqlite3.connect("../sqlite_dbs/CustomSeattle.db")
	con.create_function("dist_score", 4, dist_score)

	cur = con.cursor()
	
	sql_cmd = """   	
	CREATE TEMP VIEW bar_pos
		AS          
   		SELECT n.id, nt2.value AS name, n.lat, n.lon 
   		FROM nodes_tags AS nt1
   		JOIN nodes_tags AS nt2 
   			ON nt1.id = nt2.id
   		JOIN nodes AS n
   			ON n.id = nt1.id
   		WHERE nt1.key = 'amenity' 
   			AND nt1.value = 'bar'
   			AND nt2.key = 'name';
   		   		
	"""
	cur.execute(sql_cmd)

	sql_cmd = """

	CREATE TEMP VIEW 
	dist_matrix(idA, idB, dist)	AS 
		SELECT A.id, B.id, dist_score(A.lat, A.lon, B.lat,B.lon) AS dist
		FROM bar_pos AS A, bar_pos AS B 
		WHERE A.id > B.id
		ORDER BY dist;
	"""
	
	cur.execute(sql_cmd)

	sql_cmd = """
	WITH RECURSIVE result_tb(id, dist, counter) AS (
		SELECT D.idA+D.idB-1387947219, MIN(D.dist), 0
		FROM dist_matrix AS D
		WHERE D.idA = '1387947219' OR D.idB = '1387947219'

			UNION ALL

		SELECT D.idA+D.idB-result_tb.id, MIN(D.dist), result_tb.counter+1
		FROM dist_matrix AS D, result_tb
		WHERE D.idA = result_tb.id OR D.idB = result_tb.id
		
		)
	SELECT R.id, B.name
	FROM result_tb AS R, bar_pos AS B
	WHERE R.id = B.id	
	"""
	
	data = cur.execute(sql_cmd)
	print_results(data, False)	
	con.close()

if __name__ == "__main__":
	query1()
