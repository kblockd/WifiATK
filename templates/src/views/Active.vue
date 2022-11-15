<template>
    <div style="padding: 20px; display: flex; height: calc(100% - 40px)">
        <div style="background-color: var(--color-bg-2); border-radius: 4px; overflow: auto; width: 100%">
            <a-col :span="24" style="padding: 20px 20px 0;">
                <a-typography-title :heading="5" style="margin-top: 0;">
                    Active Log
                    <a-button shape="circle" style="margin-left: 20px" @click="getData">
                        <icon-refresh/>
                    </a-button>
                </a-typography-title>
                <a-divider style="margin-bottom: 20px; border-bottom: 1px solid rgb(var(--gray-2));"/>
                <a-table :columns="columns" :data="tableData">
                    <template #optional="{ record }">
                        <a-button type="primary" :disabled="record.client === null" @click="attack(record.bssid)"
                                  v-if="record.bssid !== attack_bssid || record.ATK_STATUS === false">
                            Attack
                        </a-button>
                        <a-button type="primary" status="danger"
                                  v-if="record.bssid === attack_bssid || record.ATK_STATUS === true">
                            Stop
                        </a-button>
                    </template>
                </a-table>
            </a-col>
        </div>
    </div>
</template>

<script>
import {defineComponent, reactive, ref, onMounted} from "vue";
import axios from 'axios'
import {IconRefresh} from '@arco-design/web-vue/es/icon';
import {Message} from "@arco-design/web-vue";

export default defineComponent({
    name: "Active",
    components: {
        IconRefresh
    },
    setup() {
        const attack_bssid = ref("")
        const tableData = reactive([])
        const columns = reactive([{
            title: 'id',
            dataIndex: 'id',
            sortable: {
                sortDirections: ['ascend', 'descend']
            }
        }, {
            title: 'bssid',
            dataIndex: 'bssid',
            sortable: {
                sortDirections: ['ascend', 'descend']
            }
        }, {
            title: 'essid',
            dataIndex: 'essid',
            sortable: {
                sortDirections: ['ascend', 'descend']
            }
        }, {
            title: 'client',
            dataIndex: 'client',
            sortable: {
                sortDirections: ['ascend', 'descend']
            }
        }, {
            title: 'channel',
            dataIndex: 'channel',
            sortable: {
                sortDirections: ['ascend', 'descend']
            }
        }, {
            title: 'privacy',
            dataIndex: 'privacy',
            sortable: {
                sortDirections: ['ascend', 'descend']
            }
        }, {
            title: 'cipher',
            dataIndex: 'cipher',
            sortable: {
                sortDirections: ['ascend', 'descend']
            }
        }, {
            title: 'authentication',
            dataIndex: 'authentication',
            sortable: {
                sortDirections: ['ascend', 'descend']
            }
        }, {
            title: 'optional',
            slotName: 'optional',
        }])
        const getData = () => {
            tableData.length = 0
            axios.get("manager/api/active/").then(r => {
                for (let i of r.data["data"]) {
                    tableData.push(i)
                }
            })
        }
        const stop = (bassid) => {
            axios.get("manager/api/attack/stop/" + attack_bssid + "/").then(r => {
                if (r.data["data"]["sucess"] === 1) {
                    Message.success("停止成功")
                    attack_bssid.value = ""
                } else {
                    Message.error('停止失败')
                }
            })
        }
        const attack = (bssid) => {
            if (attack_bssid.value !== "") {
                stop(attack_bssid)
            }
            axios.get("manager/api/attack/start/" + bssid + "/").then(r => {
                if (r.data["data"]["sucess"] === 1) {
                    attack_bssid.value = bssid
                    Message.success("攻击成功")
                } else {
                    Message.error('攻击失败')
                }
            })
        }
        onMounted(async () => {
            getData()
        })
        return {
            columns,
            tableData,
            getData,
            attack,
            stop,
            attack_bssid
        }
    }
})
</script>