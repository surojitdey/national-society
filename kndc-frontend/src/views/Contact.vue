<template>
  <div class="contact">
    <v-row align="center" justify="center" class="mt-4">
      <v-card width="78%" elevation="0">
        <v-card-title class="text-h4 grey--text text--darken-1">Contact Us</v-card-title>
        <v-row justify="center">
          <v-col cols="12" class="subtitle">
            <v-card-subtitle class="text-h4 grey--text text--darken-1 font-weight-bold">Contact</v-card-subtitle>
          </v-col>
          <v-col cols="12" class="mt-0 pt-0"> 
            <v-divider></v-divider>
          </v-col>
          <v-col cols="12" class="subtitle pa-0 ma-0">
            <span class="text-h5 grey--text text--darken-3">{{contacts.community_name}}</span>
          </v-col>
          <div v-if="contacts.show_address">
            <v-col cols="12" class="subtitle pa-0 ma-0">
              <span class="text-h5 grey--text text--darken-3">{{contacts.appartment_name}}</span>
            </v-col>
            <v-col cols="12" class="subtitle pa-0 ma-0">
              <span class="text-h5 grey--text text--darken-3">{{contacts.address_one}}</span>
            </v-col>
            <v-col cols="12" class="subtitle pa-0 ma-0">
              <span class="text-h5 grey--text text--darken-3">{{contacts.address_two}}, {{contacts.city}}-{{(contacts.pincode).substr(4,2)}}</span>
            </v-col>
          </div>
          <v-col cols="12" class="subtitle pa-0 ma-0">
            <span class="text-h5 grey--text text--darken-3" v-if="contacts.show_number">Contact: {{contacts.contact_number}}</span>
          </v-col>
          <v-col cols="12" class="subtitle pa-0 ma-0">
            <span class="text-h5 grey--text text--darken-3" v-if="contacts.show_email">Email: {{contacts.email}}</span>
          </v-col>
        </v-row>
        <v-row justify="center" align="center" class="my-5">
          <v-btn color="black" outlined @click="showDialog=true">Write to Us</v-btn>
        </v-row>
      </v-card>
    </v-row>
    <v-dialog v-model="showDialog" persistent transition="dialog-bottom-transition" width="650">
      <v-card>
        <v-container>
          <v-row justify="start" class="ma-0 pa-0">
            <v-col cols="12">
              <v-card-title>Write to Us</v-card-title>
              <v-card-subtitle>All Fields mark with * are compulsory</v-card-subtitle>
            </v-col>
            <v-col cols="12" class="px-7 py-0 ma-0">
              <v-text-field
                label="Full Name*"
                outlined
                dense
                height="8"
              ></v-text-field>
            </v-col>
            <v-col cols="12" class="px-7 py-0 ma-0">
              <v-text-field
                label="Contact No*"
                outlined
                dense
                height="8"
              ></v-text-field>
            </v-col>
            <v-col cols="12" class="px-7 py-0 ma-0">
              <v-text-field
                label="Email*"
                outlined
                dense
                height="8"
              ></v-text-field>
            </v-col>
            <v-col cols="9" class="px-7 py-0 ma-0">
              <v-textarea
                label="Message*"
                outlined
                auto-grow
              ></v-textarea>
            </v-col>
            <v-card-actions class="px-7 pb-8 ma-0">
              <v-btn outlined color="primary">Send</v-btn>
              <v-btn outlined @click="showDialog=false">Cancel</v-btn>
            </v-card-actions>
          </v-row>
        </v-container>
      </v-card>
    </v-dialog>
    <v-overlay :value="overlay">
      <v-progress-circular indeterminate color="white" width="5"></v-progress-circular>
    </v-overlay>
  </div>
</template>
<script>
import { mapActions, mapGetters } from 'vuex'
export default {
  title: 'Contact Informations for Kamakhya Nagar Society',
  metaInfo: {
    title: 'Contact Informations for Kamakhya Nagar Society'
  },
  data: () => ({
    showDialog: false,
    overlay: false
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
    this.overlay = true
    this.fetchSettings().then(() => {
      this.overlay = false
    })
  }
}
</script>
<style scoped>
.contact {
  padding-top: 64px !important;
}

.subtitle {
  display: flex !important;
  justify-content: center !important;
}
</style>
