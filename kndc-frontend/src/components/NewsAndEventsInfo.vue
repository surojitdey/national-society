<template>
  <div class="news-and-events-info">
    <v-row justify="center" class="ma-0">
      <v-col cols="12" class="pa-0">
        <v-card elevation="0" class="my-5">
          <v-card-title class="text-capitalize px-0">latest news</v-card-title>
          <v-card class="my-2" v-for="(info, index) in news" :key="index" @click="newsClicked(info)">
            <v-row justify="space-between" class="ma-0 pa-0">
              <v-col cols="3" class="px-0 py-0" v-if="info.media_file || info.thumbnail">
                <v-img class="align-end" width="80" v-if="info.thumbnail" height="80" :src="info.thumbnail"></v-img>
                <v-img class="align-end" width="80" v-else height="80" :src="info.media_file"></v-img>
              </v-col>
              <v-col cols="9" class="px-0 py-0">
                <v-card-text class="py-0" v-text="info.title"></v-card-text>
              </v-col>
            </v-row>
          </v-card>
          <v-card-actions v-if="limitedNews" class="px-0">
            <v-btn
              class="text-capitalize mx-auto rounded"
              color="black"
              outlined
              @click="getAllNews"
            >see more</v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>
    <v-row justify="center" class="ma-0">
      <v-col cols="12" class="pa-0">
        <v-card elevation="0" class="my-5">
          <v-card-title class="text-capitalize px-0">recent events</v-card-title>
          <v-card v-for="(event, index) in events" :key="index" @click="eventSelected(info)">
            <v-row justify="space-between" class="ma-0 pa-0">
              <v-col cols="3" class="px-0 py-0" v-if="event.media_file || event.thumbnail">
                <v-img class="align-end" width="80" v-if="event.thumbnail" height="80" :src="event.thumbnail"></v-img>
                <v-img class="align-end" width="80" v-else height="80" :src="event.media_file"></v-img>
              </v-col>
              <v-col cols="9" class="px-0 py-0">
                <v-card-subtitle class="py-0" v-text="`${formatDate(event.event_date)} ${event.event_time} ${event.time_convention}`"></v-card-subtitle>
                <v-card-text class="py-0" v-text="event.title"></v-card-text>
              </v-col>
            </v-row>
          </v-card>
          <v-card-actions v-if="limitedEvents" class="px-0">
            <v-btn
              class="text-capitalize mx-auto rounded"
              color="black"
              outlined
              @click="getAllEvents"
            >see more</v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>
  </div>
</template>
<script>
import { mapGetters, mapActions, mapMutations } from 'vuex'
export default {
  // props: [
  //   'news',
  //   'limitedNews',
  //   'events',
  //   'limitedEvents'
  // ],
  data: () => ({
    limitedEvents: true,
    limitedNews: true
  }),
  computed: {
    ...mapGetters('event', {
      news: 'getInformations',
      events: 'getEvents'
    }),
  },
  methods: {
    ...mapActions('event', [
      'fetchInformations',
      'fetchLimitedInformations',
      'fetchEvents',
      'fetchLimitedEvents'
    ]),
    ...mapMutations('event', [
      'setEvent',
      'setInformation'
    ]),
    getAllEvents() {
      this.fetchEvents().then(()=> {
        this.limitedEvents = false
      }).catch(() => {
        this.limitedEvents = true
      })
    },
    getAllNews() {
      this.fetchInformations().then(() => {
        this.limitedNews = false
      }).catch(() => {
        this.limitedNews = true
      })
    },
    eventSelected(event) {
      this.setEvent(event)
      this.$router.push(`/event/${event.title}-${event.id}/`)
    },
    newsClicked(item) {
      this.setInformation(item)
      this.$router.push(`/news/${item.title}-${item.id}/`)
    }
  },
  mounted() {
    console.log('******')
    this.fetchLimitedInformations()
    this.fetchLimitedEvents()
  }
}
</script>
<script>
export default {
  
}
</script>
