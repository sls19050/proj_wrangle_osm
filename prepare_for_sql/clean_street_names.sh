#!/bin/bash
#replace address names to the corrected ones
#uses the output of the audit.py

echo "replacing bad street names with the corrected ones in nodes_tags and ways_tags.csv"

while read p; do	
	bad_name="street,$(echo $p | awk -F' => ' '{print $1}'),addr"
	corrected_name="street,$(echo $p | awk -F' => ' '{print $2}'),addr"

	sed -i "s/$bad_name/$corrected_name/g" nodes_tags.csv ways_tags.csv
	
done <../audit_db/improve_street_names/convert_odd_street_names.txt