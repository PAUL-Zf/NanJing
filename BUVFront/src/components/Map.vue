<template>
  <div id="info" height="100%">
    <div id="map" height="100%">
      <svg id="myMap"></svg>
    </div>
  </div>
</template>

<script>
import * as d3 from "d3";
import { dataService } from "@/service";

export default {
  name: "Map",
  data() {
    return {
      name: null,
      locationName: null,
      info: null,
    };
  },
  mounted() {
    this.name = this.$route.params.name;
    console.log(this.name);
    // The svg
    var svg = d3.select("svg");

    // Map and projection
    var projection = d3
      .geoMercator()
      .center([108, 31]) // GPS of location to zoom on
      .scale(500) // This is like the zoom
      .translate([340, 500]);

    // add circle border
    svg
      .append("circle")
      .attr("r", 320)
      .attr("cx", 330)
      .attr("cy", 955 / 2)
      .attr("fill", "white")
      .attr("stroke", "#A2A2A2")
      .attr("stroke-width", 2);

    // Load external data and boot
    d3.json("wholeMap.json").then(function (data) {
      // Draw the map
      svg
        .append("g")
        .selectAll("path")
        .data(data.features)
        .join("path")
        .attr("class", (d) => d.properties.name)
        .attr("fill", "white")
        // .attr("opacity", 0.7)
        .attr("d", d3.geoPath().projection(projection))
        .attr("stroke", "#878F9B")
        .attr("stroke-width", 2)
        .attr("stroke-opacity", 0.8);
    });

    // Load external data and boot
    d3.json("test.json").then((data) => {
      // Draw the map
      svg
        .append("g")
        .selectAll("path")
        .data(data.features)
        .join("path")
        .attr("class", (d) => d.properties.name)
        .attr("fill", (d) => (d.properties.name === "" ? "none" : "#D3D9D8"))
        .attr("opacity", 0.7)
        .attr("d", d3.geoPath().projection(projection))
        .attr("stroke", "black")
        .attr("stroke-width", 0.5)
        .attr("stroke-opacity", 0.3);

      // get the info of queried person
      this.fetchData(projection, svg);
    });
  },
  methods: {
    fetchData(projection, svg) {
      dataService.queryByName({ name: this.name }, (response) => {
        this.info = response;

        let tooltip2 = d3
          .select("#map")
          .append("div")
          .attr("class", "tooltip")
          .style("position", "absolute")
          .style("background-color", "#D3D9D8")
          .style("opacity", 0)
          .style("border", "solid")
          .style("border-width", "1px")
          .style("border-radius", "5px")
          .style("padding", "10px");

        // locate point on the map
        const path = d3.geoPath().projection(projection);
        for (let i = 0; i < this.info.length; i++) {
          let event = this.info[i];
          let location = [
            Number(event["location"][0]),
            Number(event["location"][1]),
          ];
          let locationName = event["name"];

          let proLocation = projection(location);
          svg
            .append("circle")
            .attr("id", "event" + i)
            .attr("cx", proLocation[0])
            .attr("cy", proLocation[1])
            .attr("fill", "#878F9B")
            .attr("stroke", "black")
            .attr("stroke-width", 1)
            .attr("r", 4)
            .attr("cursor", "pointer")
            .on("mouseover", function (d) {
              d3.select("#event" + i).attr("r", 6);
              return tooltip2
                .style("top", d.pageY - 80 + "px")
                .style("left", d.pageX + 15 + "px")
                .style("opacity", 1)
                .html("<p>" + locationName + "</p>");
            })
            .on("mouseout", function () {
              d3.select("#event" + i).attr("r", 4);
              return tooltip2.style("opacity", 0.0);
            });

          if (i < this.info.length - 1) {
            let src = [
              Number(event["location"][0]),
              Number(event["location"][1]),
            ];
            let nextEvent = this.info[i + 1];
            let dest = [
              Number(nextEvent["location"][0]),
              Number(nextEvent["location"][1]),
            ];

            let line = { type: "LineString", coordinates: [src, dest] };

            svg
              .append("path")
              .attr("d", path(line))
              .style("fill", "none")
              .style("stroke", "#A57B7A")
              .style("stroke-width", 2.5);
          }
        }
      });
    },
  },
  computed: {},
};
</script>

<style scoped>
#info {
  width: 100%;
  height: 100%;
}

#map {
  position: relative;
  left: 10%;
  width: 35%;
  height: 100%;
}

#myMap {
  width: 100%;
  height: 100%;
}

.tooltip {
  position: absolute;
  width: 80;
  height: auto;
  opacity: 0;
  font-family: simsun;
  font-size: 14px;
  text-align: center;
  border-style: solid;
  border-width: 1px;
  background-color: red;
  border-radius: 5px;
}

#info {
  background: url(../assets/background-00.png) center center no-repeat;
  background-size: 100% 100%;
}
</style>