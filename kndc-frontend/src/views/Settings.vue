<template>
  <div class="contact-setting">
    <v-card elevation="0">
      <v-container>
        <v-row justify="center" class="d-flex justify-start">
          <v-col cols="12" sm="4">
            <v-checkbox
              v-model="enableEvents"
              label="Enable Events"
              color="project_primary"
            ></v-checkbox>
          </v-col>
          <v-col cols="12" sm="5" class="d-flex justify-end">
            <v-checkbox
              v-model="enableNews"
              label="Enable News"
              color="project_primary"
            ></v-checkbox>
          </v-col>
          <v-col cols="12" sm="5" >
            <v-checkbox
              v-model="showComplaints"
              label="Make Complaints & Grievances visible to Public"
              color="project_primary"
            ></v-checkbox>
          </v-col>
          <v-col cols="12" sm="4" class="d-flex justify-end">
            <v-checkbox
              v-model="enablePosts"
              label="Enable Posts"
              color="project_primary"
            ></v-checkbox>
          </v-col> 
        </v-row>
      </v-container>
      <v-divider></v-divider>
      <v-container>
        <FeesSettings :fees="fees" :feesId="feesId"></FeesSettings>
      </v-container>
      <v-divider></v-divider>
      <v-card-title class="text-h5 font-weight-bold text-uppercase d-flex justify-center">Contacts Setting</v-card-title>
      <v-container>
        <v-row justify="center" class="d-flex justify-start">
          <v-col cols="12" sm="3">
            <v-checkbox
              v-model="showAddress"
              label="Show Address"
              color="project_primary"
            ></v-checkbox>
          </v-col>
          <v-col cols="12" sm="3" class="d-flex justify-center">
            <v-checkbox
              v-model="showNumber"
              label="Show Contact Number"
              color="project_primary"
            ></v-checkbox>
          </v-col>
          <v-col cols="12" sm="3" class="d-flex justify-end">
            <v-checkbox
              v-model="showEmail"
              label="Show Email-id"
              color="project_primary"
            ></v-checkbox>
          </v-col>
          <v-col cols="9" class="py-0 my-0">
            <v-text-field
              label="Community Name"
              :value="settings.community_name"
              outlined
              dense
              @input="updateContactsProperty('community_name', $event)"
            ></v-text-field>
          </v-col>
          <v-col cols="9" class="py-0 my-0">
            <v-text-field
              label="Appartment Name"
              :value="settings.appartment_name"
              outlined
              dense
              @input="updateContactsProperty('appartment_name', $event)"
            ></v-text-field>
          </v-col>
          <v-col cols="9" class="py-0 my-0">
            <v-text-field
              label="Address Line 1"
              :value="settings.address_one"
              outlined
              dense
              @input="updateContactsProperty('address_one', $event)"
            ></v-text-field>
          </v-col>
          <v-col cols="9" class="py-0 my-0">
            <v-text-field
              label="Address Line 2"
              :value="settings.address_two"
              outlined
              dense
              @input="updateContactsProperty('address_two', $event)"
            ></v-text-field>
          </v-col>
          <v-col cols="5" class="py-0 my-0">
            <v-text-field
              label="City"
              :value="settings.city"
              outlined
              dense
              @input="updateContactsProperty('city', $event)"
            ></v-text-field>
          </v-col>
          <v-col cols="4" class="py-0 my-0">
            <v-text-field
              label="Pincode"
              :value="$v.settings.pincode.$model"
              outlined
              dense
              @input="updateContactsProperty('pincode', $event)"
            ></v-text-field>
            <span v-if="!$v.settings.pincode.numeric" class="validation-text red--text text-caption">This field should be a valid pincode.</span>
          </v-col>
          <v-col cols="9" class="py-0 my-0">
            <v-text-field
              label="Contact Number*"
              :value="$v.settings.contact_number.$model"
              outlined
              dense
              @input="updateContactsProperty('contact_number', $event)"
            ></v-text-field>
            <span v-if="!$v.settings.contact_number.required && $v.settings.contact_number.$dirty" class="validation-text red--text text-caption">This field should not be empty.</span>
            <span v-if="!$v.settings.contact_number.phoneNumber" class="validation-text red--text text-caption">Phone Number Must be valid.</span>
          </v-col>
          <v-col cols="9" class="py-0 my-0">
            <v-text-field
              label="Email-id*"
              :value="$v.settings.email.$model"
              outlined
              dense
              @input="updateContactsProperty('email', $event)"
            ></v-text-field>
            <span v-if="!$v.settings.email.required && $v.settings.email.$dirty" class="validation-text red--text text-caption">This field should not be empty.</span>
            <span v-if="!$v.settings.email.email" class="validation-text red--text text-caption">Email-id Must be valid.</span>
          </v-col>
        </v-row>
        <v-card-actions class="d-flex justify-center">
          <v-btn width="30%" class="white--text rounded" color="project_primary" @click="saveContacts">Save</v-btn>
        </v-card-actions>
      </v-container>
    </v-card>
    <v-dialog v-model="showDialog" persistent width="500">
      <v-card>
        <v-card-title class="headline green lighten-2">
          Contacts saved successfully
        </v-card-title>

        <v-divider></v-divider>

        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn
            color="primary"
            text
            @click="showDialog=false"
          >
            Ok
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>
<script>
import { required, numeric, email } from 'vuelidate/lib/validators'
import { mapGetters, mapMutations, mapActions } from 'vuex'
import FeesSettings from '@/components/FeesSettings.vue'
export default {
  title: 'Contact Settings',
  metaInfo: {
    title: 'Contact Settings for Kamakhya Nagar Development Committee'
  },
  components: {
    FeesSettings
  },
  data: () => ({
    showDialog: false,
    overlay: false
  }),
  validations() {
    const phoneNumber =  val => (/^\+?([0-9]{2})\)?[-. ]?([0-9]{4})[-. ]?([0-9]{3})[-. ]?([0-9]{3})$/.test(val) || /^\(?([0-9]{4})\)?[-. ]?([0-9]{3})[-. ]?([0-9]{3})$/.test(val))
    let data = {
      settings: {
        email: {
          required,
          email
        },
        contact_number: {
          required,
          phoneNumber
        },
        pincode: {
          numeric
        }
      }
    }
    return data
  },
  computed: {
    ...mapGetters('settings', {
      settings: 'getSettings'
    }),
    ...mapGetters('fees', {
      fees: 'getFees',
      feesId: 'getFeesId'
    }),
    showAddress: {
      get() {
        return this.settings.show_address
      },
      set(value) {
        this.setSettingsProperty({
          property:'show_address',
          value
        })
      }
    },
    showNumber: {
      get() {
        return this.settings.show_number
      },
      set(value) {
        this.setSettingsProperty({
          property:'show_number',
          value
        })
      }
    },
    showEmail: {
      get() {
        return this.settings.show_email
      },
      set(value) {
        this.setSettingsProperty({
          property:'show_email',
          value
        })
      }
    },
    enableEvents: {
      get() {
        return this.settings.enable_events
      },
      set(value) {
        this.setSettingsProperty({
          property:'enable_events',
          value
        })
      }
    },
    enableNews: {
      get() {
        return this.settings.enable_news
      },
      set(value) {
        this.setSettingsProperty({
          property:'enable_news',
          value
        })
      }
    },
    enablePosts: {
      get() {
        return this.settings.enable_posts
      },
      set(value) {
        this.setSettingsProperty({
          property:'enable_posts',
          value
        })
      }
    },
    showComplaints: {
      get() {
        return this.settings.show_complaints
      },
      set(value) {
        this.setSettingsProperty({
          property:'show_complaints',
          value
        })
      }
    },
  },
  methods: {
    ...mapActions('settings', [
      'fetchSettings',
      'createSettings',
      'updateSettings'
    ]),
    ...mapActions('fees', [
      'fetchFees',
      'createFees',
      'updateFees'
    ]),
    ...mapMutations('settings', [
      'setSettingsProperty'
    ]),
    updateContactsProperty(property, value) {
      this.setSettingsProperty({
        property,
        value
      })
      // this.$v.changePassword[property].$touch()
    },
    saveContacts() {
      this.$v.$touch()
      if(!this.$v.$invalid) {
        if(!this.settings.id) {
          this.createSettings().then(() => {
            this.showDialog = true
          })
        } else {
          this.updateSettings().then(() => {
            this.showDialog = true
          })
        }
        this.saveFeesItems()
      }
    },
    saveFeesItems() {
      this.overlays = true
      if(this.feesId) {
        this.updateFees().then(()=> {
          this.fetchFeeData()
          this.updatedFees = true
          this.statusPopup = true
        })
      } else {
        this.createFees().then(()=> {
          this.fetchFeeData()
          this.createdFees = true
          this.statusPopup = true
        })
      }
    },
    fetchFeeData() {
      this.overlay = true
      this.fetchFees().then(()=>{
        this.overlays = false
      })
    }
  },
  mounted() {
    this.overlay = true
    this.fetchSettings().then(() => {
      this.overlay = false
    })
    this.fetchFeeData()
  }
}
</script>
<style scoped>
.validation-text {
  position: relative;
  bottom: 20px;
}
</style>
