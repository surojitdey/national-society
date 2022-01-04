<template>
  <div class="date-picker">
    <v-menu
      v-model="menu"
      :close-on-content-click="false"
      transition="scale-transition"
      offset-y
      max-width="290px"
      min-width="auto"
    >
      <template v-slot:activator="{ on, attrs }">
        <v-text-field
          v-model="dateFormatted"
          :class="rounded"
          :label="label"
          hint="DD/MM/YYYY"
          persistent-hint
          append-icon="mdi-calendar"
          v-bind="attrs"
          @blur="getDate"
          v-on="on"
          outlined
          dense
        ></v-text-field>
      </template>
      <v-date-picker
        v-model="$v.date.$model"
        no-title
        @input="menu = false"
      ></v-date-picker>
    </v-menu>
    <span v-if="!$v.date.required && $v.date.$dirty" class="red--text text-body-2">Date field required.</span>
  </div>
</template>
<script>
import { required, minValue } from 'vuelidate/lib/validators'
export default {
  props: [
    'label',
    'rounded',
    'date_given'
  ],
  data: (vm) => ({
    date: vm.date_given?vm.date_given:new Date().toISOString().substr(0, 10),
    dateFormatted: vm.date_given?vm.formatDate(new Date(vm.date_given).toISOString().substr(0, 10)):vm.formatDate(new Date().toISOString().substr(0, 10)),
    menu: false 
  }),
  watch: {
    date() {
      this.dateFormatted = this.formatDate(this.date)
      this.$emit('get-date', this.date)
    }
  },
  validations() {
    return {
      date: {
        required,
        minValue: minValue(new Date())
      }
    }
  },
  methods: {
    formatDate (date) {
      if(!date) return null
      const [year, month, day] = date.split('-')
      return `${day}/${month}/${year}`
    },
    parseDate (date) {
      if (!date) return null

      const [day, month, year] = date.split('/')
      return `${year}-${month.padStart(2, '0')}-${day.padStart(2, '0')}`
    },
    getDate() {
      this.date = this.parseDate(this.dateFormatted)
    }
  },
  mounted() {
    this.$emit('get-date', this.date)
  }
}
</script>
