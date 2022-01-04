<template>
  <v-card max-width="414" elevation="0" color="transparent" class="events-card" @click="$emit('event-clicked', item)">
    <v-row justify="start">
      <v-col cols="12" class="py-0">
        <v-img v-if="item.thumbnail" class="image align-end" :src="item.thumbnail" :height="imageHeight"></v-img>
        <v-img v-else-if="item.media_file!=''" class="image align-end" :src="item.media_file" :height="imageHeight" contain></v-img>
      </v-col>
      <v-col cols="1" class="title-left-border my-3 ml-3 pr-0 mr-0"></v-col>
      <v-col cols="2" v-if="item.event_date" class="my-0 pl-0 ml-0">
        <v-card-title class="event-date pa-0 ma-0 text-capitalize">{{new Date(item.event_date).toLocaleString('en-us',{day:'numeric'})}}</v-card-title>
        <v-card-title class="event-month pa-0 ma-0 text-capitalize">{{new Date(item.event_date).toLocaleString('en-us',{month:'short'})}}</v-card-title>
      </v-col>
      <v-col cols="8" class="my-0 pl-0 ml-0">
        <v-card-title class="title py-0 px-0 my-0 text-capitalize">{{item.title}}</v-card-title>
      </v-col>
      <v-col cols="12" class="my-0">
        <v-card-subtitle class="py-0 px-0 my-0 description text-truncate text-justify">{{item.description}}</v-card-subtitle>
      </v-col>
    </v-row>
  </v-card>
</template>
<script>
export default {
  props: [
    'item',
    'imageHeight'
  ]  
}
</script>
<style scoped>
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
</style>