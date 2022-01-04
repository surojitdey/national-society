<template>
  <div class="fees-settings">
    <v-card elevation="0" class="ma-auto" width="90%">
      <v-card-title class="text-h5 d-flex justify-center font-weight-bold text-uppercase">fees payment</v-card-title>
      <v-row no-gutters justify="end" class="mt-3">
        <v-btn
          :loading="loading"
          class="ma-0 pa-0"
          color="primary"
          plain
          @click="getAllUnpaidDetails"
        >
          All unpaid details
        </v-btn>
      </v-row>
      <v-row no-gutters justify="space-around" class="mt-3">
        <v-col cols="3"></v-col>
        <v-col cols="3">
          <span>From Date</span>
        </v-col>
        <v-col cols="3">
          <span>To Date</span>
        </v-col>
        <v-col cols="1"></v-col>
        <v-col cols="1"></v-col>
      </v-row>
      <v-row no-gutters justify="space-around" class="mb-3">
        <v-col cols="3">
          <v-autocomplete
            :disabled="overlays"
            :items="residents"
            :filter="customFilter"
            v-model="selectedResident"
            item-text="full_name"
            item-value="id"
            label="Residents"
            outlined
            filled
            class="rounded"
            dense
            cache-items
            rounded
            
          ></v-autocomplete>
        </v-col>
        <v-col cols="3">
          <v-row justify="space-between" align="center">
            <v-col cols="6">
              <v-select
                :items="monthArray"
                v-model="fromMonth"
                label="Month"
                item-text="text"
                item-value="value"
                class="rounded"
                dense
                outlined
                filled
                
              ></v-select>
            </v-col>
            <v-col cols="6">
              <v-select
                :items="yearArray"
                v-model="fromYear"
                label="Year"
                item-text="text"
                item-value="value"
                class="rounded"
                dense
                outlined
                filled
                
              ></v-select>
            </v-col>
          </v-row>
        </v-col>
        <v-col cols="3">
          <v-row justify="space-between" align="center">
            <v-col cols="6">
              <v-select
                :items="monthArray"
                v-model="toMonth"
                label="Month"
                item-text="text"
                item-value="value"
                class="rounded"
                dense
                outlined
                filled
                
              ></v-select>
            </v-col>
            <v-col cols="6">
              <v-select
                :items="yearArray"
                v-model="toYear"
                label="Year"
                item-text="text"
                item-value="value"
                class="rounded"
                dense
                outlined
                filled
                
              ></v-select>
            </v-col>
          </v-row>
        </v-col>
        <v-col cols="1">
          <v-btn @click="checkPaymentStatus" color="project_primary" class="white--text rounded">Go</v-btn>
        </v-col>
        <v-col cols="1">
          <v-btn @click="resetPage" color="primary" class="white--text rounded">Reset</v-btn>
        </v-col>
      </v-row>
    </v-card>
    <v-divider v-if="payments.length>0" class="mb-3"></v-divider>
    <v-card elevation="0" color="transparent" v-if="payments.length>0">
      <v-row justify="space-around">
        <v-col cols="2" class="d-flex justify-center">
          <span class="header-text text-capitalize">Resident Name</span>
        </v-col>
        <v-col cols="2" class="d-flex justify-center">
          <span class="header-text text-capitalize">Amount</span>
        </v-col>
        <v-col cols="1" class="d-flex justify-center">
          <span class="header-text text-capitalize">Month</span>
        </v-col>
        <v-col cols="1" class="d-flex justify-center">
          <span class="header-text text-capitalize">Year</span>
        </v-col>
        <v-col cols="2" class="d-flex justify-center">
          <span class="header-text text-capitalize">Payment Status</span>
        </v-col>
      </v-row>
    </v-card>
    <v-card color="#F5F5F5" elevation="0" class="my-6" v-for="(user, index) in payments" :key="index">
      <v-row justify="space-around">
        <v-col cols="2" class="d-flex justify-center">
          <span class="header-text text-capitalize">{{user.full_name}}</span>
        </v-col>
        <v-col cols="2" class="d-flex justify-center">
          <v-expansion-panels class="rounded" popout flat focusable>
            <v-expansion-panel>
              <v-expansion-panel-header color="#F5F5F5" class="d-flex align-start py-1">{{user.amount}}</v-expansion-panel-header>
              <v-expansion-panel-content>
                <div v-for="(item, index) in user.amount_break_up" :key="index">{{index}} {{item}}</div>
              </v-expansion-panel-content>
            </v-expansion-panel>
          </v-expansion-panels>
        </v-col>
        <v-col cols="1" class="d-flex justify-center">
          <span class="header-text text-capitalize">{{getMonthString(user.payment_month)}}</span>
        </v-col>
        <v-col cols="1" class="d-flex justify-center">
          <span class="header-text text-capitalize">{{user.payment_year}}</span>
        </v-col>
        <v-col cols="2" class="d-flex justify-center">
          <v-select
            class="pa-0 ma-0 rounded"
            :class="user.status=='paid'?'green--text':'red--text'"
            chips
            :background-color="user.status=='paid'?'green':'project_red'"
            :items="paymentStatusItems"
            item-text="text"
            item-value="value"
            :value="user.status"
            outlined
            dense
            @change="savePaymentDetails('status', $event, index, user)"
          ></v-select>
        </v-col>
      </v-row>
    </v-card>

    <v-dialog v-model="confirmChangeDialog" width="30%" persistent>
      <v-card>
        <v-alert dense text type="error">You want to change payment status?</v-alert>
        <v-card-actions class="d-flex justify-start">
          <v-btn
            class="white--text text-uppercase mx-2"
            width="30%"
            color="#423D3D"
            @click="deletePaymentDetails"
          >Yes</v-btn>
          <v-btn
            class="white--text text-uppercase mx-2"
            width="30%"
            color="#423D3D"
            @click="confirmChangeDialog=false"
          >No</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
    <v-dialog v-model="showStatusOfPayment" width="30%" persistent>
      <v-card>
        <v-alert dense v-if="feesPaid" text type="error">Resident has paid the fees already.</v-alert>
        <v-alert dense v-if="successPayment" text type="success">Payment of fees is succesfull.</v-alert>
        <v-card-actions class="d-flex justify-start">
          <v-btn
            class="white--text text-uppercase mx-2"
            width="30%"
            color="#423D3D"
            @click="closePopup"
          >Cancel</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
    <v-overlay v-model="overlays">
      <v-progress-circular indeterminate color="white" width="5"></v-progress-circular>
    </v-overlay>
  </div>
