<template>
  <div>
    <el-card shadow="never" style="margin-bottom: 16px;">
      <div style="display:flex;justify-content: space-between; align-items: center; gap: 16px;">
        <div>
          <div style="font-size:18px; color:#333">欢迎您，{{userInfo?.username || '用户'}}</div>
          <div style="font-size:14px;color:#999">
            欢迎使用实验室预约系统，当前身份：{{ roleText }}
          </div>
        </div>
      </div>
    </el-card>

    <el-card shadow="never" style="margin-bottom: 16px;">
      <div style="display:flex;align-items: center; gap:50px">
        <div>
          开放的实验室<b style="margin-left: 5px; font-size:18px;">{{openLabcount}}</b>
        </div>
        <div>
          我的预约<b style="margin-left: 5px; font-size:18px;">{{reservationCount}}</b>
        </div>
      </div>
    </el-card>
    <div style="font-size:20px;font-weight:bold;margin-bottom:10px;">功能介绍</div>
    <el-card shadow="never" style="margin-bottom: 16px;">
      <el-row>
        <el-col :span="12" v-for="(item,index) in features" :key="index">
          <div class="feature-item">
            <div class="feature-title">{{ item.title }}</div>
            <div class="feature-desc">{{ item.desc }}</div>
          </div>
        </el-col>
      </el-row>
    </el-card>
  </div>
</template>

<script setup>
import { useUser } from '@/utils/user'
import { getLabPageList } from '@/api/lab'
import {getReservationPageList} from '@/api/reservation'
import { ref, computed, onMounted } from 'vue'
const {userInfo}=useUser()

const openLabcount=ref(0)
const reservationCount=ref(0)
const roleText = computed(() => ({ student: '学生', admin: '管理员' })[userInfo.value?.role] || '未知')

const features=[
   {
    title: '业务预约',
    desc: '实验室 / 设备浏览、提交预约、我的预约与管理员审核。'
  },
  {
    title: '实验室ai助手',
    desc: 'Tool Calling:查库、流式输出'
  }
]

onMounted(async()=>{
  try{
    const res=await getLabPageList({page:1,page_size:1,status:1})
    if (res.code===200)openLabcount.value=res.data?.total||0
    }catch{
      openLabcount.value=0
    }
  
  try{
    const res=await getReservationPageList({page:1,page_size:1,status:1})
    if (res.code===200)reservationCount.value=res.data?.total||0
    }catch{
      reservationCount.value=0
    }
  
})

</script>

<style scoped>
.feature-item {
  padding: 10px;
}
.feature-title {
  font-size: 16px;
  font-weight: 600;
  color: #333;
}
.feature-desc {
  margin-top: 8px;
  color: #666;
  font-size: 13px;
}
</style>