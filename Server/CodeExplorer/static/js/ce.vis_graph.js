
function visGraphOptions() {
    return {
        nodes: {
            shape: 'dot',
            scaling: {
                min: 5,
                max: 40,
                label: { min: 5, max: 40 }
            },
            font: { size: 12, face: 'Tahoma' },
            color: {
                highlight: { border : 'red', background: '#FFB6C1' }
            }
        },
        edges: {
            width: 0.15,
            color: { inherit: 'from' },
            smooth: { type: 'continuous', roundness: 0 },
        },
        //physics: {
            //enabled: true,
            //forceAtlas2Based: {
                //gravitationalConstant: -26,
                //centralGravity: 0.005,
                //springLength: 230,
                //springConstant: 0.18
            //},
            //maxVelocity: 146,
            //solver: 'forceAtlas2Based',
            //timestep: 0.35,
            //stabilization: { iterations: 150 }
        //},
        physics: {
            stabilization: true,
            barnesHut: {
                gravitationalConstant: -80000,
                springConstant: 0.001,
                springLength: 200
            }
        },
        interaction: {
            tooltipDelay: 200,
            hideEdgesOnDrag: false,
            multiselect: true
        }
    };
}

// Public object
var visNetwork = undefined;

var aXhttp = new XMLHttpRequest();

aXhttp.onreadystatechange = function() {
    if (aXhttp.readyState == 4 && aXhttp.status == 200) {
        var graphData = JSON.parse(aXhttp.responseText);

        var nodeDataSet = new vis.DataSet(graphData['nodes']);
        var nodesJSON = nodeDataSet.get({returnType:"Object"});

        var edgeDataSet = new vis.DataSet(graphData['edges']);
        var edgesJSON = edgeDataSet.get({returnType:"Object"});

        // create a network
        var container = $('#ceGraph').get(0);
        var data = {nodes:nodeDataSet, edges:edgeDataSet};
        visNetwork = new vis.Network(container, data, visGraphOptions());

        // add select on click
        visNetwork.on("click", function (params) {
            $("#ceClassSelector").val(params.nodes[0]).change();
        });
    }
};

// Get graph
aXhttp.open("GET", "http://127.0.0.1:8080/CodeExplorer/graph", true);
aXhttp.send();

