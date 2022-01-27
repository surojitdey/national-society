<template> 
  <v-container fluid class="signup">
    <v-card color="grey lighten-2" class="py-16 my-16" width="60%">
      <v-form v-model="formValid" id="signup-form" @submit.prevent="signup">
        <v-row justify="center" no-gutters>
          <v-col cols="7" class="px-10 pb-0">
            <span class="text-h5 font-weight-bold text-uppercase justify-center">Registration Details</span>
          </v-col>
          <v-col cols="7" class="px-10 pt-0">
            <span class="text-body-2">All fields marked with * are mandatory</span>
          </v-col>
          <v-col cols="12" class="py-4">
            <v-divider></v-divider>
          </v-col>
          <v-col cols="7" class="px-10">
            <v-text-field
              autofocus
              outlined
              dense
              class="rounded"
              v-model.trim="$v.primaryData.society_registration_number.$model"
              label="Society Registration Id *"
              :success="$v.primaryData.society_registration_number.isValidRegistration && $v.primaryData.society_registration_number.required"
            ></v-text-field>
            <span v-if="!$v.primaryData.society_registration_number.required && $v.primaryData.society_registration_number.$dirty" class="validation-text red--text text-body-2">Registration Id will be required.</span>
            <!-- <span v-if="!$v.primaryData.mobile_number.phoneNumber" class="validation-text red--text text-body-2">Mobile Number Must be valid.</span> -->
            <span v-if="!$v.primaryData.society_registration_number.isValidRegistration" class="validation-text red--text text-body-2">Please enter a valid registration id.</span>
          </v-col>
          <v-col cols="7" class="px-10">
            <v-text-field
              outlined
              dense
              class="rounded"
              v-model.trim="$v.primaryData.mobile_number.$model"
              label="Mobile Number *"
              :success="$v.primaryData.mobile_number.isNumberExist && $v.primaryData.mobile_number.required && $v.primaryData.mobile_number.phoneNumber"
            ></v-text-field>
            <span v-if="!$v.primaryData.mobile_number.required && $v.primaryData.mobile_number.$dirty" class="validation-text red--text text-body-2">Mobile number required.</span>
            <span v-if="!$v.primaryData.mobile_number.phoneNumber" class="validation-text red--text text-body-2">Mobile Number Must be valid.</span>
            <span v-if="!$v.primaryData.mobile_number.isNumberExist" class="validation-text red--text text-body-2">Mobile Number already exist.</span>
          </v-col>
          <v-col cols="7" class="px-10">
            <v-text-field 
              v-model="$v.primaryData.password.$model"
              label="Password *"
              outlined
              dense
              class="rounded"
              :type="showPassword ? 'text': 'password'"
              :append-icon="showPassword ? 'mdi-eye' : 'mdi-eye-off'"
              @click:append="showPassword = !showPassword"
            ></v-text-field>
            <span v-if="!$v.primaryData.password.required && $v.primaryData.password.$dirty" class="validation-text red--text text-body-2">Password required.</span>
            <span v-if="!$v.primaryData.password.minLength" class="validation-text red--text text-body-2">Password must be atleast 8 charecter long.</span>
          </v-col>
          <v-col cols="7" class="px-10">
            <v-text-field 
              v-model="$v.primaryData.confirmPassword.$model"
              label="Confirm Password *"
              outlined
              dense
              class="rounded"
              :type="showConfirmPassword ? 'text': 'password'"
              :append-icon="showConfirmPassword ? 'mdi-eye' : 'mdi-eye-off'"
              @click:append="showConfirmPassword = !showConfirmPassword"
            ></v-text-field>
            <span v-if="!$v.primaryData.confirmPassword.required && $v.primaryData.confirmPassword.$dirty" class="validation-text red--text text-body-2">Confirm Password required.</span>
            <span v-if="!$v.primaryData.confirmPassword.sameAsPassword && $v.primaryData.confirmPassword.$dirty" class="validation-text red--text text-body-2">Confirm Password must be as Password.</span>
          </v-col>
          <v-col cols="7" class="px-10 pb-0">
            <span class="text-h5 font-weight-bold text-uppercase">Profile</span>
          </v-col>
          <v-col cols="7" class="px-10 pt-0">
            <span class="text-body-2">All fields marked with * are mandatory</span>
          </v-col>
          <v-col cols="12" class="py-4">
            <v-divider></v-divider>
          </v-col>
          <v-col cols="7" class="px-10">
            <v-text-field 
              v-model="$v.primaryData.full_name.$model"
              label="Full Name *"
              outlined
              dense
              class="rounded"
            ></v-text-field>
            <span v-if="!$v.primaryData.full_name.required && $v.primaryData.full_name.$dirty" class="validation-text red--text text-body-2">Full Name required.</span>
          </v-col>
          <v-col cols="7" class="px-10">
            <v-text-field 
              v-model="$v.primaryData.address.$model"
              label="Address *"
              outlined
              dense
              class="rounded"
            ></v-text-field>
            <span v-if="!$v.primaryData.address.required && $v.primaryData.address.$dirty" class="validation-text red--text text-body-2">Address required.</span>
          </v-col>
          <v-col cols="7" class="px-10">
            <v-text-field 
              v-model="$v.primaryData.email.$model"
              label="Email"
              outlined
              dense
              class="rounded"
            ></v-text-field>
            <span v-if="!$v.primaryData.email.email && $v.primaryData.email.$dirty" class="validation-text red--text text-caption">Email-id Must be valid.</span>
          </v-col>
          <v-col cols="7" class="px-10">
            <v-text-field 
              v-model="$v.primaryData.company.$model"
              label="Company"
              outlined
              dense
              class="rounded"
            ></v-text-field>
          </v-col>
          <v-col cols="7" class="px-10">
            <v-text-field 
              v-model="$v.primaryData.designation.$model"
              label="Designation"
              outlined
              dense
              class="rounded"
            ></v-text-field>
          </v-col>
          <v-col cols="7" class="px-10">
            <v-text-field 
              v-model="primaryData.family_members"
              outlined
              dense
              class="rounded"
            >
              <template v-slot:label>
                <span>Number of Family Members <strong>excluding yourself</strong></span>
              </template>
            </v-text-field>
            <span v-if="!$v.primaryData.family_members.numeric" class="validation-text red--text text-body-2">This Field should be numeric.</span>
            <span v-if="!$v.primaryData.family_members.maxValue" class="validation-text red--text text-body-2">Should not be grater than 10.</span>
          </v-col>
          <v-col cols="7" class="px-10" v-for="(v, index) in $v.familyData.$each.$iter" :key="index">
            <v-select
              v-model.trim="v.relation.$model"
              label="Relation"
              outlined
              dense
              class="rounded"
              :items="relationItems"
              item-text="name"
              item-value="value"
            ></v-select>
            <span v-if="!v.relation.required && v.relation.$dirty" class="validation-text red--text text-body-2">Relation required.</span>
            <v-text-field 
              v-model.trim="v.member_name.$model"
              outlined
              dense
              class="rounded"
              label="Member Name"
            ></v-text-field>
            <span v-if="!v.member_name.required && v.member_name.$dirty" class="validation-text red--text text-body-2">Family member name required.</span>
          </v-col>
          <v-col cols="7">
            <v-card-actions class="px-7">
              <v-btn type="submit" for="signup-form" class="text-uppercase white--text rounded" color="#434D3D">Sign Up</v-btn>
              <v-btn @click="reset" class="text-uppercase white--text rounded" color="grey">Cancel</v-btn>
            </v-card-actions>
          </v-col>
        </v-row>
      </v-form>
    </v-card>
    <v-dialog v-model="sendOtp" persistent width="300">
      <SendOtp
        title="Verify OTP"
        :data="primaryData"
        otp_type="signup"
        :mobile_number="primaryData.mobile_number"
        @cancel-otp="sendOtp=false"
        @verify-success="signup"
        @verify-failed="sendOtp=false,errorMsg='Invalid OTP.'"
        @invalid-request="sendOtp=false,errorMsg='Somthing went wrong.'"
      ></SendOtp>
    </v-dialog>
  </v-container>
