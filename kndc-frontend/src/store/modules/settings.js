import Vue from 'vue'
import ApiService from '../../services/api.service'
// import { TokenService } from '@/services/token.service'
// import _ from 'lodash'

const state = {
  setting: {
    community_name: '',
    appartment_name: '',
    address_one: '',
    address_two: '',
    city: '',
    pincode: '',
    contact_number: '',
    email: '',
    show_address: true,
    show_number: true,
    show_email: true,
    enable_events: true,
    enable_news: true,
    enable_posts: true,
    show_complaints: true,
  },
}

const mutations = {
  setSettings(state, setting) {
    Vue.set(state, 'setting', ...setting)
  },
  setSettingsProperty(state, { property, value }) {
    Vue.set(state.setting, property, value)
  },
}

const actions = {
  createSettings({ getters }) {
    return ApiService.post('/config-api/v-1/contacts/', getters.getSettings)
  },
  updateSettings({ getters }) {
    return ApiService.post(`/config-api/v-1/update-contacts/`, getters.getSettings)
  },
  fetchSettings({ commit }) {
    return ApiService.get('/config-api/v-1/contacts/').then((response) => {
      if (response.data.length > 0) {
        commit('setSettings', response.data)
      }
    })
  },
}

const getters = {
  getSettings: state => state.setting,
}

export default {
  namespaced: true,
  state,
  mutations,
  actions,
  getters
}
