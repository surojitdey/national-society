<template>
  <div class="add-complaints">
    <v-card class="rounded-lg py-4">
      <v-card-title class="justify-center">Add Complaints and Grievances</v-card-title>
      <v-row align="center" justify="center" class="mx-1">
        <v-col cols="9">
          <v-text-field
            label="Title"
            class="rounded"
            outlined
            autofocus
            v-model.trim="$v.editedTitle.$model"
            background-color="grey lighten-4">
          </v-text-field>
          <span v-if="!$v.editedTitle.required && $v.editedTitle.$dirty" class="red--text text-body-2">Title required.</span>
          <span v-if="!$v.editedTitle.maxLength" class="red--text text-body-2">Title should be 100 characters long.</span>
        </v-col>
        <v-col cols="9">
          <v-textarea
            label="What's your complaint?"
            class="rounded"
            outlined
            v-model.trim="$v.editedDescription.$model"
            auto-grow
            background-color="grey lighten-4">
          </v-textarea>
          <span v-if="!$v.editedDescription.required && $v.editedDescription.$dirty" class="red--text text-body-2">Description required.</span>
          <span v-if="!$v.editedDescription.maxLength" class="red--text text-body-2">Description should be 2000 characters long.</span>
        </v-col>
        <v-col cols="12" class="mr-0 pr-1">
          <v-card-actions class="justify-center">
            <v-btn color="grey" class="text-uppercase white--text" width="30%" @click="$emit('cancel-edit')">Cancel</v-btn>
            <v-btn class="text-uppercase white--text" width="30%" @click="editComplaint" color="#434D3D">Post</v-btn>
          </v-card-actions>
        </v-col>
      </v-row>
    </v-card>
    <v-dialog v-model="postComplete" width="500" persistent>
      <v-card>
        <v-card-title class="headline green lighten-2">
          Complaint edited successfully
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
  props: [
    'title',
    'description',
    'complaints_id'
  ],
  data: () => ({
    postComplete: false
  }),
  validations() {
    return {
      editedTitle: {
        required,
        maxLength: maxLength(100)
      },
      editedDescription: {
        required,
        maxLength: maxLength(2000)
      }
    }
  },
  computed: {
    editedTitle: {
      get: function() {
        return this.title
      },
      set: function(value) {
        this.$emit('title-changed', value)
      }
    },
    editedDescription: {
      get: function() {
        return this.description
      },
      set: function(value) {
        this.$emit('description-changed', value)
      }
    }
  },
  methods: {
    ...mapActions('user', [
      'updateComplaintsAndGrievances',
      'fetchUserComplaintsAndGrievances'
    ]),

    editComplaint() {
      let formData = new FormData()
      this.$v.editedTitle.$touch()
      this.$v.editedDescription.$touch()

      if(!this.$v.editedTitle.$invalid && !this.$v.editedDescription.$invalid && this.editedTitle && this.editedDescription) {
        formData.append('complaints_id', this.complaints_id)
        formData.append('title', this.editedTitle)
        formData.append('description', this.editedDescription)
        this.updateComplaintsAndGrievances(formData)
        .then(() => {
          this.fetchUserComplaintsAndGrievances()
          this.$emit('cancel-edit')
          this.postComplete = true
        })
      }
    },

    finishedPost() {
      this.postComplete = false
    }
  }
}
</script>
<style scoped>

</style>
