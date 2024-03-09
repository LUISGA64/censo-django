import Vue from 'vue'
import Router from 'vue-router'
import HelloWorld from '@/components/HelloWorld'

import ListSidewalk from "@/components/Sidewalk/ListSidewalk";

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'HelloWorld',
      component: HelloWorld
    },
    {
      path: '/sidewalks',
      name: 'Sidewalks',
      component: ListSidewalk
    }
  ],
  mode: 'history'
})
