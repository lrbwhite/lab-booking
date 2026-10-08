<template>
    <div> 
        <el-card>
             <template #header>
                <div style="font-size:16px;font-weight:bold">
                <span>用户管理</span>
                </div>
             </template> 
             <div style="margin-bottom:10px;">
                <el-input 
                placeholder="请输入账号查询" 
                v-model="params.keywords" 
                style="width:240px; margin-right:10px" 
                clearable
                @keyup.enter="handleSearch"
                @clear="handleSearch"
                />
                <el-button type="primary" :icon="Search" @click="handleSearch">查询</el-button>
                <el-button type="success" :icon="Plus" @click="handleCreate">新增</el-button>
             </div>

             <el-table :header-cell-style="{background:'#f5f7fa'}" :data="tableData" style="width: 100%" v-model="loading">
                <el-table-column prop="username" label="账号" />
                <el-table-column prop="name" label="名称" />
                <el-table-column prop="email" label="邮箱" />
                <el-table-column prop="phone" label="手机号" />
                <el-table-column prop="role" label="角色" width="100" >
                    <template #default="{row}">
                        {{row.role==='admin'?'管理员':'学生'}}
                    </template>
                </el-table-column>
                <el-table-column label="操作" width="160" >
                    <template #default="{row}">
                        <el-button type="primary" text bg @click="handleEdit(row)">编辑</el-button>
                        <el-button type="danger" text bg @click="handleDelete(row)">删除</el-button>
                    </template>
                </el-table-column>
             </el-table>
             <div style="margin-top:10px; display:flex;justify-content: flex-end;">
                <el-pagination 
                v-model:current-page="params.page" 
                v-model:page-size="params.pageSize"
                :total="total"
                 background 
                 layout="prev,pager,next,total"
                 @current-change="load"
                  />
             </div>
        </el-card>

        <el-dialog v-model="dialogVisible" :title="form.id ?'编辑用户':'新增用户'" width="450">
            <el-form 
            ref="formRef" 
            :rules="rules" 
            :model="form" 
            label-width="100px" 
            style="width: 100%;padding-right: 20px;padding-top: 20px;">
                <el-form-item label="账号" prop="username">
                    <el-input :disabled="!!form.id"  v-model="form.username" placeholder="请输入账号"/>
                </el-form-item>
                <el-form-item label="密码" prop="password">
                    <el-input type="password" show-password v-model="form.password" placeholder="请输入密码"/>
                </el-form-item>
                <el-form-item label="名称" prop="name">
                    <el-input v-model="form.name" placeholder="请输入名称"/>
                </el-form-item>
                <el-form-item label="角色" prop="role">
                    <el-select v-model="form.role">
                        <el-option label="管理员" value="admin" />
                        <el-option label="学生" value="student" />
                    </el-select>
                </el-form-item>
                <el-form-item label="邮箱" prop="email">
                    <el-input v-model="form.email" placeholder="请输入邮箱"/>
                </el-form-item>
                <el-form-item label="手机号" prop="phone">
                    <el-input v-model="form.phone" placeholder="请输入手机号"/>
                </el-form-item>
            </el-form>
            <template #footer>
                <el-button>取消</el-button>
                <el-button type="primary" :loading="formLoading" @click="handleSave">确定</el-button>
            </template>
        </el-dialog>
   </div>
</template>

<script setup>
import { ref,reactive,onMounted } from 'vue'
import { getUserPageList, updateUserApi, createUserApi, deleteUserApi } from '@/api/user'
import { Search,Plus } from '@element-plus/icons-vue'
import { ElButton ,ElMessage,ElMessageBox} from 'element-plus'

const params=reactive({
    page:1,
    pageSize:10,
    keywords:''
})

const loading=ref(false)
const tableData=ref([])
const total=ref(0)
const dialogVisible=ref(false)
const formRef=ref()
const form =reactive({
    username:'',
    name:'',
    role:'student',
    email:'',
    phone:'',
    avatar:''
})

const formLoading=ref(false)

const rules = {
    username:[{required:true,message:'请输入账号',trigger:'blur'}],
    password:[{required:true,message:'请输入密码',trigger:'blur'}
        ,{min:3,max:10,message:'密码长度必须在3-10位之间',trigger:'blur'}
    ],
    name:[{required:true,message:'请输入用户名',trigger:'blur'}],
    email:[{type:'email',message:'邮箱格式错误',trigger:'blur'}],
    phone:[{pattern:/^1[3-9]\d{9}$/,message:'手机号格式错误',trigger:'blur'}],
}

const resetForm=()=>{
    Object.assign(form,{
        id:'',
        username:'',
        name:'',
        role:'student',
        email:'',
        phone:'',
        avatar:''
    })
}

const handleCreate=()=>{
    resetForm()
    dialogVisible.value=true
}

const handleEdit=(row)=>{
    resetForm()
    Object.assign(form,{
        id:row.id,
        username:row.username,
        name:row.name,
        role:row.role,
        email:row.email,
        phone:row.phone,
        avatar:row.avatar
    })
    dialogVisible.value=true
}

//删除用户
const handleDelete=(row)=>{
    ElMessageBox.confirm(`确认删除用户[${row.name}]?`,'提示',{type:'warning'}).then(
        async()=>{
            const res=await deleteUserApi(row.id)
            if(res.code===200){
                ElMessage.success('操作成功')
                load()
            }
        }
    ).catch(()=>{})
}

//保存用户
const handleSave=async()=>{
    const valid=await formRef.value.validate().catch(()=>false)
    if (!valid) return
    formLoading.value=true
    try {
        const res=form.id? await updateUserApi(form):await createUserApi(form)
        if(res.code===200){
            dialogVisible.value=false
            ElMessage.success('操作成功')
            load()
        }
    } finally{
        formLoading.value=false
    }
}




//加载分页数据
const load=async()=>{
    loading.value=true
    try {
        const res=await getUserPageList({
            page: params.page,
            page_size:params.pageSize,
            keywords:params.keywords
    })
    if(res.code===200){
        tableData.value=res.data.list
        total.value=res.data.total
    }
    }finally{
        loading.value=false
    }
}

const handleSearch=async()=>{
    params.page=1
    load()
}

onMounted(()=>{
    load()
})
</script>
