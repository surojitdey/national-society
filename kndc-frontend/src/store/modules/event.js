import Vue from 'vue'
import ApiService from '../../services/api.service'
// import { TokenService } from '@/services/token.service'
import _ from 'lodash'

const state = {
  events: [],
  event: {},
  informations: [],
  information: {}
}

const mutations = {
  setEvents(state, events) {
    Vue.set(state, 'events', [...events])
  },
  setEvent(state, event) {
    Vue.set(state, 'event', {...event})
  },
  setEventProperty(state, {property, value}) {
    Vue.set(state.event, property, value)
  },
  setInformations(state, informations) {
    Vue.set(state, 'informations', [...informations])
  },
  setInformation(state, information) {
    Vue.set(state, 'information', { ...information })
  },
  setInformationProperty(state, {property, value}) {
    Vue.set(state.information, property, value)
  },
}

const actions = {
  fetchEvents({ commit }) {
    return ApiService.get('/events-api/v-1/events/').then((response) => {
      commit('setEvents', response.data)
    })
  },
  fetchLimitedEvents({ commit }) {
    return ApiService.get('/events-api/v-1/limited-events/').then((response) => {
      commit('setEvents', response.data)
    })
  },
  fetchEventById({ commit }, event_id) {
    return ApiService.get(`/events-api/v-1/events/${event_id}`).then((response) => {
      commit('setEvent', response.data)
    })
  },

  postEvents({ dispatch }, data) {
    return ApiService.post('/events-api/v-1/events/', data).then(() => {
      dispatch('fetchEvents')
    })
  },

  updateEvents({ dispatch }, data) {
    return ApiService.post('/events-api/v-1/update-event/', data).then(() => {
      dispatch('fetchEvents')
    })
  },

  deleteEvents({ dispatch }, data) {
    return ApiService.post('/events-api/v-1/delete-event/', data).then(() => {
      dispatch('fetchEvents')
    })
  },


  // News/Information
  fetchInformations({ commit }) {
    return ApiService.get('/events-api/v-1/news/').then((response) => {
      commit('setInformations', response.data)
    })
  },

  fetchLimitedInformations({ commit }) {
    return ApiService.get('/events-api/v-1/limited-news/').then((response) => {
      commit('setInformations', response.data)
    })
  },

  fetchInformationById({ commit }, news_id) {
    return ApiService.get(`/events-api/v-1/news/${news_id}`).then((response) => {
      commit('setInformation', response.data)
    })
  },

  addInformation({ dispatch }, data) {
    return ApiService.post('/events-api/v-1/news/', data).then(() => {
      dispatch('fetchInformations')
    })
  },

  updateInformation({ dispatch, getters }) {
    let formData = new FormData()

    if (typeof getters.getInformation.media_file === 'string') {
      for (let key in _.omit(getters.getInformation, 'media_file')) {
        formData.append(key, getters.getInformation[key])
      }
    } else {
      for (let key in getters.getInformation) {
        formData.append(key, getters.getInformation[key])
      }
    }
    return ApiService.post('/events-api/v-1/update-news/',formData).then(() => {
      dispatch('fetchInformations')
    })
  },

  deleteInfomarion({ dispatch }, data) {
    return ApiService.post('/events-api/v-1/delete-news/', data).then(() => {
      dispatch('fetchInformations')
    })
  },
}

const getters = {
  getEvents: state => state.events,
  getEvent: state => state.event,
  getInformations: state => state.informations,
  getInformation: state => state.information
}

export default {
  namespaced: true,
  state,
  mutations,
  actions,
  getters
}
