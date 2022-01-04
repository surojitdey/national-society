<template>
  <div class="related-events">
    <v-row class="related-events-title" align="center" justify="start">
      <v-col cols="4">
        <span class="heading-title text-capatilize">Related Events</span>
      </v-col>
      <v-divider class="title-line"></v-divider>
    </v-row>
    <v-row class="related-events-content" justify="start">
      <v-col cols="4" class="mb-3" v-for="(item, index) in events" :key="index">
        <EventCard
          @event-clicked="eventSelected($event)"
          :item="item"
          :imageHeight="200"
        ></EventCard>
      </v-col>
    </v-row>
    <v-row align="center" justify="end" v-if="!loadComplete" class="read-more">
      <v-btn
        text
        class="read-more-btn"
        @click="loadAllEvents"
        :disabled="loading"
        :loading="loading"
      >
        <span class="text-capitalize">read more</span>
        <v-icon size="20">mdi-arrow-right</v-icon>
        <template v-slot:loader>
          <span class="text-capitalize">loading...</span>
        </template>
      </v-btn>
    </v-row>
  </div>
</template>

<script>
import { mapMutations } from 'vuex'
import EventCard from '@/components/EventCard'
export default {
  props: [
    'events',
    'loadComplete'
  ],
  components: {
    EventCard
  },
  data: () => ({
    loading: false
  }),
  watch: {
    loadComplete() {
      if(this.loadComplete) {
        this.loading = false
      } else {
        this.loading = true
      }
    }
  },
  methods: {
    ...mapMutations('event', [
      'setEvent'
    ]),
    eventSelected(event) {
      this.setEvent(event)
      this.$router.push(`/event/${event.title.replace(/\s/g, '-')}-${event.id}/`)
    },
    loadAllEvents() {
      this.$emit('load-all-events')
      this.loading = true
    }
  }
}
</script>

<style scoped>
.related-events {
  background-color: #F8F8F8 !important;
  padding-bottom: 55px !important;
}
.related-events .related-events-title {
  padding-left: 18% !important;
  padding-top: 26px !important;
}

.related-events .related-events-content {
  padding: 8px 18% !important;
}

.heading-title {
  font-size: 3rem !important;
}

/* .related-events .image {
  border-radius: 10px !important;
} */

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
  word-break: break-word;
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

/* .events-card {
  border-bottom: 1px solid #423D3D !important;
} */
</style>
