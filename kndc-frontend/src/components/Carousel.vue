<template>
  <div>
    <v-carousel
        light
        cycle
        interval="6000"
        :show-arrows="false"
        hide-delimiter-background
        hide-delimiters
        delimiter-icon="mdi-minus"
        class="carousel"
        height="650"
    >
        <v-carousel-item
            v-for="(item, i) in items"
            :key="i"
            :src="item.src"
            transition="scroll-x-transition"
            eager
        ></v-carousel-item>
    </v-carousel>
    <v-row class="carousel-message fit-content" align="center" justify="center">
      <v-card class="carousel-center-text-card">
        <v-row justify="center" no-gutters>
          <v-col cols="12" class="d-flex justify-center">
            <v-card-title class="text-h4 message white--text font-weight-bold">We are living in Kamakhya Nagar Society</v-card-title>
          </v-col>
          <v-col cols="12" class="py-0 d-flex justify-center">
            <v-card-subtitle class="text-h5 message white--text px-4 pt-0">where we evolve and create better ways of living...</v-card-subtitle>
          </v-col>
        </v-row>
      </v-card>
    </v-row>
    <!-- <v-row class="carousel-society-registration" align="center" justify="center">
      <v-card dark class="rounded-border-registration registration-card-color">
        <v-card-title class="d-flex justify-center text-uppercase">Register Society here</v-card-title>
        <v-row justify="center" class="mx-16 pl-16">
          <v-col cols="8">
            <v-text-field outlined dense class="rounded" label="Society Name"></v-text-field>
          </v-col>
          <v-col cols="4">
            <v-text-field outlined dense class="rounded" label="Mobile Number"></v-text-field>
          </v-col>
          <v-col cols="12">
            <v-textarea no-resize filled rows="3" dense class="rounded" label="Address"></v-textarea>
          </v-col>
          <v-col cols="4">
            <v-text-field outlined dense class="rounded" label="City"></v-text-field>
          </v-col>
          <v-col cols="4">
            <v-text-field outlined dense class="rounded" label="Country"></v-text-field>
          </v-col>
          <v-col cols="4">
            <v-text-field outlined dense class="rounded" label="Pin Code"></v-text-field>
          </v-col>
        </v-row>
        <v-row no-gutters justify="center" class="mx-16 px-16">
          <v-card-actions>
            <v-btn class="mx-1 rounded">Submit</v-btn>
          </v-card-actions>
        </v-row>
      </v-card>
    </v-row> -->
  </div>
</template>

<script>
import Image1 from '@/assets/hero01__1615360120_203.109.44.209.jpg'
import Image2 from '@/assets/hero02__1615360295_203.109.44.209.jpg'
import Image3 from '@/assets/hero03__1615360359_203.109.44.209.jpg'
import Image4 from '@/assets/hero04__1615360459_203.109.44.209.jpg'
export default {
  data: () => ({
      items: [
        {
          src: Image1,
        },
        {
          src: Image2,
        },
        {
          src: Image3,
        },
        {
          src: Image4,
        },
      ]
  })
}
</script>

<style scoped>
.carousel {
  position: relative;
}
.carousel >>> .v-carousel__controls {
  justify-content: flex-end;
  bottom: 45%;
}
.carousel >>> .v-item-group {
  transform: rotate(90deg);
  background-color: rgba(128,128,128, 0.1);
  backdrop-filter: blur(10px);
}
.carousel >>> .v-item--active {
  color: #434D3D !important;
}
.theme--light>>>.v-btn--active:hover::before, .theme--light>>>.v-btn--active::before {
  opacity: 0 !important;
}
.carousel >>> .v-carousel__controls__item {
  color: white;
  opacity: 1;
  z-index: 2;
}
.carousel >>> .v-btn--icon.v-size--small {
  width: inherit;
  height: inherit;
}
.carousel >>> .v-carousel__controls__item .v-icon {
  font-size: 60px !important;
  font-weight: bold !important;
  opacity: 1 !important;
}

.carousel-center-text-card {
  background-color: #88394A !important;
  backdrop-filter: blur(24px) !important;
}

.carousel-message {
  position: absolute;
  top: 450px;
  left: 10%;
  right: 43%;
}
.carousel-message .message {
  word-break: break-word !important;
}

.carousel-society-registration {
  position: absolute;
  top: 150px;
  left: 45%;
  right: 0%;
}

.rounded-border-registration {
  border-bottom-left-radius: 25% 100%;
  border-top-left-radius: 25% 100%;

}

.registration-card-color {
  background: linear-gradient(to right, rgba(66, 61, 61), rgba(183, 158, 138, 0.8));
  /* background: linear-gradient(to right, #1A237E, #CFD8DC); */
  /* background: linear-gradient(to right, #607D8B, #CFD8DC); */
}

@media (max-width: 840px) {
    .small-off {
        display: none;
    }

    .carousel {
      height:  500px !important;
    }
}

@media (max-width: 500px) {
    .carousel {
      height:  300px !important;
    }
}
</style>
