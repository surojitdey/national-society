<template>
    <v-app-bar class="navbar ma-auto" color="" elevation="2" app absolute width="">
        <v-app-bar-nav-icon class="md-off" @click="navigationDrawer = true"></v-app-bar-nav-icon>
        <v-row align="center" justify="space-between">
            <v-col cols="2" class="">
                <router-link to="/" exact>
                    <v-img class="logo-img" :src="logo" height="46" width="164" max-width="220"></v-img>
                </router-link>
            </v-col>
            <v-col class="small-off d-flex justify-end">
                <v-row justify="end" v-if="!isAdmin">
                    <v-btn
                        active-class="btn--active"
                        plain v-for="(item, index) in listItems"
                        :key="index"
                        :href="`/${item.route}`"
                        class="small-off pa-0 mx-3"
                        color="black"
                    >
                        {{item.text}}
                    </v-btn>
                </v-row>
            </v-col>
            <v-divider vertical inset class="small-off ma-4"></v-divider>
            <v-col class="auth-btn-on fit-content">
                <v-row justify="space-between" class="pr-3">
                    <v-btn outlined class="mx-2 rounded" color="black" v-if="!loggedIn" @click="$route.path=='/signup'? $router.go('/'): $router.push('/signup')">Become a member</v-btn>
                    <v-btn outlined class="mx-2 rounded" color="black" v-if="!loggedIn" @click="$route.path=='/signin'? $router.go('/'): $router.push('/signin')">Sign In</v-btn>
                    <v-menu bottom offset-y auto v-if="loggedIn">
                        <template v-slot:activator="{ on, attrs }">
                            <v-btn icon v-bind="attrs" v-on="on">
                                <v-icon>mdi-account-circle</v-icon>
                            </v-btn>
                        </template>

                        <v-list flat>
                            <v-list-item-group color="primary">
                                <v-list-item disabled>
                                    <v-list-item-title class="text-uppercase">{{user.full_name}}</v-list-item-title>
                                </v-list-item>
                                <v-list-item
                                    
                                    v-for="(item, index) in verticalListItemsActive"
                                    :key="index"
                                    :href="`${accountUrl}`"
                                >
                                    <v-list-item-title class="text-uppercase">{{item.title}}</v-list-item-title>
                                </v-list-item>
                                <v-list-item
                                    @click="signout()"
                                >
                                    <v-list-item-title class="text-uppercase">sign out</v-list-item-title>
                                </v-list-item>
                            </v-list-item-group>
                        </v-list>
                    </v-menu>
                </v-row>
            </v-col>
        </v-row>
        <v-menu left bottom class="auth-btn-off">
            <template v-slot:activator="{ on, attrs}">
                <v-btn class="auth-btn-off" icon v-bind="attrs" v-on="on">
                    <v-icon>mdi-dots-vertical</v-icon>
                </v-btn>
            </template>

            <v-list flat>
                <v-list-item-group v-if="!loggedIn" v-model="selectedVirticalList" color="primary">
                    <v-list-item v-for="(item, index) in verticalListItems" :key="index" @click="$router.push(item.route)">
                        <v-list-item-title>{{item.title}}</v-list-item-title>
                    </v-list-item>
                </v-list-item-group>
                <v-list-item-group v-else v-model="selectedVirticalList" color="primary">
                    <v-list-item disabled>
                        <v-list-item-title>{{user.full_name}}</v-list-item-title>
                    </v-list-item>
                    <v-list-item v-for="(item, index) in verticalListItemsActive" :key="index" @click="item.route==='account' ? ($route.path=='/account'? $router.go('/'): $router.push('/account')): signout()">
                        <v-list-item-title>{{item.title}}</v-list-item-title>
                    </v-list-item>
                </v-list-item-group>
            </v-list>
        </v-menu>
        <v-navigation-drawer class="md-off" absolute app v-model="navigationDrawer">
            <v-list class="md-off" nav dense>
                <v-list-item v-for="(item, index) in listItems" :key="index" :href="`/${item.route}`">
                    <v-list-item-title>{{item.text}}</v-list-item-title>
                </v-list-item>
            </v-list>
        </v-navigation-drawer>
    </v-app-bar>
</template>

<script>
import logo from '@/assets/KNDC.png'
import { mapGetters, mapActions } from 'vuex'
export default {
    data: () => ({
        logo,
        verticalListItems: [
            {
                title: 'Sign In',
                route: 'signin'
            },
            {
                title: 'Sign Up',
                route: 'signup'
            }
        ],
        verticalListItemsActive: [
            {
                title: 'account',
                route: 'account'
            },
            // {
            //     title: 'Sign Out',
            //     route: 'signout'
            // },
        ],
        selectedVirticalList: null,
        navigationDrawer: false,
        listItems: [
            {
                text: 'ABOUT',
                route: 'about'
            },
            {
                text: 'RESIDENTS',
                route: 'residents'
            },
            {
                text: 'COMPLAINTS & GRIEVANCES',
                route: 'complaints'
            },
            {
                text: 'EVENTS',
                route: 'events'
            },
            {
                text: 'CONTACT US',
                route: 'contacts'
            },
        ],
    }),
    computed: {
        ...mapGetters('JWT',[
            'loggedIn',
            'isAdmin'
        ]),
        ...mapGetters('user',{
            user: 'getUser'
        }),
        accountUrl() {
            return this.isAdmin?'/account/residents':'/account/profile'
            // return this.isAdmin?{name: 'Residents'}:{name: 'Profile'}
        }
    },
    methods: {
        ...mapActions('JWT', [
            'logout'
        ]),
        ...mapActions('user', [
            'fetchUser'
        ]),
        signout() {
            this.logout()
            location.reload()
        }
    },
    mounted() {
        if(this.loggedIn) this.fetchUser()
    }
}
</script>

<style scoped>
.navigation-list {
    position: absolute;
    height: none !important;
}

.logo-img {
    cursor: pointer;
}

.user-authentication-section {
    flex: 0 0 21% !important;
    min-width: 21% !important;
}
.user-authentication-section-active {
    flex: 0 0 4% !important;
    min-width: 4% !important;
}

.v-application .btn--active {
    /* border-bottom: 3px solid black !important; */
    position: relative;
}
.v-application .btn--active::after, .v-btn--plain:hover::after {
    content: '';
    height: 2px;
    width: 50%;
    position: absolute;
    left: 0;
    bottom: 0;
    background-color: black;
}
.v-application .v-btn {
    filter: drop-shadow(0px 4px 14px rgba(0, 0, 0, 0.2)) !important;

}
.v-application .v-btn--outlined {
    box-sizing: border-box !important;
    border: 1px solid #434D3D !important;
}
.v-btn.rounded {
    border-radius: 3px !important;
}

@media (max-width: 1200px) {
    .navbar {
        width: 100% !important;
        left: 0px !important;
    }
    .navbar .v-image {
        height: 50px !important;
        width: 180px !important;
    }

    .small-off {
        display: none;
    }
}
@media (max-width: 840px) {
    .auth-btn-on {
        display: none;
    }
}
@media (min-width: 840px) {
    .auth-btn-off {
        display: none;
    }
}
@media (min-width: 1200px) {
    .navbar {
        left: 0px !important;
    }
    .md-off {
        display: none;
    }
}
</style>
