<template>
  <div class="complaints-and-grievances">
    <v-row justify="center">
      <v-card width="68%" class="my-15" elevation="0">
        <v-row justify="center" align="center">
          <v-col cols="5">
            <v-card-title class="px-0 text-h5 font-weight-bold text-uppercase">Complaints and Grievances</v-card-title>
          </v-col>
          <v-col cols="5" class="justify-end d-flex">
            <v-btn color="#434D3D" class="text-upperclass white--text rounded" v-if="!isAdmin" @click="addComplaintDialog=true">
              <v-icon class="mx-1">mdi-plus</v-icon>Add Complaints
            </v-btn>
          </v-col>
        </v-row>
        <v-row align="center" justify="center">
          <v-col cols="10">
            <v-card height="211" class="mb-6 rounded-lg text-card" v-for="(complaint, index) in currentPageComplaints" :key="index">
              <v-container>
                <v-chip color="green" v-if="complaint.solution_status=='solved'" outlined label class="mx-4 rounded text-uppercase subtitle-1">closed</v-chip>
                <v-row class="ma-0 pa-4">
                  <v-card-title v-text="complaint.title" class="text-h5 pa-0 text-capitalize font-weight-bold text-justify"></v-card-title>
                  <v-card-text v-text="complaint.description" v-if="complaint.description.length<200 || showMore" class="text-subtitle-1 px-0 py-2 text-justify"></v-card-text>
                  <v-card-text v-text="complaint.description.slice(0, 200)" v-else class="text-subtitle-1 px-0 py-2 text-justify"></v-card-text>
                  <a v-if="complaint.description.length>200" @click="moreLess">{{linkText}}</a>
                </v-row>
                <!-- <v-row align="end" class="mx-0 user-info">
                  <v-col cols="3" class="ma-0 pa-0">
                    <div class="mx-4 text-capitalize body-1 grey--text">{{complaint.full_name}}</div>
                  </v-col>
                  <v-col cols="3" class="ma-0 pa-0">
                    <div class="mx-4 caption grey--text">{{new Date(complaint.added).toDateString()}} {{new Date(complaint.added).getHours()}}:{{new Date(complaint.added).getMinutes()}}</div>
                  </v-col>
                </v-row> -->
              </v-container>
            </v-card>
            <v-card height="100" class=" mb-6 rounded-lg text-card" v-if="currentPageComplaints.length==0">
              <v-card-title>No data available</v-card-title>
            </v-card>
            <v-pagination
              v-model="page"
              :length="Math.ceil(complaints.length/complaintPerPage)"
              :total-visible="7"
              color="project_primary"
            ></v-pagination>
          </v-col>
        </v-row>
      </v-card>
    </v-row>
    <v-dialog
      transition="dialog-right-transition"
      max-width="700"
      persistent
      v-model="addComplaintDialog">
      <AddComplaints @cancel-add="addComplaintDialog=false"></AddComplaints>
    </v-dialog>
    <v-overlay :value="overlay">
      <v-progress-circular indeterminate color="white" width="5"></v-progress-circular>
    </v-overlay>
  </div>
</template>
<script>
import AddComplaints from '@/components/AddComplaints.vue'
import { mapGetters, mapActions } from 'vuex'
export default {
  title: 'Complaints and Grievances',
  metaInfo: {
    title: 'Complaints and Grievances for Kamakhya Nagar Development Committee'
  },
  components: {
    AddComplaints
  },
  data: () => ({
    addComplaintDialog: false,
    showMore: false,
    linkText: 'more',
    overlay: false,
    page: 1,
    complaintPerPage: 5
  }),
  computed: {
    ...mapGetters('user', {
      complaints: 'getComplaints'
    }),
    ...mapGetters('JWT', {
      isAdmin: 'isAdmin'
    }),
    ...mapGetters('settings', {
      settings: 'getSettings'
    }),
    currentPageComplaints() {
      return this.complaints.slice((this.page-1)*this.complaintPerPage,(this.page-1)*this.complaintPerPage+this.complaintPerPage)
    }
  },
  methods: {
    ...mapActions('user', [
      'fetchComplaintsAndGrievances',
      'fetchUserApprovedComplaintsAndGrievances',
    ]),
    ...mapActions('settings', [
      'fetchSettings',
    ]),
    moreLess() {
      this.showMore = !this.showMore
      if(this.showMore) {
        this.linkText = 'less'
      } else {
        this.linkText = 'more'
      }
    }
  },
  mounted() {
    this.overlay = true
    this.fetchSettings().then(() => {
      if(this.settings.show_complaints || this.isAdmin) {
        this.fetchComplaintsAndGrievances().then(() => {
          this.overlay = false
        })
      } else {
        this.fetchUserApprovedComplaintsAndGrievances().then(() => {
          this.overlay = false
        })
      }
    })
  }
}
</script>
<style scoped>
.complaints-and-grievances {
  padding-top: 64px !important;
}
.user-info {
  width: 100%;
}
.text-card {
  overflow-y: scroll;
  padding: 0;
}
.row + .row {
  margin-top: 0 !important;
}
</style>
