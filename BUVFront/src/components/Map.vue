<template>
  <div id="info" height="100%">
    <div id="map">
      <svg id="myMap"></svg>
    </div>
    <div id="profile">
      <div id="name">
        <svg id="nameTitle"></svg>
      </div>
      <div id="events">
        <div id="border"></div>
      </div>
      <div id="button" @click="goback"></div>
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
      .scale(560) // This is like the zoom
      .translate([400, 480]);

    // // add circle border
    // svg
    //   .append("circle")
    //   .attr("r", 320)
    //   .attr("cx", 330)
    //   .attr("cy", 955 / 2)
    //   .attr("fill", "white")
    //   .attr("stroke", "#A2A2A2")
    //   .attr("stroke-width", 2);

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
    goback() {
      this.$router.push("/");
    },
    fetchData(projection, svg) {
      dataService.queryByName({ name: this.name }, (response) => {
        this.info = response;

        let eventText = d3
          .select("#border")
          .append("div")
          .attr("id", "eventTime")
          .style("position", "relative")
          // .style("background-color", "#D3D9D8")
          // .style("border", "solid")
          .style("width", "500px")
          .style("top", "30px")
          .style("left", "25px")
          .style("opacity", 1)
          .style("color", "black")
          .style("font-weight", "bold ")
          .style("font-size", "24px")
          .style("text-align", "left")
          .style("font-family", "思源黑体, 黑体, 楷体")
          .html("<p>" + this.info[0]["time"] + "年" + "</br>" + "</p>");

        let eventText2 = d3
          .select("#border")
          .append("div")
          .attr("id", "event")
          .style("position", "absolute")
          // .style("background-color", "#D3D9D8")
          // .style("border", "solid")
          .style("width", "468px")
          .style("top", "80px")
          .style("left", "25px")
          .style("opacity", 1)
          .style("font-size", "18px")
          .style("text-align", "left")
          .style("font-family", "思源黑体, 黑体, 楷体")
          .html("<p>" + this.info[0]["content"] + "</p>");

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
          .style("font-size", "20px")
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
          let ex = event["content"];
          let exTime = event["time"];

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
                .style("top", d.pageY + "px")
                .style("left", d.pageX - 300 + "px")
                .style("opacity", 1)
                .html("<p>" + locationName + "</p>");
            })
            .on("mouseout", function () {
              d3.select("#event" + i).attr("r", 4);
              return tooltip2.style("opacity", 0.0);
            })
            .on("click", function () {
              var index = i + 1;
              d3.select("#eventTime")
                // .html("<p>" + index + "." + exTime + "年" + "</br>" + ex + "</p>")
                .html("<p>" + exTime + "年" + "</p>")
                .style("opacity", 1.0);
              d3.select("#event")
                // .html("<p>" + index + "." + exTime + "年" + "</br>" + ex + "</p>")
                .html("<p>" + event["content"] + "</p>")
                .style("opacity", 1.0);
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
        // Add name title
        let nameSvg = d3.select("#nameTitle");
        nameSvg
          .append("text")
          .attr("x", 78)
          .attr("y", 345)
          .text(this.name)
          .style("font-family", "Times New Roman, 秋鸿楷, 楷体")
          .style("color", "black")
          .style("font-size", "55px")
          .style("letter-spacing", "8px")
          // .style("font-weight", "bold")
          .style("fill", "#6D776E")
          .style("text-anchor", "end")
          .style("writing-mode", "vertical-lr");

        // Add time text
        let startTime = this.info[0]["time"];
        let endTime = this.info[this.info.length - 1]["time"];
        nameSvg
          .append("text")
          .attr("x", 44)
          .attr("y", 415)
          .text(startTime)
          .style("font-family", "Times New Roman, 秋鸿楷, 楷体")
          .style("font-size", "10px")
          .style("letter-spacing", "2px")
          .style("font-weight", "bold")
          .style("fill", "white");
        // .style("text-anchor", "middle")
        // .style("writing-mode", "vertical-lr");

        nameSvg
          .append("text")
          .attr("x", 423)
          .attr("y", 415)
          .text(endTime)
          .style("font-family", "Times New Roman, 秋鸿楷, 楷体")
          .style("font-size", "10px")
          .style("letter-spacing", "2px")
          .style("font-weight", "bold")
          .style("fill", "white");

        // // Add events text
        // const eventsSvg = d3
        //   .select("#event")
        //   .append("svg")
        //   .attr("width", 300 * this.info.length)
        //   .attr("height", 363);

        // for (let i = 0; i < this.info.length; i++) {
        //   let ex = this.info[i]["content"];
        //   let text = eventsSvg
        //     .append("text")
        //     .attr("class", "origin")
        //     .attr("x", i * 180 + 150)
        //     .attr("y", 10)
        //     .style("font-family", "Times New Roman, 秋鸿楷, 楷体")
        //     .style("font-size", "14px")
        //     .style("letter-spacing", "3px")
        //     // .style("font-weight", "bold")
        //     .style("fill", "#6D776E")
        //     .style("text-anchor", "start")
        //     .style("writing-mode", "vertical-lr");

        //   let strs = [];
        //   for (let j = 0; j < ex.length / 6; j++) {
        //     strs.push(ex.substr(6 * j, 6 * j + 6));
        //   }
        //   console.log(strs);
        //   text
        //     .selectAll("tspan")
        //     .data(strs)
        //     .join("tspan")
        //     .attr("class", "divide")
        //     .attr("y", text.attr("y")) //文本从x=?处开始
        //     .attr("dx", "-25px") //文本较y轴的相对位移，此处也就意味着换行
        //     .text(function (d) {
        //       return d;
        //     });

        //   // d3.selectAll(".origin").remove();
        // }

        // eventsSvg
        //   .selectAll("events")
        //   .data(eventsData)
        //   .join("text")
        //   .attr("x", (d, i) => i * 90 + 30)
        //   .attr("y", 10)
        //   .text((d) => d)
        //   .style("font-family", "Times New Roman, 秋鸿楷, 楷体")
        //   .style("font-size", "20px")
        //   .style("letter-spacing", "3px")
        //   // .style("font-weight", "bold")
        //   .style("fill", "#6D776E")
        //   .style("text-anchor", "start")
        //   .style("writing-mode", "vertical-lr");
      });
    },
  },
  computed: {},
};
</script>

