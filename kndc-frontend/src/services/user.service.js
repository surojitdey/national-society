
import ApiService from "./api.service"
import { TokenService } from "./token.service"

class AuthenticationError extends Error {
  constructor(errCode, msg) {
    super(msg)
    this.name = this.constructor.name
    this.message = msg
    this.errorCode = errCode
  }
}


const UserService = {
  async login(formData) {
    const reqData = formData
    return ApiService.post('/api/token/', reqData).then((response) => {
      TokenService.saveAccessToken(response.data.access);
      TokenService.saveRefreshToken(response.data.refresh);
      TokenService.setAdmin(response.data.is_admin);
      TokenService.setDefaultPassword(response.data.default_password);
      ApiService.setHeader();
      ApiService.mount401interceptor();
      return response;
    }).catch((err) => {
      throw new AuthenticationError(err.response.status, err.response.data);
    })
  },

  async refreshAccessToken() {
    const reqData = {
      method: "post",
      url: "/api/token/refresh/",
      data: {
        refresh: TokenService.getRefreshToken()
      }
    };
    return ApiService.custom(reqData).then((response) => {
      TokenService.saveAccessToken(response.data.access);
      ApiService.setHeader();
      return response;
    }).catch((err) => {
      throw new AuthenticationError(err.response.status, err.response.data.detail);
    })
  },

  logout() {
    TokenService.removeAccessToken();
    TokenService.removeRefreshToken();
    TokenService.removeIsAdmin();
    TokenService.removeDefaultPassword();
    ApiService.removeHeader();
    ApiService.unmount401interceptor();
  }
};

export default UserService
export { UserService, AuthenticationError }
