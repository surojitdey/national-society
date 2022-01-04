<template>
  <div class="add-post my-16">
    <v-row justify="center" align="center">
      <v-card width="78%" class="pb-16 rounded-lg">
        <v-card-title>Upload Post</v-card-title>
        <v-row class="mx-1" align="center" justify="start">
          <v-col cols="6">
            <v-img max-height="370" v-if="image" max-width="595" :src="imageUrl" @click="selectImage"></v-img>
            <v-card class="select-image-card" elevation="0" v-else width="595" height="370">
              <v-row class="select-image" align="center" no-gutters>
                <!-- <v-icon tag="button">mdi-cloud-upload</v-icon> -->
                <v-col cols="3" class="justify-center mx-auto">
                  <v-file-input
                    id="select-image"
                    accept="image/*"
                    label="Images"
                    v-model="image"
                    v-show="false"
                    @change="onAddImages"
                  ></v-file-input>
                  <v-btn text @click="selectImage">
                    <v-icon color="#D4C6BA" size="80">mdi-cloud-upload</v-icon>
                  </v-btn>
                  <v-card-text class="my-0">Upload here</v-card-text>
                </v-col>
              </v-row>
            </v-card>
          </v-col>
          <v-col cols="6" class="input-text-section py-0">
            <v-text-field
              label="Title"
              class="rounded"
              autofocus
              outlined
              v-model.trim="$v.title.$model"
              background-color="grey lighten-4">
            </v-text-field>
            <span v-if="!$v.title.required" class="validation-text red--text text-body-2">Title required.</span>
            <span v-if="!$v.title.maxLength" class="validation-text red--text text-body-2">Title should be {{$v.title.$params.maxLength.max}} characters long.</span>
            <v-textarea
              label="What's your story?"
              class="rounded"
              v-model.trim="$v.description.$model"
              auto-grow
              outlined
              background-color="grey lighten-4">
            </v-textarea>
            <span v-if="!$v.description.required" class="validation-text red--text text-body-2">Description required.</span>
            <span v-if="!$v.description.maxLength" class="validation-text red--text text-body-2">Description should be {{$v.description.$params.maxLength.max}} characters long.</span>
            <v-btn color="#423D3D" width="40%" class="white--text text-uppercase" @click="post" :disabled="disablePost">Post</v-btn>
          </v-col>
        </v-row>
      </v-card>
    </v-row>
    <v-dialog v-model="postComplete" width="500" persistent>
      <v-card>
        <v-card-title class="headline green lighten-2">
          Story posted successfully
        </v-card-title>

        <v-card-text>
          your post will be visible after admin approval
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
import { requiredUnless, maxLength } from 'vuelidate/lib/validators'
export default {
  metaInfo: {
    title: 'Add Post'
  },
  data: () => ({
    title: '',
    description: '',
    image: undefined,
    imageUrl: '',
    errorImage: '',
    disablePost: false,
    postComplete: false
  }),
  methods: {
    ...mapActions('user', [
      'postStory'
    ]),
    selectImage() {
      document.getElementById("select-image").click()
    },
    post() {
      this.disablePost = true
      let formData = new FormData()
      if(this.image != undefined) {
        formData.append('title', this.title)
        formData.append('description', this.description)
        formData.append('media_file', this.image)
        this.postStory(formData).then(() => {
          this.postComplete = true
          this.disablePost = false
        }).catch(() => {
          this.disablePost = false
        })
      } else {
        this.$v.title.$touch()
        this.$v.description.$touch()

        if(!this.$v.title.$invalid && !this.$v.description.$invalid && this.title && this.description) {
          formData.append('title', this.title)
          formData.append('description', this.description)
          this.postStory(formData).then(() => {
            this.postComplete = true
            this.disablePost = false
          }).catch(() => {
            this.disablePost = false
          })
        } else {
          this.disablePost = false
        }
      }
    },
    finishedPost() {
      this.postComplete = false
      this.$router.push('/')
    },
    onAddImages(file) {
      const reader = new FileReader()
      reader.addEventListener('load', e => this.imageUrl = e.target.result)
      reader.addEventListener('error', () => this.imageUrl = this.errorImage)
      reader.readAsDataURL(file)
    }
  },
  computed: {
    titleRequired() {
      return this.description === ''
    },
    descriptionRequired() {
      return this.title === ''
    }
  },
  validations() {
    return {
      title: {
        required: requiredUnless('titleRequired'),
        maxLength: maxLength(100)
      },
      description: {
        required: requiredUnless('descriptionRequired'),
        maxLength: maxLength(20000)
      }
    }
  }
}
</script>
<style scoped>
.add-post {
  padding-top: 64px !important;
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
  bottom: 35px;
}
</style>
