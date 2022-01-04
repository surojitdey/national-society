<template>
  <div class="add-complaints">
    <v-card class="rounded-lg py-4">
      <v-card-title class="justify-center">Add Complaints and Grievances</v-card-title>
      <v-row align="center" justify="center" class="mx-1">
        <v-col cols="9">
          <v-text-field
            label="Title"
            class="rounded"
            v-model.trim="$v.title.$model"
            autofocus
            outlined
            background-color="grey lighten-4">
          </v-text-field>
          <span v-if="!$v.title.required && $v.title.$dirty" class="validation-text red--text text-body-2">Title required.</span>
          <span v-if="!$v.title.maxLength" class="validation-text red--text text-body-2">Title should be 100 characters long.</span>
        </v-col>
        <v-col cols="9">
          <v-textarea
            label="What's your complaint?"
            class="rounded"
            v-model.trim="$v.description.$model"
            auto-grow
            outlined
            background-color="grey lighten-4">
          </v-textarea>
          <span v-if="!$v.description.required && $v.description.$dirty" class="validation-text red--text text-body-2">Description required.</span>
          <span v-if="!$v.description.maxLength" class="validation-text red--text text-body-2">Description should be {{$v.description.$params.maxLength.max}} characters long.</span>
        </v-col>
        <v-col cols="12" class="mr-0 pr-1">
          <v-card-actions class="justify-center">
            <v-btn color="grey" width="30%" class="text-uppercase white--text" @click="$emit('cancel-add')">Cancel</v-btn>
            <v-btn color="#434D3D" width="30%" class="text-uppercase white--text" @click="postComplaint">Post</v-btn>
          </v-card-actions>
        </v-col>
      </v-row>
    </v-card>
    <v-dialog v-model="postComplete" width="500" persistent>
      <v-card>
        <v-card-title class="headline green lighten-2">
          Complaint posted successfully
        </v-card-title>

        <v-card-text>
          your complaint will be visible after admin approval
        </v-card-text>

        <v-divider></v-divider>

        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn
            color="primary"
            text
            @click="finishedPost"
          >
            Ok
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>
<script>
import { mapActions } from 'vuex'
import { required, maxLength } from 'vuelidate/lib/validators'
export default {
  data: () => ({
    title: '',
    description: '',
    postComplete: false
  }),
  validations() {
    return {
      title: {
        required,
        maxLength: maxLength(100)
      },
      description: {
        required,
        maxLength: maxLength(20000)
      }
    }
  },
  methods: {
    ...mapActions('user', [
      'postComplaintsAndGrievances',
      'fetchComplaintsAndGrievances'
    ]),

    postComplaint() {
      let formData = new FormData()
      this.$v.title.$touch()
      this.$v.description.$touch()

      if(!this.$v.title.$invalid && !this.$v.description.$invalid && this.title && this.description) {
        formData.append('title', this.title)
        formData.append('description', this.description)
        this.postComplaintsAndGrievances(formData)
        .then(() => {
          this.fetchComplaintsAndGrievances()
          this.$emit('cancel-add')
          this.postComplete = true
        })
      }
    },

    finishedPost() {
      this.postComplete = false
      this.$router.push('/')
    }
  }
}
</script>
<style scoped>
.validation-text {
  position: relative;
  bottom: 30px;
}
</style>
