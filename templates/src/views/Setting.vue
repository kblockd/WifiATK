<template>
    <div style="padding: 20px; display: flex; height: calc(100% - 40px)">
        <div style="background-color: var(--color-bg-2); border-radius: 4px; overflow: auto; width: 100%">
            <a-col :span="24" style="padding: 20px 20px 0;">
                <a-form :model="settingData" :style="{width:'600px'}">
                    <a-form-item field="MAIN_STATUS" label="MAIN_STATUS">
                        <a-switch v-model="settingData.MAIN_STATUS" @change="change('MAIN_STATUS')"/>
                    </a-form-item>
                    <a-form-item field="ATK_STATUS" label="Auto Attack">
                        <a-switch v-model="settingData.ATK_STATUS" @change="change('ATK_STATUS')"/>
                    </a-form-item>
                    <a-form-item field="MONFACE" label="MONFACE">
                        <a-input v-model="settingData.MONFACE" @change="change('MONFACE')" disabled/>
                    </a-form-item>
                    <a-form-item field="ATKFACE" label="ATKFACE">
                        <a-input v-model="settingData.ATKFACE" @change="change('ATKFACE')" disabled/>
                    </a-form-item>
                    <a-form-item field="HOSTFACE" label="HOSTFACE">
                        <a-input v-model="settingData.HOSTFACE" @change="change('HOSTFACE')" disabled/>
                    </a-form-item>
                    <a-form-item field="LOGDIR" label="LOGDIR">
                        <a-input v-model="settingData.LOGDIR" @change="change('LOGDIR')" disabled/>
                    </a-form-item>
                    <a-form-item field="LOGNAME" label="LOGNAME">
                        <a-input v-model="settingData.LOGNAME" @change="change('LOGNAME')"/>
                    </a-form-item>
                    <a-form-item field="LOG" label="LOG">
                        <a-input v-model="settingData.LOG" @change="change('LOG')" disabled/>
                    </a-form-item>
<!--                    <a-form-item field="ATK_BSSID" label="ATK_BSSID">-->
<!--                        <a-input v-model="settingData.ATK_BSSID" @change="change('ATK_BSSID')" disabled/>-->
<!--                    </a-form-item>-->
<!--                    <a-form-item field="ATK_PID" label="ATK_PID">-->
<!--                        <a-input v-model="settingData.ATK_PID" @change="change('ATK_PID')" disabled/>-->
<!--                    </a-form-item>-->
<!--                    <a-form-item field="HOST_PID" label="HOST_PID">-->
<!--                        <a-input v-model="settingData.HOST_PID" @change="change('HOST_PID')" disabled/>-->
<!--                    </a-form-item>-->
<!--                    <a-form-item field="DNSMASQ_PID" label="DNSMASQ_PID">-->
<!--                        <a-input v-model="settingData.DNSMASQ_PID" @change="change('DNSMASQ_PID')" disabled/>-->
<!--                    </a-form-item>-->
                    <a-form-item field="MAIN_PID" label="MAIN_PID">
                        <a-input v-model="settingData.MAIN_PID" @change="change('MAIN_PID')" disabled/>
                    </a-form-item>
<!--                    <a-form-item field="DUMP_PID" label="DUMP_PID">-->
<!--                        <a-input v-model="settingData.DUMP_PID" @change="change('DUMP_PID')" disabled/>-->
<!--                    </a-form-item>-->
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
            "MAIN_PID": "",
            "MAIN_STATUS": false,
            "ATK_STATUS": false,
            "DUMP_PID": "",
        })
        const getData = () => {
            axios.get("../api/config/get/").then(r => {
                settingData["MONFACE"] = r.data["data"]["MONFACE"]
                settingData["MONFACE"] = r.data["data"]["MONFACE"]
                settingData["ATKFACE"] = r.data["data"]["ATKFACE"]
                settingData["HOSTFACE"] = r.data["data"]["HOSTFACE"]
                settingData["LOGDIR"] = r.data["data"]["LOGDIR"]
                settingData["LOGNAME"] = r.data["data"]["LOGNAME"]
                settingData["LOG"] = r.data["data"]["LOG"]
                settingData["ATK_BSSID"] = r.data["data"]["ATK_BSSID"]
                settingData["ATK_PID"] = r.data["data"]["ATK_PID"]
                settingData["HOST_PID"] = r.data["data"]["HOST_PID"]
                settingData["DNSMASQ_PID"] = r.data["data"]["DNSMASQ_PID"]
                settingData["MAIN_PID"] = r.data["data"]["MAIN_PID"]
                settingData["DUMP_PID"] = r.data["data"]["DUMP_PID"]
                settingData["MAIN_STATUS"] = r.data["data"]["MAIN_STATUS"] === "True"
                settingData["ATK_STATUS"] = r.data["data"]["ATK_STATUS"] === "True"
            })
        }
        const change = (r) => {
            set(r, settingData[r])
        }
        const set = (key, value) => {
            axios.get("../api/config/set/" + key + "/" + value + "/").then(r => {
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