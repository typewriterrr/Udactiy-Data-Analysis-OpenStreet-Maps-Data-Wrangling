#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#!/usr/bin/env python
# coding: utf-8

# In[4]:


#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Return a dictionary, containing the shaped data for that element.
Save the data in a file, to import the shaped data into MongoDB. 

In particular the following things should be done:
- process only 2 types of top level tags: "node" and "way"
- all attributes of "node" and "way" should be turned into regular key/value pairs, except:
    - attributes in the CREATED array should be added under a key "created"
    - attributes for latitude and longitude should be added to a "pos" array,
      for use in geospacial indexing. Make sure the values inside "pos" array are floats
      and not strings. 
- if the second level tag "k" value contains problematic characters, it should be ignored
- if the second level tag "k" value starts with "addr:", it should be added to a dictionary "address"
"""

import xml.etree.cElementTree as ET
import pprint
import re
import codecs
import json
import zipAudit
import streetAudit

lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

CREATED = [ "version", "changeset", "timestamp", "user", "uid"]

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

def shape_element(element):
    node = {}
    address = {}
    if element.tag == "node" or element.tag == "way":
        node["type"] = element.tag
        
        for key in element.attrib:
            if key in CREATED:
                if "created" not in node:
                    node["created"] = {}
                node["created"][key] = element.attrib[key]
                
            elif key in ["lat", "lon"]:
                if "pos" not in node:
                    node["pos"] = [None, None]
                if key == "lat":
                    node["pos"][0] = float(element.attrib[key])
                elif key == "lon":
                    node["pos"][1] = float(element.attrib[key])
            else:
                node[key] = element.attrib[key]
            
        for tag in element.iter("tag"):
            tag_key = tag.attrib["k"]
            tag_value = tag.attrib["v"]
          
            if not problemchars.match(tag_key): # Ignoring the problem characters
                if tag_key.startswith("addr:"): # Check for k value 'addr:'
                    if "address" not in node:
                        node["address"] = {}
                    sub_addr = tag_key[len("addr:"):] # Take the value from 'addr:' and save it in 'sub_addr'
                    #print ("Address type is ", sub_addr) # Address breakdown
                    if(sub_addr == 'street'):     # Check for value 'street'
                        tag_value = streetAudit.update_name(tag_value, streetAudit.mapping)     # Update the value with the mapped value
                        #print("Street name is", tag_value)
                    if(sub_addr == 'postcode'):     # Check for value 'postcode'
                        tag_value = zipAudit.update_zipcode(tag_value)     # Update the value with fixed zip codes
                        #print ("Zip Code is", tag_value)
                    if not lower_colon.match(sub_addr):
                        address[sub_addr] = tag_value
                        node["address"] = address
                elif lower_colon.match(tag_key):
                    node[tag_key] = tag_value
                else:
                    node[tag_key] = tag_value
        
        for nd in element.iter("nd"):
            if "node_refs" not in node:
                node["node_refs"] = []
            node["node_refs"].append(nd.attrib["ref"])
            
        return node
    else:
        return None


def process_map(file_in, pretty = False):
    # You do not need to change this file
    file_out = "{0}.json".format(file_in)
    data = []
    with codecs.open(file_out, "w") as fo:
        for _, element in ET.iterparse(file_in):
            el = shape_element(element)
            if el:
                data.append(el)
                if pretty:
                    fo.write(json.dumps(el, indent=2)+"\n")
                else:
                    fo.write(json.dumps(el) + "\n")
    return data

def test():
    # NOTE: if you are running this code on your computer, with a larger dataset, 
    # call the process_map procedure with pretty=False. The pretty=True option adds 
    # additional spaces to the output, making it significantly larger.
    
    data = process_map('omaha_nebraska', False)
    print ('Success!')
    
if __name__ == "__main__":
    test()

