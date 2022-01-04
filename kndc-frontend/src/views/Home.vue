<template>
  <div class="home">
    <Carousel></Carousel>
    <RecentNews
      v-if="settings.enable_news"
      :informations="informations"
      @load-all-news="loadAllNews"
      :loadComplete="allNews"
    ></RecentNews>
    <RelatedEvents
      v-if="settings.enable_events"
      :events="events"
      @load-all-events="loadAllEvents"
      :loadComplete="allEvents"
    ></RelatedEvents>
    <v-lazy
      :options="{
        threshold: 0.8
      }"
      min-height="200"
      transition="fade-transition"
      origin="center center"
    >
      <CommunityInfo
        v-if="settings.enable_posts"
        :CommunityData="CommunityData"
        :posts="posts" :events="events"
      ></CommunityInfo>
    </v-lazy>
  </div>
</template>

<script>
// @ is an alias to /src
import Carousel from '@/components/Carousel.vue'
import RecentNews from '@/components/RecentNews.vue'
import RelatedEvents from '@/components/RelatedEvents.vue'
import CommunityInfo from '@/components/CommunityInfo.vue'
import CommunityData from '@/data/community-info.json'
import { mapActions, mapGetters } from 'vuex'

export default {
  title: 'Kamakhya Nagar Development Committee',
  metaInfo: {
    title: 'Kamakhya Nagar Development Committee'
  },
  name: 'Home',
  components: {
    Carousel,
    RecentNews,
    RelatedEvents,
    CommunityInfo
  },
  data: () => ({
    CommunityData,
    overlay: false,
    allNews: false,
    allEvents: false
  }),
  computed: {
    ...mapGetters('user',{
      user: 'getUser',
      posts: 'getPosts'
    }),
    ...mapGetters('JWT',[
      'loggedIn',
      'access_token'
    ]),
    ...mapGetters('event', {
      events: 'getEvents',
      informations: 'getInformations'
    }),
    ...mapGetters('settings', {
      settings: 'getSettings'
    })
  },
  methods: {
    ...mapActions('user', [
      'fetchUser',
      'fetchPosts'
    ]),
    ...mapActions('event', [
      'fetchEvents',
      'fetchLimitedEvents',
      'fetchInformations',
      'fetchLimitedInformations'
    ]),
    loadAllNews() {
      this.fetchInformations().then(() => {
        this.allNews = true
      }).catch(() => {
        this.allNews = false
      })
    },
    loadAllEvents() {
      this.fetchEvents().then(() => {
        this.allEvents = true
      }).catch(() => {
        this.allEvents = false
      })
    },
  },
  mounted() {
    this.overlay = true
    if(this.loggedIn && this.access_token) {
      this.fetchUser()
    }
    this.fetchPosts()
    this.fetchLimitedEvents()
    this.fetchInformations()
  }
}
</script>

<style scoped>

</style>
