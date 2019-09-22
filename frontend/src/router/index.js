import Vue from 'vue'
import Router from 'vue-router'

// Containers
const DefaultContainer = () => import('@/containers/DefaultContainer')

// Views
const Dashboard = () => import('@/views/Dashboard')

// Users

const Login = () => import('@/views/pages/Login')
const Register = () => import('@/views/pages/Register')
const Members = () => import('@/views/member/members')
const MemberAdd = () => import('@/views/member/member-add')
const Loans = () => import('@/views/loan/loans')
const LoanAdd = () => import('@/views/loan/loan-add')
const LoanPayments = () => import('@/views/loan/loanPaymentDetails')
const LoanEdit = () => import('@/views/loan/loan-edit')
const MemberEdit = () => import('@/views/member/member-edit')
const LoanSummaryReport = () => import('@/views/reports/loan_summary')
Vue.use(Router)

export default new Router({
  mode: 'history', // https://router.vuejs.org/api/#mode
  linkActiveClass: 'open active',
  scrollBehavior: () => ({ y: 0 }),
  routes: [
    {
      path: '/app/login',
      name: 'Login',
      component: Login
    },
    {
      path: '/app/register',
      name: 'Register',
      component: Register
    },
    {
      path: '/',
      redirect: '/app/dashboard',
      name: 'Home',
      component: DefaultContainer,
      meta: { requiresAuth: true },
      children: [
        {
          path: '/app/dashboard',
          name: 'Dashboard',
          component: Dashboard,
          meta: { requiresAuth: true }
        }
      ]
    },
    {
      path: '/app/member',

      name: 'Member',
      component: DefaultContainer,
      meta: { requiresAuth: true },
      children: [
        {
          path: 'list',
          name: 'member-list',
          component: Members,
          meta: { requiresAuth: true }
        },
        {
          path: 'add',
          name: 'member-add',
          component: MemberAdd,
          meta: { requiresAuth: true }
        },
        {
          path: 'edit/:id',
          name: 'member-edit',
          component: MemberEdit,
          meta: { requiresAuth: true }
        }
      ]
    },
    {
      path: '/app/loan',

      name: 'Loan',
      component: DefaultContainer,
      meta: { requiresAuth: true },
      children: [
        {
          path: 'list',
          name: 'loan-list',
          component: Loans,
          meta: { requiresAuth: true }
        },
        {
          path: 'add',
          name: 'loan-add',
          component: LoanAdd,
          meta: { requiresAuth: true }
        },
        {
          path: 'loanpayment/:id',
          name: 'loan-add',
          component: LoanPayments,
          meta: { requiresAuth: true }
        },
        {
          path: 'edit/:id',
          name: 'loan-edit',
          component: LoanEdit,
          meta: { requiresAuth: true }
        }
      ]
    },
    {
      path: '/app/reports',

      name: 'Reports',
      component: DefaultContainer,
      meta: { requiresAuth: true },
      children: [
        {
          path: 'loan_summary_list',
          name: 'loan-list-summary',
          component: LoanSummaryReport,
          meta: { requiresAuth: true }
        }
      ]
    }
  ]
})
