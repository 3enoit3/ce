
import sys
import json
import sqlite3

import xml.etree.ElementTree as ET


# Db
def getTagsStr(iTags):
    return json.dumps(iTags)

def serializeGraphInSqlite(iNodes, iEdges, iPath):
    aDb = sqlite3.connect(iPath)

    # Nodes
    aDb.execute('DELETE FROM CodeExplorer_ceNodes')
    aDb.executemany( 'INSERT INTO CodeExplorer_ceNodes(id, props) VALUES(?,?)', [(n._id, getTagsStr(n._props)) for n in iNodes] )

    # Edges
    aDb.execute('DELETE FROM CodeExplorer_ceEdges')
    aDb.executemany( 'INSERT INTO CodeExplorer_ceEdges(n1_id, n2_id, directed, props) VALUES(?,?,?,?)', [(e._nodes[0], e._nodes[1], e._directed, getTagsStr(e._props)) for e in iEdges] )

    aDb.commit()
    aDb.close()


# Model
class Node:
    def __init__(self, iId):
        self._id = iId
        self._props = {'dummy':'dummy'}

    def __str__(self):
        return "{} {}".format(self._id, self._props)

class Edge:
    def __init__(self, iNodes, iDirected = None):
        self._nodes = iNodes
        self._directed = iDirected
        self._props = { 'weight': 1 }

    def __str__(self):
        aLink = "{} {} {}".format(
                self._nodes[0] if self._directed == self._nodes[1] else self._nodes[1],
                "->" if self._directed else "-",
                self._nodes[1] if self._directed == self._nodes[1] else self._nodes[0])

        return "{} {}".format(aLink, self._props)

class Graph:
    def __init__(self):
        self._nodes = []
        self._edges = []

        # Multi-edge hanlding
        self._edgeLinks = {}

    # Nodes
    def addNode(self, iNode):
        self._nodes.append(iNode)

    # Edges
    def addEdge(self, iEdge):
        aLinkKey = tuple(sorted(iEdge._nodes))
        aLinks = self._edgeLinks.get(aLinkKey)
        if not aLinks:
            aLinks = {}
            self._edgeLinks[aLinkKey] = aLinks

        aType = iEdge._props.get('type')
        aLink = aLinks.get(aType)
        if not aLink:
            self._edges.append(iEdge)
            aLinks[aType] = iEdge
        else:
            aLink._props['weight'] += 1

    def get(self):
        aUsedNodes = set()
        for e in self._edges:
            aUsedNodes.add(e._nodes[0])
            aUsedNodes.add(e._nodes[1])
        return ([n for n in self._nodes if n._id in aUsedNodes], self._edges)


# XML
def readXmlCompound(iXml, ioGraph):
    with open(iXml) as aFile:
        aRoot = ET.fromstring( aFile.read() )

        aClass = aRoot.find("compounddef[@kind='class']")
        if aClass is not None:
            aId = aClass.find("compoundname").text
            print "Processing class", aId

            # Node
            aNode = Node(aId)
            ioGraph.addNode(aNode)

            # Edges
            aEdges = []

            # Inheritance
            aParent = aRoot.find("basecompoundref")
            if aParent:
                aParentId = aParent.text
                aEdge = Edge( (aId, aParentId), aParentId )
                aEdge._props.update({ 'type': 'generalization' })
                ioGraph.addEdge(aEdge)

            # Aggregation
            for c in aClass.findall("sectiondef/memberdef[@kind='variable']/ref"):
                aAggregatedId = c.get('refid')
                aEdge = Edge( (aAggregatedId, aId), aId )
                aEdge._props.update({ 'type': 'aggregation' })
                ioGraph.addEdge(aEdge)

            # Dependency
            for c in aClass.findall("sectiondef/memberdef[@kind='function']/referencedby"):
                aFunction = c.text.split("::")[-1]
                aDependentId = "::".join(c.text.split("::")[:-1])

                if aDependentId:
                    aEdge = Edge( (aDependentId, aId), aId )
                    aEdge._props.update({ 'type': 'dependency', 'name': aFunction })
                    ioGraph.addEdge(aEdge)


def readXmlIndex(iXml):
    with open(iXml) as aFile:
        aRoot = ET.fromstring( aFile.read() )

        return [ (c.find("name").text, c.get('refid')) for c in aRoot.findall("compound[@kind='class']") ]


# Main

# aXMLDir = "reps/notepad-plus-plus/PowerEditor/doxygen_docs/xml/"
aXMLDir = "reps/doxygen/doxygen_docs/xml/"
aOutputDir = "./"

aProject = "Classes"

# Build class list
aRefIds = readXmlIndex(aXMLDir + "index.xml")
for n, i in aRefIds:
    print "Found", n, i

# Parse classes
aGraph = Graph()
for _, i in aRefIds:
    readXmlCompound(aXMLDir + i + ".xml", aGraph)

# for n in aGraph._nodes:
    # print n
# for e in aGraph._edges:
    # print e

# Serialize
aNodes, aEdges = aGraph.get()
print "Saving {} nodes, {} egdes".format(len(aNodes), len(aEdges))

serializeGraphInSqlite(aNodes, aEdges, aOutputDir + "codeData.sqlite3")

