<template>
  <v-container fluid class="add-security mt-16 d-flex justify-center">
    <v-card class="my-16 pb-4 rounded-lg" width="78%">
      <v-card-title class="justify-center">Add Security</v-card-title>
      <v-row justify="space-between" class="px-16 mx-md-16">
        <v-col cols="12" sm="4">
          <v-text-field class="rounded" label="Full Name*" autofocus v-model="$v.security.full_name.$model" outlined dense></v-text-field>
          <span v-if="!$v.security.full_name.required && $v.security.full_name.$dirty" class="validation-text red--text text-body-2">Full Name required.</span>
        </v-col>
        <v-col cols="12" sm="4">
          <v-text-field class="rounded" label="Father Name*" v-model="$v.security.father_name.$model" outlined dense></v-text-field>
          <span v-if="!$v.security.father_name.required && $v.security.father_name.$dirty" class="validation-text red--text text-body-2">Father Name required.</span>
        </v-col>
        <v-col cols="12" sm="4">
          <v-text-field class="rounded" label="Mobile Number*" v-model="$v.security.mobile_number.$model" outlined dense></v-text-field>
          <span v-if="!$v.security.mobile_number.required && $v.security.mobile_number.$dirty" class="validation-text red--text text-body-2">Mobile Number required.</span>
          <span v-if="!$v.security.mobile_number.phoneNumber && $v.security.mobile_number.$dirty" class="validation-text red--text text-body-2">Mobile Number Must be valid.</span>
        </v-col>
        <v-col cols="12" sm="4">
          <v-select v-model.trim="$v.security.gender.$model" class="rounded" label="Gender*" :items="genderArray" item-text="text" item-value="value" outlined dense></v-select>
          <span v-if="!$v.security.gender.required && $v.security.gender.$dirty" class="validation-text red--text text-body-2">Gender required.</span>
        </v-col>
        <v-col cols="12" sm="4">
          <DatePicker :rounded="'rounded'" :label="'Date of joining*'" @get-date="security.date_of_joining=$event"></DatePicker>
          <span v-if="!$v.dateOfJoining.required && $v.dateOfJoining.$dirty" class="validation-text red--text text-body-2">This field is required.</span>
        </v-col>
        <v-col cols="12" sm="4">
          <DatePicker :rounded="'rounded'" :label="'Date of birth*'" @get-date="security.date_of_birth=$event"></DatePicker>
          <span v-if="!$v.dateOfBirth.required && $v.dateOfBirth.$dirty" class="validation-text red--text text-body-2">This field is required.</span>
          <span v-if="!$v.dateOfBirth.maxValue" class="validation-text red--text text-body-2">This field must be a past date.</span>
        </v-col>
        <v-col cols="12" sm="4">
          <v-text-field v-model="$v.security.reference.$model" class="rounded" label="Reference" placeholder="Optional" outlined dense></v-text-field>
        </v-col>
        <v-col cols="12" sm="8">
          <v-textarea v-model="$v.security.permanent_address.$model" class="rounded" label="Permanent Address*" auto-grow outlined dense></v-textarea>
          <span v-if="!$v.security.permanent_address.required && $v.security.permanent_address.$dirty" class="validation-text red--text text-body-2">Permanent address is required.</span>
        </v-col>
        <v-col cols="6">
          <v-file-input
            id="select-photo"
            accept="image/*"
            label="Images"
            v-model="$v.security.photo.$model"
            v-show="false"
            @change="onAddPhoto"
          ></v-file-input>
          <v-img height="199.43" v-if="security.photo" width="inherit" :src="photoUrl" @click="selectImage('select-photo')"></v-img>
          <v-card class="select-image-card" elevation="0" v-else width="inherit" height="199.43">
            <v-row class="select-image" align="center" dense no-gutters>
              <v-col cols="12" class="d-flex flex-column justify-center">
                <v-btn class="fit-content ma-auto" text large @click="selectImage('select-photo')">
                  <v-icon color="#D4C6BA" size="60">mdi-cloud-upload</v-icon>
                </v-btn>
                <v-card-text class="pa-0 text-center">Upload photo here</v-card-text>
              </v-col>
            </v-row>
          </v-card>
          <span v-if="!$v.security.photo.required && $v.security.photo.$dirty" class="red--text text-body-2">Photo is required.</span>
        </v-col>
        <v-col cols="6">
          <v-file-input
            id="select-adhar"
            accept="image/*"
            label="Images"
            v-model="$v.security.adhar_card.$model"
            v-show="false"
            @change="onAddAdhar"
          ></v-file-input>
          <v-img height="200" v-if="security.adhar_card" width="inherit" :src="adharUrl" @click="selectImage('select-adhar')"></v-img>
          <v-card class="select-image-card" elevation="0" v-else width="inherit" height="200">
            <v-row class="select-image" align="center" no-gutters dense>
              <v-col cols="12" class="d-flex flex-column justify-center">
                <v-btn text large class="fit-content ma-auto" @click="selectImage('select-adhar')">
                  <v-icon color="#D4C6BA" size="60">mdi-cloud-upload</v-icon>
                </v-btn>
                <v-card-text class="pa-0 text-center">Upload adhar card here</v-card-text>
              </v-col>
            </v-row>
          </v-card>
          <span v-if="!$v.security.adhar_card.required && $v.security.adhar_card.$dirty" class="red--text text-body-2">Adhar card is required.</span>
        </v-col>
        <v-col cols="12">
          <v-card-actions class="d-flex justify-center">
            <v-btn class="white--text text-uppercase" width="30%" color="#423D3D" @click="addSecurity" :disabled="loading">Add Security</v-btn>
          </v-card-actions>
        </v-col>
      </v-row>
    </v-card>
    <v-dialog v-model="addStatus" width="50%" persistent>
      <v-card>
        <v-card-title v-if="addSuccess" class="green--text">Security details added successfully.</v-card-title>
        <v-card-title v-if="addError" class="error--text">Security details addition unsuccessful.</v-card-title>
        <v-card-actions class="d-flex justify-end">
          <v-btn
            class="white--text text-uppercase"
            width="30%"
            color="#423D3D"
            @click="cancelStatus"
          >Cancel</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>  
