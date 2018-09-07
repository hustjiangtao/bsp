import axios from 'axios';

function checkStatus (response) {
  // loading
  // 如果http状态码正常，则直接返回数据
  if (response && (response.status === 200 || response.status === 304 || response.status === 400)) {
    return response
    // 如果不需要除了data之外的数据，可以直接 return response.data
  }
  // 异常状态下，把错误信息返回去
  return {
    status: -404,
    msg: '网络异常'
  }
}

function checkCode (res) {
  // 如果code异常(这里已经包括网络错误，服务器错误，后端抛出的错误)，可以弹出一个错误提示，告诉用户
  if (res.status === -404) {
    console.log(res.data);
    // alert(res.msg)
  }
  if (res.data && (!res.data.success)) {
    console.log(res.data);
    // alert(res.data.error_msg);
  }
  return res
}

class request {
  // Axios default headers
  static headers () {
    return {
      'X-Requested-With': 'XMLHttpRequest',
      // 'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
    }
  }
  // Send Ajax Request
  static do_send (url, params, method) {
    const base_url = 'http://localhost:5000/api';
    const timeout = 10000;
    const headers = Object.assign(this.headers(), params.headers);
    const data = params.data || {};
    return axios({
      method: method,
      baseURL: base_url,
      url,
      // params, // get 请求时带的参数
      // data: qs.stringify(data),
      data: data,
      timeout: timeout,
      headers: headers,
      withCredentials: true,
    }).then(
      (response) => {
        return checkStatus(response)
      }
    ).then(
      (res) => {
        return checkCode(res)
      }
    ).catch(
      (error) => {
        const error_code = error.response.status;
        const error_message = error.response.statusText;
        console.log(error_message);
      }
    )
  }
  // Get request
  static get (url, params) {
    return this.do_send(url, params, 'GET')
  }
  // Post request
  static post (url, params) {
    return this.do_send(url, params, 'POST')
  }
  // Put request
  static put (url, params) {
    return this.do_send(url, params, 'PUT')
  }
  // Delete request
  static delete (url, params) {
    return this.do_send(url, params, 'DELETE')
  }
}

export default request;