</template>
<script>
import { mapGetters, mapActions, mapMutations } from 'vuex'
export default {
  data: () => ({
    overlays: false,
    selectedResident: null,
    selectedMonth: '',
    selectedYear: '',
    selectedIndex: null,
    selectedUser: null,
    fromMonth: '',
    fromYear: '',
    toMonth: '',
    toYear: '',
    paymentEnable: false,
    showStatusOfPayment: false,
    feesPaid: false,
    successPayment: false,
    paymentStatus: false,
    paymentStatusItems: [
      {
        text: 'Paid',
        value: "paid"
      },
      {
        text: 'Unpaid',
        value: "unpaid"
      }
    ],
    confirmChangeDialog: false,
    loading: false
  }),
  computed: {
    ...mapGetters('fees', {
      fees: 'getFees',
      payments: 'getPaymentDetails'
    }),
    ...mapGetters('user',{
      residents: 'getResidents'
    }),
    totalFees() {
      let total = 0
      for(let value in this.fees) {
        total = total + Number(this.fees[value])
      }
      return total
    },
    monthArray() {
      let arr = []
      for(let i=0;i<12;i++) {
        const today = new Date(2020,i,1)
        arr.push({
          text: today.toLocaleString('default', { month: 'long' }),
          value: today.getMonth()+1
        })
      }
      return arr
    },
    yearArray() {
      let arr = []
      const today = new Date()
      arr.push({
        text: today.getFullYear(),
        value: today.getFullYear()
      })
      for(let i=0;i<4;i++) {
        arr.push({
          text: today.getFullYear()-i,
          value: today.getFullYear()-i
        })
      }
      return arr
    },
    paymentData() {
      let payment = {
        user: this.selectedResident,
        amount: this.totalFees,
        amount_break_up: this.fees,
        payment_month: this.selectedMonth,
        payment_year: this.selectedYear,
        from_month: this.fromMonth,
        from_year: this.fromYear,
        to_month: this.toMonth,
        to_year: this.toYear
      }
      return payment
    }
  },
  methods: {
    ...mapActions('fees', [
      'fetchFees',
      'updatePayment',
      'getPaymentStatus',
      // 'deleteUserPayment',
      'fetchLimitedUnpaidPayment',
      'fetchUnpaidPayment'
    ]),
    ...mapActions('user', [
      'fetchResidents'
    ]),
    ...mapMutations('fees', [
      'removePaymentDetails',
      'setPaymentDetailsProperty'
    ]),
    updatePaymentDetailsProperty(property, value, index) {
      this.setPaymentDetailsProperty({
        property,
        value,
        index
      })
      // this.$v.changePassword[property].$touch()
    },
    getMonthString(month) {
      const today = new Date(2020,month-1,1)
      return today.toLocaleString('default', { month: 'long' })
    },
    savePaymentDetails(property, value, index, user) {
      this.overlays = true
      this.updatePaymentDetailsProperty(property, value, index)
      this.selectedIndex = index
      this.selectedUser = user
      this.confirmChangeDialog = !value

      this.updatePayment(user).then(()=> {
        this.showStatusOfPayment = true
        this.successPayment = true
      }).finally(() => {
        this.overlays = false
      })
    },
    deletePaymentDetails() {
      // this.overlays = true
      // this.deleteUserPayment(this.selectedUser).then(() => {
      //   this.showStatusOfPayment = true
      //   this.successPayment = true
      //   this.confirmChangeDialog = false
      // }).finally(() => {
      //   this.overlays = false
      // })
    },
    getAllUnpaidDetails() {
      this.loading = true
      this.fetchUnpaidPayment().finally(() => {
        this.loading = false
      })
    },
    checkPaymentStatus() {
      if(this.selectedResident) {
        this.overlays = true
        this.getPaymentStatus(this.paymentData).finally(() => {
          this.overlays = false
        })
      }
    },
    closePopup() {
      this.showStatusOfPayment = false
      this.feesPaid = false
      this.successPayment = false
    },
    customFilter (item, queryText) {
      const textOne = item.full_name.toLowerCase()
      // const textTwo = item.abbr.toLowerCase()
      const searchText = queryText.toLowerCase()

      // return textOne.indexOf(searchText) > -1 ||
      //   textTwo.indexOf(searchText) > -1
      return textOne.indexOf(searchText) > -1
    },
    fetchData() {
      this.overlays = true
      this.fetchResidents().then(() => {
        this.fetchFees().then(() => {
          this.fetchLimitedUnpaidPayment().then(() => {
            this.overlays = false
          })
        })
      })
    },
    resetPage() {
      this.removePaymentDetails()
      Object.assign(this.$data, this.$options.data.apply(this))
    }
  },
  validations() {

  },
  mounted() {
    this.fetchData()
  },
  beforeDestroy() {
    this.resetPage()
  }
}
</script>
<style scoped>
.btn-size {
  height: 30px !important;
  width: 30px !important;
}
.v-select >>> .v-text-field__details {
  display: none !important;
}
</style>
