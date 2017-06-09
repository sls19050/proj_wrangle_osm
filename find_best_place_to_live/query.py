import sqlite3
from math import sin, cos, sqrt, atan2, radians

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

	def dist(lat1, lon1, lat2, lon2):
		R = 3959 #Earth radius in miles
		dlon = radians(lon2 - lon1)
		dlat = radians(lat2 - lat1)
		a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
		c = 2 * atan2(sqrt(a), sqrt(1 - a))
		distance = R * c
		return distance

	def scoring(b_dist, w_dist):
		noise = 90 * (0.00568182/b_dist)**2
		if noise <= 60:
			b_score = 0
		else:
			b_score = 5 * (noise - 60) + 50
		w_score = 2 * w_dist * 1/3 * 35
		return b_score + w_score
	
	ilat, ilon  = 47.614259, -122.316579
	con = sqlite3.connect("../sqlite_dbs/CustomSeattle.db")
	con.create_function("dist", 4, dist)
	con.create_function("scoring", 2, scoring)

	cur = con.cursor()
	
	sql_cmd = """	
	CREATE TEMP VIEW bar_pos AS          
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
	
	CREATE TEMP VIEW apt_pos AS
		SELECT n.id, n.lat, n.lon, nt2.value AS name
		FROM nodes_tags AS nt
		JOIN nodes_tags AS nt2
			ON nt.id = nt2.id
		JOIN nodes AS n
			ON n.id = nt.id
		WHERE 
			(nt.key = 'building' OR  nt.value = 'residential')
			AND nt.value LIKE 'apartment%'
			AND nt2.key = 'name'
			
			UNION

		SELECT wt.id, AVG(n.lat) AS lat, 
			AVG(n.lon) AS lon, wt2.value AS name
		FROM ways_tags AS wt
		JOIN ways_tags AS wt2
			ON wt.id = wt2.id	
		JOIN ways_nodes AS wn
			ON wt.id = wn.id
		JOIN nodes AS n
			ON n.id = wn.node_id
		WHERE 
			(wt.key = 'building' OR  wt.value = 'residential')
			AND wt.value LIKE 'apartment%'
			AND wt2.key = 'name'
		GROUP BY wt.id;

	"""
	cur.execute(sql_cmd)

	sql_cmd = """
	
	CREATE TEMP VIEW A_B_dists AS
	SELECT A.id, A.lat, A.lon, A.name AS A_name, B.name AS B_name,
		MIN(dist(A.lat, A.lon, B.lat, B.lon)) AS b_dist,
		dist(A.lat, A.lon, 47.6148943, -122.321752517) AS w_dist
	FROM apt_pos AS A
	JOIN bar_pos AS B
	GROUP BY A.id;
	
	"""

	cur.execute(sql_cmd)

	sql_cmd = """
	SELECT A_name,
		scoring(b_dist, w_dist) AS score
	FROM A_B_dists
	ORDER BY score
	"""
	
	data = cur.execute(sql_cmd)
	print_results(data, False)	
	con.close()

if __name__ == "__main__":
	query1()
