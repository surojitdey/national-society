import Vue from 'vue'
import ApiService from '../../services/api.service'
// import { TokenService } from '@/services/token.service'
import _ from 'lodash'

const state = {
  user: {},
  changePassword: {
    password: '',
    new_password: '',
    confirm_password: ''
  },
  familyDetails: [],
  users: [],
  userStatus: {
    status: '',
    user_id: ''
  },
  posts: [],
  post: {},
  postStatus: {
    post_status: '',
    post_id: ''
  },
  complaints: [],
  complaintsStatus: {
    status: '',
    complaints_id: ''
  },
  complaintsSolutionStatus: {
    solution_status: '',
    complaints_id: ''
  },
  residents: []
}

const mutations = {
  setUser(state, user) {
    Vue.set(state, 'user', {...user})
  },
  resetUser(state) {
    Vue.set(state, 'user', {})
  },
  setUserProperty(state, { property, value }) {
    Vue.set(state.user, property, value)
  },
  setFamily(state, family) {
    Vue.set(state, 'familyDetails', [...family])
  },
  setFamilyProperty(state, { index, property, value }) {
    Vue.set(state.familyDetails[index], property, value)
  },
  setChangePasswordProperty(state, { property, value }) {
    Vue.set(state.changePassword, property, value)
  },
  resetChangePassword(state) {
    Vue.set(state.changePassword, 'password', '')
    Vue.set(state.changePassword, 'new_password', '')
    Vue.set(state.changePassword, 'confirm_password', '')
  },
  setUsers(state, users) {
    Vue.set(state, 'users', [...users])
  },
  setUserStatusProperty(state, { status, user_id }) {
    Vue.set(state.userStatus, 'status', status)
    Vue.set(state.userStatus, 'user_id', user_id)
  },
  setPosts(state, posts) {
    Vue.set(state, 'posts', [...posts])
  },
  setPost(state, post) {
    Vue.set(state, 'post', { ...post })
  },
  setPostStatusProperty(state, { status, id }) {
    Vue.set(state.postStatus, 'post_status', status)
    Vue.set(state.postStatus, 'post_id', id)
  },
  setComplaints(state, complaints) {
    Vue.set(state, 'complaints', [...complaints])
  },
  setComplaintStatusProperty(state, { status, id }) {
    Vue.set(state.complaintsStatus, 'status', status)
    Vue.set(state.complaintsStatus, 'complaints_id', id)
  },
  setComplaintSolutionStatusProperty(state, { status, id }) {
    Vue.set(state.complaintsSolutionStatus, 'solution_status', status)
    Vue.set(state.complaintsSolutionStatus, 'complaints_id', id)
  },
  setResidents(state, residents) {
    Vue.set(state, 'residents', [...residents])
  }
}

