<template> 
  <v-container fluid class="signin">
    <v-card color="grey lighten-2" class="py-16 my-16" width="60%">
      <v-card-text v-if="showError" class="red--text d-flex justify-center">Wrong credentials.</v-card-text>
      <v-form v-model="formValid" id="signin-form" @submit.prevent="signinFunction">
        <v-row justify="center" align="center">
          <v-col cols="3" class="px-10">
            <span class="text-h5 d-flex justify-center font-weight-bold text-uppercase">Sign In</span>
          </v-col>
          <v-col cols="12">
            <v-divider></v-divider>
          </v-col>
          <v-col cols="7" class="px-10">
            <v-text-field
              autofocus
              outlined
              class="rounded"
              v-model.trim="$v.signinData.mobile_number.$model"
              label="Mobile Number"
            ></v-text-field>
            <span v-if="!$v.signinData.mobile_number.required && $v.signinData.mobile_number.$dirty" class="validation-text red--text text-body-2">Mobile number required.</span>
            <span v-if="!$v.signinData.mobile_number.phoneNumber" class="validation-text red--text text-body-2">Mobile Number Must be valid.</span>
          </v-col>
          <v-col cols="7" class="px-10">
            <v-text-field 
              v-model="$v.signinData.password.$model"
              label="Password"
              outlined
              class="rounded"
              :type="showPassword ? 'text': 'password'"
              :append-icon="showPassword ? 'mdi-eye' : 'mdi-eye-off'"
              @click:append="showPassword = !showPassword"
            ></v-text-field>
            <span v-if="!$v.signinData.password.required && $v.signinData.password.$dirty" class="validation-text red--text text-body-2">Password required.</span>
            <span v-if="!$v.signinData.password.minLength" class="validation-text red--text text-body-2">Password must be atleast 8 charecter long.</span>
          </v-col>
          <v-col cols="7" class="py-0">
            <v-card-actions class="px-7 my-0 py-0">
              <v-checkbox v-model="rememberMe" label="Remember me"></v-checkbox>
            </v-card-actions>
          </v-col>
          <v-col cols="7" class="py-0">
            <v-card-actions class="px-7 py-0">
              <v-btn plain color="#003366" class="ma-0 pa-0" elevation="0" to="forgot-password" :ripple="false">Forgot password?</v-btn>
            </v-card-actions>
          </v-col>
          <v-col cols="7" class="py-0">
            <v-card-actions class="px-7">
              <v-btn width="30%" class="text-uppercase white--text rounded" color="#434D3D" type="submit" for="signin-form">Sign In</v-btn>
              <v-btn width="30%" class="text-uppercase white--text rounded" color="grey" @click="reset">Cancel</v-btn>
            </v-card-actions>
          </v-col>
        </v-row>
      </v-form>
    </v-card>
  </v-container>
</template>

<script>
import { required, minLength } from 'vuelidate/lib/validators'
import { helpers } from 'vuelidate/lib/validators'
import { mapActions, mapGetters, mapMutations } from 'vuex'
const phoneNumber = helpers.regex('phoneNumber', (/^\s*(?:\+?(\d{1,3}))?[-. (]*(\d{3})[-. )]*(\d{3})[-. ]*(\d{4})(?: *x(\d+))?\s*$/))

export default {
  title: 'Signin for Kamakhya Nagar Development Committee',
  metaInfo: {
    title: 'Signin for Kamakhya Nagar Development Committee'
  },
  data: () => ({
    signinData: {
      mobile_number: '' || localStorage.getItem('mobile_number'),
      password: '' || localStorage.getItem('password')
    },
    formValid: false,
    showError: false,
    rules: {
      phoneNumber: val => (/^\+?([0-9]{2})\)?[-. ]?([0-9]{4})[-. ]?([0-9]{3})[-. ]?([0-9]{3})$/.test(val) || /^\(?([0-9]{4})\)?[-. ]?([0-9]{3})[-. ]?([0-9]{3})$/.test(val)) || 'Phone Number Must be valid',
    },
    showPassword: false,
    isAdminSignin: false,
    rememberMe: false
  }),
  validations() {
    return {
      signinData: {
        mobile_number: {
          required,
          phoneNumber
        },
        password: {
          required,
          minLength: minLength(8)
        }
      }
    }
  },
  watch: {
    rememberMe() {
      if(this.rememberMe) {
        localStorage.setItem('mobile_number', this.signinData.mobile_number)
        localStorage.setItem('password', this.signinData.password)
      } else {
        localStorage.removeItem('mobile_number')
        localStorage.removeItem('password')
      }
    }
  },
  computed: {
    ...mapGetters([]),
    mobileNumberError() {
      return this.$v.signinData.mobile_number.required
    }
  },
  methods: {
    ...mapMutations([]),
    ...mapActions('JWT', [
      'fetchJWT'
    ]),
    signinFunction() {
      this.$v.$touch()
      if(!this.$v.$invalid) {
        this.fetchJWT({formData: this.signinData})
        .then(() => {
          this.formValid = true
          this.showError = false
          this.$router.push('/')
        })
        .catch(() => {
          this.formValid = false
          this.showError = true
        })
      }
    },
    reset() {
      this.signinData.mobile_number = ''
      this.signinData.password = ''
      this.$v.$reset()
    },
    forgotPassword() {
      console.log('clicked')
    }
  },
  mounted() {
    if(localStorage.getItem('mobile_number') && localStorage.getItem('password')) {
      this.rememberMe = true
    } else {
      this.rememberMe = false
    }
  }
}
</script>

<style scoped>
.signin {
  display: flex;
  position: relative;
  align-items: center;
  justify-content: center;
  margin: auto;
}

.admin-signin-btn {
  float: right;
}
.validation-text {
  position: relative;
  bottom: 20px;
}
</style>
