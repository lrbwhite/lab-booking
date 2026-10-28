<template>
  <div class="common-layout">
    <el-container style="min-height: 100vh;">
      <el-header style="display: flex; align-items: center; border-bottom: 1px solid #ddd;background-color: #fff;">
        <div style="display: flex; align-items:center;font-size: 24px;font-weight: bold;">实验室预约系统</div>

        <el-dropdown style="margin-left: auto;" placement="bottom-end">
          <el-button> 用户中心 </el-button>
          <template #dropdown>
            <el-dropdown-menu>
              <el-dropdown-item @click="handleProfile">用户信息</el-dropdown-item>
              <el-dropdown-item @click="handleLogout">退出登录</el-dropdown-item>
              <!-- <el-dropdown-item>The Action 3rd</el-dropdown-item> -->
            </el-dropdown-menu>
          </template>
        </el-dropdown>

      </el-header>
      <el-container>
        <el-aside width="220px">
          <el-menu router :default-active="router.currentRoute.value.path" style="height: 100%" default-active="/manager/home">
            <el-menu-item index="/manager/home">首页</el-menu-item>
            <el-menu-item index="/manager/ai-chat">AI助手</el-menu-item>
            <el-menu-item index="/manager/lablist" v-if="userInfo?.role==='student'">实验室列表</el-menu-item>
            <el-menu-item index="/manager/my-reservation" v-if="userInfo?.role==='student'">我的预约</el-menu-item>
            <el-menu-item index="/manager/lab" v-if="userInfo?.role==='admin'">实验室管理</el-menu-item>
            <el-menu-item index="/manager/equipment" v-if="userInfo?.role==='admin'">设备管理</el-menu-item>
            <el-menu-item index="/manager/audit-reservation" v-if="userInfo?.role==='admin'">预约审核</el-menu-item>
            <el-menu-item index="/manager/user" v-if="userInfo?.role==='admin'">用户管理</el-menu-item>
          </el-menu>
        </el-aside>
        <el-main>
          <router-view/>
        </el-main>
      </el-container>
    </el-container>
  </div>
</template>

<script setup>
import { logout } from '@/utils/auth'
import router from '@/router'
import {useUser} from '@/utils/user'
const {userInfo}=useUser()

const handleProfile=()=>{
    router.push('/manager/profile')
}

const handleLogout=()=>{
    logout()
    router.push('/login')
}
</script>


