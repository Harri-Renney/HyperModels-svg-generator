<template>
    <div class="top-menu-bar">
        <div class="top-menu-bar-controls">
            <span id="page-title">Annotated SVG Creator</span>
            <button id="top-menu-export-button" class="top-menu-control" @click="callApi">
                <i class="mi-export"/>
                Export
            </button>
            <select
                id="device-selector"
                class="dropdown device-selector top-menu-control"
                @change="selectDevice"
                v-model="device">
                <option selected value="none">Select Device</option>
                <option value="sensel-morph">Sensel Morph</option>
                <option value="roli-lightpad-block">Roli Lightpad Block</option>
                <option value="custom">Custom</option>
                <option value="none">None</option>
            </select>
            <button id="top-menu-cloud-save-button" class="top-menu-control">
                <i class="mi-cloud-upload"/>
                Save
            </button>
            <SignIn @toggle-sign-in-form="toggleSignInForm"/>
        </div>
    </div>
</template>

<script>
import SignIn from "./buttons/SignIn.vue";
import axios from 'axios'

export default {
    name: 'TopMenuBar',
    components: {
        SignIn,
    },
    data() {
        return {
            response: '',
            error: '',
            device: 'none',
        }
    },
    methods: {
        selectDevice() {
            this.$emit('change-device', this.device)
        },
        toggleSignInForm() {
            this.$emit('toggle-sign-in-form')
        },
        test() {
            axios.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded;';

            // Call the API
            return axios.get('http://localhost:8000/test', {
                headers: {
                    Authorization: 'Bearer ' + atob(localStorage.getItem(btoa('token')))
                }
            });
        },
        async callApi() {
            await this.test()
                .then((response) => {
                    this.response = response
                    console.log(this.response)
                    alert('Logged In')
                })
                .catch((error) => {
                    this.error = error
                })
        }
    },
}
</script>

<style scoped>
    .top-menu-bar {
        width: 100%;
        height: 50px;
        background-color: #586F7C;
        text-align: center;
        min-width: 825px;
        position: fixed;
        top: 0;
        z-index: 110;
    }

    .top-menu-control {
        height: 30px;
        font-size: 15px;
        border: none;
        border-radius: 5px;
        width: 100px;
        cursor: pointer;
        margin-left: 5px;
        margin-right: 5px;
        margin-top: 10px;
        margin-bottom: 10px;
        background-color: #F4F4F9;

    }

    .top-menu-bar-controls {
        margin-left: auto;
        margin-right: auto;
        width: 100%;
    }

    select.top-menu-control {
        width: 150px;
    }
    
    .top-menu-control:hover {
        border: 1px solid black;
    }

    #page-title {
        line-height: 50px;
        text-align: left;
        float: left;
        position: relative;
        left: 10px;
        font-weight: bold;
        font-size: 25px;
        color: #F4F4F9;
    }
</style>
