<template>
    <div> 
        <el-card>
             <template #header>
                <div style="font-size:16px;font-weight:bold">
                <span>实验室设备管理</span>
                </div>
             </template> 
             <div style="margin-bottom:10px;">
                <el-input 
                placeholder="请输入实验室名称查询" 
                v-model="params.keywords" 
                style="width:240px; margin-right:10px" 
                clearable
                @keyup.enter="handleSearch"
                @clear="handleSearch"
                />
                <el-select 
                    placeholder="请选择实验室"
                    v-model="params.lab_id"
                    style="width:200px; margin-right:8px"
                    clearable
                    @change="handleSearch"
                    @clear="handleSearch"
                >
                    <el-option v-for="item in equipmentOptions" :key="item.id" :value="item.id" :equipmentel="item.name">
                    </el-option>
                </el-select>
                <el-button type="primary" :icon="Search" @click="handleSearch">查询</el-button>
                <el-button type="success" :icon="Plus" @click="handleCreate">新增</el-button>
             </div>

             <el-table :header-cell-style="{background:'#f5f7fa'}" :data="tableData" style="width: 100%" v-model="loading">
               <el-table-column prop="lab_name" label="所属实验室" />
                <el-table-column prop="name" label="名称" />
                <el-table-column prop="spec" label="型号规格" />
                <el-table-column prop="quantity" label="数量" />
                <el-table-column prop="status" label="状态" width="100" >
                    <template #default="{row}">
                        <el-tag :type="row.status==='1'?'success':'danger'">
                        {{row.status==='1'?'正常':'维修'}}
                        </el-tag>
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
            equipmentel-width="100px" 
            style="width: 100%;padding-right: 20px;padding-top: 20px;">
                <el-form-item equipmentel="名称" prop="name">
                    <el-input v-model="form.name" placeholder="请输入名称"/>
                </el-form-item>
                <el-form-item equipmentel="描述">
                    <el-input type="textarea" v-model="form.description" placeholder="请输入描述"/>
                </el-form-item>
                <el-form-item equipmentel="位置">
                    <el-input type="textarea" v-model="form.location" placeholder="请输入位置"/>
                </el-form-item>
                <el-form-item equipmentel="容量" prop="capacity">
                    <el-input-number :min="1" v-model="form.capacity" placeholder="请输入容量"/>
                </el-form-item>
                <el-form-item equipmentel="开放时间">
                     <el-time-picker
                      v-model="form.open_time"
                      format="HH:mm"
                      value-format="HH:mm"
                      placeholder="开放时间"
                      style="width:140px;margin-right:8px"
                      />
                      <el-time-picker
                      v-model="form.close_time"
                      format="HH:mm"
                      value-format="HH:mm"
                      placeholder="关闭时间"
                      style="width:140px"
                      />
                </el-form-item>
                <el-form-item equipmentel="状态">
                    <el-radio-group v-model="form.status">
                        <el-radio equipmentel="1">开启</el-radio>
                        <el-radio equipmentel="0">关闭</el-radio>
                    </el-radio-group>
                </el-form-item>
            </el-form>
            <template #footer>
                <el-button @click="dialogVisible=false">取消</el-button>
                <el-button type="primary" :loading="formLoading" @click="handleSave">确定</el-button>
            </template>
        </el-dialog>
   </div>
</template>

<script setup>
import { ref,reactive,onMounted } from 'vue'
import { getEquipmentPageList, updateEquipmentApi, createEquipmentApi, deleteEquipmentApi } from '@/api/equipment'
import { Search,Plus } from '@element-plus/icons-vue'
import { ElButton ,ElMessage,ElMessageBox} from 'element-plus'

const params=reactive({
    page:1,
    pageSize:10,
    keywords:'',
    lab_id:null
})

const loading=ref(false)
const tableData=ref([])
const equipmentOptions=ref([])
const total=ref(0)
const dialogVisible=ref(false)
const formRef=ref()
const form =reactive({
    name:'',
    description:'',
    location:'',
    capacity:1,
    open_time:'',
    close_time:'',
    status:'1'
})

const formLoading=ref(false)

const rules = {
  name:[{required:true,message:'请输入名称',trigger:'blur'}],
  capacity:[{required:true,message:'请输入容量',trigger:'blur'}],
}

const resetForm=()=>{
    Object.assign(form,{
        id:'',
        name:'',
        description:'',
        location:'',
        capacity:20, 
        open_time:'08:00',
        close_time:'20:00',
        status:'1'
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
        name:row.name,
        description:row.description,
        location:row.location,
        capacity:row.capacity,
        open_time:row.open_time,
        close_time:row.close_time,
        status:row.status
    })
    dialogVisible.value=true
}

//删除实验室
const handleDelete=(row)=>{
    ElMessageBox.confirm(`确认删除实验室[${row.name}]?`,'提示',{type:'warning'}).then(
        async()=>{
            const res=await deleteEquipmentApi(row.id)
            if(res.code===200){
                ElMessage.success('操作成功')
                load()
            }
        }
    ).catch(()=>{})
}

//保存实验室  
const handleSave=async()=>{
    const valid=await formRef.value.validate().catch(()=>false)
    if (!valid) return
    formLoading.value=true
    try {
        const res=form.id? await updateEquipmentApi(form.id, form):await createEquipmentApi(form)
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
        const res=await getEquipmentPageList({
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

const loadequipments=async()=>{
    const res=await getEquipmentPageList({page:1,page_size:100})
    if(res.code===200){
        equipmentOptions.value=res.data?.list
    }

}

onMounted(()=>{
    loadequipments()
    load()
})
</script>
