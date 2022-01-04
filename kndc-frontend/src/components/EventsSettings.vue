<template>
  <v-container class="events pa-0 ma-0">
    <v-row class="py-5" align="center" justify="center">
      <v-col cols="6" sm="7" md="8" class="d-flex justify-end">
        <v-text-field rounded color="#FFA500" v-model="searchQuery" dense label="Search" outlined append-icon="mdi-magnify" single-line hide-details></v-text-field>
      </v-col>
      <v-col cols="5" sm="4" md="3" class="d-flex justify-end">
        <v-btn class="mr-3 rounded white--text" v-if="isAdmin" color="project_primary" @click="$router.push('/addevent')">
          <v-icon class="mx-1">mdi-plus</v-icon>Add New Event
        </v-btn>
      </v-col>
    </v-row>
    <v-row align="center" justify="center" class="mb-6">
      <v-col cols="11" class="">
        <v-card class="py-4" elevation="0" v-for="(info, index) in filteredEvents" :key="index">
          <v-row align="end" class="mx-0">
            <v-btn small class="mr-2 project_primary--text rounded" @click="editData(info)" :disabled="disabledButtons">
              Edit
              <v-icon right>mdi-pencil-outline</v-icon>
            </v-btn>
            <v-btn small class="ml-2 red--text rounded" @click="deleteSelectedEvent(info)" :disabled="disabledButtons">
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

    <v-dialog v-model="editEvent" width="70%" persistent>
      <EditEvent 
        :eventData="selectedEvent"
        :title="selectedEventTitle"
        :event_date="selectedEventDate"
        :event_time="selectedEventTime"
        :time_convention="selectedEventConvention"
        :description="selectedEventDescription"
        :imageUrl="selectedEvent.media_file"
        @title-changed="selectedEventTitle=$event"
        @description-changed="selectedEventDescription=$event"
        @date-changed="selectedEventDate=$event"
        @time-changed="selectedEventTime=$event"
        @convention-changed="selectedEventConvention=$event"
        @imageUrl-changed="selectedEvent.media_file=$event"
        @cancel-edit="editEvent=false"
      ></EditEvent>
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
import { mapGetters, mapActions } from 'vuex'
import EditEvent from '@/components/EditEvent.vue'
export default {
  title() {
    return `Event Settings`
  },
  metaInfo: {
    title: 'Event Settings'
  },
  components: {
    EditEvent
  },
  data: () => ({
    showMore: false,
    linkText: 'more',
    searchQuery: '',
    overlay: false,
    editEvent: false,
    selectedEvent: {},
    selectedEventTitle: '',
    selectedEventDate: '',
    selectedEventTime: '',
    selectedEventConvention: '',
    selectedEventDescription: '',
    deleteDialog: false,
    disabledButtons: false
  }),
  computed: {
    ...mapGetters('JWT', {
      isAdmin: 'isAdmin'
    }),
    ...mapGetters('event', {
      events: 'getEvents'
    }),
    filteredEvents() {
      if(this.searchQuery) {
        return this.events.filter((event) => {
          return this.searchQuery.toLowerCase().split(' ').every((search) => {
            return event.title.toLowerCase().includes(search) || event.description.toLowerCase().includes(search)
          })
        })
      } else {
        return this.events
      }
    }
  },
  methods: {
    ...mapActions('event', [
      'fetchEvents',
      'deleteEvents'
    ]),
    moreLess() {
      this.showMore = !this.showMore
      if(this.showMore) {
        this.linkText = 'less'
      } else {
        this.linkText = 'more'
      }
    },
    editData(event) {
      this.selectedEvent = event
      this.selectedEventTitle = event.title
      this.selectedEventDate = event.event_date
      this.selectedEventTime = event.event_time
      this.selectedEventDescription = event.description
      this.selectedEventConvention = event.time_convention
      this.editEvent = true
    },
    confirmDelete() {
      this.deleteEvents({event_id: this.selectedEvent.id}).then(() => {
        this.fetchEvents()
        this.deleteDialog = false
        this.disabledButtons = false
      })
    },
    cancelDelete() {
      this.deleteDialog = false
      this.disabledButtons = false
    },
    deleteSelectedEvent(event) {
      this.selectedEvent = event
      this.deleteDialog = true
      this.disabledButtons = true
    }
  },
  mounted() {
    this.overlay = true
    this.fetchEvents().then(() => {
      this.overlay = false
    })
  }
}
</script>
<style scoped>
.event-buttons {
  position: relative;
  margin: auto;
}
.text-card {
  overflow-y: scroll;
  padding: 0;
}
</style>
