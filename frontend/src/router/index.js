import { createRouter, createWebHistory } from 'vue-router'
import store from '../store/index.js'

const routes = [
  {
    path: '/',
    name: 'Home',
    meta: {
      label: 'Главная',
    },
    component: () => import('@/views/Home.vue')
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/Login.vue')
  },
  {
    path: '/profile/:profileId',
    name: 'Profile',
    component: () => import('@/views/Profile.vue')
  },
]

const router = createRouter({
  history: createWebHistory('/'),
  routes
})

// Keep the requested route across the API-key login after a page reload.
router.beforeEach((to) => {
  store.commit('setMobileMenuState', false)
  if (!store.getters.getLoginStatus && to.name !== 'Login') {
    return {name: 'Login', query: {redirect: to.fullPath}, replace: true}
  }
})

export default router
