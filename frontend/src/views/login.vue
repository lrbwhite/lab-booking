<template>
  <div class="login-container">
    <div class="login-form">
      <h1>实验室预约系统</h1>
      <div class="subtitle" margin-top="12px;">基于langgraph的实验室预约系统</div>
       <el-form :model="form" label-width="auto" style="max-width: 600px">
        <el-form-item label="用户名">
          <el-input size="medium" v-model="form.username" placeholder="请输入用户名" />
        </el-form-item>
        <el-form-item label="密码">
          <el-input size="medium" v-model="form.password" type="password" placeholder="请输入密码" show-password />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" style="width: 100%" @click="login">登录</el-button>
        </el-form-item>
      </el-form>
    </div>
  </div>
</template>


<script setup>
import { reactive } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'

const router = useRouter()

const form = reactive({
    username: '',
    password: ''
})

const login = () => {
    if (!form.username || !form.password) {
        ElMessage.warning('请输入用户名和密码')
        return
    }
    // TODO: 后端登录接口就绪后改为调用接口校验，成功后再跳转
    router.push('/manager/home')
}
</script>

<style scoped>
.login-container{
    height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
}

.login-form{
    width: 300px;
    min-height: 400px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    gap: 12px;
    box-shadow:0 0 10px rgba(0,0,0,0.1);
    background-color: #f5f5f5;
    border-radius: 5px;
    padding: 20px;
}

.login-form h1{
    font-size: 22px;
}

.subtitle{
    font-size: 13px;
    color: #888;
}

</style>