</template>
<script>
import { required, maxValue } from 'vuelidate/lib/validators'
import { helpers } from 'vuelidate/lib/validators'
import DatePicker from '@/components/DatePicker.vue'
import { mapActions } from 'vuex'
const phoneNumber = helpers.regex('phoneNumber', (/^\s*(?:\+?(\d{1,3}))?[-. (]*(\d{3})[-. )]*(\d{3})[-. ]*(\d{4})(?: *x(\d+))?\s*$/))
export default {
  components: {
    DatePicker
  },
  data: () => ({
    security: {
      full_name: '',
      father_name: '',
      gender: '',
      date_of_joining: '',
      permanent_address: '',
      date_of_birth: '',
      mobile_number: '',
      reference: '',
      photo: undefined,
      adhar_card: undefined,
    },
    genderArray: [
      {
        text: 'Male',
        value: 'male'
      },
      {
        text: 'Female',
        value: 'female'
      }
    ],
    photoUrl: '',
    adharUrl: '',
    errorPhoto: '',
    loading: false,
    addStatus: false,
    addSuccess: false,
    addError: false
  }),
  validations() {
    let currentDate = new Date()
    return {
      security: {
        full_name: {
          required
        },
        father_name: {
          required
        },
        gender: {
          required
        },
        date_of_joining: {
          required
        },
        date_of_birth: {
          required
        },
        permanent_address: {
          required
        },
        mobile_number: {
          required,
          phoneNumber
        },
        reference: {

        },
        photo: {
          required
        },
        adhar_card: {
          required
        }
      },
      dateOfJoining: {
        required,
        // minValue: minValue(currentDate.setDate(currentDate.getDate() - 1))
      },
      dateOfBirth: {
        required,
        maxValue: maxValue(currentDate.setDate(currentDate.getDate()))
      },
    }
  },
  computed: {
    dateOfJoining() {
      return this.security.date_of_joining ? new Date(this.security.date_of_joining) : null
    },
    dateOfBirth() {
      return this.security.date_of_birth ? new Date(this.security.date_of_birth) : null
    },
  },
  methods: {
    ...mapActions('security', [
      'postSecurityData'
    ]),
    onAddPhoto(file) {
      const reader = new FileReader()
      reader.addEventListener('load', e => this.photoUrl = e.target.result)
      reader.addEventListener('error', () => this.photoUrl = this.errorPhoto)
      reader.readAsDataURL(file)
    },
    onAddAdhar(file) {
      const reader = new FileReader()
      reader.addEventListener('load', e => this.adharUrl = e.target.result)
      reader.addEventListener('error', () => this.adharUrl = this.errorPhoto)
      reader.readAsDataURL(file)
    },
    selectImage(elementId) {
      document.getElementById(elementId).click()
    },
    cancelStatus() {
      this.security = {
        full_name: '',
        father_name: '',
        gender: '',
        date_of_joining: '',
        permanent_address: '',
        date_of_birth: '',
        mobile_number: '',
        reference: '',
        photo: undefined,
        adhar_card: undefined,
      }
      this.$v.$reset()
      this.addStatus = false
    },
    addSecurity() {
      this.loading = true
      this.$v.$touch()
      if(!this.$v.$invalid) {
        let formData = new FormData()
        for(let key in this.security) {
          formData.append(key, this.security[key])
        }
        this.postSecurityData(formData).then(() => {
          this.loading = false
          this.addSuccess = true
          this.addError = false
          this.addStatus = true
        }).catch(() => {
          this.loading = false
          this.addSuccess = false
          this.addError = true
          this.addStatus = true
        })
      } else {
        this.loading = false
      }
    }
  }
}
</script>
<style scoped>
.validation-text {
  position: relative;
  bottom: 15px;
}
.select-image-card {
  background: #F7F7F7;
  border: 1px dashed #423D3D;
}
.select-image {
  height: inherit;
}
</style>