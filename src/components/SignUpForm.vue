<template>
    <div class="sign-up-form">
        <div class="form-container">
            <form @submit.prevent="onSubmit">
                <div class="welcome-message">
                    Welcome to <span class="title">Annotated SVG Creator</span>!<br/>
                    Please sign up in order to save your designs!
                </div>
                <div class="item text">
                    <input required type="text" id="username" v-model="username" placeholder="Username">
                </div>

                <div class="item text">
                    <input required type="email" id="email" v-model="email" placeholder="Email Address">
                </div>

                <div class="item text">
                    <input required type="password" id="password" v-model="password" placeholder="Password">
                </div>

                <div class="item button">
                    <input type="submit" id="submit" value="Sign Up">
                </div>

                <div class="item skip" @click="closeSignUpForm">
                    <span class="skip">Skip and continue</span>
                </div>
            </form>
        </div>
    </div>
</template>

<script>
import axios from 'axios'
import qs from 'querystring'

export default {
    name: 'SignUpForm',
    data() {
        return {
            username: '',
            password: '',
            email: ''
        }
    },
    computed: {
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
        closeSignUpForm() {
            this.$emit('close-signup-form')
        },
        async onSubmit() {
            // Make sure username and password are not empty
            if (this.username === '' || this.password === '' || this.email === '') {
                alert('All fields must be present in order to create account')
                return
            }

            // Call the API
            await this.getResponse()
            
            // Logic for response
            if (this.status == 200) {
                this.messageContent = 'Account created successfully. Please login.'
                this.messageType = 'success'
                this.username = ''
                this.email = ''
                this.password = ''
                this.closeSignUpForm()
            } else if (this.error !== 200) {
                console.log(this.error)
                this.messageContent = 'Login failed. Please try again'
                this.messageType = 'error'
                this.password = ''
            }

            this.$emit('display-message', this.messageType, this.messageContent)
        },
        signUp() {
            // Set Content-Type header
            axios.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded;';

            // Call the API
            return axios.post('http://localhost:8000/signup', qs.stringify({
                username: this.username,
                email: this.email,
                password: this.password
            }));
        },
        async getResponse() {
            await this.signUp()
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
    z-index: 90;
}

form {
    max-width: 35%;
    background-color: #F4F4F9;
    border: solid #B8DBD9 3px;
    border-radius: 2px;
    z-index: 100;
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
    width: 49%;
    margin: auto;
    border-bottom: 4px black solid;
}

.welcome-message {
    margin: 10px;
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
}

div .skip {
    text-align: center;
    color: #586F7C;
    margin-top: 10px;
    cursor: pointer;
}

div .skip :hover {
    color: #B8DBD9;
}

span .skip {
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
</style>