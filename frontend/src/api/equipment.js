import request from '@/utils/request'

/**获取当前用户信息 */

export function getEquipmentInfo() {
  return request({
    url:'/equipment/me',
    method:'get',
  })
}

/*修改当前用户信息 */

export function updateEquipmentInfo(data) {
    return request({
        url:'/equipment/me',
        method:'put',
        data,
    })
}

/**修改当前用户密码 */
export function updatePassword(data) {
    return request({
        url:'/equipment/password',
        method:'put',
        data,
    })
}

/**分页模糊查询用户列表 */
export function getEquipmentPageList(params) {
    return request({
        url:'/equipment/list',
        method:'get',
        params,
    })
}


/**新增用户 */
export function createEquipmentApi(data) {
    return request({
        url:'/equipment',
        method:'post',
        data,
    })

}

/**更新用户 */
export function updateEquipmentApi(equipment_id, data) {
    return request({
        url:`/equipment/${equipment_id}`,
        method:'put',
        data,
    })
}

/**删除用户 */
export function deleteEquipmentApi(equipment_id) {
    return request({
        url:`/equipment/${equipment_id}`,
        method:'delete',
    })
}
