<template>
  <v-card max-hight="152" max-width="965" class="mx-auto">
    <v-card-title class="text-h2 text-uppercase">Welcome to kndc</v-card-title>
  </v-card>
</template>

<script>
import { mapGetters } from 'vuex'
export default {
  data: () => ({
    listItems: [
      {
        text: 'BECOME A MEMBER',
        route: 'signup'
      },
      {
        text: 'ABOUT',
        route: 'about'
      },
      {
        text: 'RESIDENTS',
        route: 'residents'
      },
      {
        text: 'COMPLAINTS & GRIEVANCES',
        route: 'complaints'
      },
      {
        text: 'EVENTS',
        route: 'events'
      },
      {
        text: 'CONTACT US',
        route: 'contacts'
      },
    ],
    selectedItem: null
  }),
  computed: {
    ...mapGetters('JWT',[
      'loggedIn'
    ])
  },
  mounted() {
    if(this.loggedIn) {
      this.listItems.reverse().pop()
      this.listItems.reverse()
    }
  }
}
</script>

<style scoped>
.v-card {
  position: absolute;
  /* top: 200px !important;
  left: 70px !important; */
}
</style>
