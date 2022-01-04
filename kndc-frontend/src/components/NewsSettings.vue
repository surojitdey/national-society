<template>
  <v-container class="informations pa-0 ma-0">
    <v-row class="py-5" justify="center" align="center">
      <v-col cols="5" sm="5" md="6" xl="7" class="d-flex justify-end">
        <v-text-field rounded color="#FFA500" v-model="searchQuery" dense label="Search" outlined append-icon="mdi-magnify" single-line hide-details></v-text-field>
      </v-col>
      <v-col cols="6" sm="6" md="5" xl="4" class="d-flex justify-end">
        <v-btn v-if="isAdmin" class="mr-3 white--text rounded" color="project_primary" @click="$router.push('/addinformation')">
          <v-icon class="mx-1">mdi-plus</v-icon>Add New Information/News
        </v-btn>
      </v-col>
    </v-row>
    <v-row align="center" justify="center" class="mb-6">
      <v-col cols="11">
        <v-card class="py-4" elevation="0" v-for="(info, index) in filteredInformations" :key="index">
          <v-row align="end" class="mx-0">
            <v-btn small class="mr-2 my-2 project_primary--text rounded" @click="editData(info)" :disabled="disabledButtons">
              Edit
              <v-icon right>mdi-pencil-outline</v-icon>
            </v-btn>
            <v-btn small class="ml-2 my-2 red--text rounded" @click="deleteSelectedInformation(info)" :disabled="disabledButtons">
              Delete
              <v-icon right>mdi-delete-outline</v-icon>
            </v-btn>
          </v-row>
          <v-row class="pr-3" align="start" justify="space-between">
            <v-col cols="3" v-if="info.thumbnail || info.media_file">
              <v-card max-width="236" elevation="4" class="rounded-lg">
                <v-img class="align-end" height="211" v-if="info.thumbnail" :src="info.thumbnail"></v-img>
                <v-img class="align-end" height="211" v-else :src="info.media_file"></v-img>
              </v-card>
            </v-col>
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
        </v-card>
      </v-col>
    </v-row>
    <!-- <v-overlay :value="overlay">
      <v-progress-circular indeterminate color="white" width="5"></v-progress-circular>
    </v-overlay> -->
    <v-dialog v-model="editInformation" width="70%" persistent>
      <EditNews @cancel-edit="editInformation=false"></EditNews>
    </v-dialog>
    <v-dialog v-model="deleteDialog" width="600" persistent>
      <v-card>
        <v-container>
          <v-row>
            <v-col cols="12">
              <v-card-title>Do you really want to delete this post?</v-card-title>
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
  </v-container>
</template>
<script>
import { mapGetters, mapActions, mapMutations } from 'vuex'
import EditNews from '@/components/EditNews.vue'
export default {
  title: () => ('News Settings'),
  metaInfo: {
    title: 'News Settings for Kamakhya Nagar Development Committee'
  },
  components: {
    EditNews
  },
  data: () => ({
    showMore: false,
    linkText: 'more',
    searchQuery: '',
    overlay: false,
    editInformation: false,
    deleteDialog: false,
    disabledButtons: false,
  }),
  computed: {
    ...mapGetters('JWT', {
      isAdmin: 'isAdmin'
    }),
    ...mapGetters('event', {
      informations: 'getInformations',
      info: 'getInformation'
    }),
    filteredInformations() {
      if(this.searchQuery) {
        return this.informations.filter((info) => {
          return this.searchQuery.toLowerCase().split(' ').every((search) => {
            return info.title.toLowerCase().includes(search) || info.description.toLowerCase().includes(search)
          })
        })
      } else {
        return this.informations
      }
    }
  },
  methods: {
    ...mapActions('event', [
      'fetchInformations',
      'deleteInfomarion'
    ]),
    ...mapMutations('event', [
      'setInformation',
      'setInformationProperty'
    ]),
    moreLess() {
      this.showMore = !this.showMore
      if(this.showMore) {
        this.linkText = 'less'
      } else {
        this.linkText = 'more'
      }
    },
    editData(info) {
      this.setInformation(info)
      this.editInformation = true
    },
    confirmDelete() {
      this.deleteInfomarion({event_id: this.selectedInformation.id}).then(() => {
        this.fetchInformations()
        this.deleteDialog = false
        this.disabledButtons = false
      })
    },
    cancelDelete() {
      this.deleteDialog = false
      this.disabledButtons = false
    },
    deleteSelectedInformation(event) {
      this.selectedInformation = event
      this.deleteDialog = true
      this.disabledButtons = true
    }
  },
  mounted() {
    this.overlay = true
    this.fetchInformations().then(() => {
      this.overlay = false
    })
  }
}
</script>
<style scoped>
.information-buttons {
  position: relative;
  margin: auto;
}
.text-card {
  overflow-y: scroll;
  padding: 0;
}
.row + .row {
  margin-top: 0;
}
</style>
