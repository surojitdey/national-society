<template>
  <div class="users px-5">
    <v-row class="py-5" justify="end">
      <v-col cols="12" class="d-flex justify-end">
        <v-text-field v-model="searchQuery" rounded dense color="#FFA500" label="Search" outlined append-icon="mdi-magnify" single-line hide-details></v-text-field>
      </v-col>
    </v-row>
    <v-card elevation="1">
      <v-row justify="center">
        <v-col cols="2" class="d-flex justify-center">
          <span class="header-text font-weight-bold text-capitalize">full name</span>
        </v-col>
        <v-divider vertical inset class="small-off my-3"></v-divider>
        <v-col cols="2" class="d-flex justify-center">
          <span class="header-text font-weight-bold text-capitalize">Registered Date</span>
        </v-col>
        <v-divider vertical inset class="small-off my-3"></v-divider>
        <v-col cols="2" class="d-flex justify-center">
          <span class="header-text font-weight-bold text-capitalize">contact</span>
        </v-col>
        <v-divider vertical inset class="small-off my-3"></v-divider>
        <v-col cols="1" class="d-flex justify-center">
          <span class="header-text font-weight-bold text-capitalize">stories</span>
        </v-col>
        <v-divider vertical inset class="small-off my-3"></v-divider>
        <v-col cols="4" class="d-flex justify-center">
          <span class="header-text font-weight-bold text-capitalize">action</span>
        </v-col>
      </v-row>
    </v-card>
    <v-card color="#F5F5F5" elevation="1" class="my-6" v-for="(user, index) in currentPageUsers" :key="index">
      <v-row justify="center">
        <v-col cols="2" class="d-flex justify-center">
          <span class="header-text text-capitalize">{{user.full_name}}</span>
        </v-col>
        <v-divider vertical inset class="small-off my-3"></v-divider>
        <v-col cols="2" class="d-flex justify-center">
          <span class="header-text text-capitalize">{{new Date(user.date_joined).toDateString()}}</span>
        </v-col>
        <v-divider vertical inset class="small-off my-3"></v-divider>
        <v-col cols="2" class="d-flex justify-center">
          <span class="header-text text-capitalize">{{user.mobile_number}}</span>
        </v-col>
        <v-divider vertical inset class="small-off my-3"></v-divider>
        <v-col cols="1" class="d-flex justify-center">
          <span class="header-text text-capitalize">{{user.post_user_id.length}}</span>
        </v-col>
        <v-divider vertical inset class="small-off my-3"></v-divider>
        <v-col cols="4" class="d-flex justify-center">
          <v-row justify="center">
            <v-col cols="5" v-if="user.is_active" class="d-flex justify-center">
              <v-btn color="" width="100%" small class="rounded red--text" @click="updateUserStatusProperty('deactive', user.id)">Deactivate</v-btn>
            </v-col>
            <v-col cols="5" v-else class="d-flex justify-center">
              <v-btn right width="100%" small class="rounded green--text" @click="updateUserStatusProperty('active', user.id)">
                Approve
              </v-btn>
            </v-col>
            <v-col cols="4" class="d-flex justify-center">
              <router-link :to="{name: 'User', params: {id: user.id}}" tag="span" class="clickable">
                <v-btn small width="100%" class="rounded">Details</v-btn>
              </router-link>
            </v-col>
            <v-col cols="3" class="d-flex justify-center">
              <v-btn right width="" small class="rounded green--text" @click="sendMessageToUser(user)">
                Send
              </v-btn>
            </v-col>
          </v-row>
        </v-col>
      </v-row>
    </v-card>
    <v-row justify="center" align="center">
      <v-pagination
        v-model="page"
        :length="(this.userPerPage!=null)?Math.ceil(filteredUser.length/userPerPage):1"
        :total-visible="7"
        color="project_primary"
      ></v-pagination>
      <v-col cols="1">
        <v-select
          v-model="userPerPage"
          :items="userItemsPerPage"
          item-text="text"
          item-value="value"
        ></v-select>
      </v-col>
    </v-row>
    <v-dialog v-model="showMessageBox" width="50%" persistent>
      <MessageBox
        :user="selectedUser"
        @cancel-message="closeMessageBox"
      ></MessageBox>
    </v-dialog>
  </div>
</template>
<script>
import {mapGetters, mapActions, mapMutations} from 'vuex'
import MessageBox from '@/components/MessageBox'
export default {
  title: () => ('Resident Settings'),
  metaInfo: {
    title: 'Resident Settings'
  },
  components: {
    MessageBox
  },
  data: () => ({
    overlay: true,
    searchQuery: '',
    showMessageBox: false,
    selectedUser: {},
    page: 1,
    userPerPage: 5,
    userItemsPerPage: [
      {
        text: '5',
        value: 5
      },
      {
        text: '10',
        value: 10
      },
      {
        text: '15',
        value: 15
      },
      {
        text: '20',
        value: 20
      },
      {
        text: '100',
        value: 100
      },
      {
        text: 'All',
        value: null
      },
    ]
  }),
  computed: {
    ...mapGetters('user', {
      users: 'getUsers'
    }),
    filteredUser() {
      if(this.searchQuery) {
        return this.users.filter((user) => {
          return user.full_name.toLowerCase().startsWith(this.searchQuery.toLowerCase()) || user.mobile_number.toLowerCase().startsWith(this.searchQuery.toLowerCase()) || user.address.toLowerCase().startsWith(this.searchQuery.toLowerCase())
        })
      } else {
        return this.users
      }
    },
    currentPageUsers() {
      return (this.userPerPage!=null) ? this.filteredUser.slice((this.page-1)*this.userPerPage,(this.page-1)*this.userPerPage+this.userPerPage): this.filteredUser
    }
  },
  methods: {
    ...mapActions('user', [
      'fetchUsers',
      'updateStatus'
    ]),
    ...mapMutations('user', [
      'setUserStatusProperty'
    ]),
    updateUserStatusProperty(status, user_id) {
      this.setUserStatusProperty({
        status,
        user_id
      })
      this.updateStatus()
    },
    sendMessageToUser(user) {
      this.selectedUser = user
      this.showMessageBox = true
    },
    closeMessageBox() {
      this.selectedUser = {}
      this.showMessageBox = false
    }
  },
  mounted() {
    this.overlay = true
    this.fetchUsers().then(() => {
      this.overlay = false
    })
  }
}
</script>
<style scoped>

</style>
