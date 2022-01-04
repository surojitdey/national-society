<template>
  <v-container fluid class="add-information my-16">
    <v-card class="mt-16" width="78%">
      <v-card-title class="">Add Information/News</v-card-title>
      <v-row class="px-4 pb-8" align="" justify="center">
        <v-col cols="6">
          <v-file-input
            id="select-image"
            accept="image/*"
            label="Images"
            v-model="informationData.media_file"
            v-show="false"
            @change="onAddImages"
          ></v-file-input>
          <v-img max-height="150" v-if="informationData.media_file" max-width="200" :src="imageUrl" @click="selectImage"></v-img>
          <v-card class="select-image-card" elevation="0" v-else width="595" height="370">
            <v-row class="select-image" align="center" no-gutters>
              <v-col cols="3" class="justify-center mx-auto">
                <v-btn text large @click="selectImage">
                  <v-icon color="#D4C6BA" size="80">mdi-cloud-upload</v-icon>
                </v-btn>
                <v-card-text class="my-0">Upload here</v-card-text>
              </v-col>
            </v-row>
          </v-card>
        </v-col>
        <v-col cols="6">
          <v-text-field class="rounded" label="Title*" autofocus v-model="$v.informationData.title.$model" outlined dense></v-text-field>
          <span v-if="!$v.informationData.title.required && $v.informationData.title.$dirty" class="validation-text red--text text-body-2">Title required.</span>
          <span v-if="!$v.informationData.title.maxLength" class="validation-text red--text text-body-2">Title should be {{$v.informationData.title.$params.maxLength.max}} characters long.</span>

          <v-textarea class="rounded" v-model="$v.informationData.description.$model" label="Description*" auto-grow outlined></v-textarea>
          <span v-if="!$v.informationData.description.required && $v.informationData.description.$dirty" class="validation-text red--text text-body-2">Description required.</span>
          <span v-if="!$v.informationData.description.maxLength" class="validation-text red--text text-body-2">Description should be {{$v.informationData.description.$params.maxLength.max}} characters long.</span>
          
          <v-card-actions class="mx-0 px-0">
            <v-btn class="white--text text-uppercase" width="40%" color="#423D3D" :disabled="overlay" @click="createInformation">Add Information</v-btn>
          </v-card-actions>
        </v-col>
      </v-row>
    </v-card>
    <v-dialog v-model="postComplete" width="500" persistent>
      <v-card>
        <v-card-title class="headline green lighten-2">
          News posted successfully
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
    <v-overlay :value="overlay">
      <v-progress-circular indeterminate color="white" width="5"></v-progress-circular>
    </v-overlay>
  </v-container>  
</template>
<script>
import { required, maxLength } from 'vuelidate/lib/validators'
import { mapActions } from 'vuex'
export default {
  title: 'Add News',
  metaInfo: {
    title: 'Add News'
  },
  data: () => ({
    informationData: {
      title: '',
      media_file: undefined,
      description: ''
    },
    imageUrl: '',
    errorImage: '',
    postComplete: false,
    overlay: false
  }),
  validations() {
    return {
      informationData: {
        title: {
          required,
          maxLength: maxLength(100)
        },
        description: {
          required,
          maxLength: maxLength(20000)
        }
      }
    }
  },
  methods: {
    ...mapActions('event', [
      'addInformation'
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
    createInformation() {
      this.overlay = true
      this.$v.$touch()
      if(!this.$v.$invalid) {
        let formData = new FormData()
        if(this.informationData.media_file && this.informationData.media_file.size && this.informationData.media_file.size>0) {
          formData.append('media_file', this.informationData.media_file)
        }
        formData.append('title', this.informationData.title)
        formData.append('description', this.informationData.description)

        this.addInformation(formData).then(() => {
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
.add-information {
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
