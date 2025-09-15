import { useRef, useState } from 'react'
import { useAuth } from '../../hooks/useAuth'
import { useNavigate } from 'react-router';

export default function Login(){
  const username = useRef<HTMLInputElement>(null)
  const password = useRef<HTMLInputElement>(null)
  const { signIn, signed } = useAuth();
  const navigate = useNavigate();
  const handleErrorModal = () => {
      document.getElementById('my_modal_1').showModal()
  }
  const handleOnSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault()
    const credentials = {username: username.current.value, password: password.current.value}
    try{
      await signIn(credentials)
      if(signed){
        navigate("/")
      }
    } catch(e) {
      handleErrorModal()
      throw new ErrorEvent("Error during login: " + e);
    }
  }

  return (
    <div className='flex flex-col h-screen items-center justify-center'>
      <form className=" fieldset 
                      bg-white/30 
                      border-white 
                        rounded-box 
                        w-xs border-1 p-4" onSubmit={handleOnSubmit}>

        <label className="label text-purple-900">Username</label>
        <input ref={username} type="username" 
                              className="input
                                        bg-[#FCCEFD]/80
                                        text-black" 
                              placeholder="Username" 
                              required/>

        <label className="label text-purple-900">Password</label>
        <input ref={password} type="password" 
                              className="input
                                        bg-[#FCCEFD]/80
                                        text-black" 
                              placeholder="Password" 
                              required/>

        <button className=" btn 
                            mt-4
                            x-4 py-2 lg:px-5 lg:py-2.5 
                            bg-white/20 border 
                            border-white/30 
                            rounded-lg 
                            text-purple-900 font-semibold text-sm lg:text-base 
                            hover:bg-white/30 hover:-translate-y-0.5 transition-all duration-300 
                            backdrop-blur-lg shadow-lg"
                type="submit">Login</button>
      </form>
      <h3 className=' flex 
                mt-5
                content-center
                justify-center
                '>Don't have an account?&nbsp;<a className="link text-purple-600 hover:text-purple-300" onClick={() => navigate("/register")}>Register</a>&nbsp;here</h3>

      <dialog id="my_modal_1" className="modal">
        <div className="  modal-box 
                        bg-white/85 border 
                        border-white/85
                          text-black">
          <h3 className="font-bold text-lg">Account Error</h3>
          <p className="py-4">Username or password not valid</p>
          <p className="">Have you an account? <a onClick={() => navigate("/register")} className='link text-purple-600'>Register </a> one now!</p>
          <div className="modal-action">
            <form method="dialog">
              <button className="btn x-4 py-2 lg:px-5 lg:py-2.5 
                            bg-white/20 border 
                            border-white/30 
                            rounded-lg 
                            text-purple-900 font-semibold text-sm lg:text-base 
                            hover:bg-white/30 hover:-translate-y-0.5 transition-all duration-300 
                            backdrop-blur-lg shadow-lg">Close</button>
            </form>
          </div>
        </div>
      </dialog>
    </div>
  )
}