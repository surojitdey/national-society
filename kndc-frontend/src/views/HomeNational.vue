<template>
  <div class="national-society-home">
    <h1 class="text-uppercase text-center">National Society</h1>
    <v-form v-model="formValid" id="society-registration" class="d-flex justify-center ma-5" @submit.prevent="save">
      <v-row justify="center" class="registration-form-content">
        <v-col cols="10">
          <v-text-field 
            placeholder="Mobile Number"
            persistent-placeholder
            outlined dense
            v-model="registration.mobile_number"
          ></v-text-field>
          <v-text-field 
            placeholder="Society Name"
            persistent-placeholder
            outlined dense
            v-model="registration.society_name"
          ></v-text-field>
          <v-text-field 
            placeholder="Email"
            persistent-placeholder
            outlined dense
            v-model="registration.email"
          ></v-text-field>
          <v-textarea 
            placeholder="Address"
            persistent-placeholder
            outlined
            dense
            auto-grow
            v-model="registration.address"
          ></v-textarea>
          <v-row justify="space-between">
            <v-col cols="4">
              <v-text-field 
                placeholder="City"
                persistent-placeholder
                outlined dense
                v-model="registration.city"
              ></v-text-field>
            </v-col>
            <v-col cols="4">
              <v-text-field 
                placeholder="Country"
                persistent-placeholder
                outlined dense
                v-model="registration.country"
              ></v-text-field>
            </v-col>
            <v-col cols="4">
              <v-text-field 
                placeholder="Pincode"
                persistent-placeholder
                outlined dense
                v-model="registration.pincode"
              ></v-text-field>
            </v-col>
          </v-row>
        </v-col>
        <v-col cols="10" class="d-flex justify-center">
          <v-btn for="society-registration" color="project_primary" class="white--text" type="submit">Submit</v-btn>
        </v-col>
      </v-row>
    </v-form>
  </div>
</template>
<script>
import { mapActions } from 'vuex'
export default {
  data: () => ({
    formValid: false,
    registration: {
      mobile_number: '',
      society_name: '',
      address: '',
      city: '',
      pincode: '',
      country: '',
      email: ''
    }
  }),
  methods: {
    ...mapActions('society',[
      'createSociety'
    ]),
    save() {
      this.createSociety(this.registration)
    }
  }
}
</script>
<style scoped>
.national-society-home {
  margin-top: 70px;
}
.registration-form-content {
  max-width: 50%;
}
</style>
