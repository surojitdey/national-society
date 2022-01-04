<template>
  <div class="send-otp">
    <v-card class="rounded-lg">
      <v-form id="verify-otp" @submit.prevent="verifyOtp">
        <v-row justify="center" no-gutters>
          <v-col cols="11" class="px-6">
            <v-card-title class="text-uppercase">{{title}}</v-card-title>
          </v-col>
          <v-col cols="11" class="px-10">
            <v-text-field v-model="$v.otp.$model" class="rounded" outlined label="Enter OTP"></v-text-field>
            <span v-if="!$v.otp.required" class="red--text text-body-2">OTP required.</span>
            <span v-if="!$v.otp.minLength" class="red--text text-body-2">OTP should be {{$v.otp.$params.minLength.min}} characters.</span>
            <span v-if="!$v.otp.maxLength" class="red--text text-body-2">OTP should be {{$v.otp.$params.maxLength.max}} characters.</span>
          </v-col>
          <v-col cols="11" class="px-8">
            <v-card-actions class="py-0">
              <v-btn plain color="#003366" width="30%" @click="resendOtp" class="text-uppercase d-flex justify-start px-0 rounded">Resend</v-btn>
            </v-card-actions>
          </v-col>
          <v-col cols="11" class="px-8">
            <v-card-actions>
              <v-btn class="text-uppercase white--text rounded" color="#434D3D" width="30%" type="submit" for="verify-otp">Verify</v-btn>
              <v-btn class="text-uppercase white--text rounded" color="grey" width="30%" @click="$emit('cancel-otp')">Cancel</v-btn>
            </v-card-actions>
          </v-col>
        </v-row>
      </v-form>
    </v-card>
  </div>  
</template>
<script>
import { mapActions } from 'vuex'
import { required, minLength, maxLength } from 'vuelidate/lib/validators'
export default {
  props: [
    'mobile_number',
    'data',
    'title',
    'otp_type'
  ],
  data: () => ({
    otp: ''
  }),
  validations() {
    if(this.otp !=='') {
      return {
        otp: {
          required,
          minLength: minLength(4),
          maxLength: maxLength(4)
        }
      }
    } else {
      return {
        otp: {
          minLength: minLength(4),
          maxLength: maxLength(4)
        }
      }
    }
  },
  methods: {
    ...mapActions('user', [
      'verifyOTPUser',
      'SendOTPUser'
    ]),
    verifyOtp() {
      this.verifyOTPUser({mobile_number: this.mobile_number, otp: this.otp, otp_type: this.otp_type}).then((response) => {
        if(response.data.status) {
          this.$emit('verify-success')
        } else {
          this.$emit('verify-failed')
        }
      }).catch(() => {
        this.$emit('invaild-request')
      })
    },
    resendOtp() {
      this.data.otp_type = this.otp_type
      this.SendOTPUser(this.data)
    }
  },
  mounted() {

  }
}
</script>
<style scoped>

</style>
