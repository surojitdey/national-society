<template>
  <div class="residents-fees">
    <v-card elevation="0" width="90%" class="ma-auto">
      <v-row no-gutters align="center" justify="center">
        <v-card-title class="text-h5 font-weight-bold text-uppercase">Fees Status</v-card-title>
      </v-row>
      <v-row no-gutters justify="space-around" class="mt-3">
        <v-col cols="4">
          <span>From Date</span>
        </v-col>
        <v-col cols="4">
          <span>To Date</span>
        </v-col>
        <v-col cols="1"></v-col>
        <v-col cols="1"></v-col>
      </v-row>
      <v-row no-gutters justify="space-around" class="mb-3">
        <v-col cols="4">
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
        <v-col cols="4">
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
      <v-row no-gutters align="center" justify="center">
        <v-expansion-panels focusable popout flat hover light class="expansion-panels">
          <v-expansion-panel v-for="(due, index) in unpaid" :key="index">
            <v-expansion-panel-header hide-actions class="rounded-pill">
              <v-alert
                class="ma-0 d-flex justify-center"
                dense
                text
                type="error"
                color="warning"
                outlined
                rounded="pill"
              >
                <span>You have due payment for the month of <strong>{{getMonthString(due.payment_month)}} {{due.payment_year}}</strong></span>
              </v-alert>
            </v-expansion-panel-header>
            <v-expansion-panel-content>
              <v-card elevation="0" v-for="(item, index) in fees" :key="index">
                <v-row no-gutters justify="center">
                  <v-col cols="6" class="d-flex justify-center">
                    <span class="header-text text-capitalize">{{index}}</span>
                  </v-col>
                  <v-col cols="6" class="d-flex justify-center">
                    <span class="header-text text-capitalize"><v-icon v-text="currencyIcon"></v-icon>{{item}}</span>
                  </v-col>
                </v-row>
              </v-card>
            </v-expansion-panel-content>
          </v-expansion-panel>
        </v-expansion-panels>
      </v-row>
      <v-row v-if="payments.length>0" no-gutters align="center" justify="center">
        <v-card-title class="text-h5 font-weight-bold text-uppercase">Your recent payments</v-card-title>
      </v-row>
      <v-row no-gutters align="center" justify="center">
        <v-expansion-panels focusable popout flat hover light class="expansion-panels">
          <v-expansion-panel v-for="(payment, index) in payments" :key="index">
            <v-expansion-panel-header hide-actions class="rounded-pill">
              <v-alert
                dense
                class="ma-0 d-flex justify-center"
                text
                type="success"
                outlined
                rounded="pill"
              >
                <span>{{getMonthString(Number(payment.payment_month))}} {{payment.payment_year}}</span>
              </v-alert>
            </v-expansion-panel-header>
            <v-expansion-panel-content>
              <v-card elevation="0" v-for="(item, index) in payment.amount_break_up" :key="index">
                <v-row no-gutters justify="center">
                  <v-col cols="6" class="d-flex justify-center">
                    <span class="header-text text-capitalize">{{index}}</span>
                  </v-col>
                  <v-col cols="6" class="d-flex justify-center">
                    <span class="header-text text-capitalize"><v-icon v-text="currencyIcon"></v-icon>{{item}}</span>
                  </v-col>
                </v-row>
              </v-card>
              <!-- <div class="d-flex justify-center" >{{index}} {{item}}</div> -->
            </v-expansion-panel-content>
          </v-expansion-panel>
        </v-expansion-panels>
      </v-row>
    </v-card>
  </div>
</template>
<script>
import { mapActions, mapGetters, mapMutations } from 'vuex'
export default {
  data: () => ({
    overlays: false,
    fromMonth: '',
    toMonth: '',
    fromYear: '',
    toYear: '',
    currencyIcon: 'mdi-currency-inr'
  }),
  computed: {
    ...mapGetters('fees', {
      payments: 'getPayments',
      paymentDetails: 'getPaymentDetails',
      fees: 'getFees',
      unpaid: 'getUnpaid'
    }),
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
      'fetchUserPayment',
      'getUserPaymentStatus',
      'fetchFees'
    ]),
    ...mapMutations('fees', [
      'removePaymentDetails',
      'removePayments'
    ]),
    fetchFeeData() {
      this.overlays = true
      this.fetchFees().then(() => {
        this.overlays = false
      })
    },
    getMonthString(month) {
      const today = new Date(2020,month-1,1)
      return today.toLocaleString('default', { month: 'long' })
    },
    checkPaymentStatus() {
      this.overlays = true
      this.getUserPaymentStatus(this.paymentData).finally(() => {
        this.overlays = false
      })
    },
    resetPage() {
      this.removePayments()
      this.removePaymentDetails()
      Object.assign(this.$data, this.$options.data.apply(this))
    }
  },
  mounted() {
    this.fetchFeeData()
    this.checkPaymentStatus(this.paymentData)
  } 
}
</script>
<style scoped>
.expansion-panels {
  max-width: fit-content !important;
}
</style>
