<template>
  <v-card height="360" class="rounded-lg">
    <v-row align="center" justify="center" class="pa-0 ma-0">
      <v-col cols="12" class="d-flex justify-center">
        <v-card-title>Send Message to {{user.full_name}} ({{user.mobile_number}})</v-card-title>
      </v-col>
      <v-col cols="9" class="d-flex justify-center">
        <v-textarea
          class="rounded"
          outlined
          v-model="message"
          autofocus
          auto-grow
          background-color="grey lighten-4">
        </v-textarea>
      </v-col>
      <v-col cols="5" class="d-flex justify-space-around">
        <v-btn color="green" width="40%" class="rounded white--text">Send</v-btn>
        <v-btn color="red" width="40%" class="rounded white--text" @click="$emit('cancel-message')">Cancel</v-btn>
      </v-col>
    </v-row>
  </v-card>
</template>
<script>
export default {
 props: [
   'user'
 ],
 data: () => ({
   message: ''
 })
}
</script>
<style scoped>

</style>
