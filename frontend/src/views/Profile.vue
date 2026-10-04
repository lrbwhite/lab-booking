<template>
 <div style="width: 50%">
  <el-card>
   <template #header>
    <div style="font-size:16px;font-weight:bold">
     <span>用户信息</span>
    </div>
   </template> 
   <el-form ref="formRef" :rules="rules" :model="form" label-width="100px" style="width: 100%">
    <el-form-item label="账号">
        <el-input disabled v-model="form.username" placeholder="请输入账号"/>
    </el-form-item>
    <el-form-item label="名称" prop="name">
        <el-input v-model="form.name" placeholder="请输入名称"/>
    </el-form-item>
    <el-form-item label="角色">
        <el-input disabled v-model="roleLabel"/>
    </el-form-item>
    <el-form-item label="邮箱" prop="email">
        <el-input v-model="form.email" placeholder="请输入邮箱"/>
    </el-form-item>
    <el-form-item label="手机号" prop="phone">
        <el-input v-model="form.phone" placeholder="请输入手机号"/>
    </el-form-item>
    <el-form-item>
        <el-button type="primary" :loading="submitting" @click="handleSubmit">提交</el-button>
    </el-form-item>



   </el-form>
  </el-card>
 </div>
</template>

<script setup>
import { ref,reactive,onMounted,computed } from 'vue'
import { ElMessage } from 'element-plus'
import { getUserInfo, updateUserUserInfo } from '@/api/user'
import {useUser} from '@/utils/user'

const {updateUser,userInfo}=useUser()


const loading = ref(false)
const submitting = ref(false)
const formRef = ref()

const form = ref({
  username:'',
  name:'',
  email:'',
  phone:'',
  avatar:'',
})

const rules = {
    name:[{required:true,message:'请输入用户名',trigger:'blur'}],
    email:[{type:'email',message:'邮箱格式错误',trigger:'blur'}],
    phone:[{pattern:/^1[3-9]\d{9}$/,message:'手机号格式错误',trigger:'blur'}],
}

const roleLabel = computed(()=>{
    // 后端 role 存的是中文："管理员"/"学生"，兼容英文码
    const roleMap = { '管理员':'管理员', '学生':'学生', 'admin':'管理员', 'student':'学生' }
    return roleMap[form.value.role] || '未知角色'
})

const loadUserInfo = async () => {
    loading.value = true
    try{
        const res=await getUserInfo()
        if(res.code===200){
           Object.assign(form.value,res.data)
        }
    }finally{
        loading.value = false
    }
}

//发送请求更新用户信息
const handleSubmit=async ()=>{
    const valid=await formRef.value.validate().catch(()=>false)
    if (!valid) return
    submitting.value=true
    try{
        //后端 UserUpdater 只接受 name/email/phone
        const payload={ name:form.value.name, email:form.value.email, phone:form.value.phone }
        const res=await updateUserUserInfo(payload)
        if(res.code===200){
            updateUser({ ...userInfo.value, ...payload })//同步本地存储的用户信息
            ElMessage.success('更新成功')
        }
    }finally{
        submitting.value=false
    }
}

onMounted(() => {
    loadUserInfo()
})
</script>



<style scoped></style>


