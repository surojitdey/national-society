import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import vuetify from './plugins/vuetify'
import Vuelidate from 'vuelidate'
import ApiService from './services/api.service'
import { TokenService } from './services/token.service';
import titleMixin from '@/mixins/titleMixins.js'
import VueMeta from 'vue-meta'

Vue.mixin(titleMixin)
Vue.use(VueMeta, {
  refreshOnceOnNavigation: true
})
Vue.use(Vuelidate)
Vue.config.productionTip = false

Vue.prototype.$environment = process.env

ApiService.init(`${process.env.VUE_APP_PROTOCOL}://${process.env.VUE_APP_HOST}:${process.env.VUE_APP_PORT}`, router)

if (TokenService.getAccessToken()) {
  ApiService.setHeader();
  ApiService.mount401interceptor();
}

new Vue({
  router,
  store,
  vuetify,
  render: h => h(App)
}).$mount('#app')
