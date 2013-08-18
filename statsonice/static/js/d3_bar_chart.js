// include variables: chart_id, dataset, years, height (h)

/*
var chart_id = chart_id;
var dataset = dataset;
var years = years;
var h = height;
*/

var w = $(chart_id).width();

var barPadding = 6;
var bottomPadding = 100;
var topPadding = 50;

var svg = d3.select(chart_id).append("svg")
			.attr("width",w)
			.attr("height",h);

var yScale = d3.scale.linear()
				.domain([d3.min(dataset, function(d) {return d;}), d3.max(dataset, function(d) {return d;})])
				.range([bottomPadding, h - topPadding]);

var colorScale = d3.scale.linear()
					.domain([d3.min(dataset, function(d) {return d;}), d3.max(dataset, function(d) {return d;})])
					.range([200,100]);

var bars = svg.selectAll("rect")
				.data(dataset)

bars
	.enter()
	.append("rect")
	.attr("x", function(d,i) {
		return i* w/dataset.length;
	})
	.attr("y", h - 30)
	.attr("width", Math.round(w/dataset.length) - barPadding)
	.attr("height", 0);

bars
	.transition()
	.duration(1000)
	.attr("y", function(d) {
		return h - yScale(d) - 30;
	})
	.attr("height", function(d) {return yScale(d);})
	.attr("fill", function(d) {
		return "rgb(" + (colorScale(d)) + "," + 0 + "," + (colorScale(d)) + ")";
	})
	.attr("stroke", function(d) {
		return "rgb(" + (colorScale(d) - 50) + "," + 0 + "," + (colorScale(d) - 50) + ")";
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
			return h - yScale(d) - 10;
		})
		.attr("font-family", "sans-serif")
		.attr("font-size", "14px")
		.attr("fill", "white");

// add numbers to the bar chart
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
			return h - 10;
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

