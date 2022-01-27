<template>
  <div class="fees-settings">
    <!-- <v-card elevation="0" class="ma-auto" width="450"> -->
      <v-row align="center" justify="center">
        <v-col cols="6" class="d-flex justify-start">
          <v-card-title class="text-h5 font-weight-bold text-uppercase px-0">Setup fee structure</v-card-title>
        </v-col>
        <v-col cols="3" class="d-flex justify-end">
          <v-btn
            small
            fab
            color="green"
            class="white--text btn-size mx-1"
            @click="addItemDialog=true"
          >
            <v-icon>mdi-plus</v-icon>
          </v-btn>
          <span class="py-1">Add Item</span>
        </v-col>
      </v-row>
      <v-row
        justify="center"
        v-for="(item, index) in fees"
        :key="index"
      >
        <v-col cols="5" class="d-flex justify-start my-2">
          <span>{{index}}</span>
        </v-col>
        <v-col cols="3" class="d-flex justify-end">
          <v-text-field
            :value="item"
            outlined
            dense
            prepend-inner-icon="mdi-currency-inr"
            @input="updateFeesProperty(index, $event)"
          ></v-text-field>
        </v-col>
        <v-col cols="1" class="d-flex justify-end">
          <v-btn
            small
            fab
            text
            class="project_red--text btn-size my-1"
            @click="removeFeesProperty(index)"
          >
            <v-icon>mdi-trash-can</v-icon>
          </v-btn>
        </v-col>
      </v-row>
      <v-row justify="end">
        <v-col cols="9" class="d-flex justify-center">
          <span class="mx-2 text-h6">Total <v-icon class="ml-5">mdi-currency-inr</v-icon>{{totalFees}}</span>
        </v-col>
      </v-row>
      <!-- <v-divider></v-divider> -->
      <!-- <v-card-actions class="d-flex justify-space-between">
        <v-btn class="white--text" v-if="Object.keys(this.fees).length>0" color="project_primary" @click="saveFeesItems">Save</v-btn>
      </v-card-actions> -->
    <!-- </v-card> -->
    <!-- <v-divider></v-divider> -->
    <v-dialog
      v-model="addItemDialog"
      persistent
      width="400"
    >
      <v-card>
        <v-card-title class="d-flex justify-center">Set Property Name</v-card-title>
        <v-row no-gutters>
          <v-col cols="11" class="d-flex justify-start mx-4 my-2">
            <v-text-field
              outlined
              dense
              v-model="propertyName"
            ></v-text-field>
          </v-col>
        </v-row>
        <v-card-actions class="d-flex justify-center">
          <v-btn color="grey" class="white--text" @click="discardItem">Cancel</v-btn>
          <v-btn color="project_primary" class="white--text" @click="createItem">Ok</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
    <v-dialog v-model="statusPopup" width="50%" persistent>
      <v-card>
        <v-card-title v-if="updatedFees" class="green--text">Fees are updated successfully.</v-card-title>
        <v-card-title v-if="createdFees" class="green--text">Fees are created successfully.</v-card-title>
        <v-card-actions class="d-flex justify-end">
          <v-btn
            class="white--text text-uppercase"
            width="30%"
            color="#423D3D"
            @click="statusPopup=false"
          >Cancel</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>
<script>
import { mapGetters, mapActions, mapMutations } from 'vuex'
export default {
  props: [
    'fees',
    'feesId'
  ],
  data: () => ({
    overlays: false,
    addItemDialog: false,
    propertyName: '',
    statusPopup: false,
    createdFees: false,
    updatedFees: false
  }),
  computed: {
    ...mapGetters('fees', {
      // fees: 'getFees',
      // feesId: 'getFeesId'
    }),
    ...mapGetters('user', {
      user: 'getUser'
    }),
    totalFees() {
      let total = 0
      for(let value in this.fees) {
        total = total + Number(this.fees[value])
      }
      return total
    }
  },
  methods: {
    ...mapActions('fees', [
      // 'fetchFees',
      // 'createFees',
      // 'updateFees'
    ]),
    ...mapActions('user', [
      'fetchUser'
    ]),
    ...mapMutations('fees', [
      'setFeesProperty',
      'removeFeesProperty'
    ]),
    updateFeesProperty(property, value) {
      this.setFeesProperty({
        property,
        value
      })
    },
    createItem() {
      if(this.propertyName) {
        this.updateFeesProperty(this.propertyName, 0)
      }
      this.discardItem()
    },
    discardItem() {
      this.addItemDialog = false
      this.propertyName = ''
    },
    // saveFeesItems() {
    //   this.overlays = true
    //   if(this.feesId) {
    //     this.updateFees().then(()=> {
    //       this.fetchData()
    //       this.updatedFees = true
    //       this.statusPopup = true
    //     })
    //   } else {
    //     this.createFees().then(()=> {
    //       this.fetchData()
    //       this.createdFees = true
    //       this.statusPopup = true
    //     })
    //   }
    // },
    // fetchData() {
    //   this.fetchFees().then(()=>{
    //     this.overlays = false
    //   })
    // }
  },
  validations() {

  },
  mounted() {
    // this.overlays = true
    // this.fetchData()
    this.fetchUser()
  }
}
</script>
<style scoped>
.btn-size {
  height: 30px !important;
  width: 30px !important;
}
</style>
