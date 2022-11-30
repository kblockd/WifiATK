<template>
    <a-layout class="layout-index">
        <a-layout-header>
            <a-menu mode="horizontal">
                <a-menu-item key="0" style="padding: 0; margin-right: 38px; cursor: pointer" disabled>
                    <a-typography-title :heading="5" style="margin-top: 0; margin-bottom: 0;" @click="router.push('/')">
                        TRACK
                    </a-typography-title>
                </a-menu-item>
                <div style="float:right">
                    <a-button
                        shape="circle"
                        @click="changeDark(!dark)"
                        style="margin-right: 20px;background-color: transparent;"
                    >
                        <IconMoonFill v-if="dark"/>
                        <IconSunFill v-if="!dark"/>
                    </a-button>
                </div>
            </a-menu>
        </a-layout-header>
        <a-layout-content>
            <a-layout class="layout" :style="{height: `${contentHeight}px`}">
                <a-layout-sider collapsible breakpoint="xl" :collapsed="collapsed" hide-trigger :width="200">
                    <a-menu
                        style="height: 100%"
                        :default-open-keys="['0', '1', '2', '3']"
                        :selected-keys="menuSelectKeys"
                        show-collapse-button
                        :collapsed="collapsed"
                        @menuItemClick="onClickMenuItem"
                        @collapse="collapsed = !collapsed"
                        breakpoint="xl"
                    >
                        <a-menu-item key="Dashboard">
                            <template #icon>
                                <icon-dashboard/>
                            </template>
                            Dashboard
                        </a-menu-item>
                        <a-menu-item key="Active">
                            <template #icon>
                                <icon-apps/>
                            </template>
                            Active log
                        </a-menu-item>
                        <a-menu-item key="Wifi">
                            <template #icon>
                                <icon-wifi/>
                            </template>
                            Wifi log
                        </a-menu-item>
                        <a-menu-item key="Station">
                            <template #icon>
                                <icon-dice/>
                            </template>
                            Station log
                        </a-menu-item>
                        <a-menu-item key="Setting">
                            <template #icon>
                                <icon-settings/>
                            </template>
                            Setting
                        </a-menu-item>
                    </a-menu>
                </a-layout-sider>
                <a-layout-content>
                    <RouterView/>
                </a-layout-content>
            </a-layout>
        </a-layout-content>
    </a-layout>
</template>

<script>
import {defineComponent, onMounted, ref, onUnmounted, watch} from 'vue';
import {useRoute, useRouter} from "vue-router";
import {
    IconMoonFill,
    IconSunFill,
    IconDashboard,
    IconApps,
    IconDice,
    IconWifi,
    IconSettings
} from '@arco-design/web-vue/es/icon';

export default defineComponent({
    name: 'App',
    components: {
        IconDashboard,
        IconMoonFill,
        IconSunFill,
        IconApps,
        IconDice,
        IconWifi,
        IconSettings
    },
    setup() {
        const route = useRoute()
        const router = useRouter()
        const dark = ref(window.matchMedia('(prefers-color-scheme: dark)').matches)
        const collapsed = ref(false)
        const contentHeight = ref(window.innerHeight - 60)
        const menuSelectKeys = ref([])
        const calcLeftManuSelectedKeys = (pathName) => {
            menuSelectKeys.value = [pathName]
        }
        watch(
            () => route.name,
            (val) => {
                calcLeftManuSelectedKeys(val)
            }
        )
        const onClickMenuItem = (key) => {
            router.push({
                name: key
            })
        }
        const onHeightChange = () => {
            contentHeight.value = window.innerHeight - 60
        }
        onMounted(async () => {
            calcLeftManuSelectedKeys(route.name)
            window.addEventListener('resize', onHeightChange)
        })
        onUnmounted(async () => window.removeEventListener('resize', onHeightChange))
        const changeDark = (status) => {
            dark.value = status
            if (status) {
                document.body.setAttribute('arco-theme', 'dark')
            } else {
                document.body.removeAttribute('arco-theme');
            }
        }
        onMounted(() => {
            if (dark.value) {
                document.body.setAttribute('arco-theme', 'dark')
            } else {
                document.body.removeAttribute('arco-theme');
            }
        })
        return {
            router,
            collapsed,
            dark,
            changeDark,
            contentHeight,
            menuSelectKeys,
            onClickMenuItem
        }
    }
})
</script>


<style scoped>
.layout-index {
    height: 100%;
    background: var(--color-neutral-2);
    border: 1px solid var(--color-border);
    color: var(--color-text-2);
}

.layout {
    height: 700px;
    background: var(--color-fill-2);
    border: 1px solid var(--color-border);
}
</style>
