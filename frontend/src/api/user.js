import request from '@/utils/request'

/**获取当前用户信息 */

export function getUserInfo() {
  return request({
    url:'/user/info',
    method:'get',
  })
}

/*修改当前用户信息 */

export function updateUserUserInfo(data) {
    return request({
        url:'/user/update',
        method:'put',
        data,
    })
}
