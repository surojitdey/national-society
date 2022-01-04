<template>
  <v-container fluid class="forgot-password">
    <!-- <v-stepper v-model="step">
      <v-stepper-header>
        <v-stepper-step
          :complete="step>1"
          step="1"
        >
        </v-stepper-step>
      </v-stepper-header>
    </v-stepper> -->
    <v-card color="grey lighten-2 rounded-lg" class="py-16 my-16">
      <v-card-text v-if="showError" class="red--text px-7">{{errorMsg}}</v-card-text>
      <v-form v-model="formValid" id="forgot-password-form" @submit.prevent="checkUser">
        <v-row justify="center" align="center">
          <v-col cols="7" class="px-10">
            <span class="text-h5 font-weight-bold">Forgot Password</span>
          </v-col>
          <v-col cols="12">
            <v-divider></v-divider>
          </v-col>
          <v-col cols="7" class="px-10">
            <v-text-field 
              v-model.trim="$v.userData.mobile_number.$model"
              class="rounded"
              outlined
              label="Mobile Number"
              :rules="[$v.userData.mobile_number.required, rules.phoneNumber]"
            ></v-text-field>
            <span v-if="!$v.userData.mobile_number.required" class="red--text text-body-2">Mobile number required.</span>
          </v-col>
          <v-col cols="7">
            <v-card-actions class="px-7">
              <v-btn class="text-uppercase white--text rounded" color="#434D3D" width="30%" type="submit" for="forgot-password-form">Submit</v-btn>
              <v-btn class="text-uppercase white--text rounded" color="grey" width="30%" @click="reset">Cancel</v-btn>
            </v-card-actions>
          </v-col>
        </v-row>
      </v-form>
    </v-card>

    <v-dialog v-model="passwordDialog" width="700" persistent>
      <v-card class="rounded-lg">
        <v-row justify="center" no-gutters>
          <v-col cols="7" class="px-7">
            <v-card-title class="text-uppercase">Change Password</v-card-title>
          </v-col>
          <v-col cols="7" class="px-10">
            <v-text-field 
              v-model="$v.userData.password.$model"
              class="rounded"
              outlined
              label="Password *"
              :type="showPassword ? 'text': 'password'"
              :append-icon="showPassword ? 'mdi-eye' : 'mdi-eye-off'"
              @click:append="showPassword = !showPassword"
            >
            </v-text-field>
            <span v-if="!$v.userData.password.required" class="red--text text-body-2">Password required.</span>
            <span v-if="!$v.userData.password.minLength" class="red--text text-body-2">Password must be atleast 8 charecter long.</span>
          </v-col>
          <v-col cols="7" class="px-10">
            <v-text-field 
              v-model="$v.userData.confirm_password.$model"
              class="rounded"
              outlined
              label="Confirm Password *"
              :type="showConfirmPassword ? 'text': 'password'"
              :append-icon="showConfirmPassword ? 'mdi-eye' : 'mdi-eye-off'"
              @click:append="showConfirmPassword = !showConfirmPassword"
            ></v-text-field>
            <span v-if="!$v.userData.confirm_password.required" class="red--text text-body-2">Confirm Password required.</span>
            <span v-if="!$v.userData.confirm_password.sameAsPassword" class="red--text text-body-2">Confirm Password must be as Password.</span>
          </v-col>
          <v-col cols="7" class="px-7">
            <v-card-actions>
              <v-btn
                color="#434D3D"
                class="white--text text-uppercase rounded"
                width="30%"
                @click="forgotUserPassword"
              >
                Continue
              </v-btn>
              <v-btn
                color="grey"
                class="white--text text-uppercase rounded"
                width="30%"
                @click="reset"
              >
                Cancel
              </v-btn>
            </v-card-actions>
          </v-col>
        </v-row>
      </v-card>
    </v-dialog>
    <v-dialog v-model="sendOtp" persistent width="500">
      <SendOtp
        title="Verify OTP"
        :data="userData"
        otp_type="forgot_password"
        :mobile_number="userData.mobile_number"
        @cancel-otp="sendOtp=false"
        @verify-success="forgotUserPassword"
        @verify-failed="sendOtp=false,errorMsg='OTP is not matched.'"
        @invalid-request="sendOtp=false,errorMsg='Somthing went wrong.'"
      ></SendOtp>
    </v-dialog>
  </v-container>
</template>
<script>
import { required, minLength, sameAs } from 'vuelidate/lib/validators'
import { mapActions } from 'vuex'
import SendOtp from '@/components/SendOtp'
export default {
  title: 'Forgot Password',
  metaInfo: {
    title: 'Forgot Password for Kamakhya Nagar Development Committee'
  },
  components: {
    SendOtp
  },
  data: () => ({
    userData: {
      mobile_number: '',
      password: '',
      confirm_password: ''
    },
    formValid: false,
    showError: false,
    rules: {
      phoneNumber: val => (/^\+?([0-9]{2})\)?[-. ]?([0-9]{4})[-. ]?([0-9]{3})[-. ]?([0-9]{3})$/.test(val) || /^\(?([0-9]{4})\)?[-. ]?([0-9]{3})[-. ]?([0-9]{3})$/.test(val)) || 'Phone Number Must be valid',
    },
    showPassword: false,
    showConfirmPassword: false,
    passwordDialog: false,
    errorMsg: '',
    sendOtp: false,
    step: 1
  }),
  validations() {
    if(this.passwordDialog) {
      return {
        userData: {
          mobile_number: {
            required
          },
          password: {
            required,
            minLength: minLength(8)
          },
          confirm_password: {
            required,
            sameAsPassword: sameAs('password')
          }
        }
      }
    } else {
      return {
        userData: {
          mobile_number: {
            required
          },
          password: {
            minLength: minLength(8)
          },
          confirm_password: {
            sameAsPassword: sameAs('password')
          }
        }
      }
    }
  },
  methods: {
    ...mapActions('user', [
      'checkUserExist',
      'forgotPassword'
    ]),
    checkUser() {
      this.checkUserExist({userData: this.userData}).then((response) => {
        if(response.data.isUser) {
          this.passwordDialog = true
          this.showError = false
        } else {
          this.showError = true
          this.reset()
          this.errorMsg = 'User not exist.'
        }
      })
    },
    reset() {
      this.userData.mobile_number = ''
      this.userData.password = ''
      this.userData.confirm_password = ''
      this.passwordDialog = false
      this.sendOtp = false
    },
    forgotUserPassword() {
      this.forgotPassword({userData: this.userData}).then((response) => {
        if(response.data.otp || response.data.matched_failed) {
          this.sendOtp = true
        } else {
          this.reset()
        }
      }).catch(() => {
        this.reset()
      })
    }
  }
}
</script>
<style scoped>
.forgot-password {
  display: flex;
  position: relative;
  align-items: center;
  justify-content: center;
  margin: auto;
}
</style>
