import { useEffect, useRef } from 'react'
import { useAuth }  from '../../hooks/useAuth'
import { useNavigate } from 'react-router';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faTriangleExclamation } from '@fortawesome/free-solid-svg-icons'

export default function Register(){
  const { isFirstRegistration, registration, signed } = useAuth(); 
  const username = useRef<HTMLInputElement>(null)
  const password = useRef<HTMLInputElement>(null)
  const passwordCheck = useRef<HTMLInputElement>(null)
  
  let cssFirstReg: string = "";
  const navigate = useNavigate();
  
  if(isFirstRegistration){
    cssFirstReg = 'bg-yellow-500/50';
  } else {
    cssFirstReg = 'bg-white/30';
  }

  useEffect(() => {
      if(signed){
        navigate("/")
        }
    },[]);

  const handleOnSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault()
    const regCredentials = {  username: username.current?.value, 
                              password: password.current?.value,
                              passwordControl: passwordCheck.current?.value}
    try{
      await registration(regCredentials)
      if(signed){
        navigate("/")
      }
    } catch(e) {
      throw new ErrorEvent("Error during login: " + e);
    }
  }

  return (
  <div className='flex flex-col h-screen items-center justify-center'>
    <form onSubmit={handleOnSubmit} className={`fieldset ${cssFirstReg}  border-white rounded-box w-xs border-1 p-4`}>
      {isFirstRegistration ? <FontAwesomeIcon icon={faTriangleExclamation} className='flex text-yellow-500'/> : ""}
      {isFirstRegistration ? <p>This is the first account you are trying to register, and it will have administrator permissions. </p> : ""}
      <label className="label text-purple-900">Username</label>
      <input type="text" ref={username} className="input
                                      bg-[#FCCEFD]/80
                                      text-black" placeholder="Username" />

      <label className="label text-purple-900">Password</label>
      <input type="password" ref={password} className="input
                                      bg-[#FCCEFD]/80
                                      text-black" placeholder="Password" />
      
      <label className="label text-purple-900">Password Confirm</label>
      <input type="password" ref={passwordCheck} className="input
                                      bg-[#FCCEFD]/80
                                      text-black" placeholder="Password Confirm" />

      <button className="btn x-4 py-2 lg:px-5 lg:py-2.5 bg-white/20 border border-white/30 rounded-lg text-purple-900 font-semibold hover:bg-white/30 hover:-translate-y-0.5 transition-all duration-300 backdrop-blur-lg shadow-lg text-sm lg:text-base mt-4">Regist an account</button>
    </form>
    <h3 className=' flex 
          mt-5
          content-center
          justify-center
          '>Already have an account?&nbsp;<a className="link text-purple-600 hover:text-purple-300" onClick={() => navigate("/login")}>Login</a>&nbsp;here</h3>

  </div>
  )
}