import { setAuthorization } from './general'

export function login (credentials) {
  return new Promise((resolve, reject) => {
    axios
      .post('/api/token/', credentials)
      .then(response => {
        setAuthorization(response.data.access)
        resolve(response.data)
      })
      .catch(err => {
        console.log(err)
        reject('Wrong username or password')
      })
  })
}

export function refreshtoken (credentials) {
  return new Promise((resolve, reject) => {
    axios
      .post('/api/token/refresh/', credentials)
      .then(response => {
        setAuthorization(response.data.access)
        resolve(response.data)
      })
      .catch(err => {
        console.log(err)
        reject('Wrong username or password')
      })
  })
}

export function getLocalUser () {
  const userStr = localStorage.getItem('user')

  if (!userStr) {
    return null
  }

  return JSON.parse(userStr)
}
