#!/usr/bin/env python
# coding: utf-8

# In[24]:


#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xml.etree.cElementTree as ET
import pprint
import re

"""
find out how many unique users
have contributed to the map in this particular area!

The function process_map should return a set of unique user IDs ("uid")
"""

def process_map(filename):
    users = set()
    for _, element in ET.iterparse(filename):
        try:
            users.add(element.attrib['uid'])
        except KeyError:
            continue
        pass
    
    return users


def test():
    users = process_map('omaha_nebraska')
    pprint.pprint(users)
    assert len(users) == 674


if __name__ == "__main__":
    test()


# In[ ]:




