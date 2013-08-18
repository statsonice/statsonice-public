/*
TODO:
- change back to nested goe data or make elementstats class return flat arrays
- fix resize issue
*/

// div with chart has id="element_stats"
//var element_stats = "#element_stats";
var w = $(element_stats).width();
//var w = 600;
var h = 300;
var xPadding = 10;
var yPadding = 10;

var svg = d3.select(element_stats).append("svg")
            .attr("width",w)
            .attr("height",h);

var current_chart = "bar_chart";

/*
Data
*/

/*
years = [2006,2007,2008,2009,2010,2011];
goes = [300,200,400,100,500,50,600,100,200,400,600,100,900,100,200,900,400,250,700,200,100,700,600,500,700,200,100,700,600,500,700,200,100,700,600,500];
time_series = [4,8,15,16,23,42];
*/

/*
Functions to draw the different graphs for the element stats
*/
var draw_error_chart = function() {
  clear_current_chart();

  var text = svg.selectAll("text.info")
                .data([1])
                .enter()
                .append("text");

  text
    .attr("x",w/3)
    .attr("y",h/3)
    .text("NOT ENOUGH DATA TO DISPLAY CHART");
}

var draw_goe_bar_chart = function() {

  clear_current_chart();

  var xScale = d3.scale.linear()
                  .domain([0,goes.length])
                  .range([xPadding,w-xPadding]);

  var yScale = d3.scale.linear()
                  .domain([0,d3.max(goes, function(d) {return d;})])
                  .range([yPadding,h-3*yPadding]);

  var colorScale = d3.scale.linear()
                      .domain([0,d3.max(goes, function(d) {return d;})])
                      .range([50,200]);

  var block_width = (w - 2*xPadding - Math.floor(goes.length/6)*20 - goes.length)/goes.length;

  var blocks = svg.selectAll("rect")
                  .data(goes)
                  .enter()
                  .append("rect");

  blocks
    .attr("x",function(d,i) {
        return xPadding + Math.floor(i/6)*20 + i*(block_width+1);
    })
    .attr("width",block_width)
    .attr("y",h-20)
    .attr("height",0);

  blocks
    .transition()
    .duration(500)
    .attr("y",function(d) {
        return h - yScale(d)-20;
    })
    .attr("height",function(d,i) {
        return yScale(d);
    })
    .attr("fill", function(d,i) {
      if (i%6 < 3) {
        return "rgb(" + 150 + "," + 0 + "," + 0 + ")";
      } else {
        return "rgb(" + 0 + "," + 150 + "," + 0 + ")";
      }
    });

  // add x-axis labels
  var text = svg.selectAll("text.xAxis")
                .data(years)
                .enter()
                .append("text");

  text
    .text(function(d) {
			return d;
		})
		.attr("x", function(d,i) {
			return i* (w-2*xPadding)/years.length + (w/years.length)/2;
		})
		.attr("text-anchor", "middle")
		.attr("y", function(d) {
			return h;
		})
		.attr("font-family", "sans-serif")
		.attr("font-size", "14px")
		.attr("fill", "black");

	// add data labels to bars
  var data_labels = svg.selectAll("text")
                .data(goes)
                .enter()
                .append("text");

  data_labels
    .text(function(d) {
			return d;
		})
		.attr("x", function(d,i) {
			return (1.8)*xPadding + Math.floor(i/6)*20 + i*(block_width+1);
		})
		.attr("text-anchor", "middle")
		.attr("y", function(d) {
			return h-yScale(d)-22;
		})
		.attr("font-family", "sans-serif")
		.attr("font-size", "11px")
		.attr("fill", "black");



  current_chart = "bar_chart";
}

