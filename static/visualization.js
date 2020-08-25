function RenderTreeMap()
{
    var data = [5, 10, 45, 98, 65, 21, 9];

    d3.select(".chart")
      .selectAll("div")
      .data(data)
      .enter()
      .append("div")
      .style("width", function(d) { return d + "px"})
      .text(function(d) { return d; });

      

}