</template>

<script>
import { required, sameAs, minLength, numeric, maxValue, email } from 'vuelidate/lib/validators'
import { helpers } from 'vuelidate/lib/validators'
import { mapActions } from 'vuex'
import SendOtp from '@/components/SendOtp'
const phoneNumber = helpers.regex('phoneNumber', (/^\s*(?:\+?(\d{1,3}))?[-. (]*(\d{3})[-. )]*(\d{3})[-. ]*(\d{4})(?: *x(\d+))?\s*$/))
export default {
  title: 'Registration for Kamakhya Nagar Development Committee',
  metaInfo: {
    title: 'Registration for Kamakhya Nagar Development Committee'
  },
  components: {
    SendOtp
  },
  data: () => ({
    primaryData: {
      society_registration_number: '',
      mobile_number: '',
      password: '',
      confirmPassword: '',
      full_name: '',
      address: '',
      email: '',
      company: '',
      designation: '',
      family_members: '',
      role: 'user'
    },
    formValid: false,
    rules: {
      phoneNumber: val => (/^\+?([0-9]{2})\)?[-. ]?([0-9]{4})[-. ]?([0-9]{3})[-. ]?([0-9]{3})$/.test(val) || /^\(?([0-9]{4})\)?[-. ]?([0-9]{3})[-. ]?([0-9]{3})$/.test(val)) || 'Phone Number Must be valid',
    },
    relationItems: [
      {
        name: 'Husband',
        value: 'husband'
      },
      {
        name: 'Wife',
        value: 'wife'
      },
      {
        name: 'Father',
        value: 'father'
      },
      {
        name: 'Mother',
        value: 'mother'
      },
      {
        name: 'Son',
        value: 'son'
      },
      {
        name: 'Daughter',
        value: 'daughter'
      },
      {
        name: 'Brother',
        value: 'brother'
      },
      {
        name: 'Sister',
        value: 'sister'
      },
      {
        name: 'Other',
        value: 'other'
      },
    ],
    familyData: [],
    showPassword: false,
    showConfirmPassword: false,
    sendOtp: false,
    errorMsg: '',
    numbeExist: false
  }),

  validations() {
    let data = {
      primaryData: {
        society_registration_number: {
          required,
          async isValidRegistration(value) {
            if(value === '') return true
            const response = await this.checkRegistrationValidity({registration: {society_registration_number: value}})
            if(response.data.status) {
              return !!response.data.isValid
            } else {
              return true
            }
          }
        },
        mobile_number: {
          required,
          phoneNumber,
          async isNumberExist(value) {
            if(value === '') return true
            const response = await this.checkUserExist({userData: {mobile_number: value}})
            if(response.data.status) {
              return !response.data.isUser
            } else {
              return true
            }
          }
        },
        password: {
          required,
          minLength: minLength(8)
        },
        confirmPassword: {
          required,
          sameAsPassword: sameAs('password')
        },
        full_name: {
          required
        },
        address: {
          required
        },
        email: {
          email
        },
        company: {

        },
        designation: {

        },
        family_members: {
          numeric,
          maxValue: maxValue(10)
        }
      },
      familyData: {
        $each: {
          relation: {
            required
          },
          member_name: {
            required
          }
        }
      }
    }
    return data
  },
  watch: {
    "primaryData.family_members": function (newVal) {
      if(newVal > 0 && this.familyData.length != newVal) {
        for(let i=0; i<newVal; i++) {
          this.familyData.push({'relation': '', 'member_name': ''})
        }
      } else {
        this.familyData = []
      }
    }
  },
  methods: {
    ...mapActions('user', [
      'signupUser',
      'createFamilyMembers',
      'checkUserExist'
    ]),
    ...mapActions('society', [
      'checkRegistrationValidity'
    ]),
    signup () {
      this.$v.$touch()
      if (!this.$v.$invalid) {
        this.primaryData.family_members = Number(this.primaryData.family_members)
        this.signupUser(this.primaryData).then((response) => {
          if(response.data.otp || response.data.matched_failed) {
            this.sendOtp = true
          } 
          else {
            if (this.familyData.length > 0 && this.primaryData.family_members>0) {
              this.familyData.forEach((element) => {
                element.user = response.data.user
              });
              this.createFamilyMembers(this.familyData).then(() => {
                this.$router.push('/')
              })
            } else {
              this.$router.push('/')
            }
          }
        }).catch((error) => {
          console.log('eeeee', error.status)
        })
      }
    },
    reset() {
      this.primaryData.mobile_number = ''
      this.primaryData.password = ''
      this.primaryData.confirmPassword = ''
      this.primaryData.full_name = ''
      this.primaryData.address = ''
      this.primaryData.company = ''
      this.primaryData.email = ''
      this.primaryData.designation = ''
      this.primaryData.family_members = ''
    }
  }
}
</script>

<style scoped>
.signup {
  display: flex;
  position: relative;
  align-items: center;
  justify-content: center;
  margin: auto;
}

.v-input >>> .v-label--active {
  font-size: 20px;
  top: 2px;
  overflow: initial;
}
.validation-text {
  position: relative;
  bottom: 20px;
}
</style>
