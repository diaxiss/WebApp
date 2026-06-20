import { ref, onMounted, onUnmounted } from "vue";

import placeholder_image from '../assets/placeholderCard.webp'
import { API_URL } from "../utilities/constants";

const fullscreenImage = ref<string | null>(null);
const imageWrapper = ref<HTMLElement | null>(null)
let animationFrame: number | null = null;

export function useFullscreenImage(){


    //----------------------
    // Fullscreen card
    //----------------------
    async function openImage(image: string){

        document.body.style.overflow = "hidden";

        const url = `${API_URL}/images/${image}.png`
        // Try to load the image
        const img = new Image()
        img.src = url

        // Wait for success or error
        img.onload = () => {
            fullscreenImage.value = url
        }

        img.onerror = () => {
            fullscreenImage.value = placeholder_image
        }
    }

    function closeImage(){
        document.body.style.overflow = "scroll";
        fullscreenImage.value = null
    }

    function handleMouseMove(e: MouseEvent){

        if(!imageWrapper.value) return

        if(animationFrame) cancelAnimationFrame(animationFrame)

        animationFrame = requestAnimationFrame(() => {
            const rect = imageWrapper.value!.getBoundingClientRect()

            const x = ((e.clientX - rect.left)/rect.width) - 0.5
            const y = ((e.clientY - rect.top)/rect.height) - 0.5

            const rotateX = y * -10
            const rotateY = x * 10

        imageWrapper.value!.style.transition = `transform 0.3s ease-out`
        imageWrapper.value!.style.transform = `
            perspective(800px)
            rotateX(${rotateX}deg)
            rotateY(${rotateY}deg)
            scale(1.05)
        `
        })
    }

    function resetTransform(){

        if(!imageWrapper.value) return
        imageWrapper.value.style.transition = `transform 0.5s cubic-bezier(0.22, 1, 0.36, 1)`;
        imageWrapper.value.style.transform = `
            perspective(800px)
            rotateX(0deg)
            rotateY(0deg)
            scale(1)
        `
    }

    // Close on Esc key
    onMounted(() => {
        window.addEventListener('keydown', e => {
            if (e.key === 'Escape') closeImage()
            })  
        })
    onUnmounted(() => {
        closeImage()
        window.removeEventListener('keydown', e => {
            if (e.key === 'Escape') closeImage()
            })
    })

    return {openImage, closeImage,
        handleMouseMove, resetTransform,
        fullscreenImage, imageWrapper}
}