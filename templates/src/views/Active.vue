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
                <a-table :data="tableData">
                    <template #columns>
                        <a-table-column title="id" data-index="id"
                                        :sortable="{sortDirections: ['ascend', 'descend']}"></a-table-column>
                        <a-table-column title="bssid" data-index="bssid"
                                        :sortable="{sortDirections: ['ascend', 'descend']}"></a-table-column>
                        <a-table-column title="essid" data-index="essid"
                                        :sortable="{sortDirections: ['ascend', 'descend']}"></a-table-column>
                        <a-table-column title="client" data-index="client"
                                        :sortable="{sortDirections: ['ascend', 'descend']}">
                            <template #cell="{ record }">
                              <div class="client" style="white-space: pre-wrap;" >
                                <a-space v-if="record.client !== 'NULL'">

                                  {{ record.client }}

                                </a-space>
                                <a v-else-if="record.client === 'NULL'">{{ record.client }} </a>
                              </div>
                            </template>
                        </a-table-column>
                        <a-table-column title="channel" data-index="channel"
                                        :sortable="{sortDirections: ['ascend', 'descend']}"></a-table-column>
                        <a-table-column title="privacy" data-index="privacy"
                                        :sortable="{sortDirections: ['ascend', 'descend']}"></a-table-column>
                        <a-table-column title="power" data-index="power"
                                        :sortable="{sortDirections: ['ascend', 'descend']}"></a-table-column>
                        <a-table-column title="Attack" data-index="optional" :sortable="{sortDirections: ['ascend', 'descend']}" >
                            <template #cell="{ record }">
                                <a-button type="primary" :disabled="record.ATK_FLAG === false || record.client === 'NULL' "
                                          @click="attack(record.bssid)"
                                          v-if="record.ATK_FLAG === 1 || record.ATK_FLAG === false">
                                    Attack
                                </a-button>
                                <a-button type="primary" status="danger"
                                          @click="attackStop(record.bssid)"
                                          v-if="record.ATK_FLAG === 2">
                                    Stop
                                </a-button>
                            </template>
                        </a-table-column>
                      <a-table-column title="Dump" data-index="optional" :sortable="{sortDirections: ['ascend', 'descend']}" >
                            <template #cell="{ record }">
                                <a-button type="primary" :disabled="record.DUMP_FLAG !== 1 || record.client === 'NULL'"
                                          @click="dump(record.bssid)"
                                          v-if="record.DUMP_FLAG !== 2">
                                    Dump
                                </a-button>
                                <a-button type="primary" status="danger"
                                          @click="dumpStop(record.bssid)"
                                          v-if="record.DUMP_FLAG === 2">
                                    Stop
                                </a-button>
                            </template>
                        </a-table-column>
                    </template>
                </a-table>
            </a-col>
        </div>
    </div>
</template>

<script>
import {defineComponent, reactive, onMounted} from "vue";
import axios from 'axios'
import {IconRefresh} from '@arco-design/web-vue/es/icon';
import {Message} from "@arco-design/web-vue";

export default defineComponent({
    name: "Active",
    components: {
        IconRefresh
    },
    setup() {
        const tableData = reactive([])
        const getData = () => {
            tableData.length = 0
            axios.get("../api/active/").then(r => {
                for (let i of r.data["data"]) {
                    let r = {
                        "ATK_FLAG": i["ATK_FLAG"],
                        "DUMP_FLAG": i["DUMP_FLAG"],
                        "id": i["id"],
                        "authentication": i["authentication"],
                        "bssid": i["bssid"],
                        "channel": i["channel"],
                        "cipher": i["cipher"],
                        "essid": i["essid"],
                        "privacy": i["privacy"],
                        "power": i["power"],
                    }
                    r["client"] = i["client"] === null ? "NULL" : i["client"].replace(/,/g,'\n')
                    tableData.push(r)
                }
            })
        }
        const attackStop = (bssid) => {
            axios.get("../api/attack/stop/" + bssid + "/").then(r => {
              getData()
                if (r.data["data"]["success"] === 1) {
                    Message.success("停止成功")
                } else {
                    Message.error('停止失败')
                }
            })
        }
        const attack = (bssid) => {
            axios.get("../api/attack/start/" + bssid + "/").then(r => {
                getData()
                if (r.data["data"]["success"] === 1) {
                    Message.success("攻击启动")
                } else {
                    Message.error('攻击失败')
                }
            })
        }

        const dump = (bssid) => {
            axios.get("../api/dump/start/" + bssid + "/").then(r => {
              getData()
                if (r.data["data"]["success"] === 1) {
                    Message.success("嗅探启动")
                } else {
                    Message.error('嗅探失败')
                }
            })
        }

        const dumpStop = (bssid) => {
            axios.get("../api/dump/stop/" + bssid + "/").then(r => {
              getData()
                if (r.data["data"]["success"] === 1) {
                    Message.success("嗅探停止成功")
                } else {
                    Message.error('嗅探停止失败')
                }
            })
        }
        onMounted(async () => {
            getData()
        })
        return {
            tableData,
            getData,
            attack,
            dump,
            attackStop,
            dumpStop,
        }
    }
})
</script>