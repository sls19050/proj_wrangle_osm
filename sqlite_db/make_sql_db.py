import csv, sqlite3

dict_tb_cmd = {
	'nodes' : "id INTEGER, lat REAL, lon REAL, user TEXT, uid INTEGER, version INTEGER, changeset INTEGER, timestamp DATETIME",
	'nodes_tags' : "id INTEGER, key TEXT, value TEXT, type TEXT",
	'ways' : "id INTEGER,user TEXT,uid INTEGER,version INTEGER,changeset INTEGER,timestamp DATETIME",
	'ways_nodes' : "id INTEGER, node_id INTEGER, position INTEGER",
	'ways_tags' : "id INTEGER, key TEXT, value TEXT, type TEXT",
}

dict_tb_fields = {
	'nodes' : "id, lat, lon, user, uid, version, changeset, timestamp",
	'nodes_tags' : "id, key, value, type",
	'ways' : "id, user, uid, version ,changeset ,timestamp",
	'ways_nodes' : "id, node_id , position",
	'ways_tags' : "id, key , value , type",
}

def to_unicode(data_row):	
	result_list = []
	for d in data_row:		
		result_list.append(unicode(d, 'utf-8'))		
	return result_list

def create_tb(name, con):
	tb_cmd = dict_tb_cmd[name]
	tb_fields = dict_tb_fields[name]
	value_cmd = "?" + ", ?" * (len(tb_fields.split(','))-1)

	
	cur = con.cursor()
	cur.executescript("""
		DROP TABLE IF EXISTS %s;
		CREATE TABLE %s (%s);
		""" % (name, name, tb_cmd) )
	
	with open('../prepare_csv/'+name+'.csv') as fin:
		reader = csv.reader(fin) 
		next(reader) # skip header row
		for row in reader:
			to_db = to_unicode(row)			
			cur.execute("""
				INSERT INTO %s (%s) VALUES (%s);
				""" % (name, tb_fields, value_cmd), to_db)

	
	

if __name__ == "__main__":
	con = sqlite3.connect("CustomSeattle.db")
	for key in dict_tb_fields:
		create_tb(key, con)
	con.commit()
	con.close
