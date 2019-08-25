export default {
  items: [
    {
      name: 'Dashboard',
      url: '/',
      icon: 'icon-speedometer'
      // badge: {
      //   variant: 'primary',
      //   text: 'NEW'
      // }
    },
    {
      title: true,
      name: 'Main'
    },
    {
      name: 'Member',
      url: '/member',
      icon: 'icon-puzzle',
      children: [
        {
          name: 'member list',
          url: '/app/member/list',
          icon: 'icon-list'
        },
        {
          name: 'member add',
          url: '/app/member/add',
          icon: 'icon-notebook'
        }

      ]
    },
    {
      name: 'Loan',
      url: '/loan',
      icon: 'icon-calculator',
      badge: {
        variant: 'danger'
      },
      children: [
        {
          name: 'loan list',
          url: '/app/loan/list',
          icon: 'icon-list'
        },
        {
          name: 'loan application',
          url: '/app/loan/add',
          icon: 'icon-notebook'
        }

      ]
    },
    {
      name: 'Reports',
      url: '/reports',
      icon: 'icon-pie-chart',
      children: [{

        name: 'Report',
        url: '/app/reports/payables',
        icon: 'icon-list'

      }]
    },
    {
      divider: true
    },
    {
      title: true,
      name: 'Extra'
    },
    {
      name: 'Settings',
      url: '/Settings',
      icon: 'icon-star',
      children: [
        {
          name: 'Login',
          url: '/app/login',
          icon: 'icon-star'
        },
        {
          name: 'Register',
          url: '/app/register',
          icon: 'icon-star'
        }

      ]
    }
  ]
}
