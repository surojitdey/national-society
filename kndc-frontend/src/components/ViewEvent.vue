<template>
  <v-card class="mx-auto">
    <v-img
      width="100%"
      :src="event.media_file"
      contain
    ></v-img>
    <v-divider></v-divider>
    <v-card-title>{{event.title}}</v-card-title>
    <v-card-text>
      <div>{{event.description}}</div>
    </v-card-text>
  </v-card>
</template>
<script>
export default {
  props: [
    'event'
  ]
}
</script>
<style scoped>

</style>
