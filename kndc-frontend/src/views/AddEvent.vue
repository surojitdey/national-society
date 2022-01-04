<template>
  <v-container fluid class="add-event mt-16">
    <v-card class="my-16 pb-4 rounded-lg" width="78%">
      <v-card-title class="justify-center">Add Event</v-card-title>
      <v-row class="px-4" justify="center" align="center">
        <v-col cols="4">
          <v-file-input
            id="select-image"
            accept="image/*"
            label="Images"
            v-model="eventData.media_file"
            v-show="false"
            @change="onAddImages"
          ></v-file-input>
          <v-img max-height="199.43" v-if="eventData.media_file" max-width="337" :src="imageUrl" @click="selectImage"></v-img>
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
          <v-text-field class="rounded" label="Title*" autofocus v-model="$v.eventData.title.$model" outlined dense></v-text-field>
          <span v-if="!$v.eventData.title.required && $v.eventData.title.$dirty" class="validation-text red--text text-body-2">Title required.</span>
          <span v-if="!$v.eventData.title.maxLength" class="validation-text red--text text-body-2">Title should be {{$v.eventData.title.$params.maxLength.max}} characters long.</span>
          <v-row class="py-2">
            <v-col cols="5">
              <DatePicker :rounded="'rounded'" :label="'Event Date*'" @get-date="eventData.event_date=$event"></DatePicker>
              <span v-if="!$v.dateObject.required && $v.dateObject.$dirty" class="validation-text red--text text-body-2">Event date required.</span>
              <span v-if="!$v.dateObject.minValue" class="validation-text red--text text-body-2">Event date should be an upcoming date.</span>
            </v-col>
            <v-col cols="4">
              <v-select v-model.trim="eventData.event_time" class="rounded" label="Event Time" :items="timeArray" item-text="text" item-value="value" outlined dense></v-select>
              <span v-if="!$v.eventData.event_time.required && $v.eventData.event_time.dirty" class="validation-text red--text text-body-2">Description required.</span>
            </v-col>
            <v-col cols="3">
              <v-select v-model="eventData.time_convention" class="rounded" label="Time Convention" :items="timeConventionArray" item-text="text" item-value="value" outlined dense></v-select>
              <span v-if="!$v.eventData.time_convention.required && $v.eventData.time_convention.$dirty" class="validation-text red--text text-body-2">Description required.</span>
            </v-col>
          </v-row>
          <v-textarea v-model="$v.eventData.description.$model" class="rounded" label="Description*" auto-grow outlined></v-textarea>
          <span v-if="!$v.eventData.description.required && $v.eventData.description.$dirty" class="validation-text red--text text-body-2">Description required.</span>
          <span v-if="!$v.eventData.description.maxLength" class="validation-text red--text text-body-2">Description should be {{$v.eventData.description.$params.maxLength.max}} characters long.</span>
          <v-checkbox
            v-model="$v.eventData.send_message.$model"
            label="Send message to all members about this event"
            color="project_primary"
            class="py-0 my-0"
          ></v-checkbox>
          <v-card-actions class="justify-center">
            <v-btn class="white--text text-uppercase" width="30%" color="#423D3D" :disabled="overlay" @click="createEvent">Create Event</v-btn>
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
  </v-container>  
</template>
<script>
import { required, requiredIf, maxLength, minValue } from 'vuelidate/lib/validators'
import DatePicker from '@/components/DatePicker.vue'
import { mapActions } from 'vuex'
export default {
  title: 'Add Events',
  metaInfo: {
    title: 'Add Events'
  },
  components: {
    DatePicker
  },
  data: () => ({
    eventData: {
      title: '',
      event_date: '',
      event_time: null,
      time_convention: null,
      media_file: undefined,
      description: '',
      send_message: false
    },
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
    imageUrl: '',
    errorImage: '',
    postComplete: false,
    overlay: false,
  }),
  computed: {
    dateObject() {
      return this.eventData.event_date ? new Date(this.eventData.event_date) : null
    }
  },
  validations() {
    let currentDate = new Date()
    return {
      eventData: {
        title: {
          required,
          maxLength: maxLength(100)
        },
        description: {
          required,
          maxLength: maxLength(20000)
        },
        event_time: {
          required: requiredIf(() => {
            return this.eventData.time_convention !== null
          })
        },
        time_convention: {
          required: requiredIf(() => {
            return this.eventData.event_time !== null
          })
        },
        send_message: {

        }
      },
      dateObject: {
        required,
        minValue: minValue(currentDate.setDate(currentDate.getDate() - 1))
      }
    }
  },
  methods: {
    ...mapActions('event', [
      'postEvents'
    ]),
    selectImage() {
      document.getElementById("select-image").click()
    },
    onAddImages(file) {
      const reader = new FileReader()
      reader.addEventListener('load', e => this.imageUrl = e.target.result)
      reader.addEventListener('error', () => this.imageUrl = this.errorImage)
      reader.readAsDataURL(file)
    },
    createEvent() {
      this.overlay = true
      this.$v.$touch()
      if(!this.$v.$invalid) {
        let formData = new FormData()
        if(this.eventData.media_file && this.eventData.media_file.size && this.eventData.media_file.size>0) {
          formData.append('media_file', this.eventData.media_file)
        }
        formData.append('title', this.eventData.title)
        formData.append('description', this.eventData.description)
        formData.append('event_date', this.eventData.event_date)
        formData.append('send_message', this.eventData.send_message)
        if(this.eventData.event_time) {
          formData.append('event_time', this.eventData.event_time)
        }
        if(this.eventData.time_convention){
          formData.append('time_convention', this.eventData.time_convention)
        }

        this.postEvents(formData).then(() => {
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
      this.$router.push('/')
    },
  }
}
</script>
<style scoped>
.add-event {
  display: flex;
  position: relative;
  align-items: center;
  justify-content: center;
  margin: auto;
}

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
  bottom: 20px;
}
</style>
