<template>
  <div class="select">
    <div id="my_chart"></div>
    <router-view />
  </div>
</template>

<script>
import * as d3 from "d3";
import { dataService } from "../service";

export default {
  name: "Selection",
  props: ["msg"],
  data() {
    return {
      allData: null,
      selectedPie: undefined,
    };
  },
  mounted() {
    dataService.fetchAllData({ msg: 0 }, (response) => {
      this.allData = response;
      this.showChart7();
    });
  },
  methods: {
    showChart7() {
      // 线+背景+动画+图例+时间轴
      // 参考：https://d3-graph-gallery.com/interactivity.html
      // https://d3-graph-gallery.com/graph/interactivity_brush.html#brushingforzoom
      var margin = { top: 30, right: 30, bottom: 30, left: 30 },
        width = 1600 - margin.left - margin.right,
        height = 900 - margin.top - margin.bottom;
      var centralPoint = [width / 2 + 200, height / 2];
      var c = {
        1: "#7c9d7f",
        2: "#3d3d3d",
        3: "#953e62",
        4: "#d4bb6e",
        5: "#801e2c",
        6: "#2b5389",
        7: "#a57749",
      }; //按数量由小到大
      var numlist = [
        { figure_type_id: 1, num: 5, type: "体育名将" },
        { figure_type_id: 2, num: 7, type: "工商业代表" },
        { figure_type_id: 3, num: 10, type: "中西名医" },
        { figure_type_id: 4, num: 23, type: "艺术大师" },
        { figure_type_id: 5, num: 39, type: "政治人物" },
        { figure_type_id: 6, num: 48, type: "科技栋梁" },
        { figure_type_id: 7, num: 70, type: "文史哲名家" },
      ]; //固定的顺序
      var innerRadius = 80;
      var outerRadius = 380;
      var imgWidth = 250;
      var myDomain = [1840, 2030];
      var d = this.allData.people;
      d = d.sort(function (a, b) {
        return a.figure_type_id - b.figure_type_id;
      }); // 要按类型升序排序

      //SCALE
      var x = d3
        .scaleBand()
        .range([Math.PI / 2 + 0.04, Math.PI / 2 + 2 * Math.PI - 0.1])
        .align(0)
        .domain(d.map((datum) => datum.name));
      var y = d3
        .scaleLinear()
        .range([innerRadius, outerRadius])
        .domain(myDomain);

      //SVG
      var svg = d3
        .select("#my_chart")
        .append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
        .attr("id", "main_svg")
        .append("g")
        .attr("id", "main")
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

      // //TITLE
      // // var titleImgPos = [-150, 0];
      // var titleContentPos = [30, 50];
      // svg
      //   .append("g")
      //   .attr("id", "title")
      //   // .append("image") //https://blog.csdn.net/weixin_44331765/article/details/112391810
      //   // .attr("id", "imgTitle")
      //   // .attr("href", "title.png") //图片放在public下就可以 https://blog.csdn.net/qq_30306717/article/details/121129193
      //   // .attr(
      //   //   "transform",
      //   //   "translate(" + titleImgPos[0] + "," + titleImgPos[1] + ")"
      //   // );

      // // d3.select("#title")
      //   .append("text")
      //   .attr("id", "titleContent")
      //   .attr("x", titleContentPos[0])
      //   .attr("y", titleContentPos[1])
      //   .text("遇见南京·数百年风流人物")
      //   .style("font-family", "秋鸿楷, 楷体")
      //   .style("font-size", "50px")
      //   // .style("letter-spacing", "1px")
      //   .style("font-weight", "bold")
      //   .style("fill", "#6D776E")
      //   // .style("text-anchor", "middle")
      //   .style("writing-mode", "vertical-lr");

      //CENTRAL IMAGE
      var img_x = centralPoint[0] - imgWidth / 2;
      var img_y = height / 2 - imgWidth / 2;
      svg
        .append("g")
        .attr("id", "centralImage")
        .attr("transform", "translate(" + img_x + "," + img_y + ")");

      svg
        .select("#centralImage")
        .append("image") //https://blog.csdn.net/weixin_44331765/article/details/112391810
        .attr("id", "imgProfile")
        .attr("href", "center.png") //图片放在public下就可以 https://blog.csdn.net/qq_30306717/article/details/121129193
        .style("width", `${imgWidth}px`)
        .style("height", `${imgWidth}px`);

      // RADIAL BARS
      var barsGroup = svg
        .append("g")
        .attr("id", "barsGroup")
        .attr(
          "transform",
          "translate(" + centralPoint[0] + "," + height / 2 + ")"
        );

      var pie = d3
        .pie()
        .startAngle(Math.PI / 2 + 0.04)
        .endAngle(Math.PI / 2 + 2 * Math.PI - 0.1)
        .sort(null)
        .value(function (d) {
          return d.num;
        });
      var arcData = pie(numlist);

      var arc = d3
        .arc()
        .innerRadius(innerRadius + 40)
        .outerRadius(outerRadius - 18);

      var duration = 250;

      var arc_path = barsGroup
        .selectAll(".arc")
        .data(arcData)
        .enter()
        .append("g")
        .attr("class", "arc")
        .attr("id", (d) => d.index)
        .style("cursor", "pointer")
        .on("mouseover", (event, v) => {
          d3.select(event.currentTarget)
            .transition()
            .duration(duration)
            .attr("transform", this.calcTranslate(v, 10));
          d3.select(event.currentTarget)
            .select("path")
            .transition()
            .duration(duration)
            .attr("fill", (d) => c[d.index + 1])
            .attr("opacity", 0.5);
        })
        .on("mouseout", (event, v) => {
          d3.select(event.currentTarget)
            .transition()
            .duration(duration)
            .attr("transform", "translate(0, 0)");
          d3.select(event.currentTarget)
            .select("path")
            .transition()
            .duration(duration)
            .attr("fill", (d) => c[d.index + 1])
            .attr("opacity", 0.1);
        })
        .on("click", (event, v) => {
          this.pieClick(v.index);
          d3.select("#barsGroup").selectAll(".selected").remove();
          d3.select("#barsGroup").selectAll(".selectedgroup").remove();

          if (this.selectedPie != undefined) {
            var data = this.getPeopleOfType(d, this.selectedPie);

            var groups = d3
              .select("#barsGroup")
              .append("g")
              .attr("class", "selectedgroup");

            var small_arc = d3
              .arc()
              .innerRadius((d) =>
                y(
                  d.data.birth_time == null
                    ? d.data.experience_start
                    : d.data.birth_time
                )
              ) //注意是d.data.xxxx 原来的数据放到下一级了
              .outerRadius((d) =>
                y(d.data.death_time == 9999 ? 2022 : d.data.death_time)
              )
              .padAngle(0.15)
              .padRadius(10);

            const small_pie = d3
              .pie()
              .startAngle(arcData[this.selectedPie].startAngle)
              .endAngle(arcData[this.selectedPie].endAngle)
              .sort(null)
              .value(function (d) {
                return 1;
              });

            var small_arcData = small_pie(data);

            const arcTween = function (d) {
              //都是从角度为0的位置到最终位置之间的插值，这样扇形一直是连续的
              var interpolate_end = d3.interpolate(d.startAngle, d.endAngle);
              return function (t) {
                d.endAngle = interpolate_end(t);
                return small_arc(d);
              };
            };

            groups
              .selectAll("path")
              .data(small_arcData)
              .enter()
              .append("path")
              .attr("data-id", (d) => d.data.id)
              .attr("class", "selected")
              .attr("fill", (d) => c[d.data.figure_type_id])
              .attr("opacity", 1)
              .style("cursor", "pointer")
              // .on("click", (e, value) => {
              .on("mouseover", (e, value) => {
                d3.select(e.currentTarget).attr("opacity", 0.5);
                d3.select("#" + value.data.name)
                  .transition()
                  .duration(duration - 100)
                  .style("font-weight", "bold")
                  .style("font-size", "15px");

                //PROFILE
                var profile = d3
                  .select("#main_svg")
                  .append("svg")
                  .attr("id", "profile")
                  .append("g");

                var r = [300, 150];
                var detailspos = [width / 2 - r[0], height / 2 + r[1]];

                profile
                  .append("text")
                  .attr("class", "details")
                  .attr("id", "name")
                  .attr("x", detailspos[0])
                  .attr("y", detailspos[1])
                  .text(value.data.name)
                  .style("font-family", "Times New Roman, 秋鸿楷, 楷体")
                  .style("font-size", "30px")
                  .style("fill", "black")
                  .style("text-anchor", "middle");

                var alias =
                  value.data.alias == null
                    ? ""
                    : "【别名】" + value.data.alias.split("；", 3);
                profile
                  .append("text")
                  .attr("class", "details")
                  .attr("id", "alias")
                  .attr("x", detailspos[0])
                  .attr("y", detailspos[1] + 30)
                  .text(alias)
                  .style("font-family", "Times New Roman, 秋鸿楷, 楷体")
                  .style("font-size", "20px")
                  .style("fill", "#6D776E")
                  .style("text-anchor", "middle");

                var label =
                  value.data.labels == null
                    ? ""
                    : value.data.labels.split("；", 3);
                profile
                  .append("text")
                  .attr("class", "details")
                  .attr("id", "labels")
                  .attr("x", detailspos[0])
                  .attr("y", detailspos[1] + 60)
                  .text(label)
                  .style("font-family", "Times New Roman, 秋鸿楷, 楷体")
                  .style("font-size", "20px")
                  .style("fill", "black")
                  .style("text-anchor", "middle");

                var w = [
                  d3.select("#name").node().getBBox().width,
                  d3.select("#alias").node().getBBox().width,
                  d3.select("#labels").node().getBBox().width,
                ];
                var imgSize = [d3.max(w) + 70, 180];
                var profilePos = [
                  detailspos[0] - imgSize[0] / 2,
                  detailspos[1] - 70,
                ];
                var recSize = [d3.max(w) + 68, 175];
                var rectPos = [
                  detailspos[0] - recSize[0] / 2,
                  detailspos[1] - 65,
                ];

                profile
                  .append("rect")
                  .attr(
                    "transform",
                    "translate(" + rectPos[0] + "," + rectPos[1] + ")"
                  )
                  .attr("width", recSize[0])
                  .attr("height", recSize[1])
                  // .attr("fill", "#E8DBB7")
                  .attr("fill", "#CED7D2")
                  .attr("opacity", 0.8)
                  .lower(); //相反 raise()

                profile
                  .append("image") //https://blog.csdn.net/weixin_44331765/article/details/112391810
                  .attr("id", "imgProfile")
                  .attr("href", "details-04.png") //图片放在public下就可以 https://blog.csdn.net/qq_30306717/article/details/121129193
                  .attr(
                    "transform",
                    "translate(" + profilePos[0] + "," + profilePos[1] + ")"
                  )
                  .attr("width", imgSize[0])
                  .attr("height", imgSize[1])
                  .attr("preserveAspectRatio", "none meet"); //https://blog.csdn.net/zf2014122891/article/details/124044440
              })
              .on("mouseout", (event, value) => {
                d3.select("#main_svg").selectAll("#profile").remove();
                d3.select(event.currentTarget).attr("opacity", 1);

                d3.select("#" + value.data.name)
                  .transition()
                  .duration(duration)
                  .style("font-weight", "normal")
                  .style("font-size", "13px");
              })
              .on("click", (event, v) => {
                // console.log(v.data.name);
                this.$router.push({
                  name: "about",
                  params: { name: v.data.name },
                });
              })
              .transition()
              .duration(500)
              .attrTween("d", arcTween);
          }
        });

      arc_path
        .append("path")
        .attr("d", arc)
        .attr("fill", (d) => c[d.index + 1])
        .attr("opacity", 0.1)
        .attr("stroke", "white");
      // RADIAL LINES
      var lineGroup = svg.append("g").attr("id", "lineGroup");

      lineGroup
        .selectAll("my_line")
        .data(d)
        .enter()
        .append("line")
        .attr("x1", function (d) {
          return (
            centralPoint[0] +
            y(d.birth_time == null ? d.experience_start : d.birth_time) *
              Math.cos(x(d.name) - Math.PI * 0.5)
          );
        })
        .attr("x2", function (d) {
          return (
            centralPoint[0] +
            y(d.death_time == 9999 ? 2022 : d.death_time) *
              Math.cos(x(d.name) - Math.PI * 0.5)
          );
        })
        .attr("y1", function (d) {
          return (
            height / 2 +
            y(d.birth_time == null ? d.experience_start : d.birth_time) *
              Math.sin(x(d.name) - Math.PI * 0.5)
          );
        })
        .attr("y2", function (d) {
          return (
            height / 2 +
            y(d.death_time == 9999 ? 2022 : d.death_time) *
              Math.sin(x(d.name) - Math.PI * 0.5)
          );
        })
        .attr("stroke", (d) => c[d.figure_type_id])
        .attr("opacity", 0.5)
        .attr("stroke-width", "1.5px");

      // PEOPLE'S INFO
      var infoGroup = svg
        .append("g")
        .attr("id", "info")
        .attr(
          "transform",
          "translate(" + centralPoint[0] + "," + height / 2 + ")"
        );

      infoGroup
        .selectAll("g")
        .data(d)
        .enter()
        .append("g")
        .attr("class", "peopleInfo")
        .attr("id", (d) => d.id)
        .attr("opacity", 0.8)
        .attr("transform", function (d) {
          const angleToRotate = (x(d.name) * 180) / Math.PI - 90;
          return `rotate(${angleToRotate})`;
        })
        .attr("text-anchor", function (d) {
          return (x(d.name) + Math.PI) % (2 * Math.PI) < Math.PI
            ? "end"
            : "start";
        })
        .each(function (datum) {
          const el = d3.select(this);

          // NAMES
          el.append("text")
            .attr("id", (datum) => datum.name)
            .attr("x", function (d) {
              return (x(datum.name) + Math.PI) % (2 * Math.PI) < Math.PI
                ? -(outerRadius - 20) - 10
                : outerRadius - 20 + 10;
            })
            .attr("y", 0)
            .text((datum) => datum.name)
            .style("font-size", "13px")
            .style("font-family", "秋鸿楷, 楷体")
            .style("font-weight", "normal")
            .style("dominant-baseline", "middle")
            // Rotation to improve readability
            .attr("transform", function (datum) {
              return (x(datum.name) + Math.PI) % (2 * Math.PI) < Math.PI
                ? "rotate(180)"
                : "rotate(0)";
            });
        });

      // TIME RINGS
      var decades = [1900, 1930, 1960, 1990, 2020];
      var constDates = svg.append("g").attr("id", "circlesDates");

      constDates
        .selectAll("circle")
        .data(decades)
        .join("circle")
        .attr("cx", centralPoint[0])
        .attr("cy", height / 2)
        .attr("r", (d) => y(d))
        .style("fill", "none")
        .style("stroke", "#D8D9DB")
        .style("stroke-width", "2")
        .style("pointer-events", "none");

      constDates
        .selectAll("text")
        .data(decades)
        .join("text")
        .attr("x", (d) => centralPoint[0] + y(d) + 2)
        .attr("y", (d) => height / 2)
        .text((d) => d)
        .style("fill", "#6D776E")
        .style("opacity", 0.7)
        .style("font-size", "12px")
        .style("pointer-events", "none");

      //LEGEND
      var legendPos = [240, 750];
      var interval = [50, 3]; // 横向距 纵向距
      var iconSize = [50, 50];
      var legend = svg
        .append("g")
        .attr("id", "legend")
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")")
        .selectAll("g")
        .data(numlist)
        .enter()
        .append("g")
        .attr("id", (d) => "legend-" + d.figure_type_id)
        .attr("class", "legend")
        .style("cursor", "pointer")
        .on("click", (event, v) => {
          this.pieClick(v.figure_type_id - 1);
          d3.select("#barsGroup").selectAll(".selected").remove();
          d3.select("#barsGroup").selectAll(".selectedgroup").remove();
          if (this.selectedPie != undefined) {
            var data = this.getPeopleOfType(d, this.selectedPie);

            var groups = d3
              .select("#barsGroup")
              .append("g")
              .attr("class", "selectedgroup");

            var small_arc = d3
              .arc()
              .innerRadius((d) =>
                y(
                  d.data.birth_time == null
                    ? d.data.experience_start
                    : d.data.birth_time
                )
              ) //注意是d.data.xxxx 原来的数据放到下一级了
              .outerRadius((d) =>
                y(d.data.death_time == 9999 ? 2022 : d.data.death_time)
              )
              .padAngle(0.15)
              .padRadius(10);

            const small_pie = d3
              .pie()
              .startAngle(arcData[this.selectedPie].startAngle)
              .endAngle(arcData[this.selectedPie].endAngle)
              .sort(null)
              .value(function (d) {
                return 1;
              });

            var small_arcData = small_pie(data);

            const arcTween = function (d) {
              //都是从角度为0的位置到最终位置之间的插值，这样扇形一直是连续的
              var interpolate_end = d3.interpolate(d.startAngle, d.endAngle);
              return function (t) {
                d.endAngle = interpolate_end(t);
                return small_arc(d);
              };
            };

            groups
              .selectAll("path")
              .data(small_arcData)
              .enter()
              .append("path")
              .attr("data-id", (d) => d.data.id)
              .attr("class", "selected")
              .attr("fill", (d) => c[d.data.figure_type_id])
              .attr("opacity", 1)
              .style("cursor", "pointer")
              // .on("click", (e, value) => {
              .on("mouseover", (e, value) => {
                d3.select(e.currentTarget).attr("opacity", 0.5);
                d3.select("#" + value.data.name)
                  .transition()
                  .duration(duration - 100)
                  .style("font-weight", "bold")
                  .style("font-size", "15px");

                var profile = d3
                  .select("#main_svg")
                  .append("svg")
                  .attr("id", "profile")
                  .append("g");

                var r = [300, 150];
                var detailspos = [width / 2 - r[0], height / 2 + r[1]];

                profile
                  .append("text")
                  .attr("class", "details")
                  .attr("id", "name")
                  .attr("x", detailspos[0])
                  .attr("y", detailspos[1])
                  .text(value.data.name)
                  .style("font-family", "Times New Roman, 秋鸿楷, 楷体")
                  .style("font-size", "30px")
                  .style("fill", "black")
                  .style("text-anchor", "middle");

                var alias =
                  value.data.alias == null
                    ? ""
                    : "【别名】" + value.data.alias.split("；", 3);
                profile
                  .append("text")
                  .attr("class", "details")
                  .attr("id", "alias")
                  .attr("x", detailspos[0])
                  .attr("y", detailspos[1] + 30)
                  .text(alias)
                  .style("font-family", "Times New Roman, 秋鸿楷, 楷体")
                  .style("font-size", "20px")
                  .style("fill", "#6D776E")
                  .style("text-anchor", "middle");

                var label =
                  value.data.labels == null
                    ? ""
                    : value.data.labels.split("；", 3);
                profile
                  .append("text")
                  .attr("class", "details")
                  .attr("id", "labels")
                  .attr("x", detailspos[0])
                  .attr("y", detailspos[1] + 60)
                  .text(label)
                  .style("font-family", "Times New Roman, 秋鸿楷, 楷体")
                  .style("font-size", "20px")
                  .style("fill", "black")
                  .style("text-anchor", "middle");

                var w = [
                  d3.select("#name").node().getBBox().width,
                  d3.select("#alias").node().getBBox().width,
                  d3.select("#labels").node().getBBox().width,
                ];
                var imgSize = [d3.max(w) + 70, 180];
                var profilePos = [
                  detailspos[0] - imgSize[0] / 2,
                  detailspos[1] - 70,
                ];
                var recSize = [d3.max(w) + 68, 175];
                var rectPos = [
                  detailspos[0] - recSize[0] / 2,
                  detailspos[1] - 65,
                ];

                profile
                  .append("rect")
                  .attr(
                    "transform",
                    "translate(" + rectPos[0] + "," + rectPos[1] + ")"
                  )
                  .attr("width", recSize[0])
                  .attr("height", recSize[1])
                  // .attr("fill", "#E8DBB7")
                  .attr("fill","#CED7D2")
                  .attr("opacity", 0.8)
                  .lower()//相反 raise()

                profile
                  .append("image") //https://blog.csdn.net/weixin_44331765/article/details/112391810
                  .attr("id", "imgProfile")
                  .attr("href", "details-04.png") //图片放在public下就可以 https://blog.csdn.net/qq_30306717/article/details/121129193
                  .attr(
                    "transform",
                    "translate(" + profilePos[0] + "," + profilePos[1] + ")"
                  )
                  .attr("width", imgSize[0])
                  .attr("height", imgSize[1])
                  .attr("preserveAspectRatio", "none meet"); //https://blog.csdn.net/zf2014122891/article/details/124044440
              })
              .on("mouseout", (event, value) => {
                d3.select("#main_svg").selectAll("#profile").remove();
                d3.select(event.currentTarget).attr("opacity", 1);

                d3.select("#" + value.data.name)
                  .transition()
                  .duration(duration)
                  .style("font-weight", "normal")
                  .style("font-size", "13px");
              })
              .on("click", (event, v) => {
                this.$router.push({
                  name: "about",
                  params: { name: v.data.name },
                });
              })
              .transition()
              .duration(500)
              .attrTween("d", arcTween);
          }
        });

      var x2 = function (i) {
        return legendPos[0] + interval[0] * (i - 1);
      };
      var y2 = legendPos[1];
      var y1 = legendPos[1] + interval[1];
      var x1 = function (i) {
        return legendPos[0] + interval[0] * (i - 1) - iconSize[0] / 2;
      };

      legend.each(function (d) {
        const el = d3.select(this);
        // console.log(d.type);
        // .attr("transform", "translate(" + legendPos[0] + interval * i + "," + legendPos[1] + ")")
        el.append("image")
          .attr("id", "imgLegend-" + d.figure_type_id)
          .attr("href", "cloud/" + d.figure_type_id + "-cloud-03.png") //图片放在public下就可以 https://blog.csdn.net/qq_30306717/article/details/121129193
          .attr(
            "transform",
            "translate(" + x1(d.figure_type_id) + "," + y1 + ")"
          )
          .attr("width", iconSize[0])
          .attr("height", iconSize[1]);

        el.append("text")
          .text(d.type)
          // .text("text")
          .attr("x", (d) => x2(d.figure_type_id))
          .attr("y", y2)
          .style("text-anchor", "end")
          .style("font-family", "秋鸿楷, 楷体")
          .style("font-size", "18px")
          .style("writing-mode", "vertical-lr");

      });

        //TIME SELECTOR
        var peoNumOfYear = this.getPeoNumOfYear(d) //data
        console.log(peoNumOfYear)
        var h = 70, w = 1530

        var timeselector = svg
            .append("g")
            .attr("id", "timeselector")

        var timeselectorPos = [w,h]
        var timescale = [1830,2030]
        var timescaler = d3.scaleLinear()
            .domain(timescale)
            .range([ 0, height - 100 ]);
        timeselector.append("g")
            .attr("id","timescaler")
            .attr("transform", "translate(" + timeselectorPos[0] + "," + timeselectorPos[1] + ")")
            .call(d3.axisRight(timescaler).ticks(5));

        var numscalePos = [w-100, h]
        var numscaler = d3.scaleLinear()
            .domain([0,200])
            .range([100,0])
            
        timeselector.append("g")
            .attr("id","numscaler")
            .attr("transform", "translate(" + numscalePos[0] + "," + numscalePos[1] + ")")
            .call(d3.axisTop(numscaler).ticks(1));


        // Plot the area
        timeselector.append("path")
            .attr("class", "mypath")
            .datum(peoNumOfYear)
            .attr("fill", "#8CA287")
            // .attr("fill", function (d, i) {
            //       return d3.interpolateRgb("#8CA287", "white" )(normalize(d.num));})
            .attr("opacity", 0.5)
            // .attr("stroke", "#000")
            .attr("stroke","#FCD551")
            .attr("stroke-width", 1)
            .attr("stroke-linejoin", "round")
            .attr("transform", "translate(" + numscalePos[0] + "," + numscalePos[1] + ")")
            .attr("d", d3
                        .area()
                        .y(function(d) { return timescaler(d.year) })
                        .x0(numscaler(0))
                        .x1(function(d) { return numscaler(d.num) })
                        .curve(d3.curveCardinal.tension(1))
            )

        timeselector.append("text")
          .text("时间")
          .attr("x", timeselectorPos[0] + 20)
          .attr("y", timeselectorPos[1])
          .style("text-anchor", "start")
          .style("font-family", "秋鸿楷, 楷体")
          .style("font-size", "18px")
          .style("writing-mode", "vertical-lr");

        timeselector.append("text")
          .text("数量")
          .attr("x", timeselectorPos[0] - 10)
          .attr("y", timeselectorPos[1] - 15)
          .style("text-anchor", "end")
          .style("font-family", "秋鸿楷, 楷体")
          .style("font-size", "18px")
          

        //TIPS
        var tipPos = [1350, height];
        var tips = svg
          .append("g")
          .attr("id", "tips")
          .attr("transform", "translate(" + tipPos[0] + "," + tipPos[1] + ")")
          .append("text")
          .text("注：何民魂出生年份不详，以其主要经历起始年份暂代。")
          .style("font-family", "秋鸿楷, 楷体")
          .style("font-size", "12px")
          .style("fill", "#6D776E")
          .style("opacity", 0.8)
          .style("text-anchor", "middle");
    },
    calcTranslate(data, move = 4) {
      // showChart4()
      const moveAngle = data.startAngle + (data.endAngle - data.startAngle) / 2;
      return `translate(${-move * Math.cos(moveAngle + Math.PI / 2)}, ${
        -move * Math.sin(moveAngle + Math.PI / 2)
      })`;
    },
    pieClick(index) {
      //index!
      if (this.selectedPie == index) {
        this.selectedPie = undefined;
      } else {
        this.selectedPie = index;
      }
      this.$store.commit("test/selectPie", index);
    },
    getPeopleOfType(data, index) {
      var dataOfType = [];
      data.forEach((d) => {
        if (d.figure_type_id == index + 1) {
          dataOfType.push(d);
        }
      });
      return dataOfType;
    },
    getPeoNumOfYear(data) {
            var numOfYear = []
            // console.log(data[0].birth_time)
            for(var i=1837; i<=2022; i++){
                // numOfYear[String(i)] = 0
                var noy = {}
                noy["year"] = i
                noy["num"] = 0
                data.forEach(d => {
                    if(d.birth_time == null) d.birth_time = d.experience_start
                    if(d.birth_time <= i && d.death_time > i){
                        noy["num"] += 1
                    }
                })
                numOfYear.push(noy)
            }
            // console.log(numOfYear)
            return numOfYear
    },
  },
  watch: {},
};
</script>

<style scoped>
button {
  height: 30px;
  width: 100px;
}

#my_chart {
  background: url(../assets/background-1.png) center center no-repeat;
  background-size: 100% 100%;
}
</style>