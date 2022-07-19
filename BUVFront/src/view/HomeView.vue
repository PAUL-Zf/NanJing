<template>
  <div class="home">
    <!-- <img alt="Vue logo" src="../assets/logo.png"> -->
    <!-- <HelloWorld msg="Welcome to Your Vue.js App"/> -->
    <Selection></Selection>
  </div>
</template>

<script>
// @ is an alias to /src
// import HelloWorld from '@/components/HelloWorld.vue'
import Selection from "@/components/Selection.vue";
import { mapState } from "vuex";

export default {
  name: "HomeView",
  // props: ["allData"],
  components: {
    // HelloWorld,
    Selection,
  },
  data() {
    return {
      isSucceed: true,
    };
  },
  mounted() {
    // this.$store.dispatch("test/fetchAllData");
  },
  computed: {
    // ...mapState("test", {
    //     allData: (state) => state.allData // ***
    // })
  },
};
</script>
