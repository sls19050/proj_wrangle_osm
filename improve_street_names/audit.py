"""
- audit the OSMFILE and change the variable 'mapping' to reflect the changes needed to fix 
    the unexpected street types to the appropriate ones in the expected list.
    Add mappings only for the actual problems found in this OSMFILE,
- write the update_name function, to actually fix the street name.
    The function takes a string with street name as an argument and return the fixed name
"""
import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import pprint

OSMFILE = "../example.osm"
street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)

expected = ["Street", "Avenue", "Boulevard", "Drive", "Court", "Place", "Square", "Lane", "Road", 
            "Trail", "Parkway", "Commons", "Way"]


mapping = { "St": "Street",
            "St.": "Street",
            "Ave" : "Avenue",
            "Rd." : "Road"
            }


def audit_street_type(street_types, street_name):    
    for word in street_name.split():
        m = street_type_re.search(word)
        if m:
            street_type = m.group()
            if street_type in expected:
                return 0
            else:
                pass
    
    street_types[street_type].add(street_name)


def is_street_name(elem):
    return (elem.attrib['k'] == "addr:street")


def audit(osmfile):
    osm_file = open(osmfile, "r")
    street_types = defaultdict(set)
    for event, elem in ET.iterparse(osm_file, events=("start",)):

        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_street_name(tag):
                    audit_street_type(street_types, tag.attrib['v'])
    osm_file.close()
    
    with open('odd_street_names.txt','w') as fp:
        print >>fp, street_types

    return street_types

def update_name(name, mapping):
    words = name.split()
    if words[-1] in mapping:
        words[-1] = mapping[words[-1]]
    name = " ".join(words)

    return name


if __name__ == '__main__':
    odd_street_names = audit(OSMFILE)
    for key in odd_street_names:
        better_name = update_name(key, mapping)
        print key, "=>", better_name