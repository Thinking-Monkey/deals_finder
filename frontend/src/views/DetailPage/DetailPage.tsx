import { useState, useEffect } from 'react';
import { useParams } from 'react-router';
import { useAuth } from '../../hooks/useAuth';
import http from '../../config/axios.config';
import Button from '../../components/Button'
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faStore } from '@fortawesome/free-solid-svg-icons';

interface DealDetail {
  deal_id: string;
  title: string;
  store_name: string;
  sale_price: string;
  normal_price: string;
  thumb: string;
  metacritic_score?: number;
  release_date?: string;
  last_change?: string;
  update_at?: string;
  deal_rating?: string;
  steam_app_id?: number;
  steam_rating_text?: string;
  store?: number;
}

export default function DealDetailPage() {
  const { deal_id } = useParams<{ deal_id: string }>();
  const { signed, token } = useAuth();
  const [deal, setDeal] = useState<DealDetail | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  let urlStore:string = ""

  useEffect(() => {
    async function fetchDealDetail(): Promise<void> {
      if (!deal_id) {
        setError('Deal ID not provided');
        setLoading(false);
        return;
      }

      try {
        const requestConfig = signed 
          ? { headers: { 'Authorization': `Bearer ${token}` } }
          : {};
        const doubleEncoded = encodeURIComponent(encodeURIComponent(deal_id));

        const response = await http.get(`/dealDetail?deal_id=${doubleEncoded}`, requestConfig);
        setDeal(response.data.deal);
        setError(null);
      } catch (error: any) {
        console.error('Error fetching deal details:', error);
        setError('Failed to load deal details');
        setDeal(null);
      } finally {
        setLoading(false);
      }
    }

    fetchDealDetail();
  }, [deal_id, signed, token]);

  const processString = (str: string, separator: string) => {
    return str.toLowerCase()
        .replace(/[^a-zA-Z0-9]/g, separator)
        .replace(/_{2,}/g, '_')
        .replace(/-2,}/g, '-');
    };
  
  const urlColorSelector = (store_name: string) => {
    if(deal != null )
        switch(store_name) {
        case "Steam":
            urlStore = `https://store.steampowered.com/app/${deal.steam_app_id}`
            return "bg-teal-500";
        case "GOG":
            console.log(processString(deal.title, '_'))
            urlStore = `https://www.gog.com/en/game/${processString(deal.title, '_')}`
            return "bg-yellow-500";
        case "Humble Store":
            urlStore = `https://www.humblebundle.com/store/${processString(deal.title,'-')}`
            return "bg-red-500";
        default:
            return "bg-yellow-500";
        }
  };

  const formatPrice = (price: string): string => {
    return Number(price).toLocaleString('en-US', { 
      style: 'currency', 
      currency: 'USD' 
    });
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center min-h-screen">
        <div className="text-white text-xl">Loading deal details...</div>
      </div>
    );
  }

  if (error || !deal) {
    return (
      <div className="flex justify-center items-center min-h-screen">
        <div className="text-red-500 text-xl">{error || 'Deal not found'}</div>
      </div>
    );
  }

  const formatData = (date: string): string =>{
    const dateString = new Date(date); // Converti in millisecondi

    // Formato italiano
    return dateString.toLocaleDateString('en-EN');
  }

  const openExternalURL = (url: string) => {
    window.open(url, '_blank', 'noopener,noreferrer');
  };


  return (
    <div className="min-h-screen bg-white/30 text-white p-6">
      <div className="max-w-4xl mx-auto">

        {/* Main content */}
        <div className="bg-gray-800/50 rounded-lg overflow-hidden shadow-xl">
          <div className="md:flex">
            {/* Image section */}
            <div className="md:w-1/2">
              <img
                src={deal.thumb}
                alt={deal.title}
                className="w-full h-96 object-cover"
              />
            </div>

            {/* Details section */}
            <div className="md:w-1/2 p-8">
              <h1 className="text-3xl font-bold mb-4">{deal.title}</h1>
              
              <div className="mb-6">
                <span className={`inline-block px-3 py-1 rounded-full text-black font-semibold ${urlColorSelector(deal.store_name)}`}>
                  {deal.store_name}
                </span>
              </div>

              {/* Price section */}
              <div className="mb-6">
                <div className="flex items-baseline gap-4">
                  <span className="text-4xl font-bold text-green-400">
                    {formatPrice(deal.sale_price)}
                  </span>
                  <span className="text-xl text-gray-400 line-through">
                    {formatPrice(deal.normal_price)}
                  </span>
                </div>
              </div>
                {deal.steam_rating_text && (
                  <div>
                    <span className="text-white">Steam Score: </span>
                    <span className="text-indigo-300">{deal.steam_rating_text}</span>
                  </div> )}

                {deal.metacritic_score ?
                  <div>
                    <span className="text-white">Metacritic Score: </span>
                    <span className="text-indigo-300">{deal.metacritic_score}/100</span>
                  </div> : <div className="text-red-300">Metacritic score: not present </div>}

                {deal.release_date ?
                  <div>
                    <span className="text-white">Release Date: </span>
                    <span className="text-indigo-300">{formatData(deal.release_date)}</span>
                  </div> : <span className="text-red-300">Release Data: Not Present</span>
                }

                {deal.deal_rating && (
                  <div>
                    <span className="text-white">Deal Rating: </span>
                    <span className="text-indigo-300">{deal.deal_rating}/10</span>
                  </div>
                )}
              </div>
            </div>
          </div>
        <div className="flex mt-8 justify-between">  
            <Button 
                onClick={() => window.history.back()}
                title='← Back to deals'
            />
          <Button 
            onClick={() => openExternalURL(urlStore)}
            title={<FontAwesomeIcon icon={faStore} className='flex text-purple-600'/>}
          />
          </div>
        </div>
    </div> 
  );
}