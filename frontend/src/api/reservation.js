import request from "@/utils/request"

export function createReservationApi(data) {
    return request({
        url: "/reservation",
        method: "post",
        data,
    })
}
