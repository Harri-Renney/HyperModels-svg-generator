<template>
    <TopMenuBar @toggle-sign-in-form="showSignInForm = !showSignInForm"/>
    <LeftControlPicker />

    <transition
    name="show-hide-sign-in-form"
    enter-active-class="animate__animated animate__fadeInDown animate__faster"
    leave-active-class="animate__animated animate__fadeOutUp animate__faster"
    >
    <SignInForm 
    v-if="showSignInForm"
    @display-message="displayMessage"
    @close-sign-in-form="showSignInForm = !showSignInForm"/>
    </transition>

    <transition
    name="show-hide-sign-up-form"
    enter-active-class="animate__animated animate__fadeInDown animate__faster"
    leave-active-class="animate__animated animate__fadeOutUp animate__faster">
        <SignUpForm
        v-if="showSignUpForm"
        @close-signup-form="this.showSignUpForm = false"
        >
        </SignUpForm>
    </transition>
    
    <transition
    name="show-hide-message"
    enter-active-class="animate__animated animate__fadeInDown animate__faster"
    leave-active-class="animate__animated animate__fadeOutUp animate__faster"
    >
    <Message
    v-if="showMessage"
    :messageType="messageType"
    :messageContent="messageContent"
    @close-message="showMessage = false"/>
    </transition>
</template>

<script>
import TopMenuBar from "./components/TopMenuBar.vue"
import LeftControlPicker from "./components/LeftControlPicker.vue"
import SignInForm from "./components/SignInForm.vue"
import Message from "./components/Message.vue"
import SignUpForm from "./components/SignUpForm.vue"

export default {
    name: "App",
    components: {
        TopMenuBar,
        LeftControlPicker,
        SignInForm,
        Message,
        SignUpForm
    },
    data() {
        return {
            showSignInForm: false,
            showMessage: false,
            messageType: '',
            messageContent: '',
            showSignUpForm: false
        }
    },
    methods: {
        displayMessage(messageType, messageContent) {
            this.messageType = messageType
            this.messageContent = messageContent
            this.showMessage = true
            setTimeout(() => this.showMessage = false, 4000)
        },
        loggedIn() {
            return localStorage.getItem(btoa('user') !== null)
        },
        displaySignUpForm() {
            console.log('hello')
            this.showSignUpForm = true;
        }
    },
    mounted() {
        if (!this.loggedIn()) {
            setTimeout(() => {
                this.displaySignUpForm()
            }, 500);
        }
    }
};
</script>

<style>
    body {
        margin: 0;
        font-family: 'Roboto', sans-serif;
        height: 100%;
    }

    html {
        background-color: #F4F4F9;
        height: 100%;
    }

    #app {
        height: 100%;
    }

    .top-menu-bar {
        z-index: 100;
    }

    .sign-in-form {
        z-index: 50;
    }

    .left-control-picker {
        float: left;
    }
</style>
