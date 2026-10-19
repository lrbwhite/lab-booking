import request from "@/utils/request"

export function createReservationApi(data) {
    return request({
        url: "/reservation",
        method: "post",
        data,
    })
}


export function getReservationPageListApi(params) {
    return request({
        url: "/reservation/list",
        method: "get",
        params,
    })
}

export function cancelReservationApi(id) {
    return request({
        url: `/reservation/${id}/cancel`,
        method: "put",
    })
}
export function auditReservationApi(id,status) {
    return request({
        url: `/reservation/${id}/audit`,
        method: "put",
        data:{status}
    })
}