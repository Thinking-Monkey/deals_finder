/* eslint-disable @typescript-eslint/no-explicit-any */
import { createContext, useEffect } from 'react';
import { useLocalStorage } from 'usehooks-ts';
import type { ReactNode } from 'react';
import http from '../config/axios.config'

interface User {
  username: string
}

interface Credentials {
    username: string | undefined,
    password: string | undefined
}

interface RegCredentials {
    username: string | undefined,
    password: string | undefined,
    passwordCheck: string | undefined
}
export interface AuthContextData {
  signed: boolean;
  user: User | null;
  signIn({username, password}: Credentials): Promise<void>;
  signOut(): Promise<void>;
  token: string;
  renewToken(): Promise<void>;
  isFirstRegistration: boolean;
  registration({username, password, passwordCheck}: RegCredentials): Promise<void>;
}


const AuthContext = createContext<AuthContextData>({} as AuthContextData);

const AuthProvider = ({ children }: { children: ReactNode }) => {
  const [user, setUser] = useLocalStorage<User | null>('user', null);
  const [signed, setSigned] = useLocalStorage<boolean>('signed', false);
  const [token, setToken, removeToken] = useLocalStorage<string>('bearer', '');
  const [refreshToken, setRToken, removeRToken] = useLocalStorage<string>('rtk', '');
  const [isFirstRegistration, setFR, removeFR] = useLocalStorage<boolean>('ifr', true)
  
  const adminExist = async () => {
  const res = await http.get('/admin-exist');
  if(isFirstRegistration && res.data.adminExist ){
     setFR(false)
    }
  }

  useEffect(() => {
    adminExist()
  }, [])

  async function signIn(credentials: Credentials): Promise<void> {
    // eslint-disable-next-line no-useless-catch
    try{
      const res = await http.post("/signin", credentials);
      setUser(res.data.user)
      setSigned(true)
      setToken(res.data.access)
      setRToken(res.data.refresh)
      setFR(true)
    } catch(error: any) {
      throw error;
    } 
  }

  async function signOut(): Promise<void> {
    // TODO
    const logout = {
      refresh: refreshToken
    }
    await http.post("/signout", logout) //attualmente disabilitata la logout da server
    setUser(null)
    setSigned(false)
    removeToken()
    removeRToken()
    removeFR()
  }

  async function registration(regCredentials: RegCredentials): Promise<void> {
    // eslint-disable-next-line no-useless-catch
    try{
      const res = await http.post("/signon", regCredentials);
      if(res){
        setUser(res.data.user)
        setSigned(true)
        setToken(res.data.access)
        setRToken(res.data.refresh)
      }
      if(isFirstRegistration){
        setFR(false)
      }
    } catch(error: any) {
      throw error;
    }
  }

  async function renewToken(): Promise<void> {
    // TODO
    // const res = await http.post("/login", credentials);
  }

  return (
    <AuthContext.Provider
      value={{  signed, user, signIn, signOut, token, renewToken, 
                isFirstRegistration, registration}}
    >
      {children}
    </AuthContext.Provider>
  );
};

export { AuthContext, AuthProvider}