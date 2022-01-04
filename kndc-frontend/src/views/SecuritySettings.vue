<template>
  <div class="security-settings px-5">
    <v-row class="py-5" align="center" justify="end">
      <v-col cols="2" class="d-flex justify-start">
        <v-btn class="rounded-xl primary--text" plain @click="$router.push('/add-security')">
          <v-icon size="inherit" class="mx-1">mdi-plus</v-icon>Add Security
        </v-btn>
      </v-col>
      <v-col cols="3" class="d-flex justify-center">
        <v-btn class="rounded-xl primary--text" plain @click="setTime = true">Add Timings</v-btn>
      </v-col>
      <v-col cols="3" class="d-flex justify-center">
        <v-btn class="rounded-xl primary--text" plain @click="viewTime=true">View Security Timetable</v-btn>
      </v-col>
      <v-col cols="4" class="d-flex justify-end">
        <v-text-field v-model="searchQuery" rounded dense color="#FFA500" label="Search" outlined append-icon="mdi-magnify" single-line hide-details></v-text-field>
      </v-col>
    </v-row>
    <v-card elevation="1">
      <v-row justify="space-between" class="mx-0 px-0">
        <v-col cols="2" class="d-flex justify-center">
          <span class="header-text font-weight-bold text-capitalize">full name</span>
        </v-col>
        <v-divider vertical inset class="small-off my-3"></v-divider>
        <v-col cols="2" class="d-flex justify-center">
          <span class="header-text font-weight-bold text-capitalize">father name</span>
        </v-col>
        <v-divider vertical inset class="small-off my-3"></v-divider>
        <v-col cols="2" class="d-flex justify-center">
          <span class="header-text font-weight-bold text-capitalize">Joining Date</span>
        </v-col>
        <v-divider vertical inset class="small-off my-3"></v-divider>
        <v-col cols="1" class="d-flex justify-center">
          <span class="header-text font-weight-bold text-capitalize">contact</span>
        </v-col>
        <v-divider vertical inset class="small-off my-3"></v-divider>
        <v-col cols="4" class="d-flex justify-center">
          <span class="header-text font-weight-bold text-capitalize">action</span>
        </v-col>
      </v-row>
    </v-card>
    <v-card color="#F5F5F5" elevation="1" class="my-6" v-for="(security, index) in currentPageSecurities" :key="index">
      <v-row justify="space-between" class="mx-0 px-0">
        <v-col cols="2" class="d-flex justify-center">
          <span class="header-text text-capitalize">{{security.full_name}}</span>
        </v-col>
        <v-divider vertical inset class="small-off my-3"></v-divider>
        <v-col cols="2" class="d-flex justify-center">
          <span class="header-text text-capitalize">{{security.father_name}}</span>
        </v-col>
        <v-divider vertical inset class="small-off my-3"></v-divider>
        <v-col cols="2" class="d-flex justify-center">
          <span class="header-text text-capitalize">{{new Date(security.date_of_joining).toDateString()}}</span>
        </v-col>
        <v-divider vertical inset class="small-off my-3"></v-divider>
        <v-col cols="1" class="d-flex justify-center">
          <span class="header-text text-capitalize">{{security.mobile_number}}</span>
        </v-col>
        <v-divider vertical inset class="small-off my-3"></v-divider>
        <v-col cols="4" class="d-flex justify-center">
          <v-row justify="center">
            <v-col cols="4" v-if="security.status==='deactive'" class="d-flex justify-center">
              <v-btn
                width="100%"
                small
                class="rounded red--text"
                @click="deactivateStatus(security)"
                :disabled="disable"
              >Deactive</v-btn>
            </v-col>
            <v-col cols="4" v-else class="d-flex justify-center">
              <v-btn
                width="100%"
                small
                class="rounded green--text"
                @click="activateStatus(security)"
                :disabled="disable"
              >Active</v-btn>
            </v-col>
            <v-col cols="4" class="d-flex justify-center">
              <v-btn
                small
                width="100%"
                class="rounded"
                :disabled="disable"
                @click="editSecurityDetails(security)"
              >edit</v-btn>
            </v-col>
            <v-col cols="4" class="d-flex justify-center">
              <v-btn
                width=""
                small
                class="rounded black--text"
                :disabled="disable"
                @click="viewSecurityTimings(security)"
              >Timings</v-btn>
            </v-col>
          </v-row>
        </v-col>
      </v-row>
    </v-card>
    <v-row justify="center" align="center">
      <v-pagination
        v-model="page"
        :length="securityPerPage!=null ? Math.ceil(filteredSecurity.length/securityPerPage) : 1"
        :total-visible="7"
        color="project_primary"
      ></v-pagination>
      <v-col cols="1">
        <v-select
          v-model="securityPerPage"
          :items="securityItemsPerPage"
          item-text="text"
          item-value="value"
        ></v-select>
      </v-col>
    </v-row>
    <v-dialog v-model="setTime" width="80%">
      <SetTime @time_added="setTimeSuccess" @cancel-set-time="setTime=false"></SetTime>
    </v-dialog>
    <v-dialog v-model="viewTime" width="80%">
      <ViewTime :secutitiesTime="secutitiesTime" @time-updated="fetchSecuritiesTime" :allTime="viewTime"></ViewTime>
    </v-dialog>
    <v-dialog v-model="showSecurityTime" width="80%">
      <ViewTime :secutitiesTime="securityTime" :allTime="viewTime"></ViewTime>
    </v-dialog>
    <v-dialog v-model="editSecurity" width="80%">
      <EditSecurity
        @cancel-edit="closeEditDialog"
        @error-edit="errorEditDialog"
        :security="security"
      ></EditSecurity>
    </v-dialog>
    <v-dialog v-model="statusPopup" width="50%" persistent>
      <v-card>
        <v-card-title v-if="editSuccess" class="green--text">Security details updated successfully.</v-card-title>
        <v-card-title v-if="editError" class="error--text">Security details updated unsuccessful.</v-card-title>
        <v-card-title v-if="timeAdded" class="green--text">Security time added successfully.</v-card-title>
        <v-card-actions class="d-flex justify-end">
          <v-btn
            class="white--text text-uppercase"
            width="30%"
            color="#423D3D"
            @click="statusPopup=false"
          >Cancel</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>  
