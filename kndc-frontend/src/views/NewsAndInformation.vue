<template>
  <div class="news_information">
    <v-row align="center">
      <v-img :src="backgroundImage" class="align-end">
        <v-overlay :absolute="true" :value="true" color="transparent">
          <span class="upper-title text-uppercase display-2">News</span>
        </v-overlay>
      </v-img>
    </v-row>
    <v-row justify="space-between" class="card-content">
      <v-col cols="8">
        <v-card color="white" class="my-5" elevation="0" width="100%">
          <v-card-title v-text="information.title" class="text-capitalize px-0 content-title"></v-card-title>
          <v-img :src="information.media_file" max-height="372" class="align-end"></v-img>
          <v-card-text v-text="information.description" class="text-justify px-0"></v-card-text>
        </v-card>
      </v-col>
      <v-col cols="4">
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
                    <v-card-text class="py-0 info-title text-truncate" v-text="info.title"></v-card-text>
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
              <v-card class="my-2" v-for="(event, index) in events" :key="index" @click="eventSelected(event)">
                <v-row justify="space-between" class="ma-0 pa-0">
                  <v-col cols="3" class="px-0 py-0" v-if="event.media_file || event.thumbnail">
                    <v-img class="align-end" max-width="90" v-if="event.thumbnail" height="80" :src="event.thumbnail"></v-img>
                    <v-img class="align-end" max-width="90" v-else height="80" :src="event.media_file"></v-img>
                  </v-col>
                  <v-col cols="9" class="px-0 py-0">
                    <v-card-subtitle class="py-0 info-subtitle" v-text="`${formatDate(event.event_date)} ${event.event_time} ${event.time_convention}`"></v-card-subtitle>
                    <v-card-text class="py-0 info-title text-truncate" v-text="event.title"></v-card-text>
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
      </v-col>
    </v-row>
  </div>
</template>
<script>
import backgroundImage from '@/assets/background-image.png'
import { mapGetters, mapActions, mapMutations } from 'vuex'
export default {
  title() {
    return `News-${this.$route.params.news_id}`
  },
  metaInfo: {
    title: `News of Kamakhya Nagar Development Committee`
  },
  data: () => ({
    overlay: false,
    attrs: {
      class: 'mb-6',
      boilerplate: true,
      elevation: 2,
    },
    backgroundImage,
    limitedEvents: true,
    limitedNews: true
  }),
  computed: {
    ...mapGetters('event', {
      information: 'getInformation',
      news: 'getInformations',
      events: 'getEvents'
    }),
    news_id() {
      return this.$route.params.news_id.split('-')[this.$route.params.news_id.split('-').length - 1]
    }
  },
  methods: {
    ...mapActions('event', [
      'fetchInformationById',
      'fetchInformations',
      'fetchLimitedInformations',
      'fetchEvents',
      'fetchLimitedEvents'
    ]),
    ...mapMutations('event', [
      'setEvent',
      'setInformation'
    ]),
    formatDate (date) {
      if(!date) return null
      const [year, month, day] = date.split('-')
      return `${day}/${month}/${year}`
    },
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
      this.$router.push(`/event/${event.title.replace(/\s/g, '-')}-${event.id}/`)
    },
    newsClicked(item) {
      this.setInformation(item)
      this.$router.push(`/news/${item.title.replace(/\s/g, '-')}-${item.id}/`)
    }
  },
  mounted() {
    this.fetchInformationById(this.news_id)
    this.fetchLimitedEvents()
    this.fetchLimitedInformations()
  }
}
</script>
<style scoped>
.news_information {
  padding-top: 64px;
}
.upper-title {
  font-size: 45px !important;
}
.content-title {
  font-size: 32px !important;
  word-break: break-word;
}
.card-content {
  margin: auto;
  width: 70%;
}
</style>
<style scoped>
.info-title {
  font-size: 14px !important;
}
.info-subtitle {
  font-size: 12px !important;
}
</style>
