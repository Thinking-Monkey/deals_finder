import { useState, useEffect } from 'react'
export default function Card(props: {   title: string,
                                        price: number,
                                        dealPrice: number,
                                        color: string, 
                                        imgUrl: string, 
                                        alt: string,
                                        isLogged: boolean }){


    
    const [barCss, setBarCss] = useState<string>("")  

    const [cardButtonCss, setCardButtonCss] = useState<string>(`${props.color}
                        rounded-lg
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
        <div className="card overflow-hidden flex flex-col w-80 shadow-sm border-1 rounded-t-lg">
            <figure>
                <img
                src={props.imgUrl}
                alt={props.alt} 
                className='h-2/6 w-full'/>
            </figure>
            <hr className={barCss} />
            <div className="card-body h-4/6 items-center bg-white/50">
                <h2 className=" card-title font-black text-xl
                                text-center text-white
                                ">{ props.title }</h2>             
                <button type="button" className={cardButtonCss}>{locale(props.dealPrice)}</button>
                <div className="card-actions justify-end">
                   <p className="font-thin text-s sm:text-base md:text-lg text-center text-white pt-2 leading-relaxed">
                     Instead of <span className="text-[#f5600b]">{locale(props.price)}</span></p>
                </div>
            </div>
        </div>
        )
}