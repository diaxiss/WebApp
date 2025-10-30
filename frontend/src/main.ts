import { createApp } from 'vue'
import { createRouter, createWebHistory, type RouteRecordRaw } from 'vue-router'
import './style.css'
import App from './App.vue'
import GoogleSignInPlugin  from 'vue3-google-signin'

import Home from './pages/Home.vue'
import Sets from './pages/Sets.vue' 
import SetDetails from './pages/SetDetails.vue'
import Profile from './pages/Profile.vue'
import Collection from './pages/Collection.vue'
import Wishlist from './pages/Wishlist.vue'

const routes: RouteRecordRaw[] = [
  { path: '/', component: Home},
  { path: '/profile', component: Profile, meta: { requiresAuth: true}},
  { path: '/sets', component: Sets },
  { path: '/collection', component: Collection, meta: { requiresAuth: true} },
  { path: '/wishlist', component: Wishlist, meta: { requiresAuth: true} },
  { path: '/sets/:id', component: SetDetails}
]

export const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach((to, _, next) => {
  const isLoggedIn = Boolean(localStorage.getItem('accessToken'))

  if(to.meta.requiresAuth && !isLoggedIn) {
    next('/')
  }
  else{
    next()
  }
})

const app = createApp(App)

app.use(router)

app.use(GoogleSignInPlugin, {
  clientId: import.meta.env.VITE_GOOGLE_CLIENT_ID,
});

app.mount('#app')