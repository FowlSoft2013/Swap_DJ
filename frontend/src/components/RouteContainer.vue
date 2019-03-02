<template>
    <div class="main-container">
      <div class="app-container">
        <router-view></router-view>
      </div>

      <Footer></Footer>
    </div>
</template>

<script>
import Footer from './Footer.vue'

export default {
    name: "RouteContainer",
    components: { Footer }
}
</script>

<style>
html, body {
  height:100%;
  width:100%;
  display: flex;
  flex-direction: column;
}
.main-container {
  height: 100%;
  width: 100%;
  overflow: auto;
  background-color: #8EC5FC;
  background: linear-gradient(rgba(139,198,236, .9),rgba(149,153,226, .9)), url('../assets/dj1.jpg');
  background-size: 100%;
  background-repeat: no-repeat;
  -webkit-background-size: 100%; 
  -moz-background-size: 100%; 
  -o-background-size: 100%; 
  background-size: 100%; 
  -webkit-background-size: cover; 
  -moz-background-size: cover; 
  -o-background-size: cover; 
  overflow-y: scroll; /* has to be scroll, not auto */
  -webkit-overflow-scrolling: touch;
}

.app-container {
  height: auto;
  min-height: 90%;
  width:100%;
  opacity: .95;
} 
label {
  color: white;
}
</style>
