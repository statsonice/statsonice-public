// include variables: chart_id, dataset, years, height (h)


//var chart_id = "#chart";
//var dataset = [10,-6,5,1,-10,-3];
//var years = [2007,2008,2009,2010,2011,2012];


var h = 300;
var w = $(chart_id).width();

var barPadding = 6;
var padding = 55;

// choose the midline position for the graph
midline = h/2;
if (d3.max(dataset, function(d) {return d;}) < 0) {
	midline = 0;
} else if (d3.min(dataset, function(d) {return d;}) > 0) {
	midline = h
} else if (d3.max(dataset, function(d) {return d;}) > 0 && d3.min(dataset, function(d) {return d;}) < 0) {
	midline = Math.abs(d3.max(dataset, function(d) {return d;}))/(d3.max(dataset, function(d) {return d;})-d3.min(dataset, function(d) {return d;})) * h;
}

var svg = d3.select(chart_id).append("svg")
			.attr("width",w)
			.attr("height",h);

// y scaling variables
var mag = d3.max(dataset, function(d) {return d;}) - d3.min(dataset, function(d) {return d;});
var yScale = function(d) {
				return d/mag*(h - padding);
			}
/*
var yScale = d3.scale.linear()
				.domain([d3.min(dataset, function(d) {return d;}), d3.max(dataset, function(d) {return d;})])
				.range([-h/2 + padding, h/2 - padding]);
*/

var colorScalePos = d3.scale.linear()
					.domain([0, d3.max(dataset, function(d) {return d;})])
					.range([200,100]);

var colorScaleNeg = d3.scale.linear()
					.domain([d3.min(dataset, function(d) {return d;}), 0])
					.range([150,250]);

var bars = svg.selectAll("rect")
				.data(dataset)

bars
	.enter()
	.append("rect")
	.attr("x", function(d,i) {
		return i* w/dataset.length;
	})
	.attr("y", h/2)
	.attr("width", Math.round(w/dataset.length) - barPadding)
	.attr("height", 0);

bars
	.transition()
	.duration(500)
	.attr("y", function(d) {
			if (d > 0) {
				return midline - padding/2 - yScale(d);
			} else {
				return midline - padding/2;
			}
		})
	.attr("height", function(d) {
		if (d < 0) {
			return -yScale(d);
		} else {
			return yScale(d);
		}
	})
	.attr("fill", function(d) {
		if (d > 0) {
			return "rgb(" + 0 + "," + (colorScalePos(d)) + "," + 0 + ")";
		} else {
			return "rgb(" + (colorScaleNeg(d)) + "," + 0 + "," + 0 + ")";
		}
	})
	.attr("stroke", function(d) {
		if (d > 0) {
			return "rgb(" + 0 + "," + (colorScalePos(d) - 50) + "," + 0 + ")";
		} else {
			return "rgb(" + (colorScaleNeg(d) - 50) + "," + 0 + "," + 0 + ")";
		}
	})
	.attr("stroke-width", 2);

// add numbers to the bar chart
var values = svg.selectAll("text")
		.data(dataset)
		.enter()
		.append("text")
		.text(function(d) {
			return d;
		})
		.attr("x", function(d,i) {
			return i* w/dataset.length + (w/dataset.length - barPadding)/2;
		})
		.attr("text-anchor", "middle")
		.attr("y", function(d) {
			if (d > 0) {
				return midline - padding/2 -  yScale(d) - 5;
			} else {
				return midline - padding/2 - yScale(d) + 15;
			}
		})
		.attr("font-family", "sans-serif")
		.attr("font-size", "14px")
		.attr("fill", "black");

// add years to the bar chart
var xAxis = svg.selectAll("text.xAxis")
		.data(dataset)
		.enter()
		.append("text")
		.text(function(d,i) {
			return years[i];
		})
		.attr("x", function(d,i) {
			return i* w/dataset.length + (w/dataset.length - barPadding)/2;
		})
		.attr("text-anchor", "middle")
		.attr("y", function(d) {
			return h - 5;
		})
		.attr("font-family", "sans-serif")
		.attr("font-size", "14px")
		.attr("fill", "black");

// code to resize the chart when the window is resized
window.onresize = function(event) {
	w = $(chart_id).width();

	bars
		.attr("x", function(d,i) {
			return i* w/dataset.length;
		})
		.attr("width", Math.round(w/dataset.length) - barPadding);

	// add numbers to the bar chart
	values
			.attr("x", function(d,i) {
				return i* w/dataset.length + (w/dataset.length - barPadding)/2;
			})
			.attr("text-anchor", "middle");

	// add numbers to the bar chart
	xAxis
			.attr("x", function(d,i) {
				return i* w/dataset.length + (w/dataset.length - barPadding)/2;
			})
			.attr("text-anchor", "middle");
}