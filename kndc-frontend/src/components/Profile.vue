<template>
  <div class="profile mb-16">
    <v-card elevation="1">
      <v-card-title class="text-h5 font-weight-bold text-uppercase d-flex justify-center">Profile</v-card-title>
      <v-divider></v-divider>
      <v-row justify="center" align="center">
        <v-col cols="12"></v-col>
        <v-col cols="2">
          <span>Mobile Number *</span>
        </v-col>
        <v-col cols="4">
          <v-text-field dense :value="$v.user.mobile_number.$model" :rules="[$v.user.mobile_number.required, rules.phoneNumber]" @input="updateUserProperty('mobile_number', $event)"></v-text-field>
          <span v-if="!$v.user.mobile_number.required" class="red--text text-body-2">Mobile number required.</span>
        </v-col>
      </v-row>
      <v-row justify="center" align="center">
        <v-col cols="2">
          <span>Name *</span>
        </v-col>
        <v-col cols="4">
          <v-text-field dense :value="$v.user.full_name.$model" @input="updateUserProperty('full_name', $event)"></v-text-field>
          <span v-if="!$v.user.full_name.required" class="red--text text-body-2">Full Name required.</span>
        </v-col>
      </v-row>
      <v-row justify="center" align="center">
        <v-col cols="2">
          <span>Address *</span>
        </v-col>
        <v-col cols="4">
          <v-text-field dense :value="$v.user.address.$model" @input="updateUserProperty('address', $event)"></v-text-field>
          <span v-if="!$v.user.address.required" class="red--text text-body-2">Address required.</span>
        </v-col>
      </v-row>
      <v-row justify="center" align="center">
        <v-col cols="2">
          <span>Email</span>
        </v-col>
        <v-col cols="4">
          <v-text-field dense :value="$v.user.email.$model" @input="updateUserProperty('email', $event)"></v-text-field>
          <span v-if="!$v.user.email.email" class="red--text text-body-2">Email invalid.</span>
        </v-col>
      </v-row>
      <v-row justify="center" align="center">
        <v-col cols="2">
          <span>Company</span>
        </v-col>
        <v-col cols="4">
          <v-text-field dense :value="$v.user.company.$model" @input="updateUserProperty('company', $event)"></v-text-field>
        </v-col>
      </v-row>
      <v-row justify="center" align="center">
        <v-col cols="2">
          <span>Designation</span>
        </v-col>
        <v-col cols="4">
          <v-text-field dense :value="$v.user.designation.$model" @input="updateUserProperty('designation', $event)"></v-text-field>
        </v-col>
      </v-row>
      <!-- <v-row justify="center" align="center">
        <v-col cols="2">
          <span class="text-capitalize">Family members</span>
        </v-col>
        <v-col cols="4">
          <v-text-field dense :value="$v.user.family_members.$model" @input="updateUserProperty('family_members', $event)"></v-text-field>
          <span v-if="!$v.user.family_members.numeric" class="red--text text-body-2">This Field should be numeric.</span>
          <span v-if="!$v.user.family_members.maxValue" class="red--text text-body-2">Should not be grater than 10.</span>
        </v-col>
      </v-row>
      <v-row justify="center" align="center" v-for="(v, index) in $v.familyMembers.$each.$iter" :key="index">
        <v-col cols="3"></v-col>
        <v-col cols="2">
          <span>Relation</span>
        </v-col>
        <v-col cols="4">
          <v-select
            :value="v.relation.$model"
            :items="relationItems"
            item-text="name"
            item-value="value"
            dense
            @change="updateFamilyProperty(index, 'relation', $event)"
          ></v-select>
          <span v-if="!v.relation.required" class="red--text text-body-2">Relation required.</span>
        </v-col>
        <v-col cols="3"></v-col>
        <v-col cols="3"></v-col>
        <v-col cols="2">
          <span>Member Name</span>
        </v-col>
        <v-col cols="4">
          <v-text-field 
            :value="v.member_name.$model"
            dense
            @input="updateFamilyProperty(index, 'member_name', $event)"
          ></v-text-field>
          <span v-if="!v.member_name.required" class="red--text text-body-2">Family member name required.</span>
        </v-col>
        <v-col cols="3"></v-col>
        <v-col cols="2"></v-col>
        <v-col cols="3">
          <v-btn small outlined class="text-uppercase rounded" color="#434D3D">Remove Member</v-btn>
        </v-col>
      </v-row> -->
      <!-- <v-row justify="center" align="center">
        <v-col cols="2">
          <span>Family members</span>
        </v-col>
        <v-col cols="4">
          <v-text-field dense :value="$v.user.family_members.$model" @input="updateUserProperty('family_members', $event)"></v-text-field>
          <span v-if="!$v.user.family_members.required" class="red--text text-body-2">Number of family members required.</span>
          <span v-if="!$v.user.family_members.numeric" class="red--text text-body-2">This Field should be numeric.</span>
          <span v-if="!$v.user.family_members.maxValue" class="red--text text-body-2">Should not be grater than 10.</span>

          <v-text-field dense :value="$v.familyMembersNumber.$model" @input="$v.familyMembersNumber.$touch()"></v-text-field>
          <span v-if="!$v.familyMembersNumber.required" class="red--text text-body-2">Number of family members required.</span>
          <span v-if="!$v.familyMembersNumber.numeric" class="red--text text-body-2">This Field should be numeric.</span>
          <span v-if="!$v.familyMembersNumber.maxValue" class="red--text text-body-2">Should not be grater than 10.</span>
        </v-col>
      </v-row>
      <v-row justify="center" align="center" v-for="(v, index) in $v.familyMembers.$each.$iter" :key="index">
        <v-col cols="3"></v-col>
        <v-col cols="2">
          <span>Relation</span>
        </v-col>
        <v-col cols="4">
          <v-select
            :value="v.relation.$model"
            :items="relationItems"
            item-text="name"
            item-value="value"
            dense
            @change="updateFamilyProperty(index, 'relation', $event)"
          ></v-select>
          <span v-if="!v.relation.required" class="red--text text-body-2">Relation required.</span>
        </v-col>
        <v-col cols="3"></v-col>
        <v-col cols="3"></v-col>
        <v-col cols="2">
          <span>Member Name</span>
        </v-col>
        <v-col cols="4">
          <v-text-field 
            :value="v.member_name.$model"
            dense
            @input="updateFamilyProperty(index, 'member_name', $event)"
          ></v-text-field>
          <span v-if="!v.member_name.required" class="red--text text-body-2">Family member name required.</span>
        </v-col>
        <v-col cols="3"></v-col>
        <v-col cols="2"></v-col>
        <v-col cols="3">
          <v-btn class="primary">Remove Member</v-btn>
        </v-col>
      </v-row> -->
      <v-row justify="center" align="center">
        <v-col cols="4" class="d-flex justify-space-between">  
          <v-btn @click="save" color="project_primary" class="text-uppercase white--text rounded" width="30%" :disabled="disabledSave">Save</v-btn>
          <v-btn @click="resetUser" color="grey" class="text-uppercase white--text rounded" width="30%" :disabled="disabledSave">Cancel</v-btn>
        </v-col>
      </v-row>
    </v-card>

    <v-dialog v-model="sendOtp" persistent width="500">
      <SendOtp
        title="Verify OTP"
        :data="user"
        otp_type="number_change"
        :mobile_number="user.mobile_number"
        @cancel-otp="sendOtp=false"
        @verify-success="save"
        @verify-failed="sendOtp=false,errorMsg='Invalid OTP.'"
        @invalid-request="sendOtp=false,errorMsg='Somthing went wrong.'"
      ></SendOtp>
    </v-dialog>
  </div>
