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
                <el-button type="primary" @click="handleSearch">查询</el-button>
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
   </div>
</template>

<script setup>
import { ref,reactive,onMounted } from 'vue'
import { getUserPageList } from '@/api/user'

const params=reactive({
    page:1,
    pageSize:10,
    keywords:''
})

const loading=ref(false)
const tableData=ref([])

const total=ref(0)

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
