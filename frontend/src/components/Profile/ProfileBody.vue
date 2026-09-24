<template><div class="profile-body">
<div class="sections"><div class="sections-item active">Твиты</div></div>
<p v-if="error" role="alert">{{error}}</p>
<p v-if="!userTweets.length && !error">У этого пользователя пока нет твитов.</p>
<Tweet v-for="tweet in userTweets" :key="tweet.id" :tweet-data="tweet" @delete-tweet="getTweets" @get-tweets="getTweets" />
<button v-if="hasMore" @click="getTweets(true)">Ещё твиты</button>
</div></template>
<script>
import Tweet from '@/components/Tweet/index.vue';
import axios from 'axios';
export default {components:{Tweet},data(){return {userTweets:[],error:'',hasMore:false}},
mounted(){this.getTweets()},methods:{async getTweets(more=false){
try {const offset=more===true?this.userTweets.length:0;
const {data}=await axios.get('/api/tweets',{params:{author_id:this.$route.params.profileId,offset,limit:100},headers:{'api-key':this.$store.state.currentUserApiKey}});
this.userTweets=offset?[...this.userTweets,...data.tweets]:data.tweets;
this.hasMore=data.tweets.length===100;this.error='';
this.$store.commit('setProfileTweetCount',this.userTweets.length);
}catch(e){this.error=e.response?.data?.error_message || 'Не удалось загрузить твиты';}
}}};
</script><style scoped>

.sections{border-bottom:1px solid #38444d;padding:20px;color:#1da1f2}.profile-body>p{padding:16px;color:#aab8c2}button{margin:16px;padding:10px}</style>