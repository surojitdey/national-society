<template>
  <div class="complaints-notification">
    <v-row align="center" justify="center">
      <v-col cols="11">
        <v-card class="my-6" elevation="0" v-for="(info, index) in currentPageComplaints" :key="index">
          <v-container>
            <v-row class="mx-0" align="center">
              <v-chip outlined label :color="info.status=='rejected'? 'red': info.status=='new'?'warning':'green'" v-if="info.solution_status=='unsolved'" class="rounded my-2 text-uppercase subtitle-1">{{info.status == 'new'? 'pending': info.status}}</v-chip>
              <v-chip outlined label color="green" v-if="info.solution_status=='solved'" class="rounded my-2 text-uppercase subtitle-1">closed</v-chip>
              <v-btn color="primary" text dense fab small @click="editComplaint(info)">
                <v-icon>mdi-pencil-outline</v-icon>
              </v-btn>
              <v-btn color="red" text dense fab small @click="deletePost(info)">
                <v-icon>mdi-delete-outline</v-icon>
              </v-btn>
            </v-row>
            <v-row align="center" justify="start">
              <v-col v-if="info.title || info.description">
                <v-card height="211" elevation="4" class="rounded-lg text-card">
                  <v-row class="ma-0 pa-4">
                    <v-card-title v-text="info.title" class="text-h5 pa-0 text-capitalize font-weight-bold text-justify"></v-card-title>
                    <v-card-text v-text="info.description" v-if="info.description.length<200 || showMore" class="text-subtitle-1 px-0 py-2 text-justify"></v-card-text>
                    <v-card-text v-text="info.description.slice(0, 200)" v-else class="text-subtitle-1 px-0 py-2 text-justify"></v-card-text>
                    <a v-if="info.description.length>200" @click="moreLess">{{linkText}}</a>
                  </v-row>
                </v-card>
              </v-col>
            </v-row>
            
          </v-container>
        </v-card>
        <v-row justify="center" align="center">
          <v-pagination
            v-model="page"
            :length="complaintPerPage!=null ? Math.ceil(complaints.length/complaintPerPage) : 1"
            :total-visible="7"
            color="project_primary"
          ></v-pagination>
          <v-col cols="1">
            <v-select
              v-model="complaintPerPage"
              :items="complaintItemsPerPage"
              item-text="text"
              item-value="value"
            ></v-select>
          </v-col>
        </v-row>
      </v-col>
    </v-row>
    <v-dialog v-model="showEdit" width="700" persistent>
      <EditComplaint 
        :complaints_id="editedComplaintId"
        :title="editedTitle"
        :description="editedDescription"
        @cancel-edit="showEdit=false"
        @title-changed="editedTitle=$event"
        @description-changed="editedDescription=$event">
      </EditComplaint>
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
  </div>  
</template>
<script>
import EditComplaint from '@/components/EditComplaint.vue'
import { mapActions, mapGetters, mapMutations } from 'vuex'
export default {
  title: () => ('My Complaints'),
  metaInfo: {
    title: 'Residents Complaints'
  },
  components: {
    EditComplaint
  },
  data: () => ({
    showMore: false,
    linkText: 'more',
    disabledButtons: false,
    showEdit: false,
    editedComplaintId: new Number(),
    editedTitle: '',
    editedDescription: '',
    deleteDialog: false,
    deleteComplaintId: new Number(),
    overlay: false,
    page: 1,
    complaintPerPage: 5,
    complaintItemsPerPage: [
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
    ...mapGetters('user',{
      complaints: 'getComplaints'
    }),
    currentPageComplaints() {
      return this.complaintPerPage!=null ? this.complaints.slice((this.page-1)*this.complaintPerPage,(this.page-1)*this.complaintPerPage+this.complaintPerPage) : this.complaints
    }
  },
  methods: {
    ...mapActions('user', [
      'fetchUserComplaintsAndGrievances',
      'deleteComplaintsAndGrievances'
    ]),
    ...mapMutations('user', [
      ''
    ]),
    moreLess() {
      this.showMore = !this.showMore
      if(this.showMore) {
        this.linkText = 'less'
      } else {
        this.linkText = 'more'
      }
    },
    editComplaint(post) {
      this.editedComplaintId = post.id
      this.editedTitle = post.title
      this.editedDescription = post.description
      this.showEdit = true
    },
    deletePost(post) {
      this.deleteComplaintId = post.id
      this.deleteDialog = true
    },
    cancelDelete() {
      this.deleteComplaintId = new Number()
      this.deleteDialog = false
    },
    confirmDelete() {
      this.deleteComplaintsAndGrievances(this.deleteComplaintId).then(() => {
        this.fetchUserComplaintsAndGrievances()
        this.deleteDialog = false
      })
    }
  },
  mounted() {
    this.overlay = true
    this.fetchUserComplaintsAndGrievances().then(() => {
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
</style>
