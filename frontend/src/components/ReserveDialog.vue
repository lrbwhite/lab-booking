<template>
    <div>
         <el-dialog 
            :model-value="visible" 
            title="预约" 
            width="450"
            @open="formRef.resetFields()" 
            @close="emit('update:visible', false)">
            <el-form 
            ref="formRef" 
            :rules="rules" 
            :model="form" 
            label-width="100px" 
            style="width: 100%;padding-right: 30px;padding-top: 16px;">
                <el-form-item label="实验室">
                    <el-input :model-value="labName" disabled/> 
                </el-form-item>
                <el-form-item label="设备">
                    <el-input :model-value="equipmentName" disabled/> 
                </el-form-item>
                <el-form-item label="预约时间" prop="date">
                    <el-date-picker
                        v-model="form.date"
                        type="date"
                        format="yyyy-MM-dd"
                        value-format="yyyy-MM-dd"
                        placeholder="请选择日期"
                        style="width: 100%"
                    />
                </el-form-item>
                <el-form-item label="开始时间" prop="start_time">
                    <el-time-picker
                        v-model="form.start_time"
                        value-format="HH:mm"
                        format="HH:mm"
                        placeholder="请选择开始时间"
                    />
                </el-form-item>
                <el-form-item label="结束时间" prop="end_time">
                    <el-time-picker
                        v-model="form.end_time"
                        value-format="HH:mm"
                        format="HH:mm"
                        placeholder="请选择结束时间"
                    />
                </el-form-item>
                <el-form-item label="备注">
                    <el-input type="textarea" v-model="form.remark" placeholder="请输入备注" />
                </el-form-item>    
            </el-form>
            <template #footer>
                    <el-button @click="emit('update:visible', false)">取消</el-button>
                    <el-button type="primary" :loading="submitLoading" @click="handleSubmit">确认</el-button>
                </template>
        </el-dialog>
    </div>
</template>

<script setup>
import { ref,reactive } from "vue"
import { ElMessage } from "element-plus"
import { createReservationApi } from "@/api/reservation"


const props = defineProps({
    visible: Boolean,
    labId: Number,
    labName: String,
    equipmentId: Number,
    equipmentName: String,
})
const emit=defineEmits(["update:visible"])

const formRef = ref()
const form = reactive({
    date: "",
    start_time: "9:00",
    end_time: "18:00",
    remark: ""
})
const submitLoading=ref(false)
const rules = reactive({
    date: [{ required: true, message: "请选择日期", trigger: "change" }],
    start_time: [{ required: true, message: "请选择开始时间", trigger: "change" }],
    end_time: [{ required: true, message: "请选择结束时间", trigger: "change" }]
})

const handleSubmit=async()=>{
    const valid=await formRef.value.validate().catch(()=>false)
    if(!valid)return
    submitLoading.value=true
    try{
        const res=await createReservationApi({
            lab_id: props.labId,
            equipment_id: props.equipmentId,
            date: form.date,
            start_time: form.start_time,
            end_time: form.end_time,
            remark: form.remark,
        })
        if(res.code===200){
            ElMessage.success("预约已提交，请等待审核")
            emit("update:visible", false)
        }
    }finally{
        submitLoading.value=false
    }

}
 
</script>
