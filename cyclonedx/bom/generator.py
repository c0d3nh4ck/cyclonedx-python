# This file is part of CycloneDX Python module.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Copyright (c) Steve Springett. All Rights Reserved.

from xml.etree import ElementTree


def build_xml_bom(components):
    declaration = '<?xml version="1.0" encoding="UTF-8"?>\n'
    namespace = {'xmlns': 'http://cyclonedx.org/schema/bom/1.0', 'version': '1'}
    bom = ElementTree.Element("bom", namespace)
    xml_components = ElementTree.SubElement(bom, "components")
    for component in components:
        component_xml = build_xml_component_element(
            component.publisher,
            component.name,
            component.version,
            component.description,
            component.hashes,
            component.licenses,
            component.purl,
            component.modified
        )
        xml_components.append(component_xml)
    xml_pretty_print(bom)
    return declaration + ElementTree.tostring(bom, "unicode")


def build_xml_component_element(publisher, name, version, description, hashes, licenses, purl, modified):
    component = ElementTree.Element("component", {"type": "library"})

    if publisher and publisher != "UNKNOWN":
        ElementTree.SubElement(component, "publisher").text = publisher

    if name and name != "UNKNOWN":
        ElementTree.SubElement(component, "name").text = name

    if version and version != "UNKNOWN":
        ElementTree.SubElement(component, "version").text = version

    if description and description != "UNKNOWN":
        ElementTree.SubElement(component, "description").text = description

    if hashes:
        hashes_elm = ElementTree.SubElement(component, "hashes")
        for h in hashes:
            ElementTree.SubElement(hashes_elm, "hash", alg=h.algorithm).text = h.value

    if len(licenses):
        licenses_elm = ElementTree.SubElement(component, "licenses")
        for license in licenses:
            license_elm = ElementTree.SubElement(licenses_elm, "license")
            ElementTree.SubElement(license_elm, "name").text = license.name

    if purl:
        ElementTree.SubElement(component, "purl").text = purl

    ElementTree.SubElement(component, "modified").text = modified if modified else "false"

    return component


def xml_pretty_print(elem, level=0):
    i = "\n" + level*"    "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "    "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            xml_pretty_print(elem, level+1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i
    return elem
