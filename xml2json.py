#!/usr/bin/python
# Usage: xml2json orig.xml output.json

from collections import defaultdict
from xml.etree import cElementTree as ET
import sys, json

def etree_to_dict(t):
    d = {t.tag: {} if t.attrib else None}
    children = list(t)
    if children:
        dd = defaultdict(list)
        for dc in map(etree_to_dict, children):
            for k, v in dc.iteritems():
                dd[k].append(v)
        d = {t.tag: {k:v[0] if len(v) == 1 else v for k, v in dd.iteritems()}}
    if t.attrib:
        d[t.tag].update(('@' + k, v) for k, v in t.attrib.iteritems())
    if t.text:
        text = t.text.strip()
        if children or t.attrib:
            if text:
              d[t.tag]['#text'] = text
        else:
            d[t.tag] = text
    return d

xmlFile = open(sys.argv[1], 'r')
xmlStr = xmlFile.read()
xmlFile.close()

tree = ET.XML(xmlStr)
xmljson = etree_to_dict(tree)

jsonFile = open(sys.argv[2], 'w')
json.dump(xmljson, jsonFile)
jsonFile.close()