const actions = {
  // create user for everyone.
  signupUser({getters}, formData ) {
    console.log('data', getters, formData)
    return ApiService.post('/user-api/v-1/user/', _.omit(formData, 'confirmPassword'))
  },

  createFamilyMembers(_, data) {
    return ApiService.post('/user-api/v-1/user-family/', data)
  },

  fetchUsers({ commit }) {
    return ApiService.get('/user-api/v-1/get-all-users/').then((response) => {
      commit('setUsers', response.data)
    })
  },

  updateUser({getters}) {
    return ApiService.post(`/user-api/v-1/update-user/`, getters.getUser)
  },

  updatePassword({ getters}) {
    return ApiService.post(`/user-api/v-1/update-password/`, _.omit(getters.getChangePassword, 'confirm_password'))
  },

  fetchUser({commit}) {
    return ApiService.get('/user-api/v-1/get-user/').then((response) => {
      commit('setUser', response.data)
    })
  },

  async fetchUserNameById(_, id) {
    const response = await ApiService.post('/user-api/v-1/get-user-by-id/', {user_id: id})
    return response.data.user
  },

  async fetchUserById(_, userId) {
    const response = await ApiService.get(`/user-api/v-1/user/${userId}/`);
    return response.data
  },

  fetchFamily({commit}) {
    return ApiService.get('/user-api/v-1/user-family/').then((response) => {
      commit('setFamily', response.data)
    })
  },

  updateStatus({dispatch, getters}) {
    return ApiService.post('/user-api/v-1/update-user-status/', getters.getUserStatus).then(() => {
      dispatch('fetchUsers')
    })
  },

  postStory({dispatch}, data) {
    return ApiService.post('/post-api/v-1/post/', data).then(()=>{
      dispatch('fetchPosts')
    })
  },

  updateStory({dispatch}, data) {
    return ApiService.post('/post-api/v-1/update-post/', data).then(()=>{
      dispatch('fetchPosts')
    })
  },

  deleteStory(_, id) {
    console.log('post_id', id)
    return ApiService.post('/post-api/v-1/delete-post/', {post_id: id})
  },
  
  fetchPosts({commit}) {
    return ApiService.get('/post-api/v-1/post/').then((response) => {
      commit('setPosts', response.data)
    })
  },

  fetchPostById({commit}, post_id) {
    return ApiService.get(`/post-api/v-1/post/${post_id}`).then((response) => {
      commit('setPost', response.data)
    })
  },

  fetchAllPosts({commit}) {
    return ApiService.get('/post-api/v-1/get-all-post/').then((response) => {
      commit('setPosts', response.data)
    })
  },

  fetchUserPosts({commit}) {
    return ApiService.get('/post-api/v-1/get-user-post/').then((response) => {
      commit('setPosts', response.data)
    })
  },

  updatePostStatus({ getters }) {
    return ApiService.post('/post-api/v-1/approve-post/', getters.getPostStatus)
  },

  postComplaintsAndGrievances({ getters }, data) {
    console.log('****', getters, data)
    return ApiService.post('/complaints-and-grievances-api/v-1/complaints-and-grievances/', data)
  },
  updateComplaintsAndGrievances({ getters }, data) {
    console.log('****', getters, data)
    return ApiService.post('/complaints-and-grievances-api/v-1/update-complaints-and-grievances/', data)
  },
  
  fetchComplaintsAndGrievances({ commit }) {
    return ApiService.get('/complaints-and-grievances-api/v-1/complaints-and-grievances/').then((response) => {
      commit('setComplaints', response.data)
    })
  },
  
  fetchAllComplaintsAndGrievances({ commit }) {
    return ApiService.get('/complaints-and-grievances-api/v-1/get-all-complaints-and-grievances/').then((response) => {
      commit('setComplaints', response.data)
    })
  },
  
  fetchUserComplaintsAndGrievances({ commit }) {
    return ApiService.get('/complaints-and-grievances-api/v-1/get-user-complaints-and-grievances/').then((response) => {
      commit('setComplaints', response.data)
    })
  },
  fetchUserApprovedComplaintsAndGrievances({ commit }) {
    return ApiService.get('/complaints-and-grievances-api/v-1/get-user-approved-complaints-and-grievances/').then((response) => {
      commit('setComplaints', response.data)
    })
  },
  
  updateComplaintsAndGrievancesStatus({ getters }) {
    return ApiService.post('/complaints-and-grievances-api/v-1/approve-complaints-and-grievances/', getters.getComplaintStatus)
  },
  
  updateComplaintsAndGrievancesSolutionStatus({ getters }) {
    return ApiService.post('/complaints-and-grievances-api/v-1/solution-status-complaints-and-grievances/', getters.getComplaintSolutionStatus)
  },
  deleteComplaintsAndGrievances(_, id) {
    return ApiService.post('/complaints-and-grievances-api/v-1/delete-complaint/', {complaints_id: id})
  },
  
  checkUserExist(_, { userData }) {
    return ApiService.post('/user-api/v-1/get-user-by-mobile-number/', userData)
  },
  forgotPassword(_, { userData }) {
    return ApiService.post('/user-api/v-1/forgot-password/', userData)
  },

  fetchResidents({ commit }) {
    return ApiService.get('/user-api/v-1/get-approved-user/').then((response) => {
      commit('setResidents', response.data)
    })
  },

  SendOTPUser(_, data) {
    return ApiService.post('/user-api/v-1/sent-otp/', data)
  },
  verifyOTPUser(_, data) {
    return ApiService.post('/user-api/v-1/verify-otp/', data)
  }
}

const getters = {
  getUser: state => state.user,
  getFamily: state => state.familyDetails,
  getChangePassword: state => state.changePassword,
  getUsers: state => state.users,
  getUserStatus: state => state.userStatus,
  getPosts: state => state.posts,
  getPost: state => state.post,
  getPostStatus: state => state.postStatus,
  getComplaints: state => state.complaints,
  getComplaintStatus: state => state.complaintsStatus,
  getComplaintSolutionStatus: state => state.complaintsSolutionStatus,
  getResidents: state => state.residents
}

export default {
  namespaced: true,
  state,
  mutations,
  actions,
  getters
}
