<script setup lang="ts">

import "../styles/PageHeader.css"

import { GoogleSignInButton, type CredentialResponse } from 'vue3-google-signin';

import { googleAuthentificationSuccess, handleLogout } from '../utilities/userAuthentification';
import { imageFallback } from '../utilities/misc';


import { userName, userPicture } from '../utilities/constants';
import { accessToken } from '../utilities/constants';
import { useRoute } from "vue-router";


const onLoginError = async (response: CredentialResponse) => {
    console.log('Error: ', response)
}
const route = useRoute()

</script>

<template>

    <div class="header">
        <nav class="nav-bar">
            <router-link to="/">Home</router-link>
            <router-link to="/users">Users</router-link>
            <router-link to="/sets">Sets</router-link>
            <router-link to="/wishlist" v-if="userName" :key="route.fullPath">Wishlist</router-link>
            <router-link to="/collection" v-if="userName" :key="route.fullPath">Collection</router-link>
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
            <router-link to="/profile" v-if="userName" :key="route.fullPath">
                <img class="profile-picture" :src="`${userPicture}`"
                @error="imageFallback"/>
            </router-link>
        </div>
    </div>

</template>