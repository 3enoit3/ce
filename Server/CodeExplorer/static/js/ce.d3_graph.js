
var aXhttp = new XMLHttpRequest();

// Initialize graph when JSON is ready
aXhttp.onreadystatechange = function() {
    if (aXhttp.readyState == 4 && aXhttp.status == 200) {
        var graphData = JSON.parse(aXhttp.responseText);

        var width = $('#ceGraph').width();
        var height = $('#ceGraph').height();
        var svg = d3.select('#ceGraph').append('svg')
            .attr('width', width)
            .attr('height', height);
        var color = d3.scaleOrdinal(d3.schemeCategory20);

        // Simulation
        var simulation = d3.forceSimulation()
            .force("link", d3.forceLink().id(function(d) { return d.id; }))
            .force("charge", d3.forceManyBody())
            .force("center", d3.forceCenter(width / 2, height / 2));

        // Edges
        var link = svg.append("g")
            .attr("class", "links")
            .selectAll("line")
            .data(graphData.links)
            .enter().append("line")
            .attr("stroke-width", function(d) { return Math.sqrt(d.value); });

        // Nodes
        var node = svg.selectAll('.nodes')
            .data(graphData.nodes)
            .enter().append("g")
            .attr("class", "nodes")
            //.call(d3.drag()
                //.on("start", dragstarted)
                //.on("drag", dragged)
                //.on("end", dragended));

        node.append("circle")
            .attr("r", 5)
            .attr("fill", function(d) { return color(d.group); })

        //node.append("text")
            //.attr("dx", 12)
            //.attr("dy", ".35em")
            //.text(function(d) { return d.label; });
        //var labels = svg.append("g")
            //.attr("class", "labels")
            //.selectAll("text")
            //.data(graphData.nodes)
            //.enter().append("text")
            //.attr("dx", 12)
            //.attr("dy", ".35em")
            //.text(function(d) { return d.name });

        node.append("title")
            .text(function(d) { return d.label; });

        function dragstarted(d) {
            if (!d3.event.active) simulation.alphaTarget(0.3).restart();
            d.fx = d.x;
            d.fy = d.y;
        }

        function dragged(d) {
            d.fx = d3.event.x;
            d.fy = d3.event.y;
        }

        function dragended(d) {
            if (!d3.event.active) simulation.alphaTarget(0);
            d.fx = null;
            d.fy = null;
        }

        simulation
            .nodes(graphData.nodes)
            .on("tick", ticked);

        simulation.force("link")
            .links(graphData.links);

        function ticked() {
            link
                .attr("x1", function(d) { return d.source.x; })
                .attr("y1", function(d) { return d.source.y; })
                .attr("x2", function(d) { return d.target.x; })
                .attr("y2", function(d) { return d.target.y; });

            node
                .attr("cx", function(d) { return d.x; })
                .attr("cy", function(d) { return d.y; });
        }
    }
};

// Get graph
aXhttp.open("GET", "http://127.0.0.1:8080/CodeExplorer/graph/d3", true);
aXhttp.send();

