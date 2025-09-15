import { useRef } from 'react'
import { useAuth } from '../../hooks/useAuth'
import { useNavigate } from 'react-router';

export default function Login(){
  const username = useRef<HTMLInputElement>(null)
  const password = useRef<HTMLInputElement>(null)
  const { signIn } = useAuth();
  const navigate = useNavigate();

  const handleOnSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault()
    const credentials = {username: username.current.value, password: password.current.value}
    await signIn(credentials)
    navigate("/")
  }

  return (
    <div className='flex h-screen items-center justify-center'>
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
    </div>
  )
}