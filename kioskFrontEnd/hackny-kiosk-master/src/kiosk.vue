<template>
    <div>
        <h1 >Skin Kiosk</h1>
        <p v-if="state.number == 1">Press # to take a photo of your rash</p>
        <p v-else-if="state.number == 2">Based on preliminary analysis, you may have a real disorder.
            If you would like to have a professional review your rash, please press #.
        </p>
        <p v-else-if="state.number == 3">It appears that your rash is not a serious concern. Thanks for visiting! </p>
        <p v-else-if="state.number == 4">In order to cover costs of having dermatologists ready 24/7, 
            please pay a fee of 25 dollars using card or apple pay.</p>
        <p v-else-if="state.number == 5">Please enter your phone number followed by #.</p>
        <p v-else-if="state.number == 6">Dr. Doe will contact you shortly. Thank you for your patience. Please press any key to end.</p>
    </div>
</template>

<script lang='ts'>
import Vue from "vue";
import axios from "axios";
const state = {
  value: null,
  number: 1
};
function getNewData() {
  axios
    .get("http://localhost:3001/data")
    .then(function(response) {
      state.value = response.data.data;

      if (response.data.new) {
        switch (state.number) {
          case 1:
            if (state.value == "#") {
              state.number = 2;
            }
            break;
          case 2:
            if (state.value == "#") {
              state.number = 4;
            }
            break;
          case 3:
            state.number = 1;
            break;
          case 4:
            if (state.value == "Peter") {
              state.number = 5;
            }
            break;
          case 5:
            if (state.value.length == 10) {
              state.number = 6;
            }
            break;
          case 6:
            state.number = 1;
            break;
          default:
            break;
        }
        console.log(state.number);
      }
      console.log(response.data);
    })
    .catch(function(error) {
      console.log(error);
    });
}

setInterval(getNewData, 250);

export default Vue.extend({
  methods: { getNewData: getNewData },
  data: function() {
    return {
      state: state
    };
  }
});
</script>

<style lang='scss' scoped>
h1 {
  font-size: 3em;
  color: white;
  font-family: "Space Mono", monospace;
  @import url("https://fonts.googleapis.com/css?family=Space+Mono");
  text-align: center;
  margin: 0.5em;
  text-shadow: 3px 2px black;
}
p {
  font-family: "Space Mono", monospace;
  @import url("https://fonts.googleapis.com/css?family=Space+Mono");
  text-align: center;
  margin: 0.5em;
}
html {
  background-image: linear-gradient(red, yellow);
}
</style>