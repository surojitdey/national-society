<template>
  <div class="community-info">
    <div class="background-images">
      <div class="semi-circle big-semi-circle"></div>
      <div class="semi-circle big-semi-circle-right"></div>
      <div class="semi-circle small-semi-circle"></div>
      <div class="semi-circle small-semi-circle-right-upper"></div>
      <div class="semi-circle small-semi-circle-left-middle"></div>
      <v-img class="upper-polygon" :src="polygon"></v-img>
      <v-img class="middle-polygon-right" :src="polygon"></v-img>
      <v-img class="lower-polygon" :src="polygon"></v-img>
      <v-img class="lower-polygon-right" :src="polygon"></v-img>
    </div>
    <v-row justify="center">
      <span class="display-2 text-uppercase">Community Stories</span>
    </v-row>
    <v-row justify="center" class="py-2">
      <div class="large-divider ma-3"></div>
      <div class="small-divider ma-3"></div>
      <div class="large-divider ma-3"></div>
    </v-row>
    <v-row align="center" justify="end">
      <v-btn class="white--text rounded" v-if="!isAdmin && access_token && loggedIn" color="#72B41A" @click="$router.push('/addpost')">
        <v-icon class="mx-1" color="white">mdi-plus</v-icon>Add Post
      </v-btn>
    </v-row>
    <v-row justify="center">
      <v-col cols="12" class="px-0">
        <v-card class="my-6" elevation="0" v-for="(info, index) in posts" :key="index" @click="postSelected(info)">
          <v-lazy
            :options="{
              threshold: 0.8
            }"
            min-height="200"
            transition="scale-transition"
            origin="left center"
          >
            <v-container class="px-0">
              <v-row>
                <v-col cols="3" v-if="info.thumbnail || info.media_file">
                  <v-card max-width="236" elevation="4">
                    <v-img class="align-end" height="211" v-if="info.thumbnail" :src="info.thumbnail"></v-img>
                    <v-img class="align-end" height="211" v-else :src="info.media_file"></v-img>
                  </v-card>
                </v-col>
                <v-col v-if="info.title || info.description">
                    <v-card height="211" elevation="4">
                      <v-row class="ma-0 pa-4">
                        <v-card-title v-text="info.title" class="text-h5 pa-0 text-capitalize font-weight-bold content-title"></v-card-title>
                        <v-card-text v-text="info.description" v-if="info.description.length<200 || showMore" class="text-subtitle-1 text-justify"></v-card-text>
                        <v-card-text v-text="info.description.slice(0, 200)" v-else class="text-subtitle-1 text-justify"></v-card-text>
                        <a v-if="info.description.length>200" @click="moreLess">{{linkText}}</a>
                      </v-row>
                      <v-row align="end" class="ma-0 px-4 user-info">
                        <v-col cols="2" class="ma-0 pa-0">
                          <v-card-text class="text-capitalize body-2 grey--text">{{info.full_name}}</v-card-text>
                        </v-col>
                        <v-divider vertical inset class="my-1 mx-3"></v-divider>
                        <!-- <v-col cols="1" class="ma-0 pa-0">
                        </v-col> -->
                        <v-col cols="5" class="ma-0 pa-0">
                          <v-card-text class="caption grey--text">- {{new Date(info.added).toDateString()}} {{new Date(info.added).getHours()}}:{{new Date(info.added).getMinutes()}}</v-card-text>
                        </v-col>
                      </v-row>
                    </v-card>
                </v-col>
              </v-row>
            </v-container>
          </v-lazy>
        </v-card>
      </v-col>
    </v-row>
  </div>
</template>

<script>
import { mapGetters, mapMutations } from 'vuex'
import polygon from '@/assets/Polygon.svg'
import polygon_2 from '@/assets/Polygon-2.svg'

export default {
  props: [
    'posts'
  ],
  data: () => ({
    showMore: false,
    linkText: 'more',
    polygon,
    polygon_2
  }),
  computed: {
    ...mapGetters('JWT', {
      isAdmin: 'isAdmin',
      loggedIn: 'loggedIn',
      access_token: 'access_token'
    }),
  },
  methods: {
    ...mapMutations('user', [
      'setPost'
    ]),
    getImgUrl(url) {
      return require('@/assets/' + url)
    },
    moreLess() {
      this.showMore = !this.showMore
      if(this.showMore) {
        this.linkText = 'less'
      } else {
        this.linkText = 'more'
      }
    },
    formatDate (date) {
      if(!date) return null
      const [year, month, day] = date.split('-')
      return `${day}/${month}/${year}`
    },
    postSelected(post) {
      this.setPost(post)
      this.$router.push(`/post/${post.title.replace(/\s/g, '-')}-${post.id}/`)
    },
  },
}
</script>

<style scoped>
.background-images {
  height: 0;
}

.big-semi-circle {
  position: relative;
  right: 32%;
  top: 240px;
  width: 127px;
  height: 63px;
  transform: matrix(0, -1, -1, 0, 0, 0);
  background: rgba(183, 158, 138, 0.5);
}

.big-semi-circle-right {
  position: absolute;
  left: 93.3%;
  bottom: 13%;
  width: 127px;
  height: 63px;
  transform: matrix(0, 1, 1, 0, 0, 0);
  background: rgba(183, 158, 138, 0.5);
}

.small-semi-circle {
  position: relative;
  width: 41.71px;
  height: 20.86px;
  right: 21%;
  bottom: 56px;
  transform: rotate(-105.01deg);
  background: rgba(66, 61, 61, 0.35);
}

.small-semi-circle-right-upper {
  position: relative;
  width: 41.71px;
  height: 20.86px;
  left: 100%;
  top: 56px;
  transform: rotate(-105.01deg);
  background: rgba(66, 61, 61, 0.35);
}

.small-semi-circle-left-middle {
  position: relative;
  width: 41.71px;
  height: 20.86px;
  right: 16%;
  top: 680px;
  transform: rotate(-45deg);
  background: rgba(66, 61, 61, 0.35);
}

.semi-circle {
  border-radius: 150px 150px 0 0;
}

.upper-polygon {
  position: relative;
  width: 36.08px;
  height: 29.12px;
  top: 55px;
  left: 10%;
}

.middle-polygon-right {
  position: relative;
  width: 36.08px;
  height: 29.12px;
  top: 680px;
  left: 118%;
}

.lower-polygon {
  position: absolute;
  width: 36.08px;
  height: 29.12px;
  bottom: 9%;
  left: 4%;
}

.lower-polygon-right {
  position: absolute;
  width: 36.08px;
  height: 29.12px;
  bottom: 9%;
  right: 10%;
}
</style>

<style scoped>
.v-card__text {
  padding: 0px !important;
}

.community-info {
  padding: 55px 18% !important;
}

.community-info .image {
  margin-left: 16px !important;
}

.large-divider {
  width: 67px !important;
  height: 0px !important;
  border: 3px solid #423D3D;
  border-radius: 3px !important;
}

.small-divider {
  width: 15px !important;
  height: 0px !important;
  border: 3px solid #423D3D;
  border-radius: 3px !important;
}

.v-sheet.v-card {
  border-radius: 10px !important;
}

.user-info {
  position: absolute;
  bottom: 12px;
  width: 100%;
}
.user-info .col {
  max-width: fit-content !important;
}

.content-title {
  word-break: break-word;
}
</style>