</template>
<script>
import { mapActions, mapGetters } from 'vuex'
import SetTime from '@/components/SetTime.vue'
import ViewTime from '@/components/ViewTime.vue'
import EditSecurity from '@/components/EditSecurity.vue'
export default {
  metaInfo: {
    title: 'Security Settings'
  },
  components: {
    SetTime,
    ViewTime,
    EditSecurity
  },
  data: () => ({
    searchQuery: '',
    disable: false,
    setTime: false,
    viewTime: false,
    editSecurity: false,
    statusPopup: false,
    editSuccess: false,
    editError: false,
    showSecurityTime: false,
    timeAdded: false,
    page: 1,
    securityPerPage: 5,
    securityItemsPerPage: [
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
    ...mapGetters('security', {
      securities: 'getSecurites',
      secutitiesTime: 'getSecuritesTime',
      security: 'getSecurity',
      securityTime: 'getSecurityTime'
    }),
    filteredSecurity() {
      if(this.searchQuery) {
        return this.securities.filter((security) => {
          return security.full_name.toLowerCase().startsWith(this.searchQuery.toLowerCase()) || security.mobile_number.toLowerCase().startsWith(this.searchQuery.toLowerCase()) || security.father_name.toLowerCase().startsWith(this.searchQuery.toLowerCase())
        })
      } else {
        return this.securities
      }
    },
    currentPageSecurities() {
      return this.securityPerPage!=null ? this.filteredSecurity.slice((this.page-1)*this.securityPerPage,(this.page-1)*this.securityPerPage+this.securityPerPage) : this.filteredSecurity
    }
  },
  methods: {
    ...mapActions('security', [
      'fetchSecurities',
      'fetchSecurity',
      'updateStatus',
      'fetchSecuritiesTime',
      'fetchSecurityTime'
    ]),
    deactivateStatus(security) {
      this.disable = true
      this.updateStatus({status: 'deactive',security_id: security.id}).then(() => {
        this.disable = false
      })
    },
    activateStatus(security) {
      this.disable = true
      this.updateStatus({status: 'active',security_id: security.id}).then(() => {
        this.disable = false
      })
    },
    formatDate(date) {
      if (!date) return null

      const [year, month, day] = date.split('-')
      return `${day}-${month}-${year}`
    },
    editSecurityDetails(security) {
      this.fetchSecurity({
        id: security.id
      }).then(()=> {
        this.editSecurity = true
      })
    },
    closeEditDialog() {
      this.editSecurity = false
      this.editError = false
      this.timeAdded = false
      this.editSuccess = true
      this.statusPopup = true
    },
    errorEditDialog() {
      this.editSecurity = false
      this.editSuccess = false
      this.timeAdded = false
      this.editError = true
      this.statusPopup = true
    },
    setTimeSuccess() {
      this.setTime = false
      this.editSecurity = false
      this.editSuccess = false
      this.editError = false
      this.timeAdded = true
      this.statusPopup = true
    },
    viewSecurityTimings(security) {
      this.fetchSecurityTime(security.id).then(()=>{
        this.showSecurityTime=true
      })
    }
  },
  mounted() {
    this.fetchSecurities()
    this.fetchSecuritiesTime()
  }
}
</script>
<style scoped>

</style>