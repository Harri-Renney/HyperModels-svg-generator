<template>
    <div class="left-control-picker">
        <ControlEditor @add-control="addControl"/>
    </div>
</template>

<script>
import ControlEditor from './ControlEditor.vue'
export default {
  components: { ControlEditor },
    name: 'LeftControlPicker',
    methods: {
        addControl(color, size, type, shape, annotations) {
            this.$emit('add-control', color, size, type, shape, annotations)
        }
    }
}
</script>

<style scoped>
    .left-control-picker {
        background-color: #B8DBD9;
        width: 250px;
        height: 100%;
    }
    
    .square {
        margin-top: 75px;
        margin-left: auto;
        margin-right: auto;
    }

    button {
        margin: 10px;
    }
</style>