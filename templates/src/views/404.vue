<template>
    <a-result status="404" subtitle="Whoops, that page is gone.">
        <template #extra>
            <a-space>
                <a-button type="primary" @click="router.back()">Back</a-button>
            </a-space>
        </template>
    </a-result>
</template>

<script>
import {defineComponent} from 'vue';
import {useRouter} from "vue-router";

export default defineComponent({
    name: '404',
    setup() {
        const router = useRouter()
        return {
            router
        }
    }
})
</script>
