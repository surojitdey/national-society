<template>
  <div class="post">
    <!-- <div class="background-images">
      <div class="semi-circle big-semi-circle"></div>
      <div class="semi-circle big-semi-circle-right"></div>
      <div class="circle outer-circle left-circle"></div>
    </div> -->
    <v-row align="center">
      <v-img :src="backgroundImage" class="align-end">
        <v-overlay :absolute="true" :value="true" color="transparent">
          <span class="upper-title text-uppercase display-2">community stories</span>
        </v-overlay>
      </v-img>
    </v-row>
    <v-row justify="space-between" class="card-content">
      <v-col cols="8">
        <v-card color="white" elevation="0" width="100%">
          <v-card-title v-text="post.title" class="text-capitalize px-0 content-title"></v-card-title>
          <v-card-subtitle class="text-uppercase px-0 py-4 content-subtitle">by {{post.full_name}}</v-card-subtitle>
          <v-img :src="post.media_file" max-height="372" contain class="align-end"></v-img>
          <v-card-text v-text="post.description" class="text-justify px-0"></v-card-text>
        </v-card>
        <v-row no-gutters>
          <v-badge class="mr-5" :content="likeCount" :value="likeCount" overlap color="project_primary">
            <v-chip color="#F5F5F5" @click="likePost">
              <v-icon left>mdi-thumb-up</v-icon>
              Like
            </v-chip>
          </v-badge>
          <v-badge class="mx-5" :content="dislikeCount" :value="dislikeCount" overlap color="project_primary">
            <v-chip color="#F5F5F5" @click="dislikePost">
              <v-icon left>mdi-thumb-down</v-icon>
              Dislike
            </v-chip>
          </v-badge>
        </v-row>
        <v-card color="white" elevation="0" width="100%">
          <v-row no-gutters align="center">
            <v-card-title class="px-0 text-capitalize">Comments</v-card-title>
            <v-card-title class="px-4 text-subtitle-1">{{commentCount}} comments</v-card-title>
          </v-row>
          <div class="mb-3" v-for="(comment, index) in comments" :key="index">
            <v-card class="rounded-xl" max-width="max-content" color="#F5F5F5" elevation="0">
              <v-card-subtitle v-text="comment.full_name" class="pb-0 text-capitalize text-subtitle-2"></v-card-subtitle>
              <v-card-text v-text="comment.text" class="text-subtitle-1 black--text"></v-card-text>
            </v-card>
            <v-row no-gutters class="mx-4" align="center">
              <a v-if="loggedIn" @click="selectReply(comment, index)" class="grey--text text-uppercase text-caption view-reply-link"> Reply</a>
              <v-divider v-if="loggedIn" vertical class="my-2 mx-3"></v-divider>
              <a v-if="loggedIn && comment.can_delete" @click="removeComment(comment)" class="grey--text text-uppercase text-caption view-reply-link delete-button"> Delete</a>
              <v-divider v-if="loggedIn && comment.can_delete" vertical class="my-2 mx-3"></v-divider>
              <v-card-subtitle class="text-capitalize text-caption px-0 py-0 my-1">{{new Date(comment.added).toDateString()}} {{new Date(comment.added).getHours()}}:{{new Date(comment.added).getMinutes()}}</v-card-subtitle>
            </v-row>
            <a class="px-4 black--text view-reply-link" v-if="comment.replies" @click="setCommentsProperty({property:'show_replies', value:true, index:index})">view replies</a>
            <div v-if="comment.show_replies">
              <div class="mx-4" v-for="(reply, reply_index) in comment.replies" :key="reply_index">
                <v-card class="rounded-xl" max-width="max-content" color="#F5F5F5" elevation="0">
                  <v-card-subtitle v-text="reply.full_name" class="pb-0 text-capitalize text-subtitle-2"></v-card-subtitle>
                  <v-card-text v-text="reply.text" class="text-subtitle-1 black--text"></v-card-text>
                </v-card>
                <v-row no-gutters class="mx-4" align="center">
                  <a v-if="loggedIn && reply.can_delete" @click="removeReply(reply, index)" class="grey--text text-uppercase text-caption view-reply-link delete-button"> Delete</a>
                  <v-divider v-if="loggedIn && reply.can_delete" vertical class="my-2 mx-3"></v-divider>
                  <v-card-subtitle class="text-capitalize text-caption px-0 py-0 my-1">{{new Date(reply.added).toDateString()}} {{new Date(reply.added).getHours()}}:{{new Date(reply.added).getMinutes()}}</v-card-subtitle>
                </v-row>
              </div>
            </div>
            <v-row no-gutters class="mx-4 reply-inputbox">
              <v-textarea
                v-if="loggedIn && comment.reply"
                dense
                :value="reply.text"
                outlined
                auto-grow
                filled
                class="rounded-lg"
                rows="1"
                @input="setReplyProperty({property: 'text', value: $event})"
              >
                <template v-slot:label>
                  <span>Reply to {{comment.full_name}}...</span>
                </template>
              </v-textarea>
              <v-btn
                class="elevation-0"
                color="#F5F5F5"
                small
                fab
                v-if="loggedIn && comment.reply"
                @click="saveReply(index)"
                :disabled="comment.disable"
              >
                <v-icon>mdi-send-outline</v-icon>
              </v-btn>
            </v-row>
          </div>
          <div v-if="nextLink" class="my-3 d-flex justify-center">
            <v-btn @click="loadMoreComments" class="col-3 white--text rounded" color="primary" :loading="moreLoading">More</v-btn>
          </div>
          <v-textarea
            v-if="loggedIn"
            dense
            :value="comment.text"
            outlined
            auto-grow
            filled
            label="Write a comment..."
            class="rounded-lg"
            rows="1"
            @input="setCommentProperty({property: 'text', value: $event})"
          ></v-textarea>
          <v-card-actions v-if="loggedIn" class="d-flex justify-start px-0">
            <v-btn color="project_primary" class="rounded white--text" @click="saveComment" :disabled="disableComment">Comment</v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
      <v-col cols="4">
        <v-row justify="center" class="ma-0">
          <v-col cols="12" class="pa-0">
            <v-card elevation="0" max-height="420" class="my-5 overflow-auto">
              <v-card-title class="text-capitalize px-0">latest news</v-card-title>
              <v-card class="my-2" v-for="(info, index) in news" :key="index" @click="newsClicked(info)">
                <v-row justify="space-between" class="ma-0 pa-0">
                  <v-col cols="3" class="px-0 py-0" v-if="info.media_file || info.thumbnail">
                    <v-img class="align-end" width="80" v-if="info.thumbnail" height="80" :src="info.thumbnail"></v-img>
                    <v-img class="align-end" width="80" v-else height="80" :src="info.media_file"></v-img>
                  </v-col>
                  <v-col cols="9" class="px-0 py-0">
                    <v-card-text class="py-0 info-title text-truncate" v-text="info.title"></v-card-text>
                  </v-col>
                </v-row>
              </v-card>
              <v-card-actions v-if="limitedNews" class="px-0">
                <v-btn
                  class="text-capitalize mx-auto rounded"
                  color="black"
                  outlined
                  @click="getAllNews"
                >see more</v-btn>
              </v-card-actions>
            </v-card>
          </v-col>
        </v-row>
        <v-row justify="center" class="ma-0">
          <v-col cols="12" class="pa-0">
            <v-card elevation="0" max-height="420" class="my-5 overflow-auto">
              <v-card-title class="text-capitalize px-0">recent events</v-card-title>
              <v-card class="my-2" v-for="(event, index) in events" :key="index" @click="eventSelected(event)">
                <v-row justify="space-between" class="ma-0 pa-0">
                  <v-col cols="3" class="px-0 py-0" v-if="event.media_file || event.thumbnail">
                    <v-img class="align-end" max-width="90" v-if="event.thumbnail" height="80" :src="event.thumbnail"></v-img>
                    <v-img class="align-end" max-width="90" v-else height="80" :src="event.media_file"></v-img>
                  </v-col>
                  <v-col cols="9" class="px-0 py-0">
                    <v-card-subtitle class="py-0 info-subtitle" v-text="`${formatDate(event.event_date)} ${event.event_time} ${event.time_convention}`"></v-card-subtitle>
                    <v-card-text class="py-0 info-title text-truncate" v-text="event.title"></v-card-text>
                  </v-col>
                </v-row>
              </v-card>
              <v-card-actions v-if="limitedEvents" class="px-0">
                <v-btn
                  class="text-capitalize mx-auto rounded"
                  color="black"
                  outlined
                  @click="getAllEvents"
                >see more</v-btn>
              </v-card-actions>
            </v-card>
          </v-col>
        </v-row>
      </v-col>
    </v-row>
  </div>
