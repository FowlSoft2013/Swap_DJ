import VueRouter from 'vue-router'
import App from './pages/App.vue'
import Callback from './pages/Callback.vue'
import Home from './pages/Home.vue'

const routes = [
   { path: '/app', component: App, props: true },
   { path: '/', component: Home, props: true },
   { path: '/callback', component: Callback, props: true },
]

  const router = new VueRouter({
      routes,
      mode: 'history'
  })

  export default router 