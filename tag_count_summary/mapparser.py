"""
Use iterative parsing to generate a dictionary
1) with tag as the key and
2) number of times this tag used as value
Then export the dictionary as a json file
"""


import xml.etree.cElementTree as ET
import pprint
import json

def count_tags(osmFile):
	tags = {}
	parser = ET.iterparse(osmFile)
	for _, elem in parser:
		if elem.tag in tags:
			tags[elem.tag] += 1
		else:
			tags[elem.tag] = 1
	del parser
	
	with open('tag_count_summary.json','w') as fp:
		json.dump(tags, fp)


if __name__ == "__main__":
    count_tags('../example.osm')
