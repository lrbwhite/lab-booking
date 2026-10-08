import request from '@/utils/request'

/**获取当前用户信息 */

export function getUserInfo() {
  return request({
    url:'/user/me',
    method:'get',
  })
}

/*修改当前用户信息 */

export function updateUserUserInfo(data) {
    return request({
        url:'/user/me',
        method:'put',
        data,
    })
}

/**修改当前用户密码 */
export function updatePassword(data) {
    return request({
        url:'/user/password',
        method:'put',
        data,
    })
}

/**分页模糊查询用户列表 */
export function getUserPageList(params) {
    return request({
        url:'/user/list',
        method:'get',
        params,
    })
}


/**新增用户 */
export function createUserApi(data) {
    return request({
        url:'/user',
        method:'post',
        data,
    })

}

/**更新用户 */
export function updateUserApi(user_id, data) {
    return request({
        url:`/user/${user_id}`,
        method:'put',
        data,
    })
}

/**删除用户 */
export function deleteUserApi(user_id) {
    return request({
        url:`/user/${user_id}`,
        method:'delete',
    })
}
