import Vue from 'vue'
import VueRouter from 'vue-router'
import BootstrapVue from 'bootstrap-vue'
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'
import Axios from 'axios'
import URLs from './service.js'
import router from './router.js'
import RouteContainer from './components/RouteContainer.vue'

Vue.config.productionTip = false
Vue.prototype.$http = Axios
Vue.use(BootstrapVue)
Vue.use(VueRouter)

function getAppleDevToken(){
  return Axios.get(URLs.baseURL + 'apple_music', {withCredentials: true})
}

new Vue({
    router,
    beforeCreate() {
      getAppleDevToken()
        .then((response) => {
          const appData = {
            name: 'Swap DJ',
            build: '0.0.5'
          }

          document.addEventListener('musickitloaded', () => {
            MusicKit.configure({
              developerToken: response.data,
              app: appData
            })
          })

          let appleMusicScript = document.createElement('script')
          appleMusicScript.setAttribute('src', 'https://js-cdn.music.apple.com/musickit/v1/musickit.js')
          document.head.appendChild(appleMusicScript)
        })
        .catch((error) => {
          console.log(error)
        })
    },
    render(h){
      return h(RouteContainer)
    }
  }).$mount('#route-container')


