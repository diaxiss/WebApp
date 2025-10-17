import { ref, onMounted, onUnmounted } from "vue";

import placeholder_image from '../assets/placeholder.png'

const fullscreenImage = ref<string | null>(null);
const imageWrapper = ref<HTMLElement | null>(null)
let animationFrame: number | null = null;

export function useFullscreenImage(){


    //----------------------
    // Fullscreen card
    //----------------------
    async function openImage(image: string | null){
        fullscreenImage.value = image ? `http://localhost:8000/images/${image}` : placeholder_image
    }

    function closeImage(){
        fullscreenImage.value = null
    }

    function handleMouseEnter() {
    if (!imageWrapper.value) return

    void imageWrapper.value.offsetWidth;

    // Temporary small transition on hover start
    imageWrapper.value.style.transition = 'transform 0.2s cubic-bezier(0.22, 1, 0.36, 1)'
    imageWrapper.value.style.transform = 'perspective(800px) scale(1.05)'
    }

    function handleMouseMove(e: MouseEvent){

        if(!imageWrapper.value) return

        if(animationFrame) cancelAnimationFrame(animationFrame)

        animationFrame = requestAnimationFrame(() => {
            const rect = imageWrapper.value!.getBoundingClientRect()
            const x = e.clientX - rect.left
            const y = e.clientY - rect.top

            const centerX = rect.width / 2
            const centerY = rect.height / 2

            const rotateX = ((y- centerY) / centerY) * -10
            const rotateY = ((x- centerX) / centerX) * 10

        imageWrapper.value!.style.transition = `transform 0.1s ease-out`
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
        imageWrapper.value.style.transition = `transform 0.3s cubic-bezier(0.22, 1, 0.36, 1)`;
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
    window.removeEventListener('keydown', e => {
        if (e.key === 'Escape') closeImage()
        })
    })

    return {openImage, closeImage,
        handleMouseEnter, handleMouseMove, resetTransform,
        fullscreenImage, imageWrapper}
}