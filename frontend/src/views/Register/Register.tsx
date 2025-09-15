import 'react'

export default function Register(){
   return (
    <div className='flex h-screen items-center justify-center'>
      <fieldset className="fieldset bg-white/30 border-white rounded-box w-xs border-1 p-4">

        <label className="label text-purple-900">Email</label>
        <input type="email" className="input
                                       bg-[#FCCEFD]/80
                                       text-black" placeholder="Email" />

        <label className="label text-purple-900">Password</label>
        <input type="password" className="input
                                       bg-[#FCCEFD]/80
                                       text-black" placeholder="Password" />
        
        <label className="label text-purple-900">Password Confirm</label>
        <input type="password" className="input
                                       bg-[#FCCEFD]/80
                                       text-black" placeholder="Password Confirm" />

        <button className="btn x-4 py-2 lg:px-5 lg:py-2.5 bg-white/20 border border-white/30 rounded-lg text-purple-900 font-semibold hover:bg-white/30 hover:-translate-y-0.5 transition-all duration-300 backdrop-blur-lg shadow-lg text-sm lg:text-base mt-4">Regist an account</button>
      </fieldset>
    </div>
  )
}