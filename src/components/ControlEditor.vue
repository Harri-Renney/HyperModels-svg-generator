<template>
    <div class="control-editor-container">
        <div class="control-editor">
            <div class="item color-editor">
                <label for="color-picker" class="label">Colour:</label>
                <input class="color-picker" type="color" v-model="color"/>
                <input class="color-text" type="text" v-model="color"/>
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
                    <option value="toggle">Toggle</option>
                    <option value="horz_slider">Horizontal Slider</option>
                    <option value="vert_slider">Vertical Slider</option>
                    <option value="ciPad">ciPad</option>
                    <option value="endless">Endless</option>
                </select>
            </div>

            <div class="annotations">
                <div class="item">
                    <label for="osc-address" class="label">OSC Address:</label>
                    <input type="text" v-model="annotations.osc_address" class="text-input"/>
                </div>

                <div class="item">
                    <label for="osc-args" class="label">OSC Arguments:</label>
                    <input type="text" v-model="annotations.ocs_args" class="text-input"/>
                </div>

                <div class="item">
                    <label for="min" class="label">Minimum Value:</label>
                    <input type="text" v-model="annotations.min" class="text-input"/>
                </div>

                <div class="item">
                    <label for="max" class="label">Maximum Value:</label>
                    <input type="text" v-model="annotations.max" class="text-input"/>
                </div>

                <div class="item">
                    <label for="init" class="label">Initial Value:</label>
                    <input type="text" v-model="annotations.init" class="text-input"/>
                </div>
                
                <div class="item">
                    <label for="incr" class="label">Increment Value:</label>
                    <input type="text" v-model="annotations.incr" class="text-input"/>
                </div>
            </div>

            <div class="item always-show add">
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
            expand: false,
            expandCollapseIcon: 'mi-chevron-double-down',
            annotations: {
                osc_address: '',
                osc_args: '',
                min: '',
                max: '',
                init: '',
                incr: '',
            }
        }
    },
    methods: {
        addControl() {
            if (this.color == '' || this.size <= 0 || this.size >= 10 || this.controltype == '' || this.controlshape == '') {
                alert("You must select a value for all inputs.")
                return
            }

            this.$emit('add-control', this.color, this.size, this.controltype, this.controlshape, this.annotations)
        },
        expandCollapse() {
            this.expand = !this.expand
            this.expandCollapseIcon = this.expand ? 'mi mi-chevron-double-up' : 'mi mi-chevron-double-down'
        }
    },
}
</script>

<style scoped>
.color-editor {
    height: 90px !important;
}

.control-editor-container {
    width: 100%;
    position: relative;
    top: 60px;
}

input[type="text"] {
    width: 100%;
    box-sizing: border-box;
    padding: 5px;
    height: 35px;
    outline: none;
    background-color: #F4F4F9;
    border: none;
    border-bottom: 2px black solid;
    border-radius: 2px;
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
    margin-bottom: 10px;
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

.annotations .label {
    line-height: 20px;
}

.annotations .item {
    height: 65px;
}

</style>