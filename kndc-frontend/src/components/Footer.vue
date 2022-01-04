<template>
  <v-footer color="#423D3D" padless>
    <v-card dark flat tile color="transparent" width="100%">
      <v-row align="start" justify="space-around" class="ma-0 upper-section">
        <v-col cols="2" class="d-grid justify-center">
          <v-row align="center" justify="center" class="pa-7">
            <router-link to="/" exact>
                <v-img class="logo-img" color="white" :src="logo" height="46" width="164" max-width="220"></v-img>
            </router-link>
            <v-col cols="12"></v-col>
            <v-col cols="12"></v-col>
            <v-col cols="10">
              <v-row justify="space-around">
                <v-btn icon color="white">
                  <v-icon>mdi-facebook</v-icon>
                </v-btn>
                <v-btn icon color="white">
                  <v-icon>mdi-instagram</v-icon>
                </v-btn>
                <v-btn icon color="white">
                  <v-icon>mdi-youtube</v-icon>
                </v-btn>
                <v-btn icon color="white">
                  <v-icon>mdi-whatsapp</v-icon>
                </v-btn>
              </v-row>
            </v-col>
          </v-row>
        </v-col>
        <v-col cols="3" class="d-grid justify-center">
          <v-card-title class="header-title pl-7">About</v-card-title>
          <v-list class="ma-0 pa-0" flat nav dense color="transparent">
            <v-list-item active-class="btn--active" exact-path class="ma-0 pa-0" v-for="(item, index) in listItems" :key="index" :href="`/${item.route}`">
              <v-list-item-icon class="px-0 mr-1 d-flex justify-end">
                <v-icon size="16">mdi-greater-than</v-icon>
              </v-list-item-icon>
              <v-list-item-title class="item-text">{{item.text}}</v-list-item-title>
            </v-list-item>
          </v-list>
        </v-col>
        <v-col cols="3" class="d-grid justify-center">
          <v-card-title class="header-title fit-content pl-7">Contact Info</v-card-title>
          <v-list class="ma-0 pa-0" nav dense color="transparent">
            <v-list-item class="ma-0 pa-0">
              <v-list-item-icon class="pr-0 mr-1 d-flex justify-end">
                <v-icon size="16">mdi-greater-than</v-icon>
              </v-list-item-icon>
              <v-list-item-icon class="inner-icon">
                <v-icon size="16">mdi-phone-outline</v-icon>
              </v-list-item-icon>
              <v-list-item-title class="item-text">
                <span>{{contacts.contact_number}}</span>
              </v-list-item-title>
            </v-list-item>
            <v-list-item class="ma-0 pa-0">
              <v-list-item-icon class="pr-0 mr-1 d-flex justify-end">
                <v-icon size="16">mdi-greater-than</v-icon>
              </v-list-item-icon>
              <v-list-item-icon class="inner-icon">
                <v-icon size="16">mdi-email-outline</v-icon>
              </v-list-item-icon>
              <v-list-item-title class="item-text">
                <span>{{contacts.email}}</span>
              </v-list-item-title>
            </v-list-item>
            <v-list-item three-line class="contact-address ma-0 pa-0">
              <v-list-item-icon class="pr-0 mr-1 d-flex justify-end">
                <v-icon size="16">mdi-greater-than</v-icon>
              </v-list-item-icon>
              <v-list-item-icon class="inner-icon">
                <v-icon size="16">mdi-home-outline</v-icon>
              </v-list-item-icon>
              <v-list-item-title class="item-text text-truncate">
                <span>{{contacts.appartment_name}}, {{contacts.address_one}}, {{contacts.address_two}}, {{contacts.city}}-{{(contacts.pincode).substr(4,2)}}</span>
              </v-list-item-title>
            </v-list-item>
          </v-list>
        </v-col>
      </v-row>
      <v-divider></v-divider>
      <v-row align="center" no-gutters>
        <v-card dark flat tile width="100%" color="rgba(183, 158, 138, 0.26)">
          <v-row align="center" justify="end" no-gutters>
            <v-col cols="3">
                <v-card-text class="copy-right">
                  <v-icon size="18" class="copy-right-icon">mdi-copyright</v-icon>
                  <span>2021 KNDC, All Right Reserved</span>
                </v-card-text>
            </v-col>
          </v-row>
        </v-card>
      </v-row>
    </v-card>
  </v-footer>  
</template>

<script>
import logo from '@/assets/KNDC.png'
import { mapActions, mapGetters } from 'vuex'
export default {
  data: () => ({
    logo,
    listItems: [
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
  }),
  computed: {
    ...mapGetters('settings', {
      contacts: 'getSettings'
    })
  },
  methods: {
    ...mapActions('settings', [
      'fetchSettings'
    ])
  },
  mounted() {
    this.fetchSettings()
  }
}
</script>

<style scoped>
.logo-img {
    cursor: pointer;
    filter: brightness(0) invert(1);
}

.upper-section {
  height: 80%;
}

.header-title {
  font-size: 24px !important;
}
.inner-icon {
  border-radius: 50% !important;
  background-color: #615651 !important;
  margin-right: 8px !important;
  display: flex;
  justify-content: center;
}
.item-text {
  font-size: 16px !important;
  color: #A5B2B8 !important;
}
.item-text:hover, .btn--active .item-text {
  color: #FFFFFF !important;
}
.contact-address {
  min-height: 50px !important;
  align-items: flex-start !important;
}
.copy-right {
  font-size: 18px !important;
}

.copy-right-icon {
  padding-bottom: 2px !important;
  margin-right: 2px !important;
}
</style>
