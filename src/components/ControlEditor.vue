<template>
    <div class="control-editor-container">
        <div class="control-editor">
            <div class="item">
                <label for="color-picker" class="label">Colour:</label>
                <input class="color-picker" type="color" v-model="color"/>
            </div>

            <div class="item">
                <label for="size-picker" class="label">Size:</label>
                <input type="number" min="1" max="9" v-model="size" class="size-picker"/>
            </div>

            <div class="item">
                <label for="shape-picker" class="label">Control Shape:</label>
                <select
                    id="shape-picker-dropwdown"
                    class="dropdown shape-picker"
                    v-model="controlshape">
                    <option selected value="square">Square</option>
                    <option value="circle">Circle</option>
                    <option value="triangle">Triangle</option>
                    <option value="ring">Ring</option>
                </select>
            </div>

            <div class="item">
                <label for="control-picker" class="label">Control Type:</label>
                <select
                    id="control-picker-dropwdown"
                    class="dropdown control-picker"
                    v-model="controltype">
                    <option selected value="pad">Pad</option>
                    <option value="slider">Slider</option>
                    <option value="endless">Endless</option>
                </select>
            </div>

            <div class="item">
                <span class="button" @click="addControl">
                    <i class="mi mi-circle-add"/>
                    Add Control
                </span>
            </div>
        </div>
    </div>
</template>

<script>

export default {
    name: 'ControlEditor',
    data () {
        return {
            color: '#586F7C',
            size: 3,
            controltype: 'pad',
            controlshape: 'square',
        }
    },
    methods: {
        addControl() {
            if (this.color == '' || this.size <= 0 || this.size >= 10 || this.controltype == '' || this.controlshape == '') {
                alert("You must select a value for all inputs.")
                return
            }

            this.$emit('add-control', this.color, this.size, this.controltype, this.controlshape)
        }
    }
}
</script>

<style scoped>
.control-editor-container {
    width: 100%;
    height: 31%;
    position: relative;
    top: 60px;
}

input[type="color"] {
	width: 50px;
	height: 50px;
	border: none;
	border-radius: 40px;
	background: none;
    cursor: pointer;
}

input[type="color"]::-webkit-color-swatch-wrapper {
	padding: 0;
}

input[type="color"]::-webkit-color-swatch {
	border: solid 1px #2F4550; /*change color of the swatch border here*/
	border-radius: 40px;
}

input[type="color"]{
    position: relative;
    right: -40px;
}

label {
    float: left;
    line-height: 50px;
}

.size-picker {
    height: 10px;
    font-size: 15px;
    line-height: 15px;
    border: none;
    border-radius: 5px;
    width: 30px;
    cursor: pointer;
    background-color: #F4F4F9;
    padding: 10px;
    position: relative;
    top: 10px;
    right: -60px;
}

input[type="number"]::-webkit-inner-spin-button {
  opacity: 1;
}

.button {
    height: 50px;
    font-size: 15px;
    line-height: 15px;
    border: none;
    border-radius: 5px;
    width: 100px;
    cursor: pointer;
    background-color: #F4F4F9;
    padding: 10px;
    position: relative;
    top: 10px;
    left: 30px;
}

.mi {
    position: relative;
    top: 2px;
    margin-right: 2px;
}

.control-editor {
    border: 2px solid #2F4550;
    border-radius: 5px;
    width: 80%;
    margin-left: auto;
    margin-right: auto;
    padding: 10px;
    height: 100%;
}

.item {
    margin-top: 5px;
    height: 55px;
    width: 100%;
}

.control-picker {
    width: 100px;
}

.dropdown {
    height: 30px;
    font-size: 15px;
    line-height: 15px;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    background-color: #F4F4F9;
    position: relative;
    top: 10px;
    right: -10px;
}

.shape-picker {
    width: 90px;
}

</style>