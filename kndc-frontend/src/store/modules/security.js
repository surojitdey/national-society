import Vue from 'vue'
import ApiService from '../../services/api.service'
import _ from 'lodash'

const state = {
  securities: [],
  activeSecurities: [],
  security: {},
  securitiesTime: [],
  securityTime: []
}

const mutations = {
  setSecurities(state, securities) {
    Vue.set(state, 'securities', [...securities])
  },
  setActiveSecurities(state, securities) {
    Vue.set(state, 'activeSecurities', [...securities])
  },
  setSecurity(state, security) {
    Vue.set(state, 'security', {...security})
  },
  setSecurityProperty(state, {property, value}) {
    Vue.set(state.security, property, value)
  },
  setSecuritiesTime(state, securitiesTime) {
    Vue.set(state, 'securitiesTime', [...securitiesTime])
  },
  setSecurityTime(state, securityTime) {
    Vue.set(state, 'securityTime', [...securityTime])
  },
}

const actions = {
  fetchSecurities({commit}) {
    return ApiService.get('/security-api/v-1/get-security/').then((response) => {
      commit('setSecurities', response.data)
    })
  },
  fetchSecurity({commit}, data) {
    return ApiService.post('/security-api/v-1/get-security-by-id/', data).then((response) => {
      commit('setSecurity', response.data)
    })
  },
  fetchActiveSecurities({commit}) {
    return ApiService.get('/security-api/v-1/get-active-security/').then((response) => {
      commit('setActiveSecurities', response.data)
    })
  },
  postSecurityData({ dispatch }, data) {
    return ApiService.post('/security-api/v-1/create-security/', data).then(() => {
      dispatch('fetchSecurities')
    })
  },
  updateSecurityData({ dispatch, getters }) {
    return ApiService.post('/security-api/v-1/update-security/', getters.getSecurity).then(() => {
      dispatch('fetchSecurities')
    })
  },
  updateStatus({dispatch}, data) {
    return ApiService.post('/security-api/v-1/update-security-status/', data).then(()=> {
      dispatch('fetchSecurities')
      dispatch('fetchActiveSecurities')
      dispatch('fetchSecuritiesTime')
    })
  },
  fetchSecuritiesTime({commit}) {
    return ApiService.get('/security-api/v-1/get-security-time/').then((response) => {
      commit('setSecuritiesTime', response.data)
    })
  },
  fetchSecurityTime({ commit }, security_id) {
    return ApiService.get(`/security-api/v-1/get-individual-security-time?security_id=${security_id}`).then((response) => {
      commit('setSecurityTime', response.data)
    })
  },
  createSequrityTime({dispatch}, data) {
    return ApiService.post('/security-api/v-1/set-security-time/', data).then(() => {
      dispatch('fetchSecuritiesTime')
    })
  },
  deleteSecurityTime({dispatch}, data) {
    return ApiService.post('/security-api/v-1/delete-security-time/', data).then(() => {
      dispatch('fetchSecuritiesTime')
    })
  },
  updateSecurityTime({dispatch}, data) {
    return ApiService.post('/security-api/v-1/update-security-time/', _.omit(data, 'startManu', 'endManue')).then(() => {
      dispatch('fetchSecuritiesTime')
    })
  }
}

const getters = {
  getSecurites: state => state.securities,
  getActiveSecurities: state => state.activeSecurities,
  getSecurity: state => state.security,
  getSecuritesTime: state => state.securitiesTime,
  getSecurityTime: state => state.securityTime,
}

export default {
  namespaced: true,
  state,
  mutations,
  actions,
  getters
}
