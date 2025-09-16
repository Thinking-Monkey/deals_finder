// import { useState, useEffect } from 'react'
// import Card from '../../components/Card'
// import Button from '../../components/Button'
// import DropDownButton from '../../components/DropDownButton'
// import { useAuth } from '../../hooks/useAuth';
// import RegisterLogin from '../../components/RegisterLogin';
// import http from '../../config/axios.config'

// interface Deal {
//   deal_id: string,
//   title: string,
//   store_name: string,
//   sale_price: string,
//   normal_price: string,
//   thumb: string
// }


// export default function Homepage(){
  
//   const { signed, token } = useAuth();
//   const [dealList, setDealList] = useState(Array<Deal>);
//   const [hasNext, setHasNext] = useState<boolean>(true)
//   const [pageNum, setPageNum] = useState<number>(1)
//   const [storeFilter, setStoreFilter] = useState(Array<string>)
//   const [priceFilter, setPriceFilter] = useState(Array<number>)

//   useEffect(() => {
//     async function cardsBuilder(): Promise<void> {
//       try {
//         const requestConfig = signed 
//           ? { headers: { 'Authorization': `Bearer ${token}` } }
//           : {};
        
//         const response = await http.get('/deals', requestConfig);
//         setDealList(response.data.deals);
//       } catch(error) {
//         setDealList([])
//         console.error('Deals loading error:', error);
//       }
//     }

//     async function populateFilter(): Promise<void> {
//       const filterList = await http.get('/filtersData', { headers: { 'Authorization': `Bearer ${token}` }})      
//       setPriceFilter(filterList.data.prices)
//       setStoreFilter(filterList.data.stores)
//     }

//     cardsBuilder();
    
//     if(signed){
//       populateFilter();
//     }

//     }, [signed])
  
//   const handleLoadMore = () => {
//     async function cardsBuilder(): Promise<void> {
//       try {
//         const response = await http.get(`/deals?page=${pageNum+1}`, { headers: { 'Authorization': `Bearer ${token}` } });
//         setDealList(response.data.deals);
//         setHasNext(response.data.hasNext)
//         setPageNum(pageNum+1)
//       } catch(error) {
//         setDealList([])
//         console.error('Deals loading error:', error);
//       }
//     }

//     cardsBuilder();
//   }

//   const handleLoadPrevious = () => {
//     async function cardsBuilder(): Promise<void> {
//       try {
//         const response = await http.get(`/deals?page=${pageNum-1}`, { headers: { 'Authorization': `Bearer ${token}` } });
//         setDealList(response.data.deals);
//         console.log(response.data)
//         setHasNext(response.data.hasNext)
//         setPageNum(pageNum-1)
//       } catch(error) {
//         setDealList([])
//         console.error('Deals loading error:', error);
//       }
//     }

//     cardsBuilder();
//   }

//   const handleFilter = () => {
//     async function cardsBuilder(): Promise<void> {
//       try {
//         const response = await http.get(`/deals?`, { headers: { 'Authorization': `Bearer ${token}` } });
//         setDealList(response.data.deals);
//         console.log(response.data)
//         setHasNext(response.data.hasNext)
//         setPageNum(pageNum-1)
//       } catch(error) {
//         setDealList([])
//         console.error('Deals loading error:', error);
//       }
//     }

//     cardsBuilder();
//   }

//   const colorSelector = (store_name: string): string => {
//     switch(store_name){
//       case "Steam":
//         return "bg-teal-500"
//       case "GOG":
//         return "bg-yellow-500"
//       case "Humble Store":
//         return "bg-red-500"
//       default:
//         return "bg-yellow-500"
//     }
//   }

//   return (
//     <>
//       <div className='flex-initial'>
//         { signed ? <div className='flex gap-20 items-center-safe justify-center py-5'>
//           <DropDownButton title="Store" contents={storeFilter}/>
//           <DropDownButton title="Price" contents={priceFilter}/>
//           {/* <DropDownButton title="Sort" /> */}
//         </div> : ""} 
//         <ul className=' p-1 flex flex-wrap items-center justify-center
//                         content-center' >
//           { (dealList) ? dealList.map((deal: Deal)=> {
//               return <li className='  flex-shrink-0 m-6 realative
//                                       overflow-hidden ' key={deal.title}>
//                       < Card 
//                         title={deal.title}
//                         imgUrl={deal.thumb}
//                         alt="Sample Image"
//                         color={colorSelector(deal.store_name)}
//                         price={Number(deal.normal_price)}
//                         dealPrice={Number(deal.sale_price)}
//                         deal_id={deal.deal_id}
//                         isLogged={signed}
//                       /></li>
//               }
//             ) : "There isn´t any deal"
//           }
//         </ul>
//         <div className='flex items-center-safe justify-center py-5'>
//           {  signed && hasNext ? <Button title="LOAD MORE" onClick={handleLoadMore}/> : <Button title="LOAD PREVIOUS" onClick={handleLoadPrevious}/> }
//           { !signed ? <RegisterLogin /> : "" }

//         </div>
//       </div>
//     </>
//   )
// }

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

interface FilterData {
  stores: Array<{id: string, name: string}>,
  prices: Array<number>
}

