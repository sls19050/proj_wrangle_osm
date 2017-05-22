import xml.etree.cElementTree as ET
import pprint
import re

"""
Find number of unique users who 
contributed to the map in this particular area.
Return a set of unique user IDs ("uid")
"""

def get_user(element):
    if 'uid' in element.attrib:
        return element.attrib['uid']
    else:
        return False

def process_map(filename):
    users = set()
    for _, element in ET.iterparse(filename):
        uid = get_user(element)
        if uid:
            users.add(uid)

    with open('unique_user_ids.txt','w') as fp:
        for user_id in users:
            fp.write(user_id)
            fp.write('\n')

if __name__ == "__main__":
    process_map('../map_files/CustomSeattle.osm')