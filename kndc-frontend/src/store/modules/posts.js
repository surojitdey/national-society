import Vue from 'vue'
import ApiService from '../../services/api.service'


const state = {
 comment: {
   comment_id: null,
   post: null,
   text: ''
 },
 comments: [],
 reply: {
   comment: null,
   text: ''
 },
 like: {
   post: null,
   like: false,
   dislike: false
 },
 likeCount: 0,
 dislikeCount: 0,
 commentCount: 0,
 nextLink: '',
 previousLink: ''
}

const mutations = {
  setCommentProperty(state, {property, value}) {
    Vue.set(state.comment, property, value)
  },
  resetComment(state) {
    Vue.delete(state.comment, 'post')
    Vue.delete(state.comment, 'text')
  },
  setComments(state, comments) {
    if (!comments.previous) {
      Vue.set(state, 'comments', [...comments.data])
    } else {
      let com = state.comments
      com.push(comments.data)
      com.flat()
      Vue.set(state, 'comments', [...com.flat()])
    }
  },
  setCommentsProperty(state, {property, value, index}) {
    Vue.set(state.comments[index], property, value)
  },
  // setCommentReplyProperty(state, {index, reply}) {
  //   let com = state.comments
  //   if(com[index].replies) {
  //     com[index].replies.push(reply)
  //   } else {
  //     com[index].replies = [reply]
  //   }
  //   Vue.set(state, 'comments', [...com])
  // },
  resetComments(state) {
    Vue.set(state, 'comments', [])
  },
  setReplyProperty(state, { property, value }) {
    Vue.set(state.reply, property, value)
  },
  resetReply(state) {
    Vue.delete(state.reply, 'comment')
    Vue.delete(state.reply, 'text')
  },
  setLikeProperty(state, {property, value}) {
    Vue.set(state.like, property, value)
  },
  setLikeDislikeCount(state, data) {
    Vue.set(state, 'likeCount', Number(data.like))
    Vue.set(state, 'dislikeCount', Number(data.dislike))
  },
  setCommentCount(state, count) {
    Vue.set(state, 'commentCount', Number(count))
  },
  setNextLink(state, link) {
    Vue.set(state, 'nextLink', link)
  }
}

const actions = {
  createComment({getters, dispatch}) {
    return ApiService.post('/comment-api/v-1/create-comment/', getters.getComment).then(() => {
      dispatch('fetchComments')
    })
  },
  deleteComment({getters, dispatch}) {
    return ApiService.post('/comment-api/v-1/delete-comment/', getters.getComment).then(() => {
      dispatch('fetchComments')
    })
  },
  fetchComments({ commit, getters }) {
    const url = getters.getNextLink ? getters.getNextLink : `/comment-api/v-1/fetch-comments/?post=${getters.getComment.post}`
    return ApiService.get(url)
    .then((response) => {
      console.log('comments', response.data.data)
      commit('setComments', response.data)
      commit('setCommentCount', response.data.count)
      commit('setNextLink', response.data.next)
    })
  },
  fetchLikeDislike({ commit, getters }) {
    return ApiService.get(`/comment-api/v-1/fetch-like-dislike/?post=${getters.getComment.post}`)
    .then((response) => {
      commit('setLikeDislikeCount', response.data)
    })
  },
  createReply({getters, dispatch, commit}, index) {
    return ApiService.post('/comment-api/v-1/create-reply/', getters.getReply).then(() => {
      dispatch('fetchComments').then(() => {
        commit('setCommentsProperty', { property: 'show_replies', value: true, index: index })
      })
    }).catch((error) => {
      console.log('error', error)
    })
  },
  deleteReply({getters, dispatch, commit}, index) {
    return ApiService.post('/comment-api/v-1/delete-reply/', getters.getReply).then(() => {
      dispatch('fetchComments').then(() => {
        commit('setCommentsProperty', {property: 'show_replies', value: true, index: index})
      })
    })
  },
  likeDislike({getters, dispatch}) {
    return ApiService.post('/comment-api/v-1/like-dislike/', getters.getLike).then(() => {
      dispatch('fetchLikeDislike')
    })
  },
}

const getters = {
  getComment: state => state.comment,
  getComments: state => state.comments,
  getReply: state => state.reply,
  getLike: state => state.like,
  getLikeCount: state => state.likeCount,
  getDislikeCount: state => state.dislikeCount,
  getCommentCount: state => state.commentCount,
  getNextLink: state => state.nextLink
}

export default {
  namespaced: true,
  state,
  mutations,
  actions,
  getters
}
