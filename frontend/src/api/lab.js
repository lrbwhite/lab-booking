import request from '@/utils/request'

/**获取当前用户信息 */

export function getLabInfo() {
  return request({
    url:'/lab/me',
    method:'get',
  })
}

/*修改当前用户信息 */

export function updateLabLabInfo(data) {
    return request({
        url:'/lab/me',
        method:'put',
        data,
    })
}

/**修改当前用户密码 */
export function updatePassword(data) {
    return request({
        url:'/lab/password',
        method:'put',
        data,
    })
}

/**分页模糊查询用户列表 */
export function getLabPageList(params) {
    return request({
        url:'/lab/list',
        method:'get',
        params,
    })
}


/**新增用户 */
export function createLabApi(data) {
    return request({
        url:'/lab',
        method:'post',
        data,
    })

}

/**更新用户 */
export function updateLabApi(lab_id, data) {
    return request({
        url:`/lab/${lab_id}`,
        method:'put',
        data,
    })
}

/**删除用户 */
export function deleteLabApi(lab_id) {
    return request({
        url:`/lab/${lab_id}`,
        method:'delete',
    })
}
