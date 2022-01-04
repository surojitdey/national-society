<template>
  <div class="news-information">
    <!-- <div class="background-images align-start">
      <div class="semi-circle big-semi-circle"></div>
      <div class="semi-circle big-semi-circle-right"></div>
      <div class="semi-circle small-semi-circle"></div>
      <div class="circle outer-circle left-circle"></div>
      <div class="circle outer-circle right-upper-circle"></div>
      <div class="circle outer-circle right-lower-circle"></div>
      <v-img class="upper-polygon" :src="polygon"></v-img>
      <v-img class="lower-polygon" :src="polygon"></v-img>
      <v-img class="right-upper-polygon" :src="polygon_2"></v-img>
      <v-img class="right-lower-polygon" :src="polygon"></v-img>
    </div> -->
    <v-row justify="center">
      <span class="display-2 text-uppercase">Recent News</span>
    </v-row>
    <v-row justify="center" class="py-2">
      <div class="large-divider ma-3"></div>
      <div class="small-divider ma-3"></div>
      <div class="large-divider ma-3"></div>
    </v-row>

    <vue-horizontal ref="horizontal" responsive>
      <section v-for="(item, index) in informations" :key="index">
        <v-card height="fit-content" elevation="0" class="ma-4 py-4" @click="newsClicked(item)">
          <v-row justify="start" class="">
            <v-col cols="12" class="py-0">
              <v-img v-if="item.thumbnail" class="image align-end" height="180" :src="item.thumbnail"></v-img>
              <v-img v-else-if="item.media_file" class="image align-end" height="180" :src="item.media_file"></v-img>
            </v-col>
            <v-col cols="12" class="my-0">
              <v-card-title class="py-0 px-0 my-0 text-truncate content-title">{{item.title}}</v-card-title>
            </v-col>
            <v-col cols="12" class="my-0">
              <v-card-subtitle class="py-0 px-0 my-0 text-truncate text-justify">{{item.description}}</v-card-subtitle>
            </v-col>
            <v-col class="py-0">
              <v-divider class="title-line"></v-divider>
            </v-col>
          </v-row>
        </v-card>
      </section>
    </vue-horizontal>
  </div>
</template>

<script>
// import VueHorizontalList from 'vue-horizontal-list'
import VueHorizontal from "vue-horizontal"
import { mapMutations } from 'vuex'
import polygon from '@/assets/Polygon.svg'
import polygon_2 from '@/assets/Polygon-2.svg'
export default {
  components: {
    // VueHorizontalList,
    VueHorizontal
  },
  props: [
    'informations',
    'loadComplete'
  ],
  data: () => ({
    options: {
      responsive: [
        { end: 576, size: 1 },
        { start: 576, end: 768, size: 2 },
        { start: 768, end: 992, size: 3 },
        { start: 992, end: 1200, size: 4 },
        { start: 1200, size: 5 },
      ],
    },
    loading: false,
    loader: null,
    polygon,
    polygon_2
  }),
  watch: {
    loadComplete() {
      if(this.loadComplete) {
        this.loading = false
      } else {
        this.loading = true
      }
    }
  },
  methods: {
    ...mapMutations('event', [
      'setInformation'
    ]),
    newsClicked(item) {
      this.setInformation(item)
      this.$router.push(`/news/${item.title.replace(/\s/g, '-')}-${item.id}/`)
    },
    loadAllNews() {
      this.$emit('load-all-news')
      this.loading = true
    }
  },
  mounted() {
    setTimeout(()=>{
      this.$refs.horizontal.scrollToIndex(1)
    }, 2000)
  }
}
</script>

<style scoped>

</style>

<style scoped>

.news-information {
  /* max-width: 1400px; */

  margin-left: auto;
  margin-right: auto;

  padding: 76px 0px;
  padding-left: 80px;
  padding-right: 80px;
}

.news-information .image {
  /* margin-left: 16px !important; */
  border-radius: 10px !important;
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

.news-content {
  margin-left: 72px;
  margin-right: 72px;
}

.content-title {
  word-break: break-word;
}

.news-card {
  border-bottom: 1px solid #423D3D;
}

.read-more-btn {
  font-size: 20px !important;
  color: #423D3D !important;
}

.background-images {
  height: 0;
}

.big-semi-circle {
  position: relative;
  right: 9.2%;
  top: 74px;
  width: 127px;
  height: 63px;
  transform: matrix(0, -1, -1, 0, 0, 0);
  background: rgba(183, 158, 138, 0.5);
}

.big-semi-circle-right {
  position: relative;
  left: 100%;
  top: 975px;
  width: 127px;
  height: 63px;
  transform: matrix(0, 1, 1, 0, 0, 0);
  background: rgba(183, 158, 138, 0.5);
}

.small-semi-circle {
  position: relative;
  width: 41.71px;
  height: 20.86px;
  left: 12%;
  bottom: 127px;
  transform: rotate(-105.01deg);
  background: rgba(66, 61, 61, 0.35);
}

.semi-circle {
  border-radius: 150px 150px 0 0;
}

.upper-polygon {
  position: relative;
  width: 36.08px;
  height: 29.12px;
  top: 180px;
  right: 5%;
}

.lower-polygon {
  position: relative;
  width: 36.08px;
  height: 29.12px;
  top: 890.17px;
  right: 3.5%;
}

.right-upper-polygon {
  position: relative;
  width: 36.08px;
  height: 29.12px;
  bottom: 212px;
  right: 8%;
  float: right;
}

.right-lower-polygon {
  position: relative;
  width: 36.08px;
  height: 29.12px;
  top: 610.17px;
  left: 3%;
  float: right;
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

/* @media (min-width: 1200px) {
  .news-information {
    padding-left: 80px;
    padding-right: 80px;
  }
} */
</style>

<style scoped>
@media (max-width: 1900px) and (min-width: 1750px) {
  .big-semi-circle {
    position: relative;
    right: 6.9%;
    top: 74px;
    width: 127px;
    height: 63px;
    transform: matrix(0, -1, -1, 0, 0, 0);
    background: rgba(183, 158, 138, 0.5);
  }
  .big-semi-circle-right {
    position: relative;
    left: 100%;
    top: 1135px;
    width: 127px;
    height: 63px;
    transform: matrix(0, 1, 1, 0, 0, 0);
    background: rgba(183, 158, 138, 0.5);
  }
  .upper-polygon {
    right: 2%;
  }
  .lower-polygon {
    top: 1073.17px;
    right: 2%;
  }
  .right-lower-polygon {
    top: 754px;
    left: 0;
  }
}
</style>