<style scoped>
#info {
  position: relative;
  width: 100%;
  height: 98%;
}

#button {
  position: absolute;
  top: 3%;
  left: 86%;
  width: 60px;
  height: 60px;
  background: url(../assets/back.png) center center no-repeat;
  background-size: 100% 105%;
}

#map {
  position: relative;
  float: left;
  left: 15%;
  width: 40%;
  height: 100%;
}

#myMap {
  position: relative;
  width: 100%;
  height: 100%;
}

#profile {
  position: relative;
  float: left;
  left: 25%;
  width: 30%;
  height: 100%;
}

#name {
  position: relative;
  float: left;
  width: 100%;
  height: 50%;
}

#nameTitle {
  width: 100%;
  height: 100%;
}

#events {
  position: relative;
  float: left;
  width: 100%;
  height: 50%;
}

#border {
  position: relative;
  float: left;
  /* background-color: green; */
  /* left: 20%; */
  width: 100%;
  height: 80%;
  overflow-x: hidden;
  overflow: hidden;
}

#eventTime {
  position: absolute;
  float: left;
  width: 100%;
  height: 98%;
  left: 10%;
  top: 10%;
  font-family: "思源黑体, 黑体, 楷体";
  font-size: "20px";
}

#event {
  position: absolute;
  float: left;
  width: 100%;
  height: 98%;
  font-family: "思源黑体, 黑体, 楷体";
  font-size: "20px";
}

#text {
  font-size: 20px;
}

/* .tooltip {
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
} */

#info {
  background: url(../assets/background.png) center center no-repeat;
  background-size: 100% 105%;
}
</style>

<!-- .style("font-family", "Times New Roman, 秋鸿楷, 楷体")
        //     .style("font-size", "14px")
        //     .style("letter-spacing", "3px")
        //     // .style("font-weight", "bold")
        //     .style("fill", "#6D776E")
        //     .style("text-anchor", "start")
        //     .style("writing-mode", "vertical-lr"); -->