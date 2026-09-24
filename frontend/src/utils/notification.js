import store from '@/store/index.js'

export function notification({type, message}){
  store.commit('addNotification', {type, message});
}