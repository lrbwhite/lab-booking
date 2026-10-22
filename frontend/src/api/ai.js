import request from '@/utils/request'

export function chatapi(data) {
  return request({
    url: '/ai/chat',
    method: 'post',
    data,
    timeout:30000
  })
}