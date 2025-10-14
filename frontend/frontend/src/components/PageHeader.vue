<script setup lang="ts">
import { GoogleSignInButton, type CredentialResponse } from 'vue3-google-signin';
import { accessToken, googleAuthentificationSuccess, handleLogout } from '../utilities/userAuthentification';
import { userName, userPicture } from '../utilities/constants';
import placeholder_image from '../assets/placeholder.png'

const onLoginError = async (response: CredentialResponse) => {
    console.log('Error: ', response)
}

</script>

<template>

    <div class="header">
        <nav class="nav-bar">
            <router-link to="/">Home</router-link>
            <router-link to="/sets">Sets</router-link>
            <router-link to="/wishlist" v-if="userName">Wishlist</router-link>
            <router-link to="/collection" v-if="userName">Collection</router-link>
        </nav>
        <div class="sign-in-buttons">
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
            <router-link to="/profile" v-if="userName">
                <img :src="userPicture || placeholder_image"
                    style="height: 25px; width: 25px; border-radius: 12.5px;"/>
            </router-link>
        </div>
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
    margin-left: 10px;
    gap: 10px;
}

.sign-in-buttons{
    margin-left: auto;
    margin-right: 10px;
    gap: 10px;
}

</style>