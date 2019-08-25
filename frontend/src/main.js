// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import 'core-js/es6/promise'
import 'core-js/es6/string'
import 'core-js/es7/array'
import Vue from 'vue'
import BootstrapVue from 'bootstrap-vue'
import App from './App'
import router from './router'
// import cssVars from 'css-vars-ponyfill'
import Vuex from 'vuex'
import store from './store/index'
import { initialize } from './helper/general'
import ElementUI from 'element-ui'
// import 'element-ui/lib/theme-chalk/index.css'
import lang from 'element-ui/lib/locale/lang/en'
import locale from 'element-ui/lib/locale'
import VueSweetalert2 from 'vue-sweetalert2';
const options = {
  confirmButtonColor: '#41b882',
  cancelButtonColor: '#ff7674'
}

import { ServerTable, ClientTable, Event } from 'vue-tables-2'
Vue.use(ClientTable, {}, false, 'bootstrap4')
Vue.use(ServerTable, {}, false, 'bootstrap4')
Vue.use(Event)
Vue.use(VueSweetalert2, options)

// configure language
locale.use(lang)

Vue.use(ElementUI)
require('./bootstrap')
Vue.use(Vuex)
// todo
// cssVars()

Vue.use(BootstrapVue)

/* eslint-disable no-new */
initialize(store, router)
new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')
