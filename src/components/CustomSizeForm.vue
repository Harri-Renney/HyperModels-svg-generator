<template>
    <div class="sign-up-form">
        <div class="form-container">
            <form @submit.prevent="onSubmit">
                <div class="welcome-message">
                    Enter custom dimensions for your device below.
                </div>
                <div class="item text">
                    <input required type="text" id="width" v-model="custom_size.custom_width" placeholder="Width">
                </div>

                <div class="item select">
                    <select name="width_unit" v-model="width_unit">
                        <option selected value="grid">Default - Grid Squares</option>
                        <option value="cm">cm - Centimetres</option>
                        <option value="mm">mm - Milimetres</option>
                        <option value="px">px - Pixels</option>
                    </select>
                </div>

                <div class="item text">
                    <input required type="text" id="heihght" v-model="custom_size.custom_height" placeholder="Height">
                </div>

                <div class="item select">
                    <select name="height_unit" v-model="height_unit">
                        <option selected value="grid">Default - Grid Squares</option>
                        <option value="cm">cm - Centimetres</option>
                        <option value="mm">mm - Milimetres</option>
                        <option value="px">px - Pixels</option>
                    </select>
                </div>

                <div class="item button">
                    <input type="submit" id="submit" value="Set Custom Dimensions as Device">
                </div>

                <div class="item cancel" @click="closeCustomSizeForm">
                    <span class="cancel">Cancel</span>
                </div>
            </form>
        </div>
    </div>
</template>

<script>
export default {
    name: 'CustomSizeForm',
    data() {
        return {
            custom_size: {
                custom_width: null,
                custom_height: null,
            },
            width_unit: 'px',
            height_unit: 'px',
        }
    },
    methods: {
        closeCustomSizeForm() {
            this.$emit('close-custom-size-form')
        },
        onSubmit() {
            this.$emit('set-custom-size-device', this.custom_size)
            // this.device.height = this.custom_size.custom_height
            // this.device.width = this.custom_size.custom_width
        }
    }
}
</script>

<style scoped>

.form-container {
    width: 100%;
    top: 20%;
    position: absolute;
    margin-left: auto;
    margin-right: auto;
}

.sign-up-form {
    position: absolute;
    height: 100%;
    width: 100%;
    background-color: #00000055;
    z-index: 200;
}

form {
    max-width: 35%;
    background-color: #F4F4F9;
    border: solid #B8DBD9 3px;
    border-radius: 2px;
    z-index: 200;
    margin-left: auto;
    margin-right: auto
}

.item {
    margin-left: auto;
    margin-right: auto;
    margin-bottom: 10px;
    width: 65%;
}

input {
    width: 100%;
    box-sizing: border-box;
    padding: 5px;
    height: 35px;
    outline: none;
    background-color: #F4F4F9;
    border: none;
    font-size: 20px;
    margin-left: auto;
    margin-right: auto;
}

input:focus {
    border-bottom: 2px #586F7C solid;
}

.button {
    text-align: center; 
    border: 2px black solid;
    width: 80%;
    margin: auto;
    border-bottom: 4px black solid;
}

.welcome-message {
    margin-left: auto;
    margin-right: auto;
    line-height: 50px;
    position: relative;
    left: 10px;
    font-weight: bold;
    font-size: 25px;
    color: #586F7C;
    text-align: center;
}

.title {
    color: #2F4550;
}

.text {
    border-bottom: 2px black solid;
    float: left;
}

div .cancel {
    text-align: center;
    color: #586F7C;
    margin-top: 10px;
    cursor: pointer;
}

div .cancel :hover {
    color: #B8DBD9;
}

span .cancel {
    width: 100%;
    box-sizing: border-box;
    height: 35px;
    outline: none;
    border: none;
    font-size: 15px;
    display: inline-block;
}

.required {
    color: #EF476F;
    float: left;
}

#submit {
    cursor: pointer;
}

input[type="select"] {
    float: right;
}
</style>