</template>
<script>
import { mapGetters, mapActions, mapMutations } from 'vuex'
import backgroundImage from '@/assets/background-image.png'
export default {
  title() {
    return `Post-${this.$route.params.post_id}`
  },
  metaInfo: {
    title: `Post of Kamakhya Nagar Development Committee`
  },
  data: () => ({
    overlay: false,
    backgroundImage,
    limitedEvents: true,
    limitedNews: true,
    disableComment: false,
    moreLoading: false
  }),
  computed: {
    ...mapGetters('JWT', {
      loggedIn: 'loggedIn'
    }),
    ...mapGetters('user', {
      post: 'getPost'
    }),
    ...mapGetters('event', {
      news: 'getInformations',
      events: 'getEvents'
    }),
    ...mapGetters('posts', {
      comment: 'getComment',
      comments: 'getComments',
      reply: 'getReply',
      likeCount: 'getLikeCount',
      dislikeCount: 'getDislikeCount',
      commentCount: 'getCommentCount',
      nextLink: 'getNextLink'
    }),
    post_id() {
      return this.$route.params.post_id.split('-')[this.$route.params.post_id.split('-').length - 1]
    }
  },
  methods: {
    ...mapActions('user', [
      'fetchPostById'
    ]),
    ...mapActions('event', [
      'fetchInformations',
      'fetchLimitedInformations',
      'fetchEvents',
      'fetchLimitedEvents'
    ]),
    ...mapActions('posts', [
      'createComment',
      'deleteComment',
      'fetchComments',
      'createReply',
      'deleteReply',
      'likeDislike',
      'fetchLikeDislike'
    ]),
    ...mapMutations('event', [
      'setEvent',
      'setInformation'
    ]),
    ...mapMutations('posts', [
      'setCommentProperty',
      'resetComments',
      'resetComment',
      'setCommentsProperty',
      'setReplyProperty',
      'resetReply',
      'setLikeProperty'
    ]),
    formatDate (date) {
      if(!date) return null
      const [year, month, day] = date.split('-')
      return `${day}/${month}/${year}`
    },
    getAllEvents() {
      this.fetchEvents().then(()=> {
        this.limitedEvents = false
      }).catch(() => {
        this.limitedEvents = true
      })
    },
    getAllNews() {
      this.fetchInformations().then(() => {
        this.limitedNews = false
      }).catch(() => {
        this.limitedNews = true
      })
    },
    eventSelected(event) {
      this.setEvent(event)
      this.$router.push(`/event/${event.title.replace(/\s/g, '-')}-${event.id}/`)
    },
    newsClicked(item) {
      this.setInformation(item)
      this.$router.push(`/news/${item.title.replace(/\s/g, '-')}-${item.id}/`)
    },
    saveComment() {
      this.disableComment = true
      if(this.comment.text) {
        this.createComment().then(() => {
          this.setCommentProperty({property: 'text', value: ''})
        }).finally(() => {
          this.disableComment = false
        })
      } else {
        this.disableComment = false
      }
    },
    saveReply(index) {
      this.setCommentsProperty({
        property: 'disable',
        value: true,
        index: index
      })
      if(this.reply.text) {
        this.createReply(index).then(() => {
          this.setReplyProperty({property: 'text', value: '', index: index})
        }).finally(()=> {
          this.setCommentsProperty({
            property: 'disable',
            value: false,
            index: index
          })
          this.setCommentsProperty({
            property:'show_replies',
            value:true,
            index:index
          })
        })
      } else {
        this.setCommentsProperty({
          property: 'disable',
          value: false,
          index: index
        })
      }
    },
    selectReply(comment, index) {
      this.setCommentsProperty({
        property: 'reply',
        value: {},
        index: index
      })
      this.setCommentsProperty({
        property: 'disable',
        value: false,
        index: index
      })
      this.setReplyProperty({
        property: 'comment',
        value: comment.id
      })
    },
    likePost() {
      this.setLikeProperty({
        property: 'like',
        value: true
      })
      this.setLikeProperty({
        property: 'dislike',
        value: false
      })
      this.likeDislike()
    },
    dislikePost() {
      this.setLikeProperty({
        property: 'like',
        value: false
      })
      this.setLikeProperty({
        property: 'dislike',
        value: true
      })
      this.likeDislike()
    },
    loadMoreComments() {
      this.moreLoading = true
      this.fetchComments().finally(()=>{
        this.moreLoading = false
      })
    },
    removeComment(comment) {
      this.setCommentProperty({
        property: 'comment_id',
        value: comment.id
      })
      this.deleteComment().then(() => {
        console.log('delete success')
      })
    },
    removeReply(reply, index) {
      this.setReplyProperty({
        property: 'reply_id',
        value: reply.id
      })
      this.deleteReply(index).then(() => {
        console.log('delete success')
      })
    }
  },
  mounted() {
    this.overlay = true
    this.fetchPostById(this.post_id)
    this.fetchLimitedInformations()
    this.fetchLimitedEvents()
    this.setCommentProperty({
      property: 'post',
      value: this.post_id
    })
    this.setLikeProperty({
      property: 'post',
      value: this.post_id
    })
    this.fetchComments()
    this.fetchLikeDislike()
  },
  beforeDestroy() {
    Object.assign(this.$data, this.$options.data.apply(this))
    this.resetComments()
    this.resetReply()
  }
}
</script>
<style scoped>
.post {
  padding-top: 64px;
}
.post .info-block {
  padding-top: 16px !important;
}
.upper-title {
  font-size: 45px !important;
}
.content-title {
  font-size: 32px !important;
  word-break: break-word;
}
.content-subtitle {
  font-size: 14px !important;
}
.card-content {
  margin: auto;
  width: 70%;
}
.reply-inputbox {
  max-width: max-content !important;
}
.view-reply-link:hover {
  text-decoration: underline;
}
.delete-button:hover {
  color: red;
}
@media screen and (max-width: 950px) {
  .card-content {
    width: 85% !important;
  }
}
@media screen and (max-width: 750px) {
  .card-content {
    width: 100% !important;
  }
}
</style>
<style scoped>
.info-title {
  font-size: 14px !important;
}
.info-subtitle {
  font-size: 12px !important;
}
</style>
<style scoped>
.background-images {
  height: 0;
}
.semi-circle {
  border-radius: 150px 150px 0 0;
}
.big-semi-circle {
  position: relative;
  right: 34px;
  top: 620px;
  width: 127px;
  height: 63px;
  transform: matrix(0, -1, -1, 0, 0, 0);
  background: rgba(183, 158, 138, 0.5);
}

