<script setup lang="ts">
import { GoogleSignInButton, type CredentialResponse } from 'vue3-google-signin';
import { googleAuthentificationSuccess } from '../utilities/userAuthentification';
import { accessToken } from '../utilities/constants';

const onLoginError = async (response: CredentialResponse) => {
    console.log('Error: ', response)
}

</script>

<template>

    <div class="header">
        <p>Header</p>
        <GoogleSignInButton
            v-show="accessToken == null"
            type="standard"
            theme="filled_blue"
            size="large"
            text="signin_with"
            shape="rectangular"
            logo_alignment="left"
            @success="googleAuthentificationSuccess" 
            @error="onLoginError"/>
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