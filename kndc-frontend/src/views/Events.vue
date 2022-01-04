<template>
  <v-container class="events">
    <v-row align="center" justify="start" class="mt-4">
      <v-col cols="12">
        <v-text-field rounded color="#FFA500" v-model="searchQuery" label="Search" outlined append-icon="mdi-magnify" single-line hide-details></v-text-field>
      </v-col>
      <v-col cols="4" class="mb-3" v-for="(item, index) in filteredEvents" :key="index">
        <!-- <v-card max-width="414" elevation="0" color="transparent" class="events-card" @click="eventSelected(item)">
          <v-row justify="start">
            <v-col cols="12" class="py-0">
              <v-img v-if="item.thumbnail" class="image align-end" :src="item.thumbnail" height="295"></v-img>
              <v-img v-else-if="item.media_file!=''" class="image align-end" :src="item.media_file" height="295" contain></v-img>
            </v-col>
            <v-col cols="1" class="title-left-border my-3 ml-3 pr-0 mr-0"></v-col>
            <v-col cols="2" v-if="item.event_date" class="my-0 pl-0 ml-0">
              <v-card-title class="event-date pa-0 ma-0 text-capitalize">{{new Date(item.event_date).toLocaleString('en-us',{day:'numeric'})}}</v-card-title>
              <v-card-title class="event-month pa-0 ma-0 text-capitalize">{{new Date(item.event_date).toLocaleString('en-us',{month:'long'})}}</v-card-title>
            </v-col>
            <v-col cols="8" class="my-0 pl-0 ml-0">
              <v-card-title class="title py-0 px-0 my-0 text-capitalize">{{item.title}}</v-card-title>
            </v-col>
            <v-col cols="12" class="my-0">
              <v-card-subtitle class="py-0 px-0 my-0 description text-truncate text-justify">{{item.description}}</v-card-subtitle>
            </v-col>
          </v-row>
        </v-card> -->
        <EventCard
          @event-clicked="eventSelected($event)"
          :item="item"
          :imageHeight="295"
        ></EventCard>
      </v-col>
    </v-row>
  </v-container>
</template>
<script>
import { mapGetters, mapActions, mapMutations } from 'vuex'
import EventCard from '@/components/EventCard'
export default {
  title: 'Events',
  metaInfo: {
    title: 'Events of Kamakhya Nagar Development Committee'
  },
  components: {
    EventCard
  },
  data: () => ({
    showMore: false,
    linkText: 'more',
    searchQuery: '',
    overlay: false,
    loadComplete: false,
    loading: false
  }),
  computed: {
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
      'fetchLimitedEvents'
    ]),
    ...mapMutations('event', [
      'setEvent'
    ]),
    eventSelected(event) {
      this.setEvent(event)
      this.$router.push(`/event/${event.title}-${event.id}/`)
    },
    loadAllEvents() {
      this.loading = true
      this.fetchEvents().then(() => {
        this.loading = false
      })
    },
    moreLess() {
      this.showMore = !this.showMore
      if(this.showMore) {
        this.linkText = 'less'
      } else {
        this.linkText = 'more'
      }
    },
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
.events {
  padding-top: 64px !important;
}
.event-date {
  font-size: 33px !important;
}

.event-month {
  font-size: 14px !important;
}

.title-left-border {
  border-left: 5px solid #423D3D !important;
  max-width: 0px !important;
}

.title {
  font-size: 28px !important;
}

.title-line {
  border-color: #423D3D !important;
}

.description {
  font-size: 16px !important;
  line-height: 30px !important;
}
.read-more{
  padding: 0 80px;
}
.read-more-btn {
  font-size: 20px !important;
  color: #423D3D !important;
}
</style>
