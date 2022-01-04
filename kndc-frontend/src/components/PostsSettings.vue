<template>
  <div class="posts-notification">
    <v-row align="center" justify="center">
      <v-col cols="11">
        <v-row class="py-5" justify="end">
          <v-col cols="12">
            <v-text-field v-model="searchQuery" dense color="#FFA500" rounded label="Search" outlined append-icon="mdi-magnify" single-line hide-details></v-text-field>
          </v-col>
        </v-row>
        <v-card class="mb-6" elevation="0" v-for="(info, index) in filteredPosts" :key="index">
          <v-row align="center" class="mx-0">
            <!-- <v-col> -->
              <router-link :to="{name: 'User', params: {id: info.user}}" tag="span" class="clickable">
                <v-btn small class="mr-2 my-2 rounded">User Details</v-btn>
              </router-link>
              <v-btn color="" v-if="info.post_status=='new' || info.post_status=='rejected'" :disabled="disabledButtons" @click="updatePostStatusProperty('approved', info.id)" small class="mx-2 my-2 green--text rounded">Approve</v-btn>
              <v-btn color="" v-if="info.post_status=='new' || info.post_status=='approved'" :disabled="disabledButtons" @click="updatePostStatusProperty('rejected', info.id)" small class="mx-2 my-2 red--text rounded">Reject</v-btn>
              <v-btn color="" :disabled="disabledButtons" @click="deletePost(info)" small class="mx-2 my-2 red--text rounded">Delete</v-btn>
            <!-- </v-col> -->
          </v-row>
          <v-row align="center" justify="space-between">
            <v-col cols="3" v-if="info.thumbnail || info.media_file">
              <v-card max-width="236" elevation="4" class="rounded-lg">
                <v-img class="align-end" height="211" v-if="info.thumbnail" :src="info.thumbnail"></v-img>
                <v-img class="align-end" height="211" v-else :src="info.media_file"></v-img>
              </v-card>
            </v-col>
            <v-col v-if="info.title || info.description">
              <v-card height="211" elevation="4" class="rounded-lg text-card">
                <v-row class="ma-0 pa-4">
                  <v-card-title v-text="info.title" class="text-h5 pa-0 text-capitalize font-weight-bold text-justify"></v-card-title>
                  <v-card-text v-text="info.description" v-if="info.description.length<200 || showMore" class="text-subtitle-1 px-0 py-2 text-justify"></v-card-text>
                  <v-card-text v-text="info.description.slice(0, 200)" v-else class="text-subtitle-1 px-0 py-2 text-justify"></v-card-text>
                  <a v-if="info.description.length>200" @click="moreLess">{{linkText}}</a>
                </v-row>
              </v-card>
            </v-col>
          </v-row>
        </v-card>
      </v-col>
    </v-row>
    <v-dialog v-model="deleteDialog" width="600" persistent>
      <v-card>
        <v-container>
          <v-row>
            <v-col cols="12">
              <v-card-title>Do you really want to delete this post?</v-card-title>
            </v-col>
            <v-col cols="12">
              <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn class="green--text" @click="confirmDelete">Yes</v-btn>
                <v-btn class="red--text" @click="cancelDelete">No</v-btn>
              </v-card-actions>
            </v-col>
          </v-row>
        </v-container>
      </v-card>
    </v-dialog>
  </div>  
</template>
<script>
import { mapActions, mapGetters, mapMutations } from 'vuex'
export default {
  title: () => ('Post Settings'),
  metaInfo: {
    title: 'Post Settings'
  },
  data: () => ({
    showMore: false,
    linkText: 'more',
    disabledButtons: false,
    deleteDialog: false,
    deletedPostId: new Number(),
    overlay: false,
    searchQuery: ''
  }),
  computed: {
    ...mapGetters('user',{
      posts: 'getPosts'
    }),
    filteredPosts() {
      if(this.searchQuery) {
        return this.posts.filter((post) => {
          return this.searchQuery.toLowerCase().split(' ').every((search) => {
            return post.title.toLowerCase().includes(search) || post.description.toLowerCase().includes(search) || post.full_name.toLowerCase().includes(search)
          })
        })
      } else {
        return this.posts
      }
    }
  },
  methods: {
    ...mapActions('user', [
      'fetchAllPosts',
      'updatePostStatus',
      'deleteStory'
    ]),
    ...mapMutations('user', [
      'setPostStatusProperty'
    ]),
    moreLess() {
      this.showMore = !this.showMore
      if(this.showMore) {
        this.linkText = 'less'
      } else {
        this.linkText = 'more'
      }
    },
    updatePostStatusProperty(status, id) {
      this.disabledButtons = true
      this.setPostStatusProperty({
        status,
        id
      })
      this.updatePostStatus().then(() => {
        this.fetchAllPosts()
        this.disabledButtons = false
      })
    },
    deletePost(post) {
      this.deletedPostId = post.id
      this.deleteDialog = true
      this.disabledButtons = true
    },
    cancelDelete() {
      this.deletedPostId = new Number()
      this.deleteDialog = false
    },
    confirmDelete() {
      this.deleteStory(this.deletedPostId).then(() => {
        this.fetchAllPosts()
        this.deleteDialog = false
        this.disabledButtons = false
      })
    }
  },
  mounted() {
    this.overlay = true
    this.fetchAllPosts().then(() => {
      this.overlay = false
    })
  }
}
</script>
<style scoped>
.text-card {
  overflow-y: scroll;
  padding: 0;
}
.row + .row {
  margin-top: 0 !important;
}
</style>
