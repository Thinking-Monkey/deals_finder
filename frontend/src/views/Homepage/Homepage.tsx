import { useState, useEffect } from 'react'
import Card from '../../components/Card'
import Button from '../../components/Button'
import DropDownButton from '../../components/DropDownButton'
import Slider from '../../components/Slider'
import { useAuth } from '../../hooks/useAuth';
import RegisterLogin from '../../components/RegisterLogin';
import http from '../../config/axios.config'

interface Deal {
  deal_id: string,
  title: string,
  store_name: string,
  sale_price: string,
  normal_price: string,
  thumb: string
}


export default function Homepage(){
  
  const { signed, token } = useAuth();
  const [config, setConfig] = useState({})
  const [dealList, setDealList] = useState(Array<Deal>);
  
  useEffect(() => {
    if(signed){
      setConfig({
        header: {
          'Authorization': 'Bearer' + token
        }
      })
      console.log('sono passato di qui')
      console.log(token)
    } else {
      setConfig({})
    }

    async function cardsBuilder(config: object): Promise<void>{
      try {
        const response = await http.get('/deals', config);
        setDealList(response.data.deals);
      } catch(error){
        setDealList([])
        console.error('Deals loading error:', error);
      }
    }
    cardsBuilder(config);

  }, [signed])

  const colorSelector = (store_name: string): string => {
    switch(store_name){
      case "Steam":
        return "bg-teal-500"
      case "GOG":
        return "bg-yellow-500"
      case "Humble Store":
        return "bg-red-500"
      default:
        return "bg-yellow-500"
    }
  }

  return (
    <>
      <div className='flex-initial'>
        { signed ? <div className='flex gap-20 items-center-safe justify-center py-5'>
          <DropDownButton title="NONE" />
          <Slider />
          <DropDownButton title="NONE" />
        </div> : ""} 
        <ul className=' p-1 flex flex-wrap items-center justify-center
                        content-center' >
          { (dealList) ? dealList.map((deal: Deal)=> {
              return <li className='  flex-shrink-0 m-6 realative
                                      overflow-hidden ' key={deal.title}>< Card 
                title={deal.title}
                imgUrl={deal.thumb}
                alt="Sample Image"
                color={colorSelector(deal.store_name)}
                price={Number(deal.normal_price)}
                dealPrice={Number(deal.sale_price)}
                isLogged={signed}
                /></li>
              }
            ) : "There isn´t any deal"
          }
        </ul>
        <div className='flex items-center-safe justify-center py-5'>
          {  signed ? <Button title="LOAD MORE" /> : <RegisterLogin />}

        </div>
      </div>
    </>
  )
}