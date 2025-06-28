import { createRouter, createWebHistory } from 'vue-router'
import Dashboard from '../views/Dashboard.vue'
import Analysis from '../views/Analysis.vue'
import Warning from '../views/Warning.vue'

const routes = [
  { path: '/', redirect: '/dashboard' },
  { path: '/dashboard', component: Dashboard },
  { path: '/analysis', component: Analysis },
  { path: '/warning', component: Warning },
]

export default createRouter({
  history: createWebHistory(),
  routes,
})