# EXPANDED_COPYRIGHT_TEXT_START: TFDM
# (c) 2017 Leidos. All rights reserved.
# EXPANDED_COPYRIGHT_TEXT_STOP: TFDM
'''
Created on Dec 14, 2017

@author: dnie
'''
import os
from lxml import etree as ET
from xml.etree.ElementTree import ElementTree, Element, SubElement, Comment, tostring
from xml.etree import ElementTree
from xml.dom import minidom

class CommonLibGenerator:
    def buildTree(self, imgLib):
        xmlFile = ET.Element("Resource")
        headerComment = ET.Comment("This is a generated xml file for Common Image library for String Testing")
        name = ET.SubElement(xmlFile, "Name")
        name.text = "Common"

        resourcePath = ET.SubElement(xmlFile, "ResourcePath")
        resourcePath.text = "../../testlibs/CommonImage"
        xmlFile.append(headerComment)
        properties = ET.SubElement(xmlFile,"Properties")
        imageDir = {"Misc":[]}
        for img in imgLib:
            imageName = img[0:-4]
            if imageName.find("_") is not -1:
                section = imageName[0:imageName.find("_")]
                if not imageDir.has_key(section):
                    imageDir[section] = [imageName]
                else:
                    imageDir[section].append(imageName)
            else:
                imageDir["Misc"].append(imageName)


        for key in imageDir:
            if key is not "Misc":
                sectionStart = ET.Comment("************"+key+"************")
                sectionEnd = ET.Comment("____________"+key+"____________")
                properties.append(sectionStart)
                for i in imageDir[key]:
                    propertyImage = ET.SubElement(properties, "Property")
                    property_name = ET.SubElement(propertyImage, "Name")
                    property_name.text = i
                    property_path = ET.SubElement(propertyImage, "Path")
                    property_path.text = i +".png"
                properties.append(sectionEnd)
                properties.append(ET.Comment("                           "))

        sectionStart = ET.Comment("************Misc************")
        sectionEnd = ET.Comment("____________Misc____________")
        properties.append(sectionStart)
        for i in imageDir["Misc"]:
            propertyImage = ET.SubElement(properties, "Property")
            property_name = ET.SubElement(propertyImage, "Name")
            property_name.text = i
            property_path = ET.SubElement(propertyImage, "Path")
            property_path.text = i +".png"
        properties.append(sectionEnd)

        xmlString = ET.tostring(xmlFile, encoding="utf-8", xml_declaration=True, pretty_print=True)
        f = open("xmlInclude/CommonImage.xml","w+")
        f.write(xmlString)
        return xmlString

if __name__ == '__main__':
    try:
        CommonLibGenerator().buildTree(os.listdir("./CommonImage"))
    except OSError:
        print("Please Check Path, Make sure Running in testlibs/")
