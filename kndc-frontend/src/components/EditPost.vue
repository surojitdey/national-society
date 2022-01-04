<template>
  <div class="edit-post">
    <v-container>
      <v-row justify="center">
        <v-card width="100%" class="pb-4 rounded-lg">
          <v-card-title>Edit Post</v-card-title>
          <v-container>
            <v-row class="mx-1" align="">
              <v-col cols="6">
                <v-file-input
                  id="select-image"
                  accept="image/*"
                  label="Images"
                  v-model="image"
                  v-show="false"
                  @change="onAddImages"
                ></v-file-input>
                <v-img max-height="370" v-if="editedImageUrl || image" max-width="595" :src="editedImageUrl" @click="selectImage"></v-img>
                <v-card class="select-image-card" elevation="0" v-else width="595" height="370">
                  <v-row class="select-image" align="center" no-gutters>
                    <v-col cols="3" class="justify-center mx-auto">
                      <v-btn text @click="selectImage">
                        <v-icon color="#D4C6BA" size="80">mdi-cloud-upload</v-icon>
                      </v-btn>
                      <v-card-text class="my-0">Upload here</v-card-text>
                    </v-col>
                  </v-row>
                </v-card>
              </v-col>
              <v-col cols="6">
                <v-text-field
                  label="Title"
                  outlined
                  v-model.trim="$v.editedTitle.$model"
                  background-color="grey lighten-4">
                </v-text-field>
                <span v-if="!$v.editedTitle.required" class="validation-text red--text text-body-2">Title required.</span>
                <span v-if="!$v.editedTitle.maxLength" class="validation-text red--text text-body-2">Title should be 100 characters long.</span>
                <v-textarea
                  label="What's your story?"
                  v-model.trim="$v.editedDescription.$model"
                  background-color="grey lighten-4"
                  outlined>
                </v-textarea>
                <span v-if="!$v.editedDescription.required" class="validation-text red--text text-body-2">Description required.</span>
                <span v-if="!$v.editedDescription.maxLength" class="validation-text red--text text-body-2">Description should be 2000 characters long.</span>
                <v-card-actions class="px-0 mx-0">
                  <v-btn color="grey" class="mb-3 mr-2 text-upppercase white--text" @click="$emit('cancel-edit')" :disabled="disablePost">Cancel</v-btn>
                  <v-btn color="#434D3D" class="mb-3 text-uppercase white--text" @click="post" :disabled="disablePost">Post</v-btn>
                </v-card-actions>
              </v-col>
            </v-row>
          </v-container>
        </v-card>
      </v-row>
    </v-container>
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
  props: [
    'title',
    'description',
    'imageUrl',
    'post_id'
  ],
  data: () => ({
    rules: {
      required: v => !!v || 'Required',
      titleRules: v => v.length <= 100 || 'Max 100 characters',
      descriptionRules: v => v.length <= 2000 || 'Max 2000 characters',
    },
    image: undefined,
    errorImage: '',
    disablePost: false,
    postComplete: false,
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
    titleRequired() {
      return this.editedDescription === ''
    },
    descriptionRequired() {
      return this.editedTitle === ''
    }
  },
  methods: {
    ...mapActions('user', [
      'updateStory'
    ]),
    selectImage() {
      document.getElementById("select-image").click()
    },
    post() {
      this.disablePost = true
      let formData = new FormData()
      if(this.image != undefined) {
        formData.append('post_id', this.post_id)
        formData.append('title', this.editedTitle)
        formData.append('description', this.editedDescription)
        formData.append('media_file', this.image)
        this.updateStory(formData).then(() => {
          this.postComplete = true
          this.disablePost = false
        }).catch(() => {
          this.disablePost = false
        })
      } else {
        this.$v.editedTitle.$touch()
        this.$v.editedDescription.$touch()

        if(!this.$v.editedTitle.$invalid && !this.$v.editedDescription.$invalid && this.editedTitle && this.editedDescription) {
          formData.append('post_id', this.post_id)
          formData.append('title', this.editedTitle)
          formData.append('description', this.editedDescription)
          this.updateStory(formData).then(() => {
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
      reader.addEventListener('load', e => this.editedImageUrl = e.target.result)
      reader.addEventListener('error', () => this.editedImageUrl = this.errorImage)
      reader.readAsDataURL(file)
    }
  },

  validations() {
    return {
      editedTitle: {
        required: requiredUnless('titleRequired'),
        maxLength: maxLength(100)
      },
      editedDescription: {
        required: requiredUnless('descriptionRequired'),
        maxLength: maxLength(2000)
      }
    }
  }
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
  bottom: 30px;
}
</style>
