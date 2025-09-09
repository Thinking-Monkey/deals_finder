export default function ImageThumb( {imgUrl, alt} : {imgUrl: string, alt: string}){
   return (
    <figure className="
                      flex justify-center items-center 
                      object-fit">
      <img 
        src={imgUrl}
        alt={alt}
        className="w-full h-full object-cover" 
      />
    </figure>
  )
}