import {createRouter, createWebHashHistory} from 'vue-router'


const router = createRouter({
    history: createWebHashHistory(import.meta.env.BASE_URL),
    routes: [
        {
            path: '/',
            name: 'Dashboard',
            component: () => import('@/views/Dashboard.vue'),
            meta: {
                title: '仪表盘'
            }
        }, {
            path: '/Wifi',
            name: 'Wifi',
            component: () => import('@/views/Wifi.vue'),
            meta: {
                title: 'Wifi logs',
            }
        }, {
            path: '/Active',
            name: 'Active',
            component: () => import('@/views/Active.vue'),
            meta: {
                title: 'Active logs',
            }
        }, {
            path: '/Station',
            name: 'Station',
            component: () => import('@/views/Station.vue'),
            meta: {
                title: 'Station logs',
            }
    }, {
            path: '/Setting',
        name: 'Setting',
        component: () => import('@/views/Setting.vue'),
        meta: {
                title: 'Setting',
        }
    }, {
            path: '/:pathMatch(.*)*',
            name: '404',
            component: () => import('@/views/404.vue'),
            meta: {
                title: '404',
                auth: false
            }
        }
    ]
})

router.beforeEach(async (to, from) => {
    if (to.meta.title) {
        document.title = to.meta.title + ' - ' + document.title.split(' - ')[1]
    }
    return true
})

export default router
