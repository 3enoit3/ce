
// Public object
var anetwork = undefined;

var aXhttp = new XMLHttpRequest();
aXhttp.onreadystatechange = function() {
    if (aXhttp.readyState == 4 && aXhttp.status == 200) {
        var graphData = JSON.parse(aXhttp.responseText);
        s = new sigma({ graph: graphData, container: 'ceGraph' });

        // Node selection
        //nodeId = parseInt(getParameterByName('node_id'));
        //var selectedNode;
        //s.graph.nodes().forEach(function(node, i, a) {
            //if (node.id == nodeId) {
                //selectedNode = node;
                //return;
            //}
        //});

        //Initialize nodes as a circle
        s.graph.nodes().forEach(function(node, i, a) {
            node.x = Math.cos(Math.PI * 2 * i / a.length);
            node.y = Math.sin(Math.PI * 2 * i / a.length);
        });

        ////Call refresh to render the new graph
        s.refresh();
        //s.startForceAtlas2({ 'iterationsPerRender' : 40 });
        s.startForceAtlas2({ worker: false, 'startingIterations' : 30 });
        s.refresh();
        //s.startForceAtlas2({ worker: true, barnesHutOptimize: false });
        s.stopForceAtlas2();

        //if (selectedNode != undefined){
            //s.cameras[0].goTo({x:selectedNode['read_cam0:x'],y:selectedNode['read_cam0:y'],ratio:0.1});
        //}
    }
};

// Get graph
aXhttp.open("GET", "http://127.0.0.1:8080/CodeExplorer/graph/sigma", true);
aXhttp.send();

