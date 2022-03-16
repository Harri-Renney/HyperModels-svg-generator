<template>
    <div 
    class="message" 
    :style="{backgroundColor: color}"
    @mouseover="showClose = true" 
    @mouseleave="showClose = false">
        <i class="message-type-icon" :class="icon"/>
        {{ messageContent }}
        <i class="mi-close" v-if="showClose" @click="closeMessage"/>
    </div>
</template>

<script>
export default {
    name: 'Message',
    props: {
        messageType: {
            required: true,
            type: String
        },
        messageContent: {
            required: true,
            type: String
        }
    },
    data() {
        return {
            showClose: false,
        }
    },
    methods: {
        closeMessage() {
            this.$emit('close-message')
        }
    },
    computed: {
        icon() {
            switch (this.messageType) {
                case 'error':
                    return 'mi-warning'
                case 'warning':
                    return 'mi-circle-warning'
                case 'success':
                    return 'mi-heart'
                case 'information':
                    return 'mi-circle-information'
                default:
                    return 'mi-warning'
            }
        },
        color() {
            switch (this.messageType) {
                case 'error':
                    return '#EF476F'
                case 'warning':
                    return '#FFD166'
                case 'success':
                    return '#06D6A0'
                case 'information':
                    return '#118AB2'
                default:
                    return '#EF476F'
            }
        }
    }  
}
</script>

<style scoped>
    .message {
        position: relative;
        top: 60px;
        width: 300px;
        margin-right: auto;
        margin-left: auto;
        padding: 5px;
        text-align: center;
        border: 1px solid black;
        border-radius: 1px;
        z-index: 9999999999;
    }

    .message-type-icon {
        float: left;
    }

    .mi-close {
        float: right;
        position: absolute;
        right: 5px;
    }

    .mi-close:hover {
        cursor: pointer;
        color: #F4F4F9;
    }
</style>