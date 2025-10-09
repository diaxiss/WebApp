<script lang="ts">


</script>

<template>

    <div class="header">
        <p>Header</p>
        <nav class="nav-bar">
            <router-link to="/">Home</router-link>
            <router-link to="/sets">Sets</router-link>
        </nav>
    </div>

</template>

<style>

.header{
    display: flex;
    height: 100%;
    width: 100%;
    background-color: #202020;
    align-items: center; 
}
.nav-bar{
    margin-left: auto;
}

</style>