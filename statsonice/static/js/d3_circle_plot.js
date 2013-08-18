// playing with svg
var w = 400;
var h = 200;
var dataset = [35,53,107,260,317,473];
var years = [2007,2008,2009,2010,2011,2012];

var svg = d3.select("#chart").append("svg")
		.attr("width", w)
		.attr("height", h);

var circles = svg.selectAll("circle")
				.data(dataset)
				.enter()
				.append("circle");

// add data first bc white and cannot see at first
svg.selectAll("text")
		.data(dataset)
		.enter()
		.append("text")
		.text(function(d) {
			return d;
		})
		.attr("x", function(d, i) {
			return i* w/dataset.length + 20;
		})
		.attr("y", h/2 + 5)
		.attr("font-family", "sans-serif")
		.attr("font-size", "12px")
		.attr("fill", "white")
		.attr("text-anchor", "middle");

// add numbers to the bar chart
svg.selectAll("text.yAxis")
		.data(years)
		.enter()
		.append("text")
		.text(function(d,i) {
			return years[i];
		})
		.attr("x", function(d,i) {
			return i* w/dataset.length + 20;
		})
		.attr("text-anchor", "middle")
		.attr("y", function(d) {
			return h - 30;
		})
		.attr("font-family", "sans-serif")
		.attr("font-size", "14px")
		.attr("fill", "black");

// draw circles
circles.transition()
		.duration(1000)
		.delay(function(d,i) {return i*1000; })
		.attr("cx", function(d, i) {
			return i* w/dataset.length + 20;
		})
		.attr("cy", h/2)
		.attr("r", function(d) {
			return Math.sqrt(d)+8;
		})
		.attr("fill", "#00AA00")
		.attr("stroke", "#007700")
		.attr("stroke-width", function(d) {
			return Math.sqrt(Math.sqrt(d/10)) + 1;
		});
