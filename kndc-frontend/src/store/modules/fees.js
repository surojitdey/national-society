import Vue from 'vue'
import ApiService from '../../services/api.service'
// import { TokenService } from '@/services/token.service'
// import _ from 'lodash'

const state = {
  fees: {},
  feesId: null,
  payments: [],
  paymentDetails: [],
  unpaid: []
}

const mutations = {
  setFees(state, fees) {
    Vue.set(state, 'fees', {...fees})
  },
  setFeesId(state, feesId) {
    Vue.set(state, 'feesId', feesId)
  },
  setFeesProperty(state, { property, value }) {
    Vue.set(state.fees, property, value)
  },
  removeFeesProperty(state, property) {
    Vue.delete(state.fees, property)
  },
  setPayments(state, payments) {
    Vue.set(state, 'payments', [...payments])
  },
  setPaymentDetails(state, payments) {
    Vue.set(state, 'paymentDetails', [...payments])
  },
  setPaymentDetailsProperty(state, {property, value, index}) {
    Vue.set(state.paymentDetails[index], property, value)
  },
  removePaymentDetails(state) {
    Vue.set(state, 'paymentDetails', [])
  },
  removePayments(state) {
    Vue.set(state, 'payments', [])
  },
  setUnpaid(state, unpaid) {
    Vue.set(state, 'unpaid', [...unpaid])
  }
}

const actions = {
  createFees({ getters }) {
    return ApiService.post('/fees-api/v-1/fees/', {fields: getters.getFees})
  },
  updateFees({ getters }) {
    return ApiService.post(`/fees-api/v-1/update-fees/`, {fields: getters.getFees, id: getters.getFeesId})
  },
  fetchFees({commit}) {
    return ApiService.get('/fees-api/v-1/fees/').then((response) => {
      console.log('***', response.data)
      if (response.data.length > 0) {
        commit('setFees', response.data[0].fields)
        commit('setFeesId', response.data[0].id)
      }
    })
  },
  updatePayment({ dispatch }, data) {
    return ApiService.post('/fees-api/v-1/payment-fees/', data).then(() => {
      data.from_month = ''
      data.from_year = ''
      data.to_month = ''
      data.to_year = ''
      dispatch('getPaymentStatus', data)
    })
  },
  getPaymentStatus({commit}, data) {
    return ApiService.get(`/fees-api/v-1/payment-status/?user=${data.user}&payment_month=${data.payment_month}&payment_year=${data.payment_year}&from_month=${data.from_month}&from_year=${data.from_year}&to_month=${data.to_month}&to_year=${data.to_year}`)
    .then((response) => {
      if(response.data.data) {
        commit('setPaymentDetails', response.data.data)
      }
    })
  },
  getUserPaymentStatus({commit}, data) {
    return ApiService.get(`/fees-api/v-1/user-payment-status/?from_month=${data.from_month}&from_year=${data.from_year}&to_month=${data.to_month}&to_year=${data.to_year}`)
    .then((response) => {
      commit('setPayments', response.data.data)
      commit('setUnpaid', response.data.due_months)
    })
  },
  fetchUserPayment({commit}) {
    return ApiService.get(`/fees-api/v-1/user-payment/`).then((response)=> {
      commit('setPayments', response.data.data)
    })
  },
  fetchLimitedUnpaidPayment({commit}) {
    return ApiService.get(`/fees-api/v-1/pending-user-payment/`).then((response)=> {
      commit('setPaymentDetails', response.data.data)
    })
  },
  fetchUnpaidPayment({commit}) {
    return ApiService.get(`/fees-api/v-1/pending-user-payment/`).then((response)=> {
      commit('setPaymentDetails', response.data.limited_data)
    })
  },
  // deleteUserPayment({ dispatch}, data) {
  //   return ApiService.get(`/fees-api/v-1/delete-user-payment/?payment_id=${data.id}`).then(()=> {
  //     data.from_month = ''
  //     data.from_year = ''
  //     data.to_month = ''
  //     data.to_year = ''
  //     dispatch('getPaymentStatus', data)
  //   })
  // },
}

const getters = {
  getFees: state => state.fees,
  getFeesId: state => state.feesId,
  getPayments: state => state.payments,
  getPaymentDetails: state => state.paymentDetails,
  getUnpaid: state => state.unpaid
}

export default {
  namespaced: true,
  state,
  mutations,
  actions,
  getters
}
