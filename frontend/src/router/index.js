import { createRouter, createWebHistory } from 'vue-router'
import { getToken } from '@/utils/auth'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {path:'/',redirect:'/manager/home'},
    {
      path:'/manager',
      name:'Layout',
      component:()=>import('@/layouts/Layouts.vue'),
      children:[
        {path:'home',name:'home',component:()=>import('@/views/home.vue')},
        {path:'lab',name:'lab',component:()=>import('@/views/Lab.vue')},
        {path:'equ',name:'equ',component:()=>import('@/views/Equ.vue')},
        {path:'user',name:'user',component:()=>import('@/views/User.vue')}
      ]
    },
    {path:'/login',name:'login',component:()=>import('@/views/login.vue') }
  ],
})

//路由守卫
router.beforeEach((to,from)=>{
  if(to.name==='login') {
    return true
  } else {
    return getToken() ? true : '/login'
  }
})


export default router
