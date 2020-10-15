<template>
    <div class="sign-in-form">
        <form @submit.prevent="onSubmit">
            <div class="item">
                <input type="text" id="username" v-model="username" placeholder="Username">
            </div>

            <div class="item">
                <input type="password" id="password" v-model="password" placeholder="Password">
            </div>

            <div class="item">
                <input type="submit" id="submit" value="Sign In">
            </div>
        </form>
    </div>
</template>

<script>

import axios from 'axios'
import qs from 'querystring'

export default {
    name: 'SignInForm',
    data() {
        return {
            username: '',
            password: '',
            messageType: '',
            messageContent: '',
            error: '',
            response: ''
        }
    },
    computed: {
        requestBody() {
            return {
                username: this.username,
                password: this.password
            }
        }
    },
    methods: {
        async onSubmit() {
            // Make sure username and password are not empty
            if (this.username === '' || this.password === '') {
                alert('You must enter your username and password to login')
                return
            }

            // Call the API
            await this.getResponse()
            
            // Logic for response
            if (this.error === '') {
                this.messageContent = 'Login successful for ' + this.username
                this.messageType = 'success'
                this.username = ''
                this.password = ''
            } else if (this.error !== '') {
                console.log(this.error)
                this.messageContent = 'Login failed. Please try again'
                this.messageType = 'error'
                this.password = ''
            }

            this.$emit('display-message', this.messageType, this.messageContent)
        },
        signIn() {
            // Set Content-Type header
            axios.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded;';

            // Call the API
            return axios.post('http://localhost:8000/login', qs.stringify(this.requestBody));
        },
        async getResponse() {
            await this.signIn()
            .then((response) => {
                this.response = response.data
                this.error = ''
            })
            .catch((error) => {
                this.error = error
            })
        }
    }
}
</script>

<style scoped>
    .sign-in-form {
        position: absolute;
        top: 60px;
        right: 10px;
        border: 2px #586F7C solid;
        border-radius: 2px;
        background-color: #B8DBD9;
        width: 250px;
    }

    input {
        width: 100%;
        box-sizing: border-box;
        padding: 5px;
        height: 35px;
        outline: none;
        background-color: #F4F4F9;
        border: none;
        border-bottom: 2px black solid;
    }

    input:focus {
        border-bottom: 2px #586F7C solid;
    }

    #submit {
        width: 100%;
        cursor: pointer;
    }
    
    label {
        display: block;
        text-align: left;
    }
    
    .item {
        padding: 5px;
    }

</style>