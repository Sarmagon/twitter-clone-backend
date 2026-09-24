<template>
  <header v-if="me.id">
    <div class="profile-cover-pic" style="height:140px;background:#203647">

    </div>
    <div class="profile-header">
      <div class="profile-actions">
        <div class="profile-actions-image">
          <img :src="avatar">
        </div>
        <div
          v-if="!isMe"
          class="profile-actions-edit"
        >
          <!-- <div
            class="edit-button"
            @click="$store.commit('setEditProfileStatus', true)"
          >
            Редактировать
          </div> -->
          <div
            v-if="isFollowing"
            class="follow-button"
            @click="onUnfollowClick"
          >
            Перестать читать
          </div>
          <div
            v-else
            class="follow-button"
            @click="onFollowClick"
          >
            Читать
          </div>
        </div>
      </div>
      <div class="profile-info">
        <p class="profile-info-name">
          {{ name }}
        </p>
        <span class="profile-info-username">
          {{ name }}
        </span>
      </div>
      <div class="profile-description">
        {{ profile?.description || '' }}
      </div>
      <div class="profile-created-at">
        <span v-if="profileWebsite.website">
          <base-icon icon="link" />
          <a :href="profileWebsite.full_website">{{ profileWebsite.website }}</a>
        </span>

      </div>
      <div class="profile-follower-counts">
        <p>
          {{ following?.length }}
          <span>в читаемых</span>
        </p>
        <p>
          {{ followers?.length }}
          <span>читателя</span>
        </p>
      </div>
    </div>
  </header>
</template>

<script>
import {mapGetters} from 'vuex'
import moment from 'moment'
import BaseIcon from '@/components/BaseIcon/index.vue'
import { AvatarGenerator } from 'random-avatar-generator';
import { followUser, unfollowUser } from '@/services/api.js'

const generator = new AvatarGenerator();

export default {
  name: 'ProfileHeader',
  components:{
    BaseIcon
  },
  props: {
    id: Number,
    following: Array,
    followers: Array,
    name: String,
    profile: Object,
  },
  emits: ['refresh'],
  computed:{
    ...mapGetters({
      getMyProfileId: 'getMyProfileId',
      me: 'getMe'
    }),

    isMe(){
      return this.id === this.getMyProfileId
    },
  
    avatar() {
      return generator.generateRandomAvatar(Number(this.id))
    },
    profileWebsite(){
      try {
        const url = new URL(this.profile?.website);
        if (!['http:', 'https:'].includes(url.protocol)) throw new Error('Unsupported URL');
        return {website:url.host, full_website:url.href};
      } catch {return {website:'', full_website:''};}
    },
    joinedAtDate(){
      return `${moment(this.me.createdAt).format("MMM YYYY")}`
    },
    isFollowing(){
      return this.followers?.find(follower => follower.id === this.getMyProfileId)
    }
  },
  // async mounted(){
  //   try {
  //     const response = await getMe({id: this.getMyProfileId});
  //     this.$store.commit('setMe', response.data);
  //     return
  //   } catch (err) {
  //     this.$notification({
  //       type: 'error',
  //       message: 'Error when fetching user data'
  //     })
  //   }
  // },
  methods: {
    moment, 
  
    async onFollowClick() {
      try {await followUser(this.id); this.$emit('refresh');}
      catch(e) {this.$notification({type:'error',message:e.message});}
    },

    async onUnfollowClick() {
      try {await unfollowUser(this.id); this.$emit('refresh');}
      catch(e) {this.$notification({type:'error',message:e.message});}
    }
  }
}
</script>

<style lang="scss">
@use '@/assets/theme/colors.scss' as *;


.profile{
  &-cover-pic{
    border-bottom: $border-dark;
    img{
      vertical-align: middle;
    }
  }
  &-actions{
    display: flex;
    align-items: center;
    justify-content: space-between;
    &-image{
      width: 130px;
      height: 130px;
      margin-top: -80px;
      img{
        border: 1px solid $color-dark-gray;
        border-radius: 999px;
        width: 100%;
      }
    }
    &-edit{
      display: flex;
      .edit-button{
        border-radius: 999px;
        border: 1px solid $color-blue;
        color: $color-blue;
        font-weight: bold;
        font-size: 1rem;
        padding: 1rem;
        cursor: pointer;
        transition: background-color 80ms ease;
        &:hover{
          background-color: rgba($color: $color-blue, $alpha: 0.1);
        }
      }
      .follow-button{
        border-radius: 999px;
        border: 1px solid $color-blue;
        margin-left: 10px;
        color: $color-blue;
        font-weight: bold;
        font-size: 1rem;
        padding: 1rem;
        cursor: pointer;
        transition: background-color 80ms ease;
        &:hover{
          background-color: rgba($color: $color-blue, $alpha: 0.1);
        }
      }
    }
  }
  &-info{
    margin-top: 1rem;
    &-name{
      color: #fff;
      margin: 0;
      font-weight: bold;
      font-size: 1.5rem;
    }
    &-username{
      font-size: 1.2rem;
      color: $color-dark-gray;
    }
  }
  &-description{
    margin-top: 1rem;
    color: #fff;
  }
  &-created-at{
    margin-top: 1rem;
    display: flex;
    align-items: center;
    color: $color-dark-gray;
    a{
      color: $color-blue;
      &:hover{
        text-decoration: underline;
      }
    }
    span{
      display: flex;
      align-items: center;
      & + span{
        margin-left: 2rem;
      }
      svg{
        fill: $color-dark-gray;
        margin-right: .5rem;
        width: 1.2rem;
        height: 1.2rem;
      }
    }
  }
  &-follower-counts{
    display: flex;
    color: #fff;
    cursor: pointer;
    margin-top: 1rem;
    p{
      margin: 0;
      & + p{
        margin-left: 1rem;
      }
      span{
        color: $color-dark-gray;
      }
      &:hover{
        text-decoration: underline;
      }
    }
  }
}
</style>