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

	def dist_score(lat1, lon1, lat2, lon2):
		return (lat1-lat2)**2 + (lon1-lon2)**2

	ilat, ilon  = 47.614259, -122.316579
	con = sqlite3.connect("../sqlite_dbs/CustomSeattle.db")
	con.create_function("dist_score", 4, dist_score)
	cur = con.cursor()
	
	sql_cmd = """	
	CREATE TEMP VIEW bar_nodes_tags
	AS			
		SELECT * FROM nodes_tags
		WHERE key = 'amenity' 
		AND value = 'bar';
	"""
	cur.execute(sql_cmd)
	
	
	sql_cmd = """
	CREATE TEMP VIEW latest_row
	AS
		SELECT * FROM result_tb ORDER BY dist_score DESC LIMIT 1;
	"""
	cur.execute(sql_cmd)
	
	sql_cmd = """

	WITH RECURSIVE result_tb AS (

		SELECT T1.id, T1.value AS name, nodes.lat AS lat, nodes.lon AS lon,
			dist_score(nodes.lat, nodes.lon, 47.614259, -122.316579) As dist_score
		FROM nodes_tags AS T1                                      
		JOIN bar_nodes_tags AS T2
		JOIN nodes
		ON T1.id = T2.id
		WHERE T1.key = 'name'
		AND T1.id = nodes.id
		ORDER BY dist_score
		LIMIT 1

			UNION ALL
			
		SELECT T1.id, T1.value AS name, nodes.lat AS lat, nodes.lon AS lon,
			dist_score(
				nodes.lat, nodes.lon, 
				SELECT lat FROM latest_row,
				SELECT lon FROM latest_row) As dist_score
		FROM nodes_tags AS T1,
		JOIN bar_nodes_tags AS T2
		JOIN nodes
		ON T1.id = T2.id
		WHERE T1.key = 'name'
		AND T1.id = nodes.id
		AND T1.id NOT IN (SELECT id FROM result_tb)
		ORDER BY dist_score
		LIMIT 1
	),

	SELECT * FROM result_tb;
	"""
	
	data = cur.execute(sql_cmd)
	print_results(data, False)	
	con.close()

if __name__ == "__main__":
	query1()