import * as Vuex from 'vuex'
import actions from '@/store/actions.js'
import getters from '@/store/getters.js'
import mutations from '@/store/mutations.js'
import state from '@/store/state.js'

export default Vuex.createStore({
  state,
  mutations,
  getters,
  actions
})