export default function Homepage(){
  
  const { signed, token } = useAuth();
  const [dealList, setDealList] = useState(Array<Deal>);
  const [hasNext, setHasNext] = useState<boolean>(true)
  const [pageNum, setPageNum] = useState<number>(1)
  const [filterData, setFilterData] = useState<FilterData>({stores: [], prices: []})
  
  // Filter states
  const [selectedStore, setSelectedStore] = useState<string>("")
  const [selectedMinPrice, setSelectedMinPrice] = useState<number | null>(null)
  const [selectedOrdering, setSelectedOrdering] = useState<string>("")

  const orderingOptions = [
    'deal_rating', 
    'sale_price',
    'normal_price',
    'title',
    'created_at',
    'metacritic_score'
  ];

  useEffect(() => {
    loadDeals();
    
    if(signed){
      populateFilter();
    }
  }, [signed])

  const loadDeals = async (page: number = 1, useFilters: boolean = false): Promise<void> => {
    try {
      const requestConfig = signed 
        ? { headers: { 'Authorization': `Bearer ${token}` } }
        : {};
      
      let endpoint = '/deals';
      let params: string[] = [];
      
      if (useFilters && signed) {
        endpoint = '/dealsFiltered';
        
        if (selectedStore) params.push(`store_id=${selectedStore}`);
        if (selectedMinPrice !== null) params.push(`min_price=${selectedMinPrice}`);
        if (selectedOrdering) params.push(`ordering=${selectedOrdering}`);
      }
      
      if (page > 1) params.push(`page=${page}`);
      
      if (params.length > 0) {
        endpoint += '?' + params.join('&');
      }
      
      const response = await http.get(endpoint, requestConfig);
      setDealList(response.data.deals);
      setHasNext(response.data.hasNext);
      setPageNum(page);
    } catch(error) {
      setDealList([])
      console.error('Deals loading error:', error);
    }
  }

  const populateFilter = async (): Promise<void> => {
    try {
      const filterList = await http.get('/filtersData', { 
        headers: { 'Authorization': `Bearer ${token}` }
      });      
      setFilterData({
        stores: filterList.data.stores,
        prices: filterList.data.prices
      });
    } catch(error) {
      console.error('Filter loading error:', error);
    }
  }

  const handleLoadMore = () => {
    const hasFilters = selectedStore || selectedMinPrice !== null || selectedOrdering;
    loadDeals(pageNum + 1, hasFilters);
  }

  const handleLoadPrevious = () => {
    if (pageNum > 1) {
      const hasFilters = selectedStore || selectedMinPrice !== null || selectedOrdering;
      loadDeals(pageNum - 1, hasFilters);
    }
  }

  const handleStoreFilter = (storeId: string) => {
    setSelectedStore(storeId);
    setPageNum(1);
    // Apply filter immediately
    setTimeout(() => {
      loadDeals(1, true);
    }, 0);
  }

  const handlePriceFilter = (minPrice: number) => {
    setSelectedMinPrice(minPrice);
    setPageNum(1);
    // Apply filter immediately
    setTimeout(() => {
      loadDeals(1, true);
    }, 0);
  }

  const handleOrderingFilter = (ordering: string) => {
    setSelectedOrdering(ordering);
    setPageNum(1);
    // Apply filter immediately
    setTimeout(() => {
      loadDeals(1, true);
    }, 0);
  }

  const clearFilters = () => {
    setSelectedStore("");
    setSelectedMinPrice(null);
    setSelectedOrdering("");
    setPageNum(1);
    loadDeals(1, false);
  }

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
        { signed ? 
          <div className='flex gap-20 items-center-safe justify-center py-5'>
            <DropDownButton 
              title="Store" 
              contents={filterData.stores}
              onSelect={handleStoreFilter}
              selectedValue={selectedStore}
            />
            <DropDownButton 
              title="Min Price" 
              contents={filterData.prices}
              onSelect={handlePriceFilter}
              selectedValue={selectedMinPrice}
            />
            <DropDownButton 
              title="Sort" 
              contents={orderingOptions}
              onSelect={handleOrderingFilter}
              selectedValue={selectedOrdering}
            />
            {(selectedStore || selectedMinPrice !== null || selectedOrdering) && (
              <Button title="Clear Filters" onClick={clearFilters} />
            )}
          </div> : ""
        } 
        <ul className=' p-1 flex flex-wrap items-center justify-center content-center' >
          { (dealList && dealList.length > 0) ? dealList.map((deal: Deal)=> {
              return <li className='flex-shrink-0 m-6 realative overflow-hidden' key={deal.deal_id}>
                      <Card 
                        title={deal.title}
                        imgUrl={deal.thumb}
                        alt="Sample Image"
                        color={colorSelector(deal.store_name)}
                        price={Number(deal.normal_price)}
                        dealPrice={Number(deal.sale_price)}
                        deal_id={deal.deal_id}
                        isLogged={signed}
                      />
                    </li>
              }
            ) : <div>There isn't any deal</div>
          }
        </ul>
        <div className='flex items-center-safe justify-center py-5'>
          {signed && (
            <>
              {pageNum > 1 && (
                <Button title="LOAD PREVIOUS" onClick={handleLoadPrevious}/>
              )}
              {hasNext && (
                <Button title="LOAD MORE" onClick={handleLoadMore}/>
              )}
            </>
          )}
          { !signed ? <RegisterLogin /> : "" }
        </div>
      </div>
    </>
  )
}