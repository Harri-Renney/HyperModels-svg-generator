<template>
    <button 
    id="top-menu-sign-in-button" 
    class="top-menu-control"
    @click="toggleSignInForm">
        <i class="mi-user"/>
        Sign In
    </button>
</template>

<script>
export default {
    name: 'SignIn',
    methods: {
        toggleSignInForm() {
            this.$emit('toggle-sign-in-form')
        }
    }
}
</script>

<style scoped>

    #top-menu-sign-in-button {
        float: right;
        margin-right: 10px;
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
    }
</style>