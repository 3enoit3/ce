
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

class GraphRest(APIView):
    def buildOutputNode(self, iNode):
        aProps = getTags(iNode.props)
        aOuputNode = {
                'id': iNode.id,
                'label': iNode.id,
                'title': iNode.id,
                'value': len(ceEdges.objects.filter(n1_id=iNode.id)) + len(ceEdges.objects.filter(n1_id=iNode.id))
                }
        return aOuputNode

    def buildOutputEdge(self, iEdge):
        aProps = getTags(iEdge.props)
        aOuputEdge = {
                'from': iEdge.n1_id,
                'to': iEdge.n2_id,
                'type': aProps['type']
                }
        # aOuputEdge['label'] = aProps['name']
        if iEdge.directed:
            aOuputEdge['arrows'] = 'to'
        return aOuputEdge

    def get(self, request):
        aNodes = [self.buildOutputNode(n) for n in ceNodes.objects.all()]
        aEdges = [self.buildOutputEdge(e) for e in ceEdges.objects.all()]
        return JSONResponse( {'nodes':aNodes, 'edges':aEdges} )

