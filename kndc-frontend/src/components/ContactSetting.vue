<template>
  <div class="contact-setting">
    <v-card elevation="0">
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
              :value="contacts.community_name"
              outlined
              dense
              @input="updateContactsProperty('community_name', $event)"
            ></v-text-field>
          </v-col>
          <v-col cols="9" class="py-0 my-0">
            <v-text-field
              label="Appartment Name"
              :value="contacts.appartment_name"
              outlined
              dense
              @input="updateContactsProperty('appartment_name', $event)"
            ></v-text-field>
          </v-col>
          <v-col cols="9" class="py-0 my-0">
            <v-text-field
              label="Address Line 1"
              :value="contacts.address_one"
              outlined
              dense
              @input="updateContactsProperty('address_one', $event)"
            ></v-text-field>
          </v-col>
          <v-col cols="9" class="py-0 my-0">
            <v-text-field
              label="Address Line 2"
              :value="contacts.address_two"
              outlined
              dense
              @input="updateContactsProperty('address_two', $event)"
            ></v-text-field>
          </v-col>
          <v-col cols="5" class="py-0 my-0">
            <v-text-field
              label="City"
              :value="contacts.city"
              outlined
              dense
              @input="updateContactsProperty('city', $event)"
            ></v-text-field>
          </v-col>
          <v-col cols="4" class="py-0 my-0">
            <v-text-field
              label="Pincode"
              :value="$v.contacts.pincode.$model"
              outlined
              dense
              @input="updateContactsProperty('pincode', $event)"
            ></v-text-field>
            <span v-if="!$v.contacts.pincode.numeric" class="validation-text red--text text-caption">This field should be a valid pincode.</span>
          </v-col>
          <v-col cols="9" class="py-0 my-0">
            <v-text-field
              label="Contact Number*"
              :value="$v.contacts.contact_number.$model"
              outlined
              dense
              @input="updateContactsProperty('contact_number', $event)"
            ></v-text-field>
            <span v-if="!$v.contacts.contact_number.required && $v.contacts.contact_number.$dirty" class="validation-text red--text text-caption">This field should not be empty.</span>
            <span v-if="!$v.contacts.contact_number.phoneNumber" class="validation-text red--text text-caption">Phone Number Must be valid.</span>
          </v-col>
          <v-col cols="9" class="py-0 my-0">
            <v-text-field
              label="Email-id*"
              :value="$v.contacts.email.$model"
              outlined
              dense
              @input="updateContactsProperty('email', $event)"
            ></v-text-field>
            <span v-if="!$v.contacts.email.required && $v.contacts.email.$dirty" class="validation-text red--text text-caption">This field should not be empty.</span>
            <span v-if="!$v.contacts.email.email" class="validation-text red--text text-caption">Email-id Must be valid.</span>
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
export default {
  title: 'Contact Settings',
  metaInfo: {
    title: 'Contact Settings for Kamakhya Nagar Development Committee'
  },
  data: () => ({
    showDialog: false,
    overlay: false
  }),
  validations() {
    const phoneNumber =  val => (/^\+?([0-9]{2})\)?[-. ]?([0-9]{4})[-. ]?([0-9]{3})[-. ]?([0-9]{3})$/.test(val) || /^\(?([0-9]{4})\)?[-. ]?([0-9]{3})[-. ]?([0-9]{3})$/.test(val))
    let data = {
      contacts: {
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
    ...mapGetters('user', {
      contacts: 'getContacts'
    }),
    showAddress: {
      get() {
        return this.contacts.show_address
      },
      set(value) {
        this.setContactsProperty({
          property:'show_address',
          value
        })
      }
    },
    showNumber: {
      get() {
        return this.contacts.show_number
      },
      set(value) {
        this.setContactsProperty({
          property:'show_number',
          value
        })
      }
    },
    showEmail: {
      get() {
        return this.contacts.show_email
      },
      set(value) {
        this.setContactsProperty({
          property:'show_email',
          value
        })
      }
    },
  },
  methods: {
    ...mapActions('user', [
      'fetchContacts',
      'createContacts',
      'updateContacts'
    ]),
    ...mapMutations('user', [
      'setContactsProperty'
    ]),
    updateContactsProperty(property, value) {
      this.setContactsProperty({
        property,
        value
      })
      // this.$v.changePassword[property].$touch()
    },
    saveContacts() {
      this.$v.$touch()
      if(!this.$v.$invalid) {
        if(!this.contacts.id) {
          this.createContacts().then(() => {
            this.showDialog = true
          })
        } else {
          this.updateContacts().then(() => {
            this.showDialog = true
          })
        }
      }
    }
  },
  mounted() {
    this.overlay = true
    this.fetchContacts().then(() => {
      this.overlay = false
    })
  }
}
</script>
<style scoped>
.validation-text {
  position: relative;
  bottom: 20px;
}
</style>
