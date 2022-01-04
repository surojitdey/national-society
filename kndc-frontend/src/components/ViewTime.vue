<template>
  <v-row class="fill-height" no-gutters>
    <v-col>
      <v-sheet height="64">
        <v-toolbar
          flat
        >
          <v-btn
            outlined
            class="mr-4"
            color="grey darken-2"
            @click="setToday"
          >
            Today
          </v-btn>
          <v-btn
            fab
            text
            small
            color="grey darken-2"
            @click="prev"
          >
            <v-icon small>
              mdi-chevron-left
            </v-icon>
          </v-btn>
          <v-btn
            fab
            text
            small
            color="grey darken-2"
            @click="next"
          >
            <v-icon small>
              mdi-chevron-right
            </v-icon>
          </v-btn>
          <v-toolbar-title v-if="$refs.calendar">
            {{ $refs.calendar.title }}
          </v-toolbar-title>
          <v-spacer></v-spacer>
          <v-menu
            bottom
            right
          >
            <template v-slot:activator="{ on, attrs }">
              <v-btn
                outlined
                color="grey darken-2"
                v-bind="attrs"
                v-on="on"
              >
                <span>{{ typeToLabel[type] }}</span>
                <v-icon right>
                  mdi-menu-down
                </v-icon>
              </v-btn>
            </template>
            <v-list>
              <v-list-item @click="type = 'day'">
                <v-list-item-title>Day</v-list-item-title>
              </v-list-item>
              <!-- <v-list-item @click="type = 'week'">
                <v-list-item-title>Week</v-list-item-title>
              </v-list-item> -->
              <v-list-item @click="type = 'month'">
                <v-list-item-title>Month</v-list-item-title>
              </v-list-item>
            </v-list>
          </v-menu>
        </v-toolbar>
      </v-sheet>
      <v-sheet height="600">
        <v-calendar
          ref="calendar"
          v-model="focus"
          color="primary"
          :events="events"
          :event-color="getEventColor"
          :type="type"
          @click:event="showEvent"
          @click:more="viewDay"
          @click:date="viewDay"
          @change="updateRange"
        >
          <template v-slot:event="{ event }">
            <span class="text-center">{{ event.name }}</span>
          </template>
        </v-calendar>
        <v-menu
          v-model="selectedOpen"
          :close-on-content-click="false"
          :activator="selectedElement"
          offset-x
        >
          <v-card
            color="grey lighten-4"
            min-width="450px"
            flat
          >
            <v-toolbar
              :color="selectedEvent.color"
              dark
            >
              <v-row no-gutters justify="space-between" align="center">
                <v-col cols="5">
                  <v-toolbar-title v-if="!editSecurity" @click="fetchData(selectedEvent)" v-html="selectedEvent.name"></v-toolbar-title>
                  <v-select 
                    v-if="editSecurity"
                    v-model.trim="timings.security"
                    class="rounded pt-6 ma-0"
                    label="Select"
                    :items="securities"
                    item-text="full_name"
                    item-value="id"
                    outlined
                    dense
                  ></v-select>
                </v-col>
                <v-col cols="5">
                  <v-row no-gutters align="center" justify="center">
                    <span @click="startTime" v-if="!editStartTime">{{formatAMPM(new Date(selectedEvent.start))}}</span>
                    <v-menu
                      ref="startMenu"
                      v-model="$v.timings.startMenu.$model"
                      v-if="editStartTime"
                      :close-on-content-click="false"
                      :nudge-right="40"
                      :return-value.sync="$v.timings.start_time.$model"
                      transition="scale-transition"
                      offset-y
                      max-width="290px"
                      min-width="290px"
                    >
                      <template v-slot:activator="{ on, attrs }">
                        <v-text-field
                          v-model="$v.timings.start_time.$model"
                          class="rounded pt-6 edit-time-input"
                          label="Start Time"
                          readonly
                          outlined
                          dense
                          v-bind="attrs"
                          v-on="on"
                        ></v-text-field>
                      </template>
                      <v-time-picker
                        v-if="$v.timings.startMenu.$model"
                        v-model="$v.timings.start_time.$model"
                        full-width
                        header-color="project_primary"
                        @click:minute="$refs.startMenu.save($v.timings.start_time.$model)"
                      ></v-time-picker>
                    </v-menu>
                    <v-toolbar-title>-</v-toolbar-title>
                    <span @click="endTime" v-if="!editEndTime">{{formatAMPM(new Date(selectedEvent.end))}}</span>
                    <v-menu
                      ref="endMenu"
                      v-model="$v.timings.endMenu.$model"
                      v-if="editEndTime"
                      :close-on-content-click="false"
                      :nudge-right="40"
                      :return-value.sync="$v.timings.end_time.$model"
                      transition="scale-transition"
                      offset-y
                      max-width="290px"
                      min-width="290px"
                    >
                      <template v-slot:activator="{ on, attrs }">
                        <v-text-field
                          v-model="$v.timings.end_time.$model"
                          class="rounded pt-6 edit-time-input"
                          label="End Time"
                          readonly
                          outlined
                          dense
                          v-bind="attrs"
                          v-on="on"
                        ></v-text-field>
                      </template>
                      <v-time-picker
                        v-if="$v.timings.endMenu.$model"
                        v-model="$v.timings.end_time.$model"
                        header-color="project_primary"
                        full-width
                        @click:minute="$refs.endMenu.save($v.timings.end_time.$model)"
                      ></v-time-picker>
                    </v-menu>
                  </v-row>
                </v-col>
                <v-col cols="1" class="d-flex justify-end">
                  <v-btn icon small @click="deleteTime(selectedEvent)">
                    <v-icon>mdi-delete</v-icon>
                  </v-btn>
                </v-col>
              </v-row>
              <!-- <v-spacer></v-spacer> -->
            </v-toolbar>
            <v-card-actions>
              <v-btn
                text
                color="primary"
                @click="editSecurityTime"
              >
                Edit
              </v-btn>
              <v-spacer></v-spacer>
              <v-btn
                text
                color="secondary"
                @click="cancelEdit"
              >
                Cancel
              </v-btn>
            </v-card-actions>
          </v-card>
        </v-menu>
      </v-sheet>
    </v-col>
  </v-row>
