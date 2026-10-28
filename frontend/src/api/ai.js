import { getToken, logout } from '@/utils/auth'
import router from '@/router'
import { ElMessage } from 'element-plus'

const BASE_URL = import.meta.env.VITE_API_BASE_URL

export async function chatStreamApi(data, handlers, signal) {
  const { onChunk = () => {}, onStatus = () => {} } = handlers || {}
  const token = getToken()
  const res = await fetch(`${BASE_URL}/ai/chat/stream`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
    },
    body: JSON.stringify(data),
    signal,
  })

  if (res.status === 401) {
    logout()
    router.push('/login')
    throw new Error('登录已过期')
  }

  if (!res.ok) {
    let msg = '请求失败'
    try {
      const err = await res.json()
      msg = err.msg || msg
    } catch (e) {
      // 响应体不是 JSON，用默认文案
    }
    ElMessage.error(msg)
    throw new Error(msg)
  }

  const reader = res.body.getReader()
  const decoder = new TextDecoder('utf-8')
  let buffer = ''

  while (true) {
    const { done, value } = await reader.read()
    if (done) break
    buffer += decoder.decode(value, { stream: true })

    const events = buffer.split('\n\n')
    buffer = events.pop()

    for (const event of events) {
      for (const line of event.split('\n')) {
        if (!line.startsWith('data:')) continue
        const payload = line.slice(5).trim()
        if (!payload) continue
        if (payload === '[DONE]') return
        const { type = 'content', content = '' } = JSON.parse(payload)
        if (!content) continue
        if (type === 'status') onStatus(content)
        else if (type === 'content') onChunk(content)
      }
    }
  }
}