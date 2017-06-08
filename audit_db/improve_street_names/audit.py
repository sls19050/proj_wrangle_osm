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

OSMFILE = "../../map_files/CustomSeattle.osm"
street_type_re = re.compile(r'\b\S+\.?\b', re.IGNORECASE)

expected = ["street", "avenue", "boulevard", "drive", "court", "place", "square", "lane", "road", 
            "trail", "parkway", "commons", "way", "alley"]

def audit_street_type(street_types, street_name):
    counter = 0
    for word in street_name.split():        
        if word.lower() in expected:
            return 0               
    
    street_types[word].add(street_name)


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

mapping = { "st.": "Street",
            "ave" : "Avenue",            
            }


def update_name(name, mapping):
    words = name.split()
    output_name = ""
    for word in words:
        
        replace_word = word        
        if word.lower() in mapping:
            replace_word = mapping[word.lower()]
        
        output_name += " "+replace_word

    return output_name

if __name__ == '__main__':
    odd_street_names = audit(OSMFILE)
    
    with open('convert_odd_street_names.txt','w') as fp2:
        
        for key in odd_street_names:
            for odd_street_name in odd_street_names[key]:
                better_name = update_name(odd_street_name, mapping)
                print >>fp2,  odd_street_name, "=>", better_name
