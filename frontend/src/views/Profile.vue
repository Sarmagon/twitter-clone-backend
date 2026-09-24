<template>
  <div
    class="profile"
  >
    <p v-if="error" role="alert">{{ error }}</p>
    <profile-header v-if="userId"
      :id="userId"
      :following="following"
      :followers="followers"
      :name="name"
      :profile="$store.state.viewedProfile?.profile"
      @refresh="getData"
    />
    <profile-body />
    <EditProfilePopup v-if="getEditProfileStatus" />
  </div>
</template>

<script>
import ProfileBody from '@/components/Profile/ProfileBody.vue'
import ProfileHeader from '@/components/Profile/ProfileHeader.vue'
import EditProfilePopup from '@/components/EditProfilePopup/index.vue'
import { getUserInfo } from '@/services/api.js';

import { mapGetters } from 'vuex';

export default {
  name: 'ProfileView',
  components:{
    ProfileBody,
    ProfileHeader,
    EditProfilePopup
  },
  data(){
    return{
      userId: null,
      following: [],
      followers: [],
      name: '',
      error: '',
    }
  },
  computed:{
    ...mapGetters(['getMyProfileId', "getEditProfileStatus"]),
  },
  async mounted(){
    this.$store.commit('setViewedProfile', null);
    this.$store.commit('setProfileTweetCount', 0);
    this.getData();
  },
  methods: {
    async getData(){
      try {
      const { profileId } = this.$route?.params;
      const { data } = await getUserInfo(profileId)
      this.$store.commit('setViewedProfile', data.user);
      this.userId = data?.user.id;
      this.following = data?.user.following;
      this.followers = data?.user.followers;
      this.name = data?.user.name;
      this.error = '';
      } catch(e) {this.error=e.response?.data?.error_message || 'Не удалось открыть профиль';}
    }
  }
}
</script>

<style lang="scss">
@use '@/assets/theme/colors.scss' as *;



.profile{
  .profile-cover-pic{
    img{
      width: 100%;
    }
  }
  &-header{
    padding: 1rem;
  }
}
</style>