<template>
    <div>
        <el-card>
             <template #header>
                <div style="font-size:16px;font-weight:bold">
                <span>实验室设备管理</span>
                </div>
             </template>

             <div 
             ref="listRef"
             style="height: 480px;
             overflow-y: auto;
             padding: 8px 4px; 
             background-color: #fafafa;
             border-radius: 6px;">
                <div 
                v-for="(item,index) in messages"
                :key="index"
                :style="{
                    display:'flex',
                    justifyContent:item.role==='user'?'flex-end':'flex-start',
                    marginBottom:'12px'
                }">
                    <div :style="{
                        maxWidth:'70%',
                        padding:'10px 12px',
                        borderRadius:'8px',
                        backgroundColor:item.role==='user'?'#409eff':'#fff',
                        color:item.status&&!item.content?'#999':(item.role==='user'?'#fff':'#333'),
                        fontStyle:item.status&&!item.content?'italic':'normal',
                        whiteSpace:'pre-wrap',
                        lineHeight:'1.6',
                        boxShadow:'0 1px 2px rgba(0,0,0,0.06)'
                    }">
                        {{item.content||item.status}}
                    </div>
                </div>
             </div>
             <!-- 输入框 -->
             <div style="margin-top:12px; display:flex; gap:8px; align-items:flex-end;">
                <el-input 
                v-model="input" 
                type="textarea"
                :rows="2"
                placeholder="问问实验室怎么预约，开放时间..." 
                @keydown.enter.exact.prevent="handleSend"></el-input>
                <el-button type="primary" @click="handleSend" :loading="loading">发送</el-button>
             </div>
        </el-card>
    </div>
</template>

<script setup>
import {ref,reactive,nextTick,onMounted,onBeforeUnmount} from 'vue'
import { chatStreamApi } from '@/api/ai'

const messages = ref([
    {
        role:'assistant',
        content:'你好，我是实验室管理助手。你可以向我咨询实验室设备管理相关问题。具体实验室信息请到【实验室列表】页查看。'
    }
])

const loading=ref(false)

let controller=null

const input=ref('')

const listRef=ref()

const scrollToBottom = () => {
  nextTick(() => {
    const elem = listRef.value
    if (elem) elem.scrollTop = elem.scrollHeight
  })
}

onBeforeUnmount(() => {
    if (controller) controller.abort()
})

const handleSend=async()=>{
    const text=input.value.trim()
    if(!text||loading.value) return
    messages.value.push({
        role:'user',
        content:text
    })
    input.value=''
    loading.value=true
    scrollToBottom()
    const history=messages.value
        .filter((item)=>item.role==='user'||item.role==='assistant')
        .map((item)=>({role:item.role,content:item.content}))
    const reply=reactive({role:'assistant',content:'',status:''})
    messages.value.push(reply)
    controller=new AbortController()
    try {
        await chatStreamApi({message:history},{
            onChunk:(chunk)=>{
                reply.status=''
                reply.content+=chunk
                scrollToBottom()
            },
            onStatus:(text)=>{
                reply.status=text
                scrollToBottom()
            }
        },controller.signal)
    } catch(e) {
        if(e.name!=='AbortError'&&!reply.content){
            reply.status=''
            reply.content='抱歉，服务暂时不可用，请稍后再试。'
        }
    } finally {
        controller=null
        loading.value=false
    }
}

</script>