<template>
  <div class="residents-page mt-2">
    <v-row justify="end">
      <v-col cols="4" class="d-flex justify-end">
        <v-text-field v-model="searchQuery" rounded dense color="#FFA500" label="Search" outlined append-icon="mdi-magnify" single-line hide-details></v-text-field>
      </v-col>
    </v-row>
    <v-card elevation="1">
      <v-row justify="center">
        <v-col cols="3" class="d-flex justify-center">
          <span class="header-text font-weight-bold text-capitalize">full name</span>
        </v-col>
        <v-col cols="3" class="d-flex justify-center">
          <span class="header-text font-weight-bold text-capitalize">address</span>
        </v-col>
        <v-col cols="3" class="d-flex justify-center">
          <span class="header-text font-weight-bold text-capitalize">contact</span>
        </v-col>
        <v-col cols="3" class="d-flex justify-center">
          <span class="header-text font-weight-bold text-capitalize">email</span>
        </v-col>
      </v-row>
    </v-card>
    <v-card color="#F5F5F5" elevation="1" class="my-6" v-for="(user, index) in currentPageResidents" :key="index">
      <v-row justify="center">
        <v-col cols="3" class="d-flex justify-center">
          <span class="header-text text-capitalize">{{user.full_name}}</span>
        </v-col>
        <v-col cols="3" class="d-flex justify-center">
          <span class="header-text text-capitalize">{{user.address}}</span>
        </v-col>
        <v-col cols="3" class="d-flex justify-center">
          <span class="header-text text-capitalize">{{user.mobile_number}}</span>
        </v-col>
        <v-col cols="3" class="d-flex justify-center">
          <span class="header-text">{{user.email}}</span>
        </v-col>
      </v-row>
    </v-card>
    <v-pagination
      v-model="page"
      :length="Math.ceil(filteredResidents.length/residentPerPage)"
      :total-visible="7"
      color="project_primary"
    ></v-pagination>
    <v-overlay :value="overlay">
      <v-progress-circular indeterminate color="white" width="5"></v-progress-circular>
    </v-overlay>
  </div>
</template>
<script>
import { mapActions, mapGetters } from 'vuex'
export default {
  title: 'Residents of Kamakhya Nagar Development Committee',
  metaInfo: {
    title: 'Residents of Kamakhya Nagar Development Committee'
  },
  data: () => ({
    searchQuery: '',
    headers: [
      {
        text: 'Name',
        align: 'center',
        sortable: true,
        value: 'full_name'
      },
      {
        text: 'Address',
        align: 'center',
        sortable: true,
        value: 'address'
      },
      {
        text: 'Contact Number',
        align: 'center',
        value: 'mobile_number'
      }
    ],
    overlay: false,
    page: 1,
    residentPerPage: 5
  }),
  computed: {
    ...mapGetters('user',{
      residents: 'getResidents'
    }),
    filteredResidents() {
      if(this.searchQuery) {
        return this.residents.filter((user) => {
          return user.full_name.toLowerCase().startsWith(this.searchQuery.toLowerCase())
        })
      } else {
        return this.residents
      }
    },
    currentPageResidents() {
      return this.filteredResidents.slice((this.page-1)*this.residentPerPage,(this.page-1)*this.residentPerPage+this.residentPerPage)
    }
  },
  methods: {
    ...mapActions('user', [
      'fetchResidents'
    ])
  },
  mounted() {
    this.overlay = true
    this.fetchResidents().then(() => {
      this.overlay = false
    })
  }
}
</script>
<style scoped>
.residents-page {
  padding: 64px;
  min-height: 51vh;
}
</style>
