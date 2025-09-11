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
                        px-20
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
        <div className="card w-80 shadow-sm border-1 rounded-t-lg">
            <figure>
                <img
                src={props.imgUrl}
                alt={props.alt} 
                className='h-full w-full'/>
            </figure>
            <hr className={barCss} />
            <div className="card-body items-center bg-white/30">
                <h2 className=" card-title font-black text-xl
                                text-center text-white
                                ">{ props.title }</h2>
                <h3 className=" text-2xl font-thin
                                font-regular text-center text-white  
                                pb-4 sm:pb-6">{ props.subTitle }</h3>                
                <button type="button" className={cardButtonCss}>{locale(props.dealPrice)}</button>
                <div className="card-actions justify-end">
                   <p className="font-thin text-s sm:text-base md:text-lg text-center text-white pt-2 leading-relaxed">
                     Instead of <span className="text-[#FFD504]">{locale(props.price)}</span></p>
                </div>
            </div>
        </div>
        )
}