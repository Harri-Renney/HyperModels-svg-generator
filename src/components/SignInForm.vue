<template>
    <div class="sign-in-form">
        <form v-show="!signedInCheck" @submit.prevent="onSubmit">
            <div class="item">
                <input type="text" id="username" v-model="username" placeholder="Username">
            </div>

            <div class="item">
                <input type="password" id="password" v-model="password" placeholder="Password">
            </div>

            <div class="item">
                <input type="submit" id="submit" value="Sign In">
            </div>

            <div class="item">
                <input type="button" id="signup" value="Sign Up" @click="showSignUpForm">
            </div>
        </form>
        <form v-show="signedInCheck" @submit.prevent="onSubmit">
            <div class="item">
                <input type="button" id="logout" value="Log Out" @click="logout">
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
            error: {},
            response: {},
            user: {},
            signedInCheck: false,
        }
    },
    mounted() {
        this.signedIn()
    },
    computed: {
        auth() {
            return {
                auth: {
                    username: btoa(this.username),
                    password: btoa(this.password)
                }
            }
        },
        status() {
            if (this.error.length !== 0) {
                return this.error.response.status
            } else if (this.response.length !== 0) {
                return this.response.status
            } else {
                return 500;
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
            if (this.status == 200) {
                this.user = this.response.user
                this.messageContent = 'Login successful for ' + this.username
                this.messageType = 'success'
                this.username = ''
                this.password = ''
                if (typeof(Storage) !== "undefined") {
                    localStorage.setItem(btoa('token'), btoa(this.response.token))
                    localStorage.setItem(btoa('user'), btoa(JSON.stringify(this.user)))
                    this.$emit('close-sign-in-form')
                    this.$emit('successful-sign-in')
                } else {
                    this.messageType = 'error'
                    this.messageContent = 'Sign in is not supported on your browser'
                }
            } else if (this.error !== 200) {
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
            return axios.get(process.env.VUE_APP_SVG_API_URL + '/login', this.auth);
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
        },
        showSignUpForm() {
            this.$emit('show-sign-up-form')
        },
        logout() {
            console.log("here")
            this.$emit('show-logout-confirm')
        },
        signedIn() {
            this.signedInCheck = localStorage.getItem(btoa('user')) !== null
        }
    }
}
</script>

<style scoped>
    .sign-in-form {
        z-index: 105;
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

    input[type='text'] :focus {
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

    #signup {
        cursor: pointer;
    }
</style>
