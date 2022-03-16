<template>
    <div class="sign-up-form">
        <div class="form-container">
            <div class="logout-confirm">
                <div class="welcome-message">
                    Are you sure you want to sign out of <span class="title">Annotated SVG Creator</span>?<br/>
                </div>
                                
                <div class="item button">
                    <input type="button" id="logout" value="Log Out" @click="logout(true)">
                </div>

                <div class="item button">
                    <input type="button" id="stay" value="Stay Logged In" @click="logout(false)">
                </div>
            </div>
        </div>
    </div>
</template>

<script>

export default {
    name: 'LogoutConfirm',
    methods: {
        logout(really) {
            if (really == true) {
                localStorage.clear()
                this.$emit('logout')
                this.$emit('display-message', 'information', 'We hope to see you again soon!')
            }
            this.$emit('close-logout-confirm')
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

.logout-confirm {
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

input:hover {
    border-bottom: 2px #586F7C solid;
    cursor: pointer;
}

.button {
    text-align: center; 
    border: 2px black solid;
    width: 49%;
    margin: auto;
    margin-bottom: 5px;
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


</style>
