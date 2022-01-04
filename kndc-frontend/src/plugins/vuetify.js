import Vue from 'vue';
import Vuetify from 'vuetify/lib/framework';
import '@mdi/font/css/materialdesignicons.css'
import '@/styles/global_variables.sass'

Vue.use(Vuetify);

const options = {
  theme: {
    themes: {
      light: { 
        project_primary: '#434D3D',
        project_red: '#88394A',
        red: '#C60021',
        green: '#438945'
      },
    },
  },
}

export default new Vuetify({
  icons: {
    iconfont: 'mdi', // default - only for display purposes
  },
  ...options
});
