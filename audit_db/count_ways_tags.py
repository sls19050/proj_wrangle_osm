import sqlite3

def print_results(data, limiter_on=True):
	limiter = 10
	with open('count_ways_tags.txt','w') as fp:
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
	
	con = sqlite3.connect("../sqlite_dbs/CustomSeattle_cleaned.db")
	con.create_function("dist_score", 4, dist_score)

	cur = con.cursor()
	
	sql_cmd = """   	
	SELECT key, COUNT(*) AS count
	FROM ways_tags
	GROUP BY key
	ORDER BY count DESC
   		   		
	"""
	
	data = cur.execute(sql_cmd)
	print_results(data, False)	
	con.close()

if __name__ == "__main__":
	query1()
