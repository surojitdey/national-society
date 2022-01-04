<template>
  <v-card>
    <v-row
      justify="space-between"
      align="center"
      class="ma-0 pa-0"
    >
      <v-col cols="12">
        <v-row justify="space-between" align="center">
          <v-col cols="4">
            <v-checkbox
              v-model="forAllDate"
              label="For all date"
            ></v-checkbox>
          </v-col>
          <v-col cols="2" class="d-flex justify-end">
            <v-btn
              small
              color="red"
              class="white--text ma-1 btn-size"
              @click="removeRow"
              v-if="timings.length>1"
            >
              <v-icon>mdi-minus</v-icon>
            </v-btn>
            <v-btn
              small
              color="green"
              class="white--text ma-1 btn-size"
              @click="addRow"
            >
              <v-icon>mdi-plus</v-icon>
            </v-btn>
          </v-col>
        </v-row>
      </v-col>
      <v-col cols="12">
        <v-row
          justify="space-between"
          align="center"
          no-gutters
          v-for="(v,index) in $v.timings.$each.$iter"
          :key="index"
        >
          <v-col :cols="!forAllDate?2:3" class="d-flex justify-center">
            <v-row no-gutters>
              <v-col class="ma-0 pa-0" cols="12">
                <span>Select Security Guard</span>
              </v-col>
              <v-col class="ma-0 pa-0" cols="12">
                <v-select v-model.trim="v.security.$model" class="rounded" label="Select" :items="securities" item-text="full_name" item-value="id" outlined dense></v-select>
                <span v-if="!v.security.required && v.security.$dirty" class="validation-text red--text text-body-2">Security Name required.</span>
              </v-col>
            </v-row>
          </v-col>
          <v-col :cols="!forAllDate?2:3" class="d-flex justify-center">
            <v-row no-gutters>
              <v-col class="ma-0 pa-0" cols="12">
                <span>Select Day</span>
              </v-col>
              <v-col class="ma-0 pa-0" cols="12">
                <v-select v-model.trim="v.task_day.$model" :disabled="!forAllDate" class="rounded" label="Select" :items="weekDays" item-text="text" item-value="value" outlined dense></v-select>
                <span v-if="!v.task_day.required && v.task_day.$dirty" class="validation-text red--text text-body-2">Day required.</span>
              </v-col>
            </v-row>
          </v-col>
          <v-col v-if="!forAllDate" cols="2" class="d-flex justify-center">
            <v-row no-gutters>
              <v-col class="ma-0 pa-0" cols="12">
                <span>Date of task</span>
              </v-col>
              <v-col class="ma-0 pa-0" cols="12">
                <DatePicker :rounded="'rounded'" :label="'Select Date'" @get-date="setDateAndDay(index, $event)"></DatePicker>
                <!-- <span v-if="!v.task_day.required && v.task_day.$dirty" class="validation-text red--text text-body-2">Day required.</span> -->
                <span v-if="!v.dateObject.minValue" class="validation-text red--text text-body-2">Date should be an upcoming date.</span>
              </v-col>
            </v-row>
          </v-col>
          <v-col cols="2" class="d-flex justify-center">
            <v-row no-gutters justify="start">
              <v-col class="ma-0 pa-0" cols="12">
                <span>Timings (from)</span>
              </v-col>
              <v-col cols="12">
                <v-menu
                  ref="startMenu"
                  v-model="v.startMenu.$model"
                  :close-on-content-click="false"
                  :nudge-right="40"
                  :return-value.sync="v.start_time.$model"
                  transition="scale-transition"
                  offset-y
                  max-width="290px"
                  min-width="290px"
                >
                  <template v-slot:activator="{ on, attrs }">
                    <v-text-field
                      v-model="v.start_time.$model"
                      class="rounded"
                      prepend-inner-icon="mdi-clock-time-four-outline"
                      readonly
                      outlined
                      dense
                      v-bind="attrs"
                      v-on="on"
                    ></v-text-field>
                  </template>
                  <v-time-picker
                    v-if="v.startMenu.$model"
                    v-model="v.start_time.$model"
                    full-width
                    header-color="project_primary"
                    @click:minute="$refs.startMenu[index].save(v.start_time.$model)"
                  ></v-time-picker>
                </v-menu>
                <span v-if="!v.start_time.required && v.start_time.$dirty" class="validation-text red--text text-body-2">Start time required.</span>
                <span v-if="!v.start_time.isStartTimeValid && v.start_time.$dirty" class="validation-text red--text text-body-2">Start time should be less than End Time.</span>
              </v-col>
            </v-row>
          </v-col>
          <v-col cols="2" class="d-flex justify-center">
            <v-row no-gutters justify="start">
              <v-col class="ma-0 pa-0" cols="12">
                <span>Timings (to)</span>
              </v-col>
              <v-col cols="12">
                <v-menu
                  ref="endMenu"
                  v-model="v.endMenu.$model"
                  :close-on-content-click="false"
                  :nudge-right="40"
                  :return-value.sync="v.end_time.$model"
                  transition="scale-transition"
                  offset-y
                  max-width="290px"
                  min-width="290px"
                >
                  <template v-slot:activator="{ on, attrs }">
                    <v-text-field
                      v-model="v.end_time.$model"
                      class="rounded"
                      prepend-inner-icon="mdi-clock-time-four-outline"
                      readonly
                      outlined
                      dense
                      v-bind="attrs"
                      v-on="on"
                    ></v-text-field>
                  </template>
                  <v-time-picker
                    v-if="v.endMenu.$model"
                    v-model="v.end_time.$model"
                    header-color="project_primary"
                    full-width
                    @click:minute="$refs.endMenu[index].save(v.end_time.$model)"
                  ></v-time-picker>
                </v-menu>
                <span v-if="!v.end_time.required && v.end_time.$dirty" class="validation-text red--text text-body-2">End time required.</span>
                <span v-if="!v.end_time.isEndTimeValid && v.end_time.$dirty" class="validation-text red--text text-body-2">End time should be grater than Start Time.</span>
              </v-col>
            </v-row>
          </v-col>
        </v-row>
      </v-col>
    </v-row>
    <v-card-actions class="d-flex justify-end">
      <v-btn
        class="text-uppercase white--text rounded"
        color="#434D3D"
        @click="submitTimings"
      >Submit</v-btn>
      <v-btn
        class="text-uppercase white--text rounded"
        color="grey"
        @click="cancelSubmit"
      >Cancel</v-btn>
    </v-card-actions>
  </v-card>
