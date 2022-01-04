import axios from 'axios'
import { TokenService } from '@/services/token.service'
import store from '@/store'

const ApiService = {
  _401interceptor: null,

  init(baseUrl, router) {
    axios.defaults.baseURL = baseUrl
    axios.defaults.timeout = 500000
    axios.defaults.headers.common['Content-Type'] = 'application/json'
    axios.defaults.headers.common['Accept'] = 'application/json'
    this._router = router;
  },

  setHeader() {
    axios.defaults.headers.common['Authorization'] = `Bearer ${TokenService.getAccessToken()}`
  },

  removeHeader() {
    delete axios.defaults.headers.common['Authorization']
  },

  get(resource) {
    return axios.get(resource)
  },

  post(resource, data) {
    return axios.post(resource, data)
  },

  put(resource, data) {
    return axios.put(resource, data)
  },

  patch(resource, data) {
    return axios.patch(resource, data)
  },

  custom(reqData) {
    return axios(reqData)
  },

  mount401interceptor() {
    this._401interceptor = axios.interceptors.response.use(
      (response) => response,
      (error) => {
        if (error.request.status !== 401) throw error
        if (error.config.url.includes('/api/token/refresh/')) this.handleRefreshFail(error)
        else return this.refreshAndRetry(error)
      }
    )
  },

  handleRefreshFail() {
    store.dispatch('JWT/logout').then(() => {
      this._router.push('/signin');
    })
  },

  refreshAndRetry(error) {
    return store.dispatch('JWT/refreshJWT').then(() => {
      error.response.config.headers['Authorization'] = `Bearer ${TokenService.getAccessToken()}`
      return this.custom(error.config)
    })
  },

  unmount401interceptor() {
    axios.interceptors.response.eject(this._401interceptor)
  }
}

export default ApiService
