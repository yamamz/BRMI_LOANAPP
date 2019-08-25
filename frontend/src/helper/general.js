export function initialize (store, router) {
  router.beforeEach((to, from, next) => {
    const requiresAuth = to.matched.some(record => record.meta.requiresAuth)
    const currentUser = store.getters.currentUser
    console.log(store.getters.currentUser)

    if (requiresAuth && !currentUser) {
      next('/app/login')
    } else if (to.path === '/app/login' && currentUser) {
      next('/')
    } else {
      next()
    }
  })

  axios.interceptors.response.use(null, error => {
    const currentUser = store.getters.currentUser
    if (error.response.status === 401) {
      if (currentUser) {
        let refresh = currentUser.refresh
        axios
          .post('/api/token/refresh/', { refresh: refresh })
          .then(res => {
            console.log('refreshed')
            setAuthorization(res.data.access)
            store.commit('refreshToken', { refresh: refresh, access: res.data.access })
            // .push('/app')
            // el.message.error('The token authentication is expired and being refresh please try again')
          })
          .catch(() => {
            store.commit('logout')
            router.push('/app/login')
          })
      } else {

      }
    }

    return Promise.reject(error)
  })

  if (store.getters.currentUser) {
    setAuthorization(store.getters.currentUser.access)
  }
}

export function setAuthorization (token) {
  axios.defaults.headers.common['Authorization'] = `Bearer ${token}`
}
