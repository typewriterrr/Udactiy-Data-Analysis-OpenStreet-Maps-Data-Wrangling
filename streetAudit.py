#!/usr/bin/env python
# coding: utf-8

# In[30]:


"""

- audit the OSMFILE and change the variable 'mapping' to reflect the changes needed to fix 
    the unexpected street types to the appropriate ones in the expected list.
    
- write the update_name function, to actually fix the street name.
    The function takes a string with street name as an argument and should return the fixed name
"""

#!/usr/bin/env python
# coding: utf-8

# In[1]:

import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import pprint

OSMFILE = "omaha_nebraska"
street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)


expected = ["Street", "Avenue", "Boulevard", "Drive", "Court", "Place", "Square", "Lane", "Road", 
            "Trail", "Parkway", "Commons"]

# UPDATE THIS VARIABLE
mapping = {"St": "Street",
           "st": "Street",
           "St.":"Street",
           "st.": "Street",
           "St": "Street",
           "Blvd": "Boulevard",
           "blvd": "Boulevard",
           "Ave": "Avenue",
           "ave": "Avenue",
           "Ave.": "Avenue",
           "Rd.": "Road",
           "Rd": "Road",
           "Dr": "Drive",
           "dr": "Drive"
          }


def audit_street_type(street_types, street_name):
    """
    This function takes in the dictionary of street types, a string of street name to audit
    A regex to match against and the list of expected street types.
    """
    
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        if street_type not in expected:
            street_types[street_type].add(street_name)


def is_street_name(elem):
    return (elem.attrib['k'] == "addr:street")


def audit(osmfile):
    """
    This function changes the variable mapping to reflect the changes needed to 
    Fix the problem street types to the appropriate one in the expected list
    """

    osm_file = open(osmfile, "r")
    street_types = defaultdict(set)
    for event, elem in ET.iterparse(osm_file, events=("start",)):

        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_street_name(tag):
                    audit_street_type(street_types, tag.attrib['v'])
    osm_file.close()
    return street_types


def update_name(name, mapping):

    m = street_type_re.search(name)
    if m.group() not in expected:
        if m.group() in mapping.keys():
            name = re.sub(m.group(), mapping[m.group()], name)
    return name

def test():
    st_types = audit(OSMFILE)
    assert len(st_types) != 3
    pprint.pprint(dict(st_types))

    for st_type, ways in st_types.items():
        for name in ways:
            better_name = update_name(name, mapping)
            print (name, "=>", better_name)
            if name == "S 111th St":
                assert better_name == "S 111th Street"
           

if __name__ == '__main__':
    test()


# In[ ]:




