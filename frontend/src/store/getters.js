const getters = {

  isLoading: state => state.auth.loading,
  isLoggedIn: state => state.auth.isLoggedIn,
  authError: state => state.auth.auth_error,
  currentUser: state => state.auth.currentUser,
      

}
export default getters

