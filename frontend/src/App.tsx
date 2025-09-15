import Header from './components/Header'
import { BrowserRouter, Routes, Route, Navigate } from 'react-router';
import Homepage from './views/Homepage/Homepage';
import Login from './views/Login/Login';
import Register from './views/Register/Register';
import { useAuth } from './hooks/useAuth';
import { AuthProvider } from './contexts/AuthContext';

export default function App() {
  const { signed } = useAuth();

  return( 
    <BrowserRouter>
      <AuthProvider>
      <Header />
      <Routes>
        <Route path="/" element={<Homepage />} />
        <Route path="/login" element={!signed ? <Login /> : <Navigate to="/" />} />
        <Route path="/register" element={!signed ? <Register /> : <Navigate to="/" />} />
      </Routes>
      </AuthProvider>
    </BrowserRouter>
  )
}