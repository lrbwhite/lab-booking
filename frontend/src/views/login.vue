<template>
  <div class="login-container">
    <div class="login-form">
      <h1>实验室预约系统</h1>
      <div class="subtitle" margin-top="12px;">基于langgraph的实验室预约系统</div>
       <el-form ref="formRef" :rules="rules" :model="form" label-width="auto" style="max-width: 600px">
        <el-form-item prop="username" label="用户名">
          <el-input size="medium" v-model="form.username" placeholder="请输入用户名" />
        </el-form-item>
        <el-form-item prop="password" label="密码">
          <el-input size="medium" v-model="form.password" type="password" placeholder="请输入密码" show-password />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" style="width: 100%" :loading="loadingValue" @click="loginClick">登录</el-button>
        </el-form-item>
      </el-form>
    </div>
  </div>
</template>


<script setup>
import { reactive,ref } from 'vue'
import { useRouter } from 'vue-router'
import { login } from '@/api/auth'
import { ElMessage } from 'element-plus'
import { useUser } from '@/utils/user'

const {saveLoginData}=useUser()

const router = useRouter()

const formRef = ref(null)

const form = reactive({
    username: '',
    password: ''
})

const rules = reactive({
    username: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
    password: [{ required: true, message: '请输入密码', trigger: 'blur' }],
})



const loadingValue=ref(false)
const loginClick = async () => {
    const valid=await formRef.value.validate().catch(()=>false)
    if (!valid) {
        return
    }
    loadingValue.value=true
    try {
        const res=await login(form)
        saveLoginData({ token: res.data.token, userInfo: res.data.user })
        ElMessage.success('登录成功')
        router.push('/manager/home')
    } finally {
        loadingValue.value=false
    }
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