var draw_time_series = function() {

  clear_current_chart();
  var data = time_series;

  var xScale = d3.scale.linear()
                  .domain([0,data.length])
                  .range([xPadding,w-xPadding]);

  var yScale = d3.scale.linear()
                  .domain([0,d3.max(data, function(d) {return d;})])
                  .range([yPadding,h-2*yPadding]);

  var colorScale = d3.scale.linear()
                      .domain([0,d3.max(data, function(d) {return d;})])
                      .range([200,100]);

  var block_width = Math.floor((w - 2*xPadding - data.length*10)/data.length);

  var blocks = svg.selectAll("rect")
                  .data(data)
                  .enter()
                  .append("rect");

  blocks
    .attr("x",function(d,i) {
      return xPadding + i*(block_width+10);
    })
    .attr("width",block_width)
    .attr("y",h - 20)
    .attr("height",0);

  blocks
    .transition()
    .duration(500)
    .attr("y",function(d) {
      return h - yScale(d) - 20;
    })
    .attr("height",function(d,i) {
      return yScale(d);
    })
    .attr("fill", function(d,i) {
      return "rgb(" + colorScale(d) + "," + 0 + "," + colorScale(d) + ")";
    })
    .attr("stroke-width", 2)
    .attr("stroke", function(d,i) {
      return "rgb(" + (colorScale(d)-50) + "," + 0 + "," + (colorScale(d)-50) + ")";
    });

  // add x-axis labels
  var text = svg.selectAll("text.xAxis")
                .data(years)
                .enter()
                .append("text");

  text
    .text(function(d) {
			return d;
		})
		.attr("x", function(d,i) {
			return i* (w-2*xPadding)/data.length + (w/data.length)/2;
		})
		.attr("text-anchor", "middle")
		.attr("y", function(d) {
			return h;
		})
		.attr("font-family", "sans-serif")
		.attr("font-size", "14px")
		.attr("fill", "black");

	// add data labels to bars
  var data_labels = svg.selectAll("text.labels")
                      .data(data)
                      .enter()
                      .append("text");

  data_labels
    .text(function(d) {
      return d;
    })
    .attr("x", function(d,i) {
      return i* (w-2*xPadding)/data.length + (w/data.length)/2;
    })
    .attr("text-anchor", "middle")
    .attr("y", function(d) {
      return h - yScale(d);
    })
    .attr("font-family", "sans-serif")
    .attr("font-size", "14px")
    .attr("fill", "white");

  current_chart = "time_series";
}

var draw_modifier_chart = function() {
  clear_current_chart();
  // some code
  current_chart = "modifier_chart";
}

var draw_skater_chart = function() {
  clear_current_chart();
  // some code
  current_chart = "skater_chart";
}


/*
Redraw and clear functions
*/
var clear_current_chart = function() {
  svg.selectAll("rect").data([]).exit().remove();
  svg.selectAll("text").data([]).exit().remove();
}

var redraw_current_chart = function() {
  clear_current_chart();
  if (current_chart == "time_series") {
    draw_time_series();
  } else if (current_chart == "bar_chart") {
    if (goes.length == 0) {
      draw_error_chart();
    } else {
      draw_goe_bar_chart();
    }
  } else if (current_chart == "modifier_chart") {
    draw_modifier_chart();
  } else if (current_chart == "skater_chart") {
    draw_skater_chart();
  }
}


var draw_radio_chart = function() {
  var buttons = document.getElementsByName("group2");
  var chart_name = 0;

  for (var i=0, iLen=buttons.length; i<iLen; i++) {
    if (buttons[i].checked) {
      chart_name = buttons[i].value;
    }
  }

  if (chart_name == "time_series") {
    draw_time_series();
  } else if (chart_name == "bar_chart") {
    if (goes.length == 0) {
      draw_error_chart();
    } else {
      draw_goe_bar_chart();
    }
  } else if (chart_name == "modifier_chart") {
    draw_modifier_chart();
  } else if (chart_name == "skater_chart") {
    draw_skater_chart();
  }
}

/*
Event methods
*/
window.onresize = function(event) {
    w = $(element_stats).width();
    redraw_current_chart();
}

/*
Initialize Chart
*/
if (goes.length == 0) {
  draw_error_chart();
} else {
  draw_goe_bar_chart();
}


