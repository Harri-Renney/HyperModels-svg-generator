<template>
    <div class="left-control-picker">
        <button class="square" @click="addSquare()">Add Square</button>
        <button class="circle" @click="addCircle()">Add Circle</button>
    </div>
</template>

<script>
export default {
    name: 'LeftControlPicker',
    methods: {
        addSquare() {
            this.$emit('add-square-to-canvas')
        },
        addCircle() {
            this.$emit('add-circle-to-canvas')
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