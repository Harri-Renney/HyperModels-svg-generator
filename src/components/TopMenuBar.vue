<template>
    <div class="top-menu-bar">
        <div id="top-menu-export-button">
            <i class="mi-export"/>
            Export
        </div>
    </div>
</template>

<script>
export default {
    name: 'TopMenuBar'    
}
</script>

<style scoped>
    .top-menu-bar {
        width: 100%;
        height: 50px;
        background-color: darkgray;
        text-align: center;
        line-height: 50px;
    }

    i {
        height: 24px;
        width: 24px;
    }
</style>