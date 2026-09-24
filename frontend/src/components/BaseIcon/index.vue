<template>
  <component :is="iconComponent" />
</template>

<script>

const icons = import.meta.glob('./icons/*.vue', {eager:true, import:'default'});
export default {
  name: 'BaseIcon',
  props: {
    icon: {
      type: String,
      default: 'home'
    },
  },
  computed: {
    iconComponent(){
      return icons[`./icons/${this.icon}.vue`]
    }
  }
}
</script>

<style>



</style>