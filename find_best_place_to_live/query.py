"""
Uses the CustomSeattle.db and 
finds the best apartment to live in Capitol Hill, Seattle by minimizing cost of living,
where cost of living is defined by the sum of the following two metrics;
-Daily cost of walking to work
-Daily cost of losing sleep
"""

import sqlite3
from math import sin, cos, sqrt, atan2, radians

# function to print data output to a text file
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

# function to execute SQLite queries to solve the problem
def query1():

	#To calculate distance given a pair of lat and lon
	#To be used as DIST() in thee following SQL queries
	#Function obtained from : https://stackoverflow.com/questions/19412462/getting-distance-between-two-points-based-on-latitude-longitude
	def dist(lat1, lon1, lat2, lon2):
		R = 3959 #Earth radius in miles
		dlon = radians(lon2 - lon1)
		dlat = radians(lat2 - lat1)
		a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
		c = 2 * atan2(sqrt(a), sqrt(1 - a))
		distance = R * c
		return distance

	#To calculate the score of the apartment based on:
	# 1, distance to work, 2 distance to the nearest bar
	#To be used as SCORING() in the following SQL queries
	def scoring(b_dist, w_dist):
		# assume that bars generate about 90 decibels within 30 ft (or 0.00568182 miles) of the area,
		# and that the intensity of the noise is inversely proportional to the squared distance from the source,
		# as suggested in http://hyperphysics.phy-astr.gsu.edu/hbase/Acoustic/invsqs.html#c1
		noise = 90 * (0.00568182/b_dist)**2 
		if noise <= 60: # typical decibel value for normal conversations = 60, from: http://www.noisemonitoringservices.com/decibels-explained/
			b_score = 0 # I fall asleep during such noise environment easily, hence no impact to my sleep
		else:
			b_score = 5 * (noise - 60) + 50 # I arbitarily defined this cost equation
		w_score = 2 * w_dist * 1/3 * 35 # cost of walking to work (back and forth), assume my time is worth $35/hr & It takes me 1hr to walk 3miles
		return b_score + w_score
	
	con = sqlite3.connect("../sqlite_dbs/CustomSeattle.db")
	con.create_function("dist", 4, dist)
	con.create_function("scoring", 2, scoring)

	cur = con.cursor()
	
	# query for obtaining lat and lon for all bars in the area
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

	# query for obtaining lat and lon for all apartments in the area
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

	# to obtain distance to the nearest bar and distance to work for each apartment
	# workplace lat and lon = 47.6148943 & -122.321752517
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

	# to rank all apartments by their score, 
	# where score is the daily cost, and therefore the lower the better
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
