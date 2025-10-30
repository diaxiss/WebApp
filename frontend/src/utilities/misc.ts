import placeholder_image from '../assets/placeholderCard.webp'

export function imageFallback(event: Event){
  console.log(event)
  const target = event.target as HTMLImageElement || null;
  if (target){
    target.src = placeholder_image
  }
}