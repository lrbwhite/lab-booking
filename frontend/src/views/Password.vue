<template>
    <div style="width: 50%">
  <el-card>
   <template #header>
    <div style="font-size:16px;font-weight:bold">
     <span>用户信息</span>
    </div>
   </template> 
   <el-form ref="formRef" :rules="rules" :model="form" label-width="100px" style="width: 100%">
    <el-form-item label="原密码" prop="oldPassword">
        <el-input type="password" show-password v-model="form.oldPassword" placeholder="请输入原密码"/>
    </el-form-item>
    <el-form-item label="新密码" prop="newPassword">
        <el-input type="password" show-password v-model="form.newPassword" placeholder="请输入新密码"/>
    </el-form-item>
    <el-form-item label="确认新密码" prop="confirmNewPassword">
        <el-input type="password" show-password v-model="form.confirmNewPassword" placeholder="请确认新密码"/>
    </el-form-item>
    <el-form-item>
        <el-button type="primary" :loading="submitting" @click="handleSubmit">提交</el-button>
    </el-form-item>
    </el-form>
    </el-card>
    </div>
</template>

<script setup>
import {ref,reactive} from 'vue'
import {logout} from '@/utils/auth'
import {updatePassword} from '@/api/user'
import {ElMessage} from 'element-plus'
import router from '@/router'

const submitting = ref(false)
const formRef = ref()
const form=reactive({
    oldPassword:'',
    newPassword:'',
    confirmNewPassword:'',
})

const validatePass = (rule, value, callback) => {
    if (value === "") {
        callback(new Error('请确认密码'))
    } else {
        if (value !== form.newPassword) {
            callback(new Error('两次输入密码不一致'))
        } else {
            callback()
        }
    }
}

const rules = {
    oldPassword:[{required:true,message:'请输入原密码',trigger:'blur'}],
    newPassword:[{required:true,message:'请输入新密码',trigger:'blur'}],
    confirmNewPassword:[{validator:validatePass,message:'请确认新密码',trigger:'blur'}],
}

const handleSubmit = async () => {
    const valid = await formRef.value.validate().catch(()=>false)
    if (!valid) return
    submitting.value = true
    try {
        const res=await updatePassword({
            oldPassword:form.oldPassword,
            newPassword:form.newPassword,
        })
        if (res.code===200) {
            ElMessage.success('密码修改成功')
            logout()
            router.push({name:'login'})
        }
    } finally{
        submitting.value = false
    }


}

</script>
