<template>
  <div class="account mt-2">
    <v-row justify="center account-content">
      <v-col cols="3" class="pr-1">
        <v-card class="mx-0" height="100%">
          <v-list nav class="pl-0">
            <v-list-item-group v-model="selectedListItem" color="primary">
              <v-list-item class="" v-for="(item, index) in profileList" :key="index" :disabled="item.disabled" :to="{path: '/account/'+item.path}">
                <v-list-item-icon>
                  <v-icon v-text="item.icon"></v-icon>
                </v-list-item-icon>
                <v-list-item-content>
                  <v-list-item-title v-text="item.text"></v-list-item-title>
                </v-list-item-content>
              </v-list-item>
            </v-list-item-group>
          </v-list>
        </v-card>
      </v-col>
      <v-col cols="9" class="px-0">
        <v-row v-if="showAlert && isDefaultPassword" no-gutters class="px-12 pt-2" justify="center">
          <v-card color="project_red">
            <v-btn
              class="float-right"
              fab
              text
              small
              color="project-primary"
              @click="showAlert=false"
            >
              <v-icon>
                mdi-close
              </v-icon>
            </v-btn>
            <v-row no-gutters align="center" justify="space-around">
              <v-col cols="1" class="d-flex justify-center">
                <v-icon class="ma-auto" size="50" color="white">mdi-alert</v-icon>
              </v-col>
              <v-col>
                <div class="pa-8">
                  <span class="white--text"> Note**:Please change the default password first or else you will be unable to take any actions in this account.</span>
                </div>
              </v-col>
            </v-row>
          </v-card>
        </v-row>
        <router-view></router-view>
      </v-col>
    </v-row>
  </div>
</template>
<script>
import { mapGetters, mapActions } from 'vuex'
export default {
  title: 'Account',
  metaInfo: {
    title: 'Account'
  },
  data: () => ({
    selectedListItem: 0,
    profileList: [
      {
        text: 'Profile',
        icon: 'mdi-account',
        disabled: false,
        path: 'profile'
      },
      {
        text: 'My Posts',
        icon: 'mdi-post',
        disabled: false,
        path: 'myposts'
      },
      {
        text: 'My Complaints',
        icon: 'mdi-notebook-edit-outline',
        disabled: false,
        path: 'mycomplains'
      },
      {
        text: 'Fees',
        icon: 'mdi-currency-inr',
        disabled: false,
        path: 'fees'
      },
      {
        text: 'Change Password',
        icon: 'mdi-lock',
        disabled: false,
        path: 'password'
      },
    ],
    showAlert: true
  }),
  computed: {
    ...mapGetters('JWT', {
      isAdmin: 'isAdmin',
      isDefaultPassword: 'isDefaultPassword'
    }),
    ...mapGetters('settings', {
      settings: 'getSettings'
    })
  },
  methods: {
    ...mapActions('settings', [
      'fetchSettings',
    ]),
  },
  created() {
    this.fetchSettings().then(() => {
      if(this.isAdmin) {
        this.profileList.shift()
        this.profileList.shift()
        this.profileList.shift()
        this.profileList.shift()
        this.profileList.unshift({
          'text': 'Settings',
          'icon': 'mdi-cog-outline',
          'disabled': this.isDefaultPassword,
          'path': 'settings'
        })
        this.profileList.unshift({
          'text': 'Fees',
          'icon': 'mdi-currency-inr',
          'disabled': this.isDefaultPassword,
          'path': 'fees-settings'
        })
        if(this.settings.enable_news) {
          this.profileList.unshift({
            'text': 'News',
            'icon': 'mdi-information-outline',
            'disabled': this.isDefaultPassword || !this.settings.enable_news,
            'path': 'news'
          })
        }
        if(this.settings.enable_events) {
          this.profileList.unshift({
            'text': 'Events',
            'icon': 'mdi-calendar-today',
            'disabled': this.isDefaultPassword || !this.settings.enable_events,
            'path': 'events'
          })
        }
        this.profileList.unshift({
          'text': 'Complaints',
          'icon': 'mdi-notebook-edit-outline',
          'disabled': this.isDefaultPassword,
          'path': 'complains'
        })
        if(this.settings.enable_posts) {
          this.profileList.unshift({
            'text': 'Posts',
            'icon': 'mdi-post',
            'disabled': this.isDefaultPassword || !this.settings.enable_posts,
            'path': 'posts'
          })
        }
        this.profileList.unshift({
          'text': 'Securities',
          'icon': 'mdi-security',
          'disabled': this.isDefaultPassword,
          'path': 'security-setting'
        })
        this.profileList.unshift({
          'text': 'Residents',
          'icon': 'mdi-account-check',
          'disabled': this.isDefaultPassword,
          'path': 'residents'
        })
      } else {
        if(!this.settings.enable_posts) {
          this.profileList = this.profileList.filter((value)=>{
              return value.path !== 'myposts'
          })
        }
      }
    })
  }
}
</script>
<style scoped>
.account {
  padding-top: 64px !important;
}
.theme--light.v-list-item--active:hover::before, .theme--light.v-list-item--active::before {
    opacity: 1;
}
.v-list-item:before {
    border-radius: 0px 35.5px 35.5px 0px;
}
.v-list-item--link:before {
    background-color: #DBCFC5;
    bottom: 0;
    content: "";
    left: 0;
    opacity: 0;
    pointer-events: none;
    position: absolute;
    top: 10px;
    width: 40px;
    height: 60%;
    transition: 0.3s cubic-bezier(0.25, 0.8, 0.5, 1);
}
.account-content {
  min-height: inherit !important;
}
</style>
