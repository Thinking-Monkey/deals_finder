import { useState, useEffect } from 'react'
import Card from '../../components/Card'
import Button from '../../components/Button'
import DropDownButton from '../../components/DropDownButton'
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
  const [dealList, setDealList] = useState(Array<Deal>);
  
  useEffect(() => {
    async function cardsBuilder(): Promise<void> {
      try {
        const requestConfig = signed 
          ? { headers: { 'Authorization': `Bearer ${token}` } }
          : {};
        
        const response = await http.get('/deals', requestConfig);
        setDealList(response.data.deals);
      } catch(error) {
        setDealList([])
        console.error('Deals loading error:', error);
      }
    }
    cardsBuilder();

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
          <DropDownButton title="Store" />
          <DropDownButton title="Price" />
          <DropDownButton title="Sort" />
        </div> : ""} 
        <ul className=' p-1 flex flex-wrap items-center justify-center
                        content-center' >
          { (dealList) ? dealList.map((deal: Deal)=> {
              return <li className='  flex-shrink-0 m-6 realative
                                      overflow-hidden ' key={deal.title}>
                      < Card 
                        title={deal.title}
                        imgUrl={deal.thumb}
                        alt="Sample Image"
                        color={colorSelector(deal.store_name)}
                        price={Number(deal.normal_price)}
                        dealPrice={Number(deal.sale_price)}
                        deal_id={deal.deal_id}
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