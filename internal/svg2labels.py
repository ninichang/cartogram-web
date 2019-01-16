import xml
from xml.dom import minidom
import json
import sys
import re

little_m_re = re.compile(r'm ([0-9.\-]+),([0-9.\-]+) ([0-9.\-]+),([0-9.\-]+)')
big_m_re = re.compile(r'M ([0-9.\-]+),([0-9.\-]+) ([0-9.\-]+),([0-9.\-]+)')

def getInnerText(node):
    
    text = ""

    for child in node.childNodes:
        
        if child.nodeType == xml.dom.Node.TEXT_NODE:

            text += child.nodeValue
        
        else:

            text += getInnerText(child)
    
    return text

def convert(svg_filepath, scale_x, scale_y):
    svg_map = minidom.parse(svg_filepath)
    labels = {"scale_x": scale_x, "scale_y": scale_y, "labels": [], "lines": []}

    for text in svg_map.getElementsByTagName("text"):

        if not text.hasAttribute("inkscape:label"):
            continue
        
        if text.getAttribute("inkscape:label") != "gocartlabel":
            continue
        
        label_text = getInnerText(text)
        label_x = float(text.getAttribute("x"))
        label_y = float(text.getAttribute("y"))

        labels['labels'].append({'text': label_text, 'x': label_x, 'y': label_y})
    
    for path in svg_map.getElementsByTagName("path"):

        if not path.hasAttribute("inkscape:label"):
            continue
        
        if path.getAttribute("inkscape:label") != "gocartlabel":
            continue
        
        p = path.getAttribute("d").strip()

        little_m_match = little_m_re.match(p)

        if little_m_match != None:

            x1 = float(little_m_match.group(1))
            y1 = float(little_m_match.group(2))

            x2 = float(little_m_match.group(3)) + x1
            y2 = float(little_m_match.group(4)) + y1

            labels['lines'].append({'x1': x1, 'x2': x2, 'y1': y1, 'y2': y2})

            continue
        
        big_m_match = big_m_re.match(p)

        if big_m_match != None:

            x1 = float(little_m_match.group(1))
            y1 = float(little_m_match.group(2))

            x2 = float(little_m_match.group(3))
            y2 = float(little_m_match.group(4))

            labels['lines'].append({'x1': x1, 'x2': x2, 'y1': y1, 'y2': y2})

            continue
    
    return labels
    






