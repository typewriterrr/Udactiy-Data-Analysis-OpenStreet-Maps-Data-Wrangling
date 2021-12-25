#!/usr/bin/env python
# coding: utf-8

# In[7]:


#!/usr/bin/env python
# coding: utf-8

# In[1]:

"""
This script will check for the zip codes format and whether it begins with a 
68 for the City of Omaha
"""

import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import pprint

osmfile = 'omaha_nebraska'

zip_type_re = re.compile(r'\d{5}$')    #5 digit zip code, no dashes

def audit_ziptype(zip_types, zipcode):
    if zipcode[0:2]!= 68:
        zip_types[zipcode[0:2]].add(zipcode)

def is_zipcode(elem):
    return (elem.attrib['k'] == "addr:postcode")
                  
def audit_zip(osmfile):
                  osm_file = open (osmfile, "r")
                  zip_types = defaultdict(set)
                  for event, elem in ET.iterparse(osmfile, events=("start",)):
                      if elem.tag == "node" or elem.tag == "way":
                          for tag in elem.iter("tag"):
                              if is_zipcode(tag):
                                    audit_ziptype(zip_types,tag.attrib['v'])
                  osm_file.close()
                  return zip_types
                  
zip_print = audit_zip(osmfile)


def test():
    pprint.pprint(dict(zip_print))
    
if __name__ == '__main__':
    test()

def update_zipcode(zipcode):       
    """
    This function updates the zip codes by replacing the wrong zip codes with fixed ones'''
    """
    if re.findall(r'(^\d{5})-\d{4}$', zipcode):
        valid_zipcode = re.findall(r'(^\d{5})-\d{4}$',zipcode)[0]
        return valid_zipcode
    else:
        return zipcode

def test_zip():
    for zips, ways in zip_print.items():
        for name in ways:
            better_name = update_zipcode(name)
            print (name, "=>", better_name)
            
if __name__ == '__main__':
    test_zip()


# In[ ]:




