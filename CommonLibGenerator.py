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
        
        
        name = ET.SubElement(xmlFile, "Common")
        name.text = "Common"
        
        resourcePath = ET.SubElement(xmlFile, "ResourcePath")
        resourcePath.text = "../../testlibs/CommonImage"
        xmlFile.append(headerComment)
        properties = ET.SubElement(xmlFile,"Properties")
        imageDir = {"Misc":[]}
        for img in imgLib:
            imageName = img.rstrip(".png")
            if imageName.find("_") is not -1:
                section = imageName[0:imageName.find("_")]
                if not imageDir.has_key(section):
                    imageDir[section] = [imageName]
                else:
                    imageDir[section].append(imageName)
            else:
                imageDir["Misc"].append(imageName)
                #sectionStart = Comment("************"+section+"************")
                #sectionEnd = Comment("____________"+section+"____________")
                
        
        for key in imageDir:
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
            if key is not imageDir.keys()[-1]:
                properties.append(ET.Comment("                           "))
                
        #tree = ElementTree.ElementTree(xmlFile)
        #f = open("Test.xml","w+")
        #tree.write(f,encoding="utf-8",xml_declaration=True)
        xmlString = ET.tostring(xmlFile, encoding="utf-8", xml_declaration=True, pretty_print=True)
        f = open("xmlInclude/CommonImage","w+")
        f.write(xmlString)
        return xmlString
        
    def prettify(self,elem):
        rawString = ElementTree.tostring(elem, "utf-8",xml_declaration=True, pretty_print=True)
        parsed = minidom.parseString(rawString)
        return parsed.toprettyxml(indent="  ")

if __name__ == '__main__':
    try:
        CommonLibGenerator().buildTree(os.listdir("./CommonImage"))
    except OSError:
        print("CommonImage Dir cannot be found")