</template>
<script>
import { mapActions, mapGetters, mapMutations } from 'vuex'
import { required, numeric, maxValue, email } from 'vuelidate/lib/validators'
import SendOtp from '@/components/SendOtp'
export default {
  title: () => ('Resident Profile'),
  metaInfo: {
    title: 'Resident Profile'
  },
  components: {
    SendOtp
  },
  data: () => ({
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
        name: 'Other',
        value: 'other'
      },
    ],
    disabledSave: false,
    overlay: false,
    sendOtp: false,
    errorMsg: '',
    familyData: []
  }),
  computed: {
    ...mapGetters('user',{
      user: 'getUser',
      familyMembers: 'getFamily'
    }),
    familyMembersNumber () {
      return this.user.family_members
    }
  },
  methods: {
    ...mapActions('user', [
      'fetchUser',
      'fetchFamily',
      'updateUser'
    ]),
    ...mapMutations('user', [
      'setUserProperty',
      'setFamilyProperty',
      'resetUser',
      'setFamily'
    ]),
    updateUserProperty(property, value) {
      if(property==="family_members") {
        if(value > this.familyMembers.length) {
          let addedValue = value - this.familyMembers.length
          for(let i=0; i<addedValue; i++) {
            this.familyData.push({'relation': '', 'member_name': ''})
          }
          this.setFamily(this.familyData)
        }
      }
      this.setUserProperty({
        property,
        value
      })
      this.$v.user[property].$touch()
    },
    updateFamilyProperty(index, property, value) {
      this.setFamilyProperty({
        index,
        property,
        value
      })
      this.$v.familyMembers[index][property].$touch()
    },
    save() {
      this.$v.$touch()
      this.disabledSave = true
      this.overlay = true

      if (!this.$v.$invalid) {
        this.updateUser().then((response) => {
          if(response.data.otp || response.data.matched_failed) {
            this.sendOtp = true
          } else {
            this.disabledSave = false
            location.reload()
          }
          this.overlay = false
        }).catch(() => {
          this.disabledSave = false
          this.overlay = false
        })
      }
    }
  },
  mounted() {
    this.overlay = true
    this.fetchUser().then(() => {
      this.fetchFamily().then(() => {
        this.overlay = false
      })
    })
  },
  validations() {
    let data = {
      user: {
        mobile_number: {
          required
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
      familyMembers: {
        $each: {
          relation: {
            required
          },
          member_name: {
            required
          }
        }
      },
      familyMembersNumber: {
        required,
        numeric,
        maxValue: maxValue(10)
      }
    }
    return data
  },
}
</script>
<style scoped>

</style>
