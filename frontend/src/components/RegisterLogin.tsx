import 'react'

export default function RegisterLogin(){
   return (
    <div className='flex-col'>
      <h3 className=' flex 
                      mb-5
                      l'>Register or Login to view, filter and sort all offerts!</h3>
      <div className='flex gap-5'>
        <div role="button" className="    cursor-pointer
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
                                          font-(family-name: Galano Grotesque Alt)">Register</div>
        <div role="button" className="    cursor-pointer
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