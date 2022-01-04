<template>
  <div class="password mb-16">
    <v-card elevation="0">
      <v-card-title class="text-h5 font-weight-bold text-uppercase d-flex justify-center">Change Password</v-card-title>
      <v-divider></v-divider>
      <v-form id="password-change" @submit.prevent="save">
        <v-row justify="center" align="center">
          <v-col cols="12">
            <span v-if="errorMsg" class="error--text">{{errorMsg}}</span>
            <!-- <v-card-text v-if="isDefaultPassword" class="error--text text-center">
              Note**:Please change the default password first or else you will be unable to take any actions in this account.
            </v-card-text> -->
            <v-card-text v-if="updateFailed" class="error--text">
              Wrong password.
            </v-card-text>
          </v-col>
          <v-col cols="2">
            <span>Password *</span>
          </v-col>
          <v-col cols="4">
            <v-text-field 
              dense
              autofocus
              :value="$v.changePassword.password.$model" 
              @input="updateChangePasswordProperty('password', $event)"
              :type="showPassword ? 'text': 'password'"
              :append-icon="showPassword ? 'mdi-eye' : 'mdi-eye-off'"
              @click:append="showPassword = !showPassword"></v-text-field>
            <span v-if="!$v.changePassword.password.required && $v.changePassword.password.$dirty" class="red--text text-body-2">Password required.</span>
            <span v-if="!$v.changePassword.password.minLength" class="red--text text-body-2">Password should be greater than {{$v.changePassword.password.$params.minLength.min}} characters.</span>
          </v-col>
        </v-row>
        <v-row justify="center" align="center">
          <v-col cols="2">
            <span>New Password *</span>
          </v-col>
          <v-col cols="4">
            <v-text-field 
              dense 
              :value="$v.changePassword.new_password.$model" 
              @input="updateChangePasswordProperty('new_password', $event)"
              :type="showNewPassword ? 'text': 'password'"
              :append-icon="showNewPassword ? 'mdi-eye' : 'mdi-eye-off'"
              @click:append="showNewPassword = !showNewPassword"></v-text-field>
            <span v-if="!$v.changePassword.new_password.required && $v.changePassword.new_password.$dirty" class="red--text text-body-2">New password required.</span>
            <span v-if="!$v.changePassword.new_password.minLength" class="red--text text-body-2">New password should be greater than {{$v.changePassword.new_password.$params.minLength.min}} characters.</span>
          </v-col>
        </v-row>
        <v-row justify="center" align="center">
          <v-col cols="2">
            <span>Confirm Password *</span>
          </v-col>
          <v-col cols="4">
            <v-text-field 
              dense 
              :value="$v.changePassword.confirm_password.$model" 
              @input="updateChangePasswordProperty('confirm_password', $event)"
              :type="showConfirmPassword ? 'text': 'password'"
              :append-icon="showConfirmPassword ? 'mdi-eye' : 'mdi-eye-off'"
              @click:append="showConfirmPassword = !showConfirmPassword"></v-text-field>
            <span v-if="!$v.changePassword.confirm_password.required && $v.changePassword.confirm_password.$dirty" class="red--text text-body-2">Confirm password required.</span>
            <span v-if="!$v.changePassword.confirm_password.sameAsNewPassword" class="red--text text-body-2">Confirm password must be as new password.</span>
          </v-col>
        </v-row>
        <v-row justify="center" align="center">
          <v-col cols="4" class="d-flex justify-space-between">  
            <v-btn type="submit" for="password-change" color="project_primary" class="text-uppercase white--text rounded" width="30%">Save</v-btn>
            <v-btn @click="resetChangePassword" color="grey" class="text-uppercase white--text rounded" width="30%">Cancel</v-btn>
          </v-col>
        </v-row>
      </v-form>
    </v-card>
    <v-dialog v-model="sendOtp" persistent width="500">
      <SendOtp
        title="Verify OTP"
        :data="changePassword"
        otp_type="password"
        @cancel-otp="sendOtp=false"
        @verify-success="save"
        @verify-failed="sendOtp=false,errorMsg='OTP is not matched.'"
        @invalid-request="sendOtp=false,errorMsg='Somthing went wrong.'"
      ></SendOtp>
    </v-dialog>
  </div>
</template>
<script>
import { mapGetters, mapMutations, mapActions } from 'vuex'
import { required, sameAs, minLength } from 'vuelidate/lib/validators'
import SendOtp from '@/components/SendOtp'
export default {
  title: () => ('Change Password'),
  metaInfo: {
    title: 'Change Password for Kamakhya Nagar Development Committee Account'
  },
  components: {
    SendOtp
  },
  data: () => ({
    showPassword: false,
    showNewPassword: false,
    showConfirmPassword: false,
    updateFailed: false,
    sendOtp: false,
    errorMsg: ''
  }),
  computed: {
    ...mapGetters('user', {
      changePassword: 'getChangePassword'
    }),
    ...mapGetters('JWT', {
      isDefaultPassword: 'isDefaultPassword'
    }),
  },
  validations() {
    let data = {
      changePassword: {
        password: {
          required,
          minLength: minLength(8)
        },
        new_password: {
          required,
          minLength: minLength(8)
        },
        confirm_password: {
          required,
          sameAsNewPassword: sameAs('new_password')
        }
      }
    }
    return data
  },
  methods: {
    ...mapActions('user', [
      'updatePassword',
      'SendOTPUser'
    ]),
    ...mapActions('JWT', [
      'logout'
    ]),
    ...mapMutations('user', [
      'setChangePasswordProperty',
      'resetChangePassword'
    ]),
    updateChangePasswordProperty(property, value) {
      this.setChangePasswordProperty({
        property,
        value
      })
      this.$v.changePassword[property].$touch()
    },
    save() {
      this.$v.$touch()

      if (!this.$v.$invalid) {
        this.updatePassword().then((response) => {
          if(response.data.otp || response.data.matched_failed) {
            this.sendOtp = true
          } else {
            this.logout().then(() => {
              location.reload()
            })
          }
        }).catch(() => {
          this.updateFailed = true
        })
      }
    },
    updateData() {
      this.updatePassword().then(() => {
        this.logout().then(() => {
          location.reload()
        })
      })
    }
  }
}
</script>
<style scoped>

</style>
