<template>
  <div class="complains">
    <v-row align="center" justify="center">
      <v-col cols="11">
        <v-row class="py-5" justify="end">
          <v-col cols="12">
            <v-text-field v-model="searchQuery" color="#FFA500" rounded dense label="Search" outlined append-icon="mdi-magnify" single-line hide-details></v-text-field>
          </v-col>
        </v-row>
        <v-card class="mb-6" elevation="0" v-for="(complaint, index) in filteredComplaints" :key="index">
          <v-row class="mx-0" align="end">
            <!-- <v-col cols="2"> -->
              <router-link :to="{name: 'User', params: {id: complaint.user}}" tag="span" class="clickable">
                <v-btn small class="mr-2 my-2 rounded">User Details</v-btn>
              </router-link>
              <v-btn color="" v-if="(complaint.status=='new' || complaint.status=='rejected') && (complaint.solution_status!='solved')" :disabled="disabledButtons" @click="updateComplaintStatusProperty('approved', complaint.id)" small class="mx-2 my-2 green--text rounded">Approve</v-btn>
              <v-btn color="" v-if="(complaint.status=='new' || complaint.status=='approved') && (complaint.solution_status!='solved')" :disabled="disabledButtons" @click="updateComplaintStatusProperty('rejected', complaint.id)" small class="mx-2 my-2 red--text rounded">Reject</v-btn>
              <v-btn color="" v-if="complaint.solution_status=='unsolved'" :disabled="disabledButtons" @click="closeComplaint(complaint)" small class="mx-2 my-2 green--text rounded">Close</v-btn>
              <v-btn color="" v-if="complaint.solution_status=='solved'" :disabled="disabledButtons" @click="updateComplaintSolutionStatusProperty('unsolved', complaint.id)" small class="mx-2 my-2 green--text rounded">Open</v-btn>
              <v-btn color="" :disabled="disabledButtons" @click="deletePost(complaint)" small class="mx-2 my-2 red--text rounded">Delete</v-btn>
            <!-- </v-col> -->
          </v-row>
          <v-row align="center" justify="center">
            <v-col v-if="complaint.title || complaint.description">
              <v-card height="211" elevation="4" class="rounded-lg text-card">
                <v-row class="ma-0 pa-4">
                  <v-card-title v-text="complaint.title" class="text-h5 pa-0 text-capitalize font-weight-bold text-justify"></v-card-title>
                  <v-card-text v-text="complaint.description" v-if="complaint.description.length<200 || showMore" class="text-subtitle-1 px-0 py-2 text-justify"></v-card-text>
                  <v-card-text v-text="complaint.description.slice(0, 200)" v-else class="text-subtitle-1 px-0 py-2 text-justify"></v-card-text>
                  <a v-if="complaint.description.length>200" @click="moreLess">{{linkText}}</a>
                </v-row>
              </v-card>
            </v-col>
          </v-row>
        </v-card>
      </v-col>
    </v-row>
    <v-dialog v-model="showDialog" width="600" persistent>
      <v-card>
        <v-card-title>Do you want to close this complaint?</v-card-title>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn small class="green--text" @click="confirmClose">Yes</v-btn>
          <v-btn small class="red--text" @click="cancelClose">No</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
    <v-dialog v-model="deleteDialog" width="600" persistent>
      <v-card>
        <v-container>
          <v-row>
            <v-col cols="12">
              <v-card-title>Do you really want to delete this complaint?</v-card-title>
            </v-col>
            <v-col cols="12">
              <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn class="green--text" @click="confirmDelete">Yes</v-btn>
                <v-btn class="red--text" @click="cancelDelete">No</v-btn>
              </v-card-actions>
            </v-col>
          </v-row>
        </v-container>
      </v-card>
    </v-dialog>
    <!-- <v-overlay :value="overlay">
      <v-progress-circular indeterminate color="white" width="5"></v-progress-circular>
    </v-overlay> -->
  </div>
</template>
<script>
import { mapGetters, mapActions, mapMutations } from 'vuex'
export default {
  title() {
    return `Complaint Settings`
  },
  metaInfo: {
    title: 'Complaint Settings'
  },
  data: () => ({
    showMore: false,
    linkText: 'more',
    disabledButtons: false,
    showDialog: false,
    deleteDialog: false,
    editComplaintId: new Number(),
    overlay: false,
    searchQuery: ''
  }),
  computed: {
    ...mapGetters('user', {
      complaints: 'getComplaints'
    }),
    filteredComplaints() {
      if(this.searchQuery) {
        return this.complaints.filter((complaint) => {
          return this.searchQuery.toLowerCase().split(' ').every((search) => {
            return complaint.title.toLowerCase().includes(search) || complaint.description.toLowerCase().includes(search)
          })
        })
      } else {
        return this.complaints
      }
    }
  },
  methods: {
    ...mapActions('user', [
      'fetchAllComplaintsAndGrievances',
      'updateComplaintsAndGrievancesStatus',
      'updateComplaintsAndGrievancesSolutionStatus',
      'deleteComplaintsAndGrievances'
    ]),
    ...mapMutations('user', [
      'setComplaintStatusProperty',
      'setComplaintSolutionStatusProperty'
    ]),
    moreLess() {
      this.showMore = !this.showMore
      if(this.showMore) {
        this.linkText = 'less'
      } else {
        this.linkText = 'more'
      }
    },
    updateComplaintStatusProperty(status, id) {
      this.disabledButtons = true
      this.setComplaintStatusProperty({
        status,
        id
      })
      this.updateComplaintsAndGrievancesStatus().then(() => {
        this.fetchAllComplaintsAndGrievances()
        this.disabledButtons = false
      })
    },
    updateComplaintSolutionStatusProperty(status, id) {
      this.setComplaintSolutionStatusProperty({
        status,
        id
      })
      this.updateComplaintsAndGrievancesSolutionStatus().then(() => {
        this.fetchAllComplaintsAndGrievances()
        this.showDialog = false
        this.disabledButtons = false
      })
    },
    deleteComplaint(id) {
      this.deleteComplaintsAndGrievances(id)
      .then(() => { 
        this.fetchAllComplaintsAndGrievances()
      })
    },
    deletePost(post) {
      this.editComplaintId = post.id
      this.deleteDialog = true
      this.disabledButtons = true
    },
    cancelDelete() {
      this.editComplaintId = new Number()
      this.deleteDialog = false
    },
    confirmDelete() {
      this.deleteComplaintsAndGrievances(this.editComplaintId).then(() => {
        this.fetchAllComplaintsAndGrievances()
        this.deleteDialog = false
        this.disabledButtons = false
      })
    },
    closeComplaint(complaint) {
      this.editComplaintId = complaint.id
      this.showDialog = true
      this.disabledButtons = true
    },
    cancelClose() {
      this.editComplaintId = new Number()
      this.showDialog = false
    },
    confirmClose() {
      this.updateComplaintSolutionStatusProperty('solved', this.editComplaintId)
    }
  },
  mounted() {
    this.overlay = true
    this.fetchAllComplaintsAndGrievances().then(() => {
      this.overlay = false
    })
  }
}
</script>
<style scoped>
.text-card {
  overflow-y: scroll;
  padding: 0;
}
.row + .row {
  margin-top: 0 !important;
}
</style>
