import { createContext } from 'react';
import { useLocalStorage } from 'usehooks-ts';
import type { ReactNode } from 'react';
import http from "../config/axios.config"

interface User {
  username: string
}

interface Credentials {
    username: string,
    password: string
}

export interface AuthContextData {
  signed: boolean;
  user: User | null;
  signIn({username, password}: Credentials): Promise<void>;
  signOut(): Promise<void>;
  token: string;
  renewToken(): Promise<void>;
}

const AuthContext = createContext<AuthContextData>({} as AuthContextData);

const AuthProvider = ({ children }: { children: ReactNode }) => {
  const [user, setUser, removeUser] = useLocalStorage<User | null>('user', null);
  const [signed, setSigned, removeSigned] = useLocalStorage<boolean>('signed', false);
  const [token, setToken, removeToken] = useLocalStorage<string>('bearer', '');

  async function signIn(credentials: Credentials): Promise<void> {
    const res = await http.post("/login", credentials);
    setUser(res.data.user)
    setSigned(true)
    setToken(res.data.access)
  }

  async function signOut(): Promise<void> {
    setUser(null)
    setSigned(false)
    removeToken()
  }

  async function renewToken(): Promise<void> {
    // const res = await http.post("/login", credentials);
  }

  return (
    <AuthContext.Provider
      value={{ signed, user, signIn, signOut, token, renewToken }}
    >
      {children}
    </AuthContext.Provider>
  );
};

export { AuthContext, AuthProvider}