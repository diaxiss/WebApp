<script setup lang="ts">
import { GoogleSignInButton, type CredentialResponse } from 'vue3-google-signin';
import { accessToken, googleAuthentificationSuccess, handleLogout } from '../utilities/userAuthentification';
import { userName } from '../utilities/constants';

const onLoginError = async (response: CredentialResponse) => {
    console.log('Error: ', response)
}

</script>

<template>

    <div class="header">
        <p>Header</p>
        <GoogleSignInButton
            v-if="!accessToken"
            type="standard"
            theme="filled_black"
            size="large"
            text="signin_with"
            shape="pill"
            logo_alignment="left"
            @success="googleAuthentificationSuccess" 
            @error="onLoginError"/>
        <button 
            v-else
            @click="handleLogout"
            >
            Log Out
        </button>
        <nav class="nav-bar">
            <router-link to="/">Home</router-link>
            <router-link to="/sets">Sets</router-link>
            <router-link to="/profile" v-if="userName">Profile</router-link>
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
    display: flex;
    margin-left: auto;
    margin-right: 10px;
    gap: 10px;
}

</style>