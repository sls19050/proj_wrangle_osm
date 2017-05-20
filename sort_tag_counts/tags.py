import xml.etree.cElementTree as ET
import pprint
import re
import json

"""
Categorize the tag 'tag' by their keys.
Sort keys into 'lower', 'lower_colon', 'problemchars', and 'others'
Count the number of each type of key
Then export result as json file
"""

# define regular expression for sorting
re_dict = {}
re_dict['lower'] = re.compile(r'^([a-z]|_)*$')
re_dict['lower_colon'] = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
re_dict['problemchars'] = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

# sorts the input element into one of the 4 categories
# updates the count of the category
# then returns the updated keys dictionary
def key_type(element, keys):
    if element.tag == "tag":
        k_value = element.attrib['k']
        all_pass = True
        for re_key in re_dict:
            if re.search(re_dict[re_key], k_value):
                keys[re_key] += 1
                all_pass = False
        if all_pass:
            keys["other"] += 1        
    return keys

# Parse through the entire map file
# Obtain total counts of each key type
# export results as JSON file
def process_map(filename):
    #sort and count keys
    keys = {"lower": 0, "lower_colon": 0, "problemchars": 0, "other": 0}
    for _, element in ET.iterparse(filename):
        keys = key_type(element, keys)

    #export results
    with open('clean_tag_count_summary.json','w') as fp:
		json.dump(keys, fp)

if __name__ == "__main__":
    process_map('../example.osm')