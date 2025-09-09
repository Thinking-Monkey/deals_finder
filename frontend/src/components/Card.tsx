import ImageThumb from './ImageThumb.tsx'
import { useState, useEffect } from 'react'
export default function Card(props: {   title: string,
                                        subTitle: string,
                                        price: number,
                                        dealPrice: number,
                                        color: string, 
                                        imgUrl: string, 
                                        alt: string,
                                        isLogged: boolean }){


    
    const [barCss, setBarCss] = useState<string>("")                                       
    const [cardButtonCss, setCardButtonCss] = useState<string>(`rounded-lg
                        bg-[#FFD504]
                        font-black
                        text-black
                        text-[2.5em]
                        px-2
                        py-3
                        font-(family-name: Galano Grotesque Alt)`)
    
    useEffect(() => {
        if(props.isLogged) {
            setCardButtonCss((prev) => prev.concat('hover:bg-black active:scale-95 transition-transform transform'));
        } else {
            setCardButtonCss((prev) => prev.concat('disabled'));
        }
        setBarCss(`h-5 ${props.color} border-0`);
    }, [props.isLogged, props.color])
    
    const openDetail = (id: string) => {

    }

    const locale = (value: number): string => {
        return value.toLocaleString('en-US', { style: 'currency', currency: 'USD' });
    }

    return (
        <div className="
        flex flex-col
        w-80 
        h-90 sm:h-100 md:h-[22rem] lg:h-[24rem] xl:h-[25rem] 2xl:h-[26rem]
        bg-white/10
        overflow-hidden
        border-1
        rounded-[20%]
        border-gradient-to-r from-[#fff] to-[#999]/50
        shadow-lg
        mx-auto">
        
            {/* Sezione Immagine - sempre 1/3 */}
            <div className="flex flex-col h-1/3 ">
                <ImageThumb imgUrl={props.imgUrl} alt={props.alt}/>
            </div>
            
            <hr className={barCss} />

            {/* Sezione Contenuto - sempre 2/3 */}
            <div className="
                flex flex-col
                justify-center
                p-4 sm:p-6 md:p-8
                h-2/3">
                <h3 className=" text-xl sm:text-2xl 
                                font-black text-center text-white  
                                pb-1 sm:pb-2">{ props.title }</h3>
                <h4 className=" text-xl sm:text-2xl 
                                font-regular text-center text-white  
                                pb-4 sm:pb-6">{ props.subTitle }</h4>
                <button type="button" className={cardButtonCss}>{locale(props.dealPrice)}</button>
                <p className="font-thin text-s sm:text-base md:text-lg text-center text-white pt-2 leading-relaxed">
                    Instead of <span className="text-yellow-500">{locale(props.price)}</span></p>
            </div>
        </div>
        )
}