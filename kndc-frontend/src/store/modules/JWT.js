import { UserService } from "../../services/user.service"
import { TokenService } from "../../services/token.service"

const state = {
  access_token: TokenService.getAccessToken(),
  refresh_token: TokenService.getRefreshToken(),
  is_admin: TokenService.isAdmin(),
  is_default_password: TokenService.isDefaultPassword()
}

const getters = {
  access_token: state => state.access_token,
  refresh_token: state => state.refresh_token,
  loggedIn: state => state.refresh_token !== null,
  isAdmin: state => state.is_admin,
  isDefaultPassword: state => state.is_default_password
}

const mutations = {
  setJWT(state, jwt) {
    // When this updates, the getters and anything bound to them updates as well.
    state.access_token = jwt.access
    state.refresh_token = jwt.refresh;
    state.is_admin = jwt.is_admin
    state.is_default_password = jwt.default_password
  },

  setAccessToken(state, token) {
    state.access_token = token
  },

  clearAllTokens(state) {
    state.access_token = ''
  }
}

const actions = {
  async fetchJWT({ commit }, { formData }) {
    const response = await UserService.login(formData);
    commit('setJWT', response.data);
  },

  async refreshJWT({ commit }) {
    const response = await UserService.refreshAccessToken();
    commit('setAccessToken', response.data.access);
  },

  async refreshAccessToken({ commit }, token) {
    commit('setAccessToken', token)
  },

  async logout({ commit }) {
    UserService.logout();
    commit('clearAllTokens')
  }
}

export default {
  namespaced: true,
  state,
  getters,
  mutations,
  actions
}
