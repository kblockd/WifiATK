<template>
    <div style="padding: 20px; display: flex; height: calc(100% - 40px)">
        <div style="background-color: var(--color-bg-2); border-radius: 4px; overflow: auto; width: 100%">
            <a-col :span="24" style="padding: 20px 20px 0;">
                <a-form :model="settingData" :style="{width:'600px'}">
                    <a-form-item field="MAIN_STATUS" label="MAIN_STATUS">
                        <a-switch v-model="settingData.MAIN_STATUS" @change="change('MAIN_STATUS')"/>
                    </a-form-item>
                    <a-form-item field="ATK_STATUS" label="ATK_STATUS">
                        <a-switch v-model="settingData.ATK_STATUS" @change="change('ATK_STATUS')"/>
                    </a-form-item>
                    <a-form-item field="MONFACE" label="MONFACE">
                        <a-input v-model="settingData.MONFACE" @change="change('MONFACE')"/>
                    </a-form-item>
                    <a-form-item field="ATKFACE" label="ATKFACE">
                        <a-input v-model="settingData.ATKFACE" @change="change('ATKFACE')"/>
                    </a-form-item>
                    <a-form-item field="HOSTFACE" label="HOSTFACE">
                        <a-input v-model="settingData.HOSTFACE" @change="change('HOSTFACE')"/>
                    </a-form-item>
                    <a-form-item field="LOGDIR" label="LOGDIR">
                        <a-input v-model="settingData.LOGDIR" @change="change('LOGDIR')"/>
                    </a-form-item>
                    <a-form-item field="LOGNAME" label="LOGNAME">
                        <a-input v-model="settingData.LOGNAME" @change="change('LOGNAME')"/>
                    </a-form-item>
                    <a-form-item field="LOG" label="LOG">
                        <a-input v-model="settingData.LOG" @change="change('LOG')"/>
                    </a-form-item>
                    <a-form-item field="ATK_BSSID" label="ATK_BSSID">
                        <a-input v-model="settingData.ATK_BSSID" @change="change('ATK_BSSID')"/>
                    </a-form-item>
                    <a-form-item field="ATK_PID" label="ATK_PID">
                        <a-input v-model="settingData.ATK_PID" @change="change('ATK_PID')"/>
                    </a-form-item>
                    <a-form-item field="HOST_PID" label="HOST_PID">
                        <a-input v-model="settingData.HOST_PID" @change="change('HOST_PID')"/>
                    </a-form-item>
                    <a-form-item field="DNSMASQ_PID" label="DNSMASQ_PID">
                        <a-input v-model="settingData.DNSMASQ_PID" @change="change('DNSMASQ_PID')"/>
                    </a-form-item>
                </a-form>
            </a-col>
        </div>
    </div>
</template>

<script>
import {defineComponent, reactive, onMounted} from "vue";
import axios from 'axios'
import {Message} from "@arco-design/web-vue";

export default defineComponent({
    name: "Setting",
    setup() {
        const settingData = reactive({
            "MONFACE": "",
            "ATKFACE": "",
            "HOSTFACE": "",
            "LOGDIR": "",
            "LOGNAME": "",
            "LOG": "",
            "ATK_BSSID": "",
            "ATK_PID": "",
            "HOST_PID": "",
            "DNSMASQ_PID": "",
            "MAIN_STATUS": false,
            "ATK_STATUS": false,
        })
        const getData = () => {
            axios.get("manager/api/config/get/").then(r => {
                for (let i of r.data["data"]) {
                    settingData["MONFACE"] = i["MONFACE"]
                    settingData["MONFACE"] = i["MONFACE"]
                    settingData["ATKFACE"] = i["ATKFACE"]
                    settingData["HOSTFACE"] = i["HOSTFACE"]
                    settingData["LOGDIR"] = i["LOGDIR"]
                    settingData["LOGNAME"] = i["LOGNAME"]
                    settingData["LOG"] = i["LOG"]
                    settingData["ATK_BSSID"] = i["ATK_BSSID"]
                    settingData["ATK_PID"] = i["ATK_PID"]
                    settingData["HOST_PID"] = i["HOST_PID"]
                    settingData["DNSMASQ_PID"] = i["DNSMASQ_PID"]
                    settingData["MAIN_STATUS"] = i["MAIN_STATUS"]
                    settingData["ATK_STATUS"] = i["ATK_STATUS"]
                }
            })
        }
        const change = (r) => {
            set(r, settingData[r])
        }
        const set = (key, value) => {
            axios.get("manager/api/config/set/" + key + "/" + value + "/").then(r => {
                Message.success("设置成功")
            })
        }
        onMounted(async () => {
            getData()
        })
        return {
            getData,
            change,
            settingData
        }
    }
})
</script>