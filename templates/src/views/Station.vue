<template>
    <div style="padding: 20px; display: flex; height: calc(100% - 40px)">
        <div style="background-color: var(--color-bg-2); border-radius: 4px; overflow: auto; width: 100%">
            <a-col :span="24" style="padding: 20px 20px 0;">
                <a-typography-title :heading="5" style="margin-top: 0;">
                    Station Log
                    <a-button shape="circle" style="margin-left: 20px" @click="getData">
                        <icon-refresh/>
                    </a-button>
                </a-typography-title>
                <a-divider style="margin-bottom: 20px; border-bottom: 1px solid rgb(var(--gray-2));"/>
                <a-table :columns="columns" :data="tableData"></a-table>
            </a-col>
        </div>
    </div>
</template>

<script>
import {defineComponent, reactive, onMounted} from "vue";
import axios from 'axios'
import {IconRefresh} from '@arco-design/web-vue/es/icon';

export default defineComponent({
    name: "Station",
    components: {
        IconRefresh
    },
    setup() {
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
            title: 'first_time',
            dataIndex: 'first_time',
            sortable: {
                sortDirections: ['ascend', 'descend']
            }
        }, {
            title: 'last_time',
            dataIndex: 'last_time',
            sortable: {
                sortDirections: ['ascend', 'descend']
            }
        }])
        const getData = () => {
            tableData.length = 0
            axios.get("../api/station/").then(r => {
                for (let i of r.data["data"]) {
                    tableData.push(i)
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
        }
    }
})
</script>