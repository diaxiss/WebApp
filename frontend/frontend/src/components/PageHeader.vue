<script setup lang="ts">
import { GoogleSignInButton, type CredentialResponse } from 'vue3-google-signin';
import { googleAuthentificationSuccess, handleLogout } from '../utilities/userAuthentification';
import { accessToken } from '../utilities/constants';
import { userName, userPicture } from '../utilities/constants';
import { imageFallback } from '../utilities/misc';
import "../styles/PageHeader.css"

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
                <img class="profile-picture" :src="`${userPicture}`"
                @error="imageFallback"/>
            </router-link>
        </div>
    </div>

</template>