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
    methods: {
        onSubmit() {
            if (this.username === '' || this.password === '') {
                alert('You must enter your username and password to login')
                return
            }

            this.getResponse()

            console.log(this.error)
            
            if (this.error === '') {
                this.messageContent = 'Login successful for ' + this.username
                this.messageType = 'success'
                this.username = ''
                this.password = ''
            } else if (this.error !== '') {
                this.messageContent = 'Login failed. Please try again'
                this.messageType = 'error'
                this.password = ''
            }

            this.$emit('display-message', this.messageType, this.messageContent)
        },
        signIn() {
            axios.defaults.headers.post['Content-Type'] = 'application/json;';

            return axios.post('http://localhost:8000/login', {
                username: this.username,
                password: this.password
            });

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