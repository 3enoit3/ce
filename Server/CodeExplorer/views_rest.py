
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from .models import ceNodes, ceEdges
#from .serializers import ceNodesSerializer
from django.template import Context, loader
from django.http import Http404
from collections import defaultdict
import json
import itertools
import collections

class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)

def getTags(iTagsStr):
    return json.loads(iTagsStr)

class NodeRest(APIView):
    def get(self, request, node_id, format=None):
        try:
            # # Node
            # aNode = ceNodes.objects.get(pk=class_id)
            # aData = ceNodeSerializer(aClassData).data

            # # Edges
            # aEdges = ceEdges.objects.filter(directed=class_id)
            # aEdgeTypes = defaultdict(list)
            # for e in aEdges:
                # aEdgeTypes[e._props['type']].append(e.fromClass.name)

            # aData["deps"] = {}
            # for aType, aFroms in aTypedDeps.iteritems():
                # aData["deps"][aType] = [ {"from": x} for x in aFroms ]

            # # JSON
            # return JSONResponse(aData)
            return JSONResponse({})
        except ceNodes.DoesNotExist:
            raise Http404

def buildGraphVis():
    def buildOutputNode(iNode):
        aProps = getTags(iNode.props)
        aOuputNode = {
                'id': iNode.id,
                'label': iNode.id,
                'title': iNode.id,
                'value': len(ceEdges.objects.filter(n1_id=iNode.id)) + len(ceEdges.objects.filter(n1_id=iNode.id))
                }
        return aOuputNode

    def buildOutputEdge(iEdge):
        aProps = getTags(iEdge.props)
        aOuputEdge = {
                'from': iEdge.n1_id,
                'to': iEdge.n2_id,
                'type': aProps['type']
                }
        if iEdge.directed:
            aOuputEdge['arrows'] = 'to'
        return aOuputEdge

    aNodes = [buildOutputNode(n) for n in ceNodes.objects.all()]
    aEdges = [buildOutputEdge(e) for e in ceEdges.objects.all()]
    return {'nodes':aNodes, 'edges':aEdges}

def buildGraphSigma():
    aNewOutputId = itertools.count()
    aNodeOutputIds = collections.defaultdict(int)

    def buildOutputNode(iNode):
        # Output id
        aOutputId = aNewOutputId.next()
        aNodeOutputIds[iNode.id] = aOutputId

        # Add node
        aProps = getTags(iNode.props)
        aOuputNode = {
                'id': str(aOutputId),
                'label': iNode.id,
                'size': len(ceEdges.objects.filter(n1_id=iNode.id)) + len(ceEdges.objects.filter(n1_id=iNode.id)) + 1,
                'x': aOutputId,
                'y': aOutputId
                }
        return aOuputNode

    def buildOutputEdge(iEdge):
        # Output id
        aOutputId = aNewOutputId.next()

        # Add edge
        aProps = getTags(iEdge.props)
        aOuputEdge = {
                'id': str(aOutputId),
                'source': str(aNodeOutputIds[iEdge.n1_id]),
                'target': str(aNodeOutputIds[iEdge.n2_id])
                }
        return aOuputEdge

    aNodes = [buildOutputNode(n) for n in ceNodes.objects.all()]
    aEdges = [buildOutputEdge(e) for e in ceEdges.objects.all()]
    return {'nodes':aNodes, 'edges':aEdges}

def buildGraphD3():
    aNewOutputId = itertools.count()
    aNodeOutputIds = collections.defaultdict(int)

    def buildOutputNode(iNode):
        # Output id
        aOutputId = aNewOutputId.next()
        aNodeOutputIds[iNode.id] = aOutputId

        # Add node
        aProps = getTags(iNode.props)
        aOuputNode = {
                'id': str(aOutputId),
                'label': iNode.id,
                'size': len(ceEdges.objects.filter(n1_id=iNode.id)) + len(ceEdges.objects.filter(n1_id=iNode.id)) + 1,
                }
        return aOuputNode

    def buildOutputEdge(iEdge):
        # Output id
        aOutputId = aNewOutputId.next()

        # Add edge
        aProps = getTags(iEdge.props)
        aOuputEdge = {
                'source': str(aNodeOutputIds[iEdge.n1_id]),
                'target': str(aNodeOutputIds[iEdge.n2_id]),
                'value' : 1
                }
        return aOuputEdge

    aNodes = [buildOutputNode(n) for n in ceNodes.objects.all()]
    aEdges = [buildOutputEdge(e) for e in ceEdges.objects.all()]
    return {'nodes':aNodes, 'links':aEdges}

class GraphRest(APIView):

    def get(self, request, type):
        aGraph = {}
        if type == 'sigma':
            aGraph = buildGraphSigma()
        elif type == 'd3':
            aGraph = buildGraphD3()
        else:
            aGraph = buildGraphVis()
        return JSONResponse(aGraph)

