import { createApp } from 'vue'
import { createRouter, createWebHistory, type RouteRecordRaw } from 'vue-router'
import './style.css'
import App from './App.vue'
import GoogleSignInPlugin  from 'vue3-google-signin'

import Home from './pages/Home.vue'
import Sets from './pages/Sets.vue' 
import SetDetails from './pages/SetDetails.vue'
import Profile from './pages/Profile.vue'

const routes: RouteRecordRaw[] = [
  { path: '/', component: Home },
  { path: '/profile', component: Profile},
  { path: '/sets', component: Sets },
  { path: '/sets/:id', component: SetDetails, props: true}
]

export const router = createRouter({
  history: createWebHistory(),
  routes,
})
const app = createApp(App)

app.use(router)

app.use(GoogleSignInPlugin, {
  clientId: "528593109002-ppqscik1gb7adakc7nji10nlqj3d08k8.apps.googleusercontent.com",
});

app.mount('#app')