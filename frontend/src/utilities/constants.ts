import { computed, ref } from "vue"


export const API_URL = import.meta.env.VITE_API_URL

export const loading = ref<boolean>(false)


//----------------------------------
// User data and authentification
//----------------------------------

export const accessToken = ref(localStorage.getItem('accessToken'))

export const isLoggedOut = computed(() => {
    return accessToken.value === null
})

export const userName = ref<string | null>(localStorage.getItem('user'))
export const userId = ref<string | null>(localStorage.getItem('sub'))
export const userPicture = ref<string | null>(`http://localhost:8000/user_images/${localStorage.getItem('image')}.png`)