.big-semi-circle-right {
  position: relative;
  left: 93.3%;
  top: 800px;
  width: 127px;
  height: 63px;
  transform: matrix(0, 1, 1, 0, 0, 0);
  background: rgba(183, 158, 138, 0.5);
}
.circle {
  border-radius: 50%
}

.outer-circle {
  width: 28.87px;
  height: 28.87px;
}

.outer-circle:after {
  content: '';
  width: 12.67px;
  height: 12.67px;
  border-radius: 50%;
}

.left-circle {
  position: relative;
  top: 450px;
  left: 2%;
  background: #B79E8A;
  opacity: 0.58;
}

.left-circle:after {
  content: '';
  position: absolute;
  top: 28.6%;
  left: 28.6%;
  background: #FFFFFF;
  opacity: 0.58;
}

.right-lower-circle {
  position: relative;
  float: right;
  top: 287px;
  left: 0%;
  background: #B79E8A;
  opacity: 0.58;
}

.right-lower-circle::after {
  position: absolute;
  top: 27%;
  right: 27%;
  background: #FFFFFF;
  opacity: 0.58;
}

.right-upper-circle {
  position: relative;
  top: 110px;
  float: right;
  left: 4%;
  background: #B79E8A;
  opacity: 0.58;
}

.right-upper-circle::after {
  position: absolute;
  top: 27%;
  right: 27%;
  background: #FFFFFF;
  opacity: 0.58;
}
</style>