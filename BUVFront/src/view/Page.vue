<template>
  <div class="main-page" style="height: 100%">
    <Main style="width: 100%; height: 100%"></Main>
  </div>
</template>

<script>
import Main from "@/components/Main";
import { mapState } from "vuex";

export default {
  name: "TestPage",
  components: {
    Main,
  },
  data() {
    return {
      nodes: [],
      links: [],
      startTime: new Date(),
    };
  },
  mounted() {
    // this.$store.dispatch("test/fetchRoute", { x: 1 });
    // this.$store.dispatch("test/fetchAll");
    // this.$store.dispatch("test/fetchAllData");
  },
  computed: {
    // ...mapState("test", {
    //   route: (state) => state.route,
    //   station: (state) => state.station,
    //   alldata: (state) => state.alldata,
    //   selectedRoute: (state) => state.selectedRoute,
    //   contourList: (state) => state.contourList,
    //   currentTime: (state) => state.currentTime,
    //   dataConfig: (state) => state.dataConfig,
    // }),
    // initSign() {
    //   return this.route && this.station && this.alldata;
    // },
    // loadingText() {
    //   return "Loading";
    //   // return "Loading:    " + 'Route: \n' +
    //   //     !!this.route + '   Station: \n'+ !!this.station + '   Alldata: \n'+ !!this.alldata
    // },
  },
};
</script>

<style >
.boundary {
  /*border-style: dashed;*/
  border-style: solid;
  border-color: #d3dce6;
  border-width: 0.5px;
  border-radius: 3px;
}
</style>