</template>
<script>
import { mapActions, mapGetters } from 'vuex'
// import { required, maxValue, minValue } from 'vuelidate/lib/validators'
import { required, minValue } from 'vuelidate/lib/validators'
import DatePicker from '@/components/DatePicker.vue'
export default {
  components: {
    DatePicker
  },
  data: () => ({
    timings: [
      {
        security: '',
        task_date: '',
        dateObject: null,
        task_day: '',
        start_time: null,
        end_time: null,
        startMenu: false,
        endMenu: false
      }
    ],
    weekDays: [
      {
        text: 'Monday',
        value: 'mon'
      },
      {
        text: 'Tuesday',
        value: 'tue'
      },
      {
        text: 'Wednesday',
        value: 'wed'
      },
      {
        text: 'Thursday',
        value: 'thu'
      },
      {
        text: 'Friday',
        value: 'fri'
      },
      {
        text: 'Saturday',
        value: 'sat'
      },
      {
        text: 'Sunday',
        value: 'sun'
      },
    ],
    startMenu: false,
    endMenu: false,
    forAllDate: true
  }),
  validations() {
    let currentDate = new Date()
    return {  
      timings: {
        required,
        $each: {
          security: {
            required
          },
          task_date: {
            
          },
          dateObject: {
            minValue: minValue(currentDate.setDate(currentDate.getDate() - 1))
          },
          task_day: {
            required
          },
          start_time: {
            required,
            isStartTimeValid(start_time, data) {
              if(data.end_time == null) {
                return true
              }
              return start_time <= data.end_time
            }
          },
          end_time: {
            required,
            isEndTimeValid(end_time, data) {
              if(data.start_time == null) {
                return true
              }
              return end_time >= data.start_time
            }
          },
          startMenu: {
            required
          },
          endMenu: {
            required
          }
        }
      }
    }
  },
  computed: {
    ...mapGetters('security', {
      securities: 'getActiveSecurities'
    })
  },
  methods: {
    ...mapActions('security', [
      'fetchActiveSecurities',
      'createSequrityTime'
    ]),
    addRow() {
      this.timings.push(
        {
          security: '',
          task_day: '',
          start_time: null,
          end_time: null,
          startMenu: false,
          endMenu: false
        }
      )
    },
    removeRow() {
      if(this.timings.length > 1) {
        this.timings.pop()
      }
    },
    submitTimings() {
      this.$v.$touch()
      if(!this.$v.$invalid) {
        if(this.forAllDate) {
          for(let i=0; i<this.timings.length;i++) {
            delete this.timings[i].task_date
          }
        }
        this.createSequrityTime(this.timings).then(() => {
          this.$v.$reset()
          this.timings = [
            {
              security: '',
              task_day: '',
              task_date: '',
              start_time: null,
              end_time: null,
              startMenu: false,
              endMenu: false
            }
          ]
          this.$emit('time_added')
        })
      }
    },
    cancelSubmit() {
      this.$v.$reset()
      this.timings = [
        {
          security: '',
          task_day: '',
          task_date: '',
          start_time: null,
          end_time: null,
          startMenu: false,
          endMenu: false
        }
      ]
      this.$emit('cancel-set-time')
    },
    setDateAndDay(index, value) {
      this.timings[index].task_date = value
      this.timings[index].dateObject = new Date(value)
      this.timings[index].task_day = this.getDay(new Date(this.parseDate(value)).getDay())
    },
    parseDate (date) {
      if (!date) return null

      const [day, month, year] = date.split('/')
      return `${year}-${month}-${day}`
    },
    getDay(d) {
      if(d==0) {
        return 'sun'
      } else if(d==1) {
        return 'mon'
      } else if(d==2) {
        return 'tue'
      } else if(d==3) {
        return 'wed'
      } else if(d==4) {
        return 'thu'
      } else if(d==5) {
        return 'fri'
      } else if(d==6) {
        return 'sat'
      }
    },
  },
  mounted() {
    this.fetchActiveSecurities()
  },
  // beforeDestroy() {
  //   console.log('****')
  //   this.$root.$el.parentNode.removeChild(this.$root.$el)
  // }
}
</script>
<style scoped>
.validation-text {
  position: relative;
  bottom: 20px;
}
.btn-size {
  height: 30px !important;
  width: 30px !important;
}
</style>
