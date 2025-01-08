<template>
  <div>
    <button type="button" class="btn btn-primary">{{ msg }}</button>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "SharkComponent",
  data() {
    return {
      msg: "",
    };
  },
  methods: {
    getResponse() {
      const path = "http://127.0.0.1:5000/shark";
      axios
        .get(path)
        .then((response) => {
          console.log(response.data);
          this.msg = response.data;
        })
        .catch((error) => {
          console.log(error);
        });
    },
  },
  created() {
    this.getResponse();
  },
};
</script>
