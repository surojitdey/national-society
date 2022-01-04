<template>
  <div class="edit-event">
    <v-card class="rounded-lg">
      <v-card-title class="justify-center">Edit Event</v-card-title>
      <v-row class="px-4 ma-0" align="center" justify="center">
        <v-col cols="4">
          <v-file-input
            id="select-image"
            accept="image/*"
            label="Images"
            v-model="media_file"
            v-show="false"
            @change="onAddImages"
          ></v-file-input>
          <v-card class="fit-content" v-if="media_file || editedImageUrl">
            <!-- <v-btn
              class="float-right close-btn"
              fab
              text
              small
              color="white"
              @click="removeImage"
            >
              <v-icon>
                mdi-close
              </v-icon>
            </v-btn> -->
            <v-img max-height="199.43" v-if="media_file || editedImageUrl" max-width="337" :src="editedImageUrl" @click="selectImage"></v-img>
          </v-card>
          <v-card class="select-image-card" elevation="0" v-else width="337" height="199.43">
            <v-row class="select-image" align="center" no-gutters>
              <v-col cols="4" class="justify-center mx-auto">
                <v-btn text large @click="selectImage">
                  <v-icon color="#D4C6BA" size="60">mdi-cloud-upload</v-icon>
                </v-btn>
                <v-card-text class="pa-0 text-center">Upload here</v-card-text>
              </v-col>
            </v-row>
          </v-card>
        </v-col>
        <v-col cols="9">
          <v-text-field class="rounded" label="Title*" autofocus v-model="$v.editedTitle.$model" outlined dense></v-text-field>
          <span v-if="!$v.editedTitle.required" class="validation-text red--text text-body-2">Title required.</span>
          <span v-if="!$v.editedTitle.maxLength" class="validation-text red--text text-body-2">Title should be {{$v.editedTitle.$params.maxLength.max}} characters long.</span>
          <v-row class="py-2">
            <v-col cols="5">
              <DatePicker :rounded="'rounded'" :label="'Event Date*'" @get-date="setEditedDate($event)"></DatePicker>
              <span v-if="!$v.dateObject.required" class="validation-text red--text text-body-2">Event date required.</span>
              <span v-if="!$v.dateObject.minValue" class="validation-text red--text text-body-2">Event date should be an upcoming date.</span>

            </v-col>
            <v-col cols="4">
              <v-select v-model="editedEventTime" class="rounded" label="Event Time" :items="timeArray" item-text="text" item-value="value" outlined dense></v-select>
            </v-col>
            <v-col cols="3">
              <v-select v-model="editedEventTimeConvention" class="rounded" label="Time Convention" :items="timeConventionArray" item-text="text" item-value="value" outlined dense></v-select>
            </v-col>
          </v-row>
          <v-textarea v-model="$v.editedDescription.$model" class="rounded" label="Description*" auto-grow outlined></v-textarea>
          <span v-if="!$v.editedDescription.required" class="validation-text red--text text-body-2">Description required.</span>
          <span v-if="!$v.editedDescription.maxLength" class="validation-text red--text text-body-2">Description should be {{$v.editedDescription.$params.maxLength.max}} characters long.</span>
          <v-card-actions class="mx-0 px-0 justify-center">
            <v-btn class="white--text text-uppercase rounded" color="#423D3D" :disabled="overlay" @click="updateEvent">Update Event</v-btn>
            <v-btn class="white--text text-uppercase rounded" color="grey" :disabled="overlay" @click="$emit('cancel-edit')">Cancel</v-btn>
          </v-card-actions>
        </v-col>
      </v-row>
    </v-card>
    <v-dialog v-model="postComplete" width="500" persistent>
      <v-card>
        <v-card-title class="headline green lighten-2">
          Event posted successfully
        </v-card-title>

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
import { required, maxLength, minValue } from 'vuelidate/lib/validators'
import DatePicker from '@/components/DatePicker.vue'
import { mapActions } from 'vuex'
export default {
  props: [
    'eventData',
    'imageUrl',
    'title',
    'description',
    'event_date',
    'event_time',
    'time_convention'
  ],
  components: {
    DatePicker
  },
  data: () => ({
    media_file: undefined,
    timeArray: [
      {
        text: 'select',
        value: null
      },
      {
        text: '1',
        value: 1
      },
      {
        text: '2',
        value: 2
      },
      {
        text: '3',
        value: 3
      },
      {
        text: '4',
        value: 4
      },
      {
        text: '5',
        value: 5
      },
      {
        text: '6',
        value: 6
      },
      {
        text: '7',
        value: 7
      },
      {
        text: '8',
        value: 8
      },
      {
        text: '9',
        value: 9
      },
      {
        text: '10',
        value: 10
      },
      {
        text: '11',
        value: 11
      },
      {
        text: '12',
        value: 12
      },
    ],
    timeConventionArray: [
      {
        text: 'select',
        value: null
      },
      {
        text: 'AM',
        value: 'am'
      },
      {
        text: 'PM',
        value: 'pm'
      },
    ],
    errorImage: '',
    postComplete: false,
    overlay: false
  }),
  computed: {
    editedTitle: {
      get: function() {
        return this.title
      },
      set: function(value) {
        this.$emit('title-changed', value)
      }
    },
    editedEventDate: {
      get: function() {
        return this.event_date
      },
      set: function(value) {
        this.$emit('date-changed', value)
      }
    },
    editedEventTime: {
      get: function() {
        return Number(this.event_time)
      },
      set: function(value) {
        this.$emit('time-changed', value)
      }
    },
    editedEventTimeConvention: {
      get: function() {
        return this.time_convention
      },
      set: function(value) {
        this.$emit('convention-changed', value)
      }
    },
    editedDescription: {
      get: function() {
        return this.description
      },
      set: function(value) {
        this.$emit('description-changed', value)
      }
    },
    editedImageUrl: {
      get: function() {
        return this.imageUrl
      },
      set: function(value) {
        this.$emit('imageUrl-changed', value)
      }
    },
    dateObject() {
      return this.eventData.event_date ? new Date(this.eventData.event_date) : null
    }
  },
  validations() {
    let currentDate = new Date()
    if(this.editedEventTime) {
      return {
        editedTitle: {
          required,
          maxLength: maxLength(100)
        },
        editedDescription: {
          required,
          maxLength: maxLength(20000)
        },
        editedEventTimeConvention: {
          required
        },
        dateObject: {
          required,
          minValue: minValue(currentDate.setDate(currentDate.getDate() - 1))
        }
      }
    } else if(this.editedEventTimeConvention) {
      return {
        editedTitle: {
          required,
          maxLength: maxLength(100)
        },
        editedDescription: {
          required,
          maxLength: maxLength(20000)
        },
        editedEventTime: {
          required
        },
        dateObject: {
          required,
          minValue: minValue(currentDate.setDate(currentDate.getDate() - 1))
        }
      }
    } else {
      return {
        editedTitle: {
          required,
          maxLength: maxLength(100)
        },
        editedDescription: {
          required,
          maxLength: maxLength(20000)
        },
        dateObject: {
          required,
          minValue: minValue(currentDate.setDate(currentDate.getDate() - 1))
        }
      }
    }
  },
  methods: {
    ...mapActions('event', [
      'updateEvents'
    ]),
    setEditedDate(date) {
      this.$set(this.eventData, "event_date", date)
    },
    selectImage() {
      document.getElementById("select-image").click()
    },
    onAddImages(file) {
      const reader = new FileReader()
      reader.addEventListener('load', e => this.editedImageUrl = e.target.result)
      reader.addEventListener('error', () => this.editedImageUrl = this.errorImage)
      reader.readAsDataURL(file)
    },
    updateEvent() {
      this.overlay = true
      this.$v.$touch()
      if(!this.$v.$invalid) {
        let formData = new FormData()
        if(this.media_file != undefined && this.media_file.size && this.media_file.size>0) {
          formData.append('media_file', this.media_file)
        }
        formData.append('id', this.eventData.id)
        formData.append('title', this.title)
        formData.append('description', this.description)
        formData.append('event_date', this.eventData.event_date)
        if(this.event_time) {
          formData.append('event_time', this.event_time)
        }
        if(this.time_convention){
          formData.append('time_convention', this.time_convention)
        }
        this.updateEvents(formData).then(() => {
          this.postComplete = true
          this.overlay = false
        }).catch(() => {
          this.overlay = false
        })
      } else {
        this.overlay = false
      }
    },
    finishedPost() {
      this.postComplete = false
    },
    removeImage() {
      this.media_file = undefined
      this.$emit('imageUrl-changed', '')
    }
  },
}
</script>
<style scoped>
.select-image-card {
  background: #F7F7F7;
  border: 1px dashed #423D3D;
}
.select-image {
  height: inherit;
}
.input-text-section {
  height: 370px;
  display: grid;
  align-self: center;
}
.validation-text {
  position: relative;
  bottom: 14px;
}
.v-image >>> .v-responsive__content {
  background: rgba(33, 33, 33, 0.3) !important;
}
.close-btn {
  position: absolute;
  right: 0;
  z-index: 10;
}
</style>
