import 'react'
import { useNavigate } from 'react-router';

export default function RegisterLogin(){
  const navigate = useNavigate();

  const handleNavigation = (page: string) => {
    navigate(page)
  }

  return (
  <div className='flex-col'>
    <h3 className=' flex 
                    mb-5
                    content-center
                    justify-center
                    '>Register or Login to view, filter and sort all offerts!</h3>
    <div className='flex gap-5 
                    content-center
                    justify-center'>
      <button role="button" onClick={() => handleNavigation('register')} className=" cursor-pointer
                                        opacity-85
                                        rounded-xl
                                        bg-gradient-to-r from-[#FCCEFD] to-[#F7C1EF]/47
                                        hover:bg-purple-700
                                        text-purple-950
                                        font-black
                                        text-[1.1em]
                                        px-12
                                        py-5
                                        border-1
                                        border-white
                                        font-(family-name: Galano Grotesque Alt)">Register</button>
      <div role="button" onClick={() => handleNavigation('login')} className="    cursor-pointer
                                        opacity-85
                                        rounded-xl
                                        bg-gradient-to-r from-[#FCCEFD] to-[#F7C1EF]/47
                                        hover:bg-purple-700
                                        text-purple-950
                                        font-black
                                        text-[1.1em]
                                        px-12
                                        py-5
                                        border-1
                                        border-white
                                        font-(family-name: Galano Grotesque Alt)">Login</div>
    </div>
  </div>
)
}