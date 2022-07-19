<template>
  <div class="about">
    <Map></Map>
  </div>
</template>

<script>
import Map from "@/components/Map.vue";
import { mapState } from "vuex";

export default {
  name: "AboutView",

  components: {
    Map,
  },
  data() {
    return {};
  },
  mounted() {},
  computed: {},
};
</script>

<style scoped>
.about {
  width: 100%;
  height: 100%;
}

#map {
  width: 50%;
  height: 100%;
}

#myMap {
  width: 100%;
  height: 100%;
}
</style>
