
const TokenService = {
  getAccessToken() {
    return localStorage.getItem("access_token")
  },

  saveAccessToken(accessToken) {
    localStorage.setItem("access_token", accessToken)
  },

  removeAccessToken() {
    localStorage.removeItem("access_token")
  },

  getRefreshToken() {
    return localStorage.getItem("refresh_token")
  },

  saveRefreshToken(refreshToken) {
    localStorage.setItem("refresh_token", refreshToken)
  },

  removeRefreshToken() {
    localStorage.removeItem("refresh_token")
  },

  isAdmin() {
    if(typeof localStorage.getItem('is_admin') === 'string') {
      return localStorage.getItem("is_admin") === 'true' ? true : false
    }
    return localStorage.getItem("is_admin")
  },

  setAdmin(userIsAdmin) {
    localStorage.setItem("is_admin", userIsAdmin)
  },

  removeIsAdmin() {
    localStorage.removeItem("is_admin")
  },

  setDefaultPassword(adminDefaultPassword) {
    localStorage.setItem('default_password', adminDefaultPassword)
  },

  removeDefaultPassword() {
    localStorage.removeItem('default_password')
  },

  isDefaultPassword() {
    if(typeof localStorage.getItem('default_password') === 'string') {
      return localStorage.getItem('default_password') === 'true' ? true : false
    }
    return localStorage.getItem('default_password')
  }
};

export { TokenService }
