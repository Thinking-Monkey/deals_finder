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
    loadDeals(1, false);
    
    if(signed){
      populateFilter();
    }
  }, [signed])

  const loadDeals = async (
    page: number = 1, 
    useFilters: boolean | undefined,
    storeFilter?: string,
    priceFilter?: number | null,
    orderingFilter?: string
  ): Promise<void> => {
    try {
      const requestConfig = signed 
        ? { headers: { 'Authorization': `Bearer ${token}` } }
        : {};
      
      let endpoint = '/deals';
      const params: string[] = [];

      if (useFilters && signed) {
        endpoint = '/dealsFiltered';
        
        // Usa i parametri passati o i valori attuali dello state
        const currentStore = storeFilter !== undefined ? storeFilter : selectedStore;
        const currentMinPrice = priceFilter !== undefined ? priceFilter : selectedMinPrice;
        const currentOrdering = orderingFilter !== undefined ? orderingFilter : selectedOrdering;
        
        if (currentStore != "") params.push(`store=${currentStore}`);
        if (currentMinPrice !== null) params.push(`min_price=${currentMinPrice}`);
        if (currentOrdering != "") params.push(`ordering=${currentOrdering}`);
      }
      
      console.log(`Dentro Deals : ${storeFilter !== undefined ? storeFilter : selectedStore}`)
      if (page > 1) params.push(`page=${page}`);
      
      if (params.length > 0) {
        endpoint += '?' + params.join('&');
      }
      
      const response = await http.get(endpoint, requestConfig);
      console.log(response)
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
    const hasFilters = selectedStore != "" || selectedMinPrice !== null || selectedOrdering != "";
    loadDeals(pageNum + 1, hasFilters);
  }

  const handleLoadPrevious = () => {
    if (pageNum > 1) {
      const hasFilters = selectedStore != "" || selectedMinPrice !== null || selectedOrdering != "";
      loadDeals(pageNum - 1, hasFilters);
    }
  }

  const handleStoreFilter = (storeId: string) => {
    setSelectedStore(storeId);
    setPageNum(1);
    // Passa direttamente il nuovo valore invece di affidarti allo state
    loadDeals(1, true, storeId, selectedMinPrice, selectedOrdering);
  }

  const handlePriceFilter = (minPrice: number) => {
    setSelectedMinPrice(minPrice);
    setPageNum(1);
    // Passa direttamente il nuovo valore invece di affidarti allo state
    loadDeals(1, true, selectedStore, minPrice, selectedOrdering);
  }

  const handleOrderingFilter = (ordering: string) => {
    setSelectedOrdering(ordering);
    setPageNum(1);
    // Passa direttamente il nuovo valore invece di affidarti allo state
    loadDeals(1, true, selectedStore, selectedMinPrice, ordering);
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