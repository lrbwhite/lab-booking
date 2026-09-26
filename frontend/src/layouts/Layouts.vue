<template>
  <div class="common-layout">
    <el-container style="min-height: 100vh;">
      <el-header style="display: flex; border-bottom: 1px solid #ddd;background-color: #fff;">
        <div style="display: flex; align-items:center;font-size: 24px;font-weight: bold;">实验室预约系统</div>
      </el-header>
      <el-container>
        <el-aside width="220px">
          <el-menu router style="height: 100%" :default-active="$route.path">
            <el-menu-item index="/manager/home">首页</el-menu-item>
            <el-menu-item index="/manager/lab">实验室预约</el-menu-item>
            <el-menu-item index="/manager/equ">设备管理</el-menu-item>
            <el-menu-item index="/manager/user">用户管理</el-menu-item>
          </el-menu>
        </el-aside>
        <el-main>
          <router-view/>
        </el-main>
      </el-container>
    </el-container>
  </div>
</template>

