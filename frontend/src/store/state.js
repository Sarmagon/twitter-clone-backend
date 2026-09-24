import {defaultUser} from '@/services/functions.js'

export default {
  me: defaultUser(),
  isTweetPopupActive: false,
  isLoggedIn: false,
  globalIsLoading: false,
  activeNotifications: [],
  editProfilePopup: false,
  profileTweetCount: 0,
  lightbox: {
    state: false,
    images: [] 
  },
  isMobileMenuActive: false,
  viewedProfile: null,
  currentUserApiKey: sessionStorage.getItem('api-key') || 'test',
  isPaginationEnabled: false,
  paginationLimit: 5,
}