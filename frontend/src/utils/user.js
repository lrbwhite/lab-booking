//仅供页面setup函数使用

 import {ref} from 'vue'
 import { getUserInfo,setToken,setUserInfo } from './auth'

 const userInfo=ref(getUserInfo())//响应式对象

 export function useUser() {
    function saveLoginData(data) {
        setToken(data.token)
        setUserInfo(data.userInfo)
        userInfo.value=data.userInfo
    }

   function updateUser(user) {
    setUserInfo(user)
    userInfo.value=user
   }

   function reloadUser() {
    userInfo.value=getUserInfo()
   }

   return {
    saveLoginData,
    updateUser,
    reloadUser,
    userInfo
   }

 }
