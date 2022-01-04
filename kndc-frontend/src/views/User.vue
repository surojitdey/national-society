<template>
  <div class="user mt-2">
    <v-row justify="center">
      <v-card color="white" class="my-5" elevation="1" width="58%">
        <v-card-title>{{user.full_name}}</v-card-title>
        <v-col class="ml-1" cols="6">
          <span>Mobile Number: {{user.mobile_number}}</span>
        </v-col>
        <v-col class="ml-1" cols="6">
          <span>Address: {{user.address}}</span>
        </v-col>
        <v-col class="ml-1" cols="6">
          <span>Email: {{user.email}}</span>
        </v-col>
        <v-col class="ml-1" cols="6">
          <span>Company: {{user.company}}</span>
        </v-col>
        <v-col class="ml-1" cols="6">
          <span>Designation: {{user.designation}}</span>
        </v-col>
        <v-col class="ml-1" cols="6">
          <span>Number of family members: {{user.family_members}}</span>
        </v-col>
        <v-col class="ml-1" cols="6">
          <span>Active status: {{user.is_active}}</span>
        </v-col>
        <v-card-actions>
          <v-btn color="" class="mx-2 my-3 red--text" v-if="user.is_active" @click="updateUserStatusProperty('deactive', user.id)">Deactivate</v-btn>
          <v-btn color="" class="mx-2 my-3 green--text" v-else @click="updateUserStatusProperty('active', user.id)">Activate</v-btn>
        </v-card-actions>
      </v-card>
    </v-row>
    <v-overlay :value="overlay">
      <v-progress-circular indeterminate color="white" width="5"></v-progress-circular>
    </v-overlay>
  </div>
</template>
<script>
import { mapActions, mapMutations } from 'vuex'
export default {
  title() {
    return `Resident Details for Kamakhya Nagar Development Committee`
  },
  metaInfo: {
    title: 'Resident Details for Kamakhya Nagar Development Committee'
  },
  data: () => ({
    user: {
      mobile_number: '',
      full_name: '',
      email: '',
      address: '',
      company: '',
      designation: ''
    },
    overlay: false
  }),
  computed: {
    id() {
      return this.$route.params.id
    }
  },
  methods: {
    ...mapActions('user', [
      'fetchUserById',
      'updateStatus'
    ]),
    ...mapMutations('user', [
      'setUserStatusProperty'
    ]),
    updateUserStatusProperty(status, user_id) {
      this.setUserStatusProperty({
        status,
        user_id
      })
      this.updateStatus().then(() => {
        location.reload()
      })
    },
  },
  created() {
    this.overlay = true
    if(!this.id) {
      throw 'An id is required'
    }
    this.fetchUserById(this.id).then(data => this.user = data)
    .then(() => {
      this.overlay = false
    })
  }
}
</script>
<style scoped>
.user {
  padding-top: 64px !important;
}
</style>
