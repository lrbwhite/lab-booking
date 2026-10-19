<template>
    <div>
        <el-card>
             <template #header>
                <div style="font-size:16px;font-weight:bold">
                    <span>我的预约记录</span>
                </div>
             </template>
             <div style="margin-bottom:10px">
                <el-select 
                    placeholder="请选择预约状态"
                    v-model="params.status"
                    style="width:200px; margin-right:8px"
                    clearable
                    @change="handleSearch"
                    @clear="handleSearch"
                >
                    <el-option :value="0" :label="待审核" />
                    <el-option :value="1" :label="已通过" />
                    <el-option :value="2" :label="已拒绝" />
                    <el-option :value="3" :label="已取消" />
                </el-select>
             </div>
             <el-table :header-cell-style="{background:'#f5f7fa'}" :data="tableData" style="width: 100%" v-loading="loading">
                <el-table-column prop="lab_name" label="实验室" />
                <el-table-column label="预约类型" >
                    <template #default="row">
                        <el-tag :type="row.type=='实验室'?'success':'primary'">{{row.type}}</el-tag>
                    </template>
                </el-table-column>
                <el-table-column label="设备" >
                    <template #default="row">
                        {{row.equipment_name||'-'}}
                    </template>
                </el-table-column>
                <el-table-column prop="date" label="日期" />
                <el-table-column label="预约时段" >
                    <template #default="row">
                        {{row.start_time}}-{{row.end_time}}
                    </template>
                </el-table-column>
                <el-table-column prop="remark" label="备注" />
                <el-table-column label="预约状态" width="100">
                    <template #default="row">
                        <el-tag :type="statusType(row.status)">{{statusText(row.status)}}</el-tag>
                    </template>
                </el-table-column>
                <el-table-column label="操作" width="100">
                    <template #default="row">
                        <el-button type="danger" text bg v-if="row.status==0" @click="handleCancel(row)">
                            取消</el-button>
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
import { onMounted, ref, reactive } from 'vue'
import { getReservationPageListApi,cancelReservationApi } from '@/api/reservation'
import { ElMessage,ElMessageBox } from 'element-plus'

const statusType=(status)=>{
    return {0:'warning',1:'success',2:'danger',3:'info'}[status]
}
const statusText=(status)=>{
    return {0:'待审核',1:'已通过',2:'已拒绝',3:'已取消'}[status]
}

const loading=ref(false)
const tableData=ref([])
const params=reactive({
    page:1,
    page_size:10,
    status:null
})
const total=ref(0)

const load =async ()=>{
    loading.value=true
    try{
        const res=await getReservationPageListApi(params)
        if(res.code==200){
            tableData.value=res.data?.list
            total.value=res.total?.total
        }
    }finally{
        loading.value=false
    }    
}

const handleCancel=async (row)=>{
    ElMessageBox.confirm(`确定取消[${row.lab_name}]预约吗？`, '确认取消', {type:'warning'
    }).then(async () => {
        const res=await cancelReservationApi(row.id)
    if(res.code==200){
        ElMessage.success('取消成功')
        load()
    }
    })
}

const handleSearch=()=>{
    params.page=1
    load()
}


onMounted(()=>{
    load()
})
</script>