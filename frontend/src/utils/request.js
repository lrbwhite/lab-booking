import axios from 'axios'
import {getToken,logout} from './auth'
import router from '@/router'
import {ElMessage} from 'element-plus'

const service=axios.create({
    baseURL:import.meta.env.VITE_API_BASE_URL,
    timeout:30000
})

//请求拦截器
service.interceptors.request.use(
  config => {
    // 在发送请求之前做些什么
    const token=getToken()
    if(token) {
        config.headers['Authorization']=`Bearer ${token}`
    }
    return config
  },
  error => {
    // 对请求错误做些什么
    return Promise.reject(error)
  }
)

//返回的拦截器
service.interceptors.response.use(
    (res)=>{
    const data=res.data
    if(data.code===401) {
        logout()
        router.push('/login')
        return Promise.reject(data)
    }
    if(data.code !==200) {
        ElMessage.error(data.msg||'请求失败')
        return Promise.reject(data)
    }
    return data
},(error)=>{
   if(error.response) {
    const httpStatus=error.response.status
    if (httpStatus ===401) {
        logout()
        router.push('/login')
    }
    else {
        ElMessage.error(error.response.data.msg||'请求失败')

    }

}
    else {
        //后端没启动，网络异常了
        ElMessage.error('后端没启动，网络异常了')
    }
    return Promise.reject(error)
}
)

export default service
