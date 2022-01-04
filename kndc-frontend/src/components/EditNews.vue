<template>
  <div class="edit-information">
    <v-card class="rounded-lg">
      <v-card-title class="px-7 fit-content">Edit Information/News</v-card-title>
      <v-row class="px-4 ma-0">
        <v-col cols="6">
          <v-file-input
            id="select-image"
            accept="image/*"
            label="Images"
            v-show="false"
            v-model="media_file"
            @change="onAddImages"
          ></v-file-input>
          <v-img max-height="370" max-width="595" v-if="informationData.media_file" :src="imageUrl !== '' ?imageUrl:informationData.media_file" @click="selectImage"></v-img>
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
          <v-text-field class="rounded" label="Title*" autofocus :value="$v.informationData.title.$model" @input="setInformationProperty({property: 'title', value: $event})" outlined dense></v-text-field>
          <span v-if="!$v.informationData.title.required && $v.informationData.title.$dirty" class="validation-text red--text text-body-2">Title required.</span>
          <span v-if="!$v.informationData.title.maxLength" class="validation-text red--text text-body-2">Title should be {{$v.informationData.title.$params.maxLength.max}} characters long.</span>

          <v-textarea class="rounded" :value="$v.informationData.description.$model" @input="setInformationProperty({property: 'description', value: $event})" label="Description*" outlined></v-textarea>
          <span v-if="!$v.informationData.description.required && $v.informationData.description.$dirty" class="validation-text red--text text-body-2">Description required.</span>
          <span v-if="!$v.informationData.description.maxLength" class="validation-text red--text text-body-2">Description should be {{$v.informationData.description.$params.maxLength.max}} characters long.</span>
          
          <v-card-actions class="mx-0 px-0">
            <v-btn class="white--text text-uppercase rounded" width="30%" color="#423D3D" :disabled="overlay" @click="updateNews">Update</v-btn>
            <v-btn class="white--text text-uppercase rounded" width="30%" color="grey" :disabled="overlay" @click="$emit('cancel-edit')">Cancel</v-btn>
          </v-card-actions>
        </v-col>
      </v-row>
    </v-card>
    <v-dialog v-model="postComplete" width="500" persistent>
      <v-card>
        <v-card-title class="headline green lighten-2">
          News updated successfully
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
import { required, maxLength } from 'vuelidate/lib/validators'
import { mapActions, mapGetters, mapMutations } from 'vuex'
export default {
  data: () => ({
    imageUrl: '',
    errorImage: '',
    postComplete: false,
    overlay: false,
    media_file: undefined
  }),
  computed: {
    ...mapGetters('event', {
      informationData: 'getInformation'
    })
  },
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
      'updateInformation'
    ]),
    ...mapMutations('event', [
      'setInformationProperty'
    ]),
    selectImage() {
      document.getElementById("select-image").click()
    },
    onAddImages(file) {
      this.setInformationProperty({property: 'media_file', value: file})
      const reader = new FileReader()
      reader.addEventListener('load', e => this.imageUrl = e.target.result)
      reader.addEventListener('error', () => this.imageUrl = this.errorImage)
      reader.readAsDataURL(file)
    },
    updateNews() {
      this.overlay = true
      this.$v.$touch()
      if(!this.$v.$invalid) {
        this.updateInformation().then(() => {
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
  bottom: 20px;
}
</style>
