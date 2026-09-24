<template><div class="home">
<AddTweet @submit-click="handleTweetSubmit"/><hr class="gap">
<p v-if="error" role="alert">{{error}}</p>
<p v-if="!tweetData.length && !error">Здесь появятся твиты пользователей, на которых вы подпишетесь. Свои записи смотрите в профиле.</p>
<Tweet v-for="tweet in tweetData" :key="tweet.id" :tweet-data="tweet" @delete-tweet="getTweets" @get-tweets="getTweets"/>
<div class="home__pagination"><button :disabled="page===1" @click="page--; getTweets()">Назад</button>
<span>Страница {{page}}</span><button :disabled="!hasMore" @click="page++; getTweets()">Далее</button></div>
</div></template><script>
import AddTweet from '@/components/AddTweet/index.vue';
import Tweet from '@/components/Tweet/index.vue';
import {getTweetsWithPagination} from '@/services/api.js';
export default {components:{AddTweet,Tweet},data(){return {tweetData:[],page:1,hasMore:false,error:''}},
computed:{limit(){return this.$store.state.isPaginationEnabled?this.$store.state.paginationLimit:10}},
watch:{limit(){this.page=1;this.getTweets()}},mounted(){this.getTweets()},methods:{
async handleTweetSubmit(){this.$router.push('/profile/'+this.$store.getters.getMyProfileId)},
async getTweets(){try {const {data}=await getTweetsWithPagination((this.page-1)*this.limit,this.limit);
this.tweetData=data.tweets;this.hasMore=data.tweets.length===this.limit;this.error='';
}catch(e){this.error=e.message;}}
}};</script><style scoped>

.home>p{padding:16px;color:#aab8c2}.home__pagination{display:flex;gap:16px;padding:16px;align-items:center;color:white}.gap{border:4px solid #38444d;margin:0}</style>