</template>
<script>
import { mapActions, mapGetters } from 'vuex'
import { required } from 'vuelidate/lib/validators'
// import {getStartOfMonth} from 'vuetify/lib/components/VCalendar/util/timestamp'
export default {
  props: [
    'secutitiesTime',
    'allTime'
  ],
  data: () => ({
    focus: '',
    type: 'month',
    typeToLabel: {
      month: 'Month',
      // week: 'Week',
      day: 'Day'
    },
    selectedEvent: {},
    selectedElement: null,
    selectedOpen: false,
    events: [],
    colors: ['blue', 'indigo', 'deep-purple', 'cyan', 'green', 'orange', 'grey darken-1'],
    editSecurity: false,
    timings: {
      id: '',
      security: null,
      task_date: '',
      task_day: '',
      start_time: null,
      end_time: null,
      startMenu: false,
      endMenu: false
    },
    editStartTime: false,
    editEndTime: false
  }),
  validations: {
    timings: {
      security: {
        required
      },
      task_date: {
        
      },
      task_day: {
        
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
  },
  mounted () {
    // this.fetchSecuritiesTime()
    this.$refs.calendar.checkChange()
  },
  watch: {
    secutitiesTime() {
      if(this.selectedEvent && this.allTime) {
        this.updateRange({start:this.selectedEvent.extra.start, end:this.selectedEvent.extra.end})
      } else if(this.events.length!=0) {
        this.updateRange({start:this.events[0].extra.start, end:this.events[0].extra.end})
      } else {
        let start = {
          date: `${new Date().getFullYear()}-${new Date().getMonth()+1}-01`,
          day: `${new Date(new Date().getFullYear(), new Date().getMonth()+1, 1).getDate()}`,
          future: false,
          hasDay: true,
          hasTime: false,
          hour: 0,
          minute: 0,
          month: new Date().getMonth(),
          past: false,
          present: false,
          time: "",
          weekday: new Date(new Date().getFullYear(), new Date().getMonth()+1, 1).getDay(),
          year: new Date().getFullYear()
        }
        let end = {
          date: `${new Date().getFullYear()}-${new Date().getMonth()}-${new Date(new Date().getFullYear(), new Date().getMonth()+1, 0).getDate()}`,
          day: `${new Date(new Date().getFullYear(), new Date().getMonth()+1, 0).getDate()}`,
          future: false,
          hasDay: true,
          hasTime: false,
          hour: 0,
          minute: 0,
          month: new Date().getMonth(),
          past: false,
          present: false,
          time: "",
          weekday: new Date(new Date().getFullYear(), new Date().getMonth()+1, 0).getDay(),
          year: new Date().getFullYear()
        }
        this.updateRange({start:start, end:end})
      }
    }
  },
  computed: {
    ...mapGetters('security', {
      // secutitiesTime: 'getSecuritesTime',
      securities: 'getActiveSecurities'
    })
  },
  methods: {
    ...mapActions('security', [
      // 'fetchSecuritiesTime',
      'fetchActiveSecurities',
      'deleteSecurityTime',
      'updateSecurityTime'
    ]),
    viewDay ({ date }) {
      this.focus = date
      this.type = 'day'
    },
    getEventColor (event) {
      return event.color
    },
    setToday () {
      this.focus = ''
    },
    prev () {
      this.$refs.calendar.prev()
    },
    next () {
      this.$refs.calendar.next()
    },
    showEvent ({ nativeEvent, event }) {
      this.editSecurity = false
      this.editStartTime = false
      this.editEndTime = false
      this.timings.id = event.id
      this.timings.security = event.security
      this.timings.start_time = `${String(new Date(event.start).getHours()).padStart(2, '0')}:${String(new Date(event.start).getMinutes()).padStart(2, '0')}`
      this.timings.end_time = `${String(new Date(event.end).getHours()).padStart(2, '0')}:${String(new Date(event.end).getMinutes()).padStart(2, '0')}`
      this.timings.task_date = event.start.split(' ')[0]
      this.timings.task_day = this.getDayInString(new Date(event.start).getDay())
      const open = () => {
        if(new Date(event.start.split(' ')[0])>new Date().setDate(new Date().getDate() - 1)) {
          this.selectedEvent = event
          this.selectedElement = nativeEvent.target
          requestAnimationFrame(() => requestAnimationFrame(() => this.selectedOpen = true))
        }
      }

      if (this.selectedOpen) {
        this.selectedOpen = false
        requestAnimationFrame(() => requestAnimationFrame(() => open()))
      } else {
        open()
      }

      nativeEvent.stopPropagation()
    },
    updateRange ({start, end}) {
      const events = []
      
      const min = new Date(`${start.date}T00:00:00`)
      const max = new Date(`${end.date}T23:59:59`)

      for (let i = 0; i < this.secutitiesTime.length; i++) {
        const days = this.daysInMonth(min, max, this.secutitiesTime[i].task_day)
        if(this.secutitiesTime[i].task_date) {
          const startDateTime = `${this.secutitiesTime[i].task_date} ${this.secutitiesTime[i].start_time}`
          const endDateTime = `${this.secutitiesTime[i].task_date} ${this.secutitiesTime[i].end_time}`
          events.push({
            name: this.secutitiesTime[i].full_name,
            start: startDateTime,
            end: endDateTime,
            color: this.colors[this.rnd(0, this.colors.length - 1)],
            security: this.secutitiesTime[i].security,
            id: this.secutitiesTime[i].id,
            extra: {
              start: start,
              end: end
            }
          })
        } else {
          for (let j=0; j<days.length; j++) {
            const startDateTime = `${min.getFullYear()}-${min.getMonth()+1}-${days[j]} ${this.secutitiesTime[i].start_time}`
            const endDateTime = `${max.getFullYear()}-${max.getMonth()+1}-${days[j]} ${this.secutitiesTime[i].end_time}`
            events.push({
              name: this.secutitiesTime[i].full_name,
              start: startDateTime,
              end: endDateTime,
              color: this.colors[this.rnd(0, this.colors.length - 1)],
              security: this.secutitiesTime[i].security,
              id: this.secutitiesTime[i].id,
              extra: {
                start: start,
                end: end
              }
            })
          }
        }
      }
      this.events = events
      this.$refs.calendar.checkChange()
    },
    rnd (a, b) {
      return Math.floor((b - a + 1) * Math.random()) + a
    },
    daysInMonth(min,max,d) {
      let days = new Date( min.getFullYear(),min.getMonth()+1,0).getDate();
      let day = this.getDay(d)
      let daysArray = [ day - (new Date( min.getMonth()+1 +'/01/'+ min.getFullYear() ).getDay()) ]
      for ( var i = daysArray[0] + 7; i < days; i += 7 ) {
        if (i>0) {
          daysArray.push( i )
        }
      }
      return daysArray.filter(function(x){ return x > 0 })
    },
    getDay(d) {
      if(d=='sat') {
        return 0
      } else if(d=='sun') {
        return 1
      } else if(d=='mon') {
        return 2
      } else if(d=='tue') {
        return 3
      } else if(d=='wed') {
        return 4
      } else if(d=='thu') {
        return 5
      } else if(d=='fri') {
        return 6
      }
    },
    getDayInString(d) {
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
    formatAMPM(date) {
      let hours = date.getHours();
      let minutes = date.getMinutes();
      let ampm = hours >= 12 ? 'PM' : 'AM';
      hours = hours % 12;
      hours = hours ? hours : 12; // the hour '0' should be '12'
      minutes = minutes < 10 ? '0'+minutes : minutes;
      let strTime = hours + ':' + minutes + ' ' + ampm;
      return strTime;
    },
    fetchData(event) {
      this.editSecurity = true
      this.fetchActiveSecurities().then(()=> {
        this.timings.security = event.security
      })
    },
    startTime() {
      this.editStartTime = true
      this.timings.start_time = `${String(new Date(this.selectedEvent.start).getHours()).padStart(2, '0')}:${String(new Date(this.selectedEvent.start).getMinutes()).padStart(2, '0')}`
    },
    endTime() {
      this.editEndTime = true
      this.timings.end_time = `${String(new Date(this.selectedEvent.end).getHours()).padStart(2, '0')}:${String(new Date(this.selectedEvent.end).getMinutes()).padStart(2, '0')}`
    },
    cancelEdit() {
      this.selectedOpen = false
      this.editSecurity = false
      this.editStartTime = false
      this.editEndTime = false
    },
    editSecurityTime() {
      this.updateSecurityTime(this.timings).then(() => {
        this.updateRange({start:this.selectedEvent.extra.start, end:this.selectedEvent.extra.end})
        this.$refs.calendar.getVisibleEvents(this.secutitiesTime)
        this.selectedOpen = false
      })
    },
    deleteTime(event) {
      this.deleteSecurityTime({id:event.id}).then(() => {
        this.updateRange({start:this.selectedEvent.extra.start, end:this.selectedEvent.extra.end})
        this.$refs.calendar.checkChange()
        this.selectedOpen = false
      })
    }
  },
}
</script>

<style scoped>
.edit-input-box {
  /* max-width: min-content !important; */
  max-width: fit-content !important;
}
.edit-time-input {
  /* max-width: fit-content !important; */
  width: min-content !important;
}
</style>
