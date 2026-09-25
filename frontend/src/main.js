import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import ElementPus from 'element-plus'
import 'element-plus/dist/index.css'
import zhCn from 'element-plus/es/locale/lang/zh-cn'
// ========== 图标全部导入 ==========
import * as ElementPlusIconsVue from '@element-plus/icons-vue'
import '@/assets/css/global.css'

const app = createApp(App)

// 使用element-plus
app.use(router)

app.use(ElementPlus, {
  locale: zhCn
})

// ========== 循环注册所有图标 ==========
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
  app.component(key, component)
}

app.mount('#app')
