import Vue from 'vue';
import Vuex from 'vuex';
import auth from "./modules/auth";
import getters from './getters';

Vue.use(Vuex);

export default new Vuex.Store({
	modules: {
		auth,

	},
	getters,
	strict: true
});
