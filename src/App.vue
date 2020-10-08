<template>
    <TopMenuBar />
</template>

<script>
import TopMenuBar from "./components/TopMenuBar.vue";

export default {
name: "App",
components: {
    TopMenuBar,
},
};
</script>

<style>
    body {
        margin: 0;
        font-family: 'Roboto', sans-serif;
    }

    html {
        background-color: #F4F4F9;
    }
</style>
