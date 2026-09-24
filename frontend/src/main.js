import {createApp} from 'vue'
import App from './App.vue'
import router from './router/index.js'
import store from './store/index.js'
import { notification } from '@/utils/notification.js'
const app = createApp(App)

app.config.globalProperties.$notification = notification

app.use(router)
app.use(store)
app.mount('#app')
