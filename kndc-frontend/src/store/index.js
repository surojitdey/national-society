import Vue from 'vue'
import Vuex from 'vuex'

import JWT from './modules/JWT'
import user from './modules/user'
import event from './modules/event'
import security from './modules/security'
import settings from './modules/settings'
import fees from './modules/fees'
import posts from './modules/posts'
import society from './modules/society'

Vue.use(Vuex)

const store = new Vuex.Store({
  modules: {
    JWT,
    user,
    event,
    security,
    settings,
    fees,
    posts,
    society
  },
  strict: process.env.NODE_ENV !== 'production'
})

export default store
