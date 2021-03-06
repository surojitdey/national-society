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
  createSociety(_, registration) {
    return ApiService.post('society-api/v-1/create-society/', registration).then((response) => {
      console.log(response)
    }).catch((error) => {
      console.log(error)
    })
  },
  checkRegistrationValidity(_, { registration }) {
    return ApiService.post('/society-api/v-1/check-registration-validity/', registration)
  },
}

const getters = {

}

export default {
  namespaced: true,
  state,
  mutations,
  actions,
  getters
}
