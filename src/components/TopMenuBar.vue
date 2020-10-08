<template>
    <div class="top-menu-bar">
        <span id="page-title">Annotated SVG Creator</span>
        <button id="top-menu-export-button">
            <i class="mi-export"/>
            Export
        </button>
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
        background-color: #586F7C;
        text-align: center;
        position: relative;
    }

    #top-menu-export-button {
        height: 30px;
        font-size: 15px;
        border: none;
        border-radius: 5px;
        width: 100px;
        position: absolute;
        top: 10px;
        cursor: pointer;
    }

    #top-menu-export-button:hover {
        border: 1px solid black;
        background-color: #F4F4F9;
    }

    #page-title {
        line-height: 50px;
        position: absolute;
        left: 5px;
        font-weight: bold;
        font-size: 25px;
        color: #F4F4F9
    }
</style>