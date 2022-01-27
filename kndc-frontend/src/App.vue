<template>
  <v-app>
    <v-main class="wraper-class">
      <Navbar></Navbar>
      <router-view class="content-class"></router-view>
      <Footer></Footer>
    </v-main>
  </v-app>
</template>

<script>
import Navbar from './components/Navbar';
import Footer from './components/Footer';

export default {
  title: 'Kamakhya Nagar Society',
  name: 'App',
  metaInfo: {
    // if no subcomponents specify a metaInfo.title, this title will be used
    title: 'Kamakhya Nagar Society'
  },
  components: {
    Navbar,
    Footer
  },

  data: () => ({
    //
  }),
  computed: {
    
  }
};
</script>

<style scoped>
.wraper-class {
  padding: 0 !important;
  margin: 0 !important;
}
.content-class {
  overflow: hidden;
  min-height: 70vh !important;
}
</style>


