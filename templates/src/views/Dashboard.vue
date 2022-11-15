<template>
    <div style="padding: 20px; display: flex; height: calc(100% - 40px)">
        <div style="background-color: var(--color-bg-2); border-radius: 4px; overflow: auto; width: 100%">
            <a-col :span="24" style="padding: 20px 20px 0;">
                <a-typography-title :heading="5" style="margin-top: 0;">
                    欢迎回来！
                </a-typography-title>
                <a-divider style="margin-bottom: 20px; border-bottom: 1px solid rgb(var(--gray-2));"/>
                <a-row>
                    <a-col :span="6">
                        <a-statistic title="Active wifis" :value="aw" show-group-separator animation>
                            <template #suffix>
                                <icon-arrow-rise/>
                            </template>
                        </a-statistic>
                    </a-col>
                    <a-col :span="6">
                        <a-statistic title="Active clients" :value="ac" show-group-separator animation>
                            <template #suffix>
                                <icon-arrow-rise/>
                            </template>
                        </a-statistic>
                    </a-col>
                    <a-col :span="6">
                        <a-statistic title="Wifi logs" :value="wl" show-group-separator animation>
                            <template #suffix>
                                <icon-arrow-rise/>
                            </template>
                        </a-statistic>
                    </a-col>
                    <a-col :span="6">
                        <a-statistic title="Station logs" :value="sl" show-group-separator animation>
                            <template #suffix>
                                <icon-arrow-rise/>
                            </template>
                        </a-statistic>
                    </a-col>
                </a-row>
            </a-col>
        </div>
    </div>
</template>

<script>
import {defineComponent, ref, onMounted} from "vue";
import {IconArrowRise} from '@arco-design/web-vue/es/icon';
import axios from 'axios'

export default defineComponent({
    name: "Dashboard",
    components: {
        IconArrowRise
    },
    setup() {
        const aw = ref(0)
        const ac = ref(0)
        const wl = ref(0)
        const sl = ref()
        onMounted(() => {
            axios.get("../api/index/").then(r => {
                aw.value = r.data["data"]["active_wifis"]
                ac.value = r.data["data"]["active_clients"]
                wl.value = r.data["data"]["wifi_logs"]
                sl.value = r.data["data"]["station_logs"]
            })
        })
        return {
            aw,
            ac,
            wl,
            sl
        }
    }
})
</script>