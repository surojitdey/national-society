import Vue from 'vue'
import VueRouter from 'vue-router'
import store from '@/store'
import Home from '../views/Home.vue'
import Signup from '@/views/Signup.vue'
import Signin from '@/views/SignIn.vue'
import Admin from '@/views/Admin.vue'
import Account from '@/views/Account.vue'
import User from '@/views/User.vue'
import AddPost from '@/views/AddPost.vue'
import Complaints from '@/views/ComplaintsAndGrievances.vue'
import Contact from '@/views/Contact.vue'
import ForgotPassword from '@/views/ForgotPassword.vue'
import Residents from '@/views/Residents.vue'
import AddEvent from '@/views/AddEvent.vue'
import Events from '@/views/Events.vue'
import AddInformation from '@/views/AddInformation.vue'
import NewsAndInformation from '@/views/NewsAndInformation.vue'
import Event from '@/views/Event.vue'
import Post from '@/views/Post.vue'
import Profile from '@/views/Profile.vue'
import PasswordSettings from '@/views/PasswordSettings.vue'
import ResidentsSettings from '@/views/ResidentsSettings.vue'
import PostsSettings from '@/views/PostsSettings.vue'
import ComplaintsSettings from '@/views/ComplaintsSettings.vue'
import MyPosts from '@/views/MyPosts.vue'
import MyComplaints from '@/views/MyComplaints.vue'
import Settings from '@/views/Settings.vue'
import EventsSettings from '@/views/EventsSettings.vue'
import NewsSettings from '@/views/NewsSettings.vue'
import SecuritySettings from '@/views/SecuritySettings.vue'
import AddSecurity from '@/views/AddSecurity.vue'
import FeesSettings from '@/views/FeesSettings.vue'
import ResidentsFees from '@/views/ResidentsFees.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home,
    meta: {
      title: 'Kamakhyanagar Development Committee'
    }
  },
  {
    path: '/account',
    // name: 'Account',
    component: Account,
    meta: {
      requiresAuth: true,
      title: 'Account'
    },
    children:[
      {
        path: 'profile',
        name: 'Profile',
        component: Profile,
        beforeEnter: (to, from, next) => {
          if (store.getters['JWT/isAdmin']) {
            next({
              path: '/account/residents'
            })
          } else {
            next()
          }
        }
      },
      {
        path: 'residents',
        name: 'Residents',
        component: ResidentsSettings,
        beforeEnter: (to, from, next) => {
          if (!store.getters['JWT/isAdmin']) {
            next({
              path: '/account/profile'
            })
          } else if (store.getters['JWT/isDefaultPassword'] && store.getters['JWT/isAdmin']) {
            next({
              path: '/account/password'
            })
          } else {
            next()
          }
        }
      },
      {
        path: 'security-setting',
        name: 'SecuritySettings',
        component: SecuritySettings,
        beforeEnter: (to, from, next) => {
          if (!store.getters['JWT/isAdmin']) {
            next({
              path: from.path
            })
          } else if (store.getters['JWT/isDefaultPassword'] && store.getters['JWT/isAdmin']) {
            next({
              path: '/account/password'
            })
          } else {
            next()
          }
        }
      },
      {
        path: 'myposts',
        component: MyPosts,
        beforeEnter: (to, from, next) => {
          if (store.getters['JWT/isAdmin']) {
            next({
              path: '/account/posts'
            })
          } else {
            next()
          }
        }
      },
      {
        path: 'posts',
        component: PostsSettings,
        beforeEnter: (to, from, next) => {
          if (store.getters['JWT/isDefaultPassword'] && store.getters['JWT/isAdmin']) {
            next({
              path: '/account/password'
            })
          } else if(!store.getters['JWT/isAdmin']) {
            next({
              path: '/account/myposts'
            })
          } else {
            next()
          }
        }
      },
      {
        path: 'events',
        component: EventsSettings,
        beforeEnter: (to, from, next) => {
          if (store.getters['JWT/isDefaultPassword'] && store.getters['JWT/isAdmin']) {
            next({
              path: '/account/password'
            })
          } else if(!store.getters['JWT/isAdmin']) {
            next({
              path: from.path
            })
          } else {
            next()
          }
        }
      },
      {
        path: 'news',
        component: NewsSettings,
        beforeEnter: (to, from, next) => {
          if (store.getters['JWT/isDefaultPassword'] && store.getters['JWT/isAdmin']) {
            next({
              path: '/account/password'
            })
          } else if (!store.getters['JWT/isAdmin']) {
            next({
              path: from.path
            })
          } else {
            next()
          }
        }
      },
      {
        path: 'mycomplains',
        component: MyComplaints,
        beforeEnter: (to, from, next) => {
          if (store.getters['JWT/isAdmin']) {
            next({
              path: '/account/complains'
            })
          } else {
            next()
          }
        }
      },
      {
        path: 'complains',
        component: ComplaintsSettings,
        beforeEnter: (to, from, next) => {
          if (store.getters['JWT/isDefaultPassword'] && store.getters['JWT/isAdmin']) {
            next({
              path: '/account/password'
            })
          } else if(!store.getters['JWT/isAdmin']) {
            next({
              path: '/account/mycomplains'
            })
          } else {
            next()
          }
        }
      },
      {
        path: 'password',
        name: 'ChangePassword',
        component: PasswordSettings,
      },
      {
        path: 'fees-settings',
        component: FeesSettings,
        beforeEnter: (to, from, next) => {
          if (store.getters['JWT/isDefaultPassword'] && store.getters['JWT/isAdmin']) {
            next({
              path: '/account/password'
            })
          } else if (!store.getters['JWT/isAdmin']) {
            next({
              path: from.path
            })
          } else {
            next()
          }
        }
      },
      {
        path: 'fees',
        component: ResidentsFees,
        beforeEnter: (to, from, next) => {
          if (store.getters['JWT/isAdmin']) {
            next({
              path: '/account/fees-settings'
            })
          } else {
            next()
          }
        }
      },
      {
        path: 'settings',
        component: Settings,
        beforeEnter: (to, from, next) => {
          if (store.getters['JWT/isDefaultPassword'] && store.getters['JWT/isAdmin']) {
            next({
              path: '/account/password'
            })
          } else if (!store.getters['JWT/isAdmin']) {
            next({
              path: from.path
            })
          } else {
            next()
          }
        }
      },
    ]
  },
  {
    path: '/user/:id',
    name: 'User',
    component: User,
    meta: {
      requiresAuth: true,
      title: 'User'
    }
  },
  {
    path: '/addpost',
    name: 'AddPost',
    component: AddPost,
    meta: {
      requiresAuth: true,
      title: 'AddPost'
    },
    beforeEnter: (to, from, next) => {
      if (store.getters['JWT/isAdmin']) {
        next({
          path: from.path
        })
      } else {
        next()
      }
    }
  },
  {
    path: '/addevent',
    name: 'AddEvent',
    component: AddEvent,
    meta: {
      requiresAuth: true,
      title: 'AddEvent'
    },
    beforeEnter: (to, from, next) => {
      if (!store.getters['JWT/isAdmin']) {
        next({
          path: from.path
        })
      } else {
        next()
      }
    }
  },
  {
    path: '/addinformation',
    name: 'AddInformation',
    component: AddInformation,
    meta: {
      requiresAuth: true,
      title: 'AddInformation'
    },
    beforeEnter: (to, from, next) => {
      if (!store.getters['JWT/isAdmin']) {
        next({
          path: from.path
        })
      } else {
        next()
      }
    }
  },
  {
    path: '/news/:news_id',
    name: 'NewsAndInformation',
    component: NewsAndInformation
  },
  {
    path: '/event/:event_id',
    name: 'Event',
    component: Event
  },
  {
    path: '/post/:post_id',
    name: 'Post',
    component: Post
  },
  {
    path: '/events',
    name: 'Events',
    component: Events
  },
  {
    path: '/complaints',
    name: 'ComplaintsAndGrievances',
    component: Complaints,
    meta: {
      requiresAuth: true,
      title: 'ComplaintsAndGrievances'
    }
  },
  {
    path: '/about',
    name: 'About',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '../views/About.vue')
  },
  {
    path: '/contacts',
    name: 'Contact',
    component: Contact
  },
  {
    path: '/residents',
    name: 'Residents',
    component: Residents
  },
  {
    path: '/signup',
    name: 'Signup',
    component: Signup
  },
  {
    path: '/signin',
    name: 'Signin',
    component: Signin
  },
  {
    path: '/admin',
    name: 'Admin',
    component: Admin
  },
  {
    path: '/forgot-password',
    name: 'Forgot Password',
    component: ForgotPassword
  },
  {
    path: '/add-security',
    name: 'AddSecurity',
    component: AddSecurity,
    meta: {
      requiresAuth: true,
      title: 'AddSecurity'
    },
    beforeEnter: (to, from, next) => {
      if (!store.getters['JWT/isAdmin']) {
        next({
          path: from.path
        })
      } else {
        next()
      }
    }
  },
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

router.beforeEach((to, from, next) => {
  if (to.matched.some(record => record.meta.requiresAuth)) {
    // this route requires auth, check if logged in
    // if not, redirect to login page.
    if (!store.getters['JWT/loggedIn']) {
      next({
        path: '/signin',
        query: { redirect: to.fullPath }
      })
    } else {
      next()
    }
  } else if ((to.name == 'Signin' || to.name == 'Signup' || to.name == 'Admin' || to.name == 'Forgot Password') && store.getters['JWT/loggedIn']) {
    next({
      path: from.path,
      params: from.params
    })
  } else {
    next() // make sure to always call next()!
  }
})

export default router
