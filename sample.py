#!/usr/bin/env python
# coding: utf-8

# In[2]:


import xml.etree.ElementTree as ET
import pprint
from collections import defaultdict
import re

OSM_FILE = "omaha_nebraska"
SAMPLE_FILE = "sample.osm"

k = 50      #every kth top level element

def get_element(osm_file, tags=('node', 'way', 'relation')):
    context = iter(ET.iterparse(OSM_FILE, events=('start', 'end')))
    _, root = next(context)
    for event, elem in context:
        if event == 'end' and elem.tag in tags:
            yield elem
            root.clear()

with open(SAMPLE_FILE, 'w', encoding="utf8") as output:
    output.write('<?xml version="1.0" encoding="utf8"?>\n')
    output.write('<osm>\n  ')

    # Write every kth top level element
    for i, element in enumerate(get_element(OSM_FILE)):
        if i % k == 0:
            output.write(ET.tostring(element, encoding="unicode"))

    output.write('</osm>')


# In[ ]:




