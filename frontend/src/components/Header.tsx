import { useState } from 'react';
import type { AuthContextData } from '../contexts/AuthContext'
import { useAuth } from '../hooks/useAuth';

export default function Header() {
  const { signed, user, signOut }: AuthContextData = useAuth();

  const [isDropdownOpen, setIsDropdownOpen] = useState(false);
  
  const handleAvatarClick = () => {
    setIsDropdownOpen(!isDropdownOpen);
  };

  const handleDropdownItemClick = (action) => {
    setIsDropdownOpen(false);
    if (action === 'logout') {
      signOut();
    }
  }
 
  return (
    <header className="flex justify-between items-center p-4 lg:px-6 bg-white/10 backdrop-blur-xl border-b border-white/10 sticky top-0 z-50 min-h-[70px]">
      {/* Logo Section */}
      <div className="flex items-center gap-3">
        <div className="w-10 h-10 bg-gradient-to-br from-yellow-400 to-yellow-600 rounded-xl flex items-center justify-center font-bold text-white text-lg shadow-lg shadow-yellow-400/30">
        </div>
        <div className="text-white text-xl lg:text-2xl font-bold drop-shadow-lg">
          Game Deals
        </div>
      </div>

      {/* Avatar/Login Section */}
      <div className="flex items-center gap-3">
        {user ? (
          <>
            {/* User Info - nascosto su mobile */}
            <div className="hidden md:flex flex-col items-end text-white">
              <div className="font-semibold text-sm drop-shadow-md">
                {user.username}
              </div>
            </div>

            {/* Avatar con Dropdown */}
            <div className="relative">
              <button
                onClick={handleAvatarClick}
                className="w-11 h-11 bg-gradient-to-br from-green-400 to-green-600 rounded-full flex items-center justify-center text-white font-semibold border-2 border-white/20 hover:border-white/40 hover:scale-105 transition-all duration-300 shadow-lg relative overflow-hidden"
              >
                {<img 
                    src="../assets/logged.jpg" 
                    alt={user.username}
                    className="w-full h-full object-cover rounded-full"
                  />
                }
                
                {/* Status Indicator */}
                <div className="absolute bottom-0.5 right-0.5 w-3 h-3 bg-green-400 border-2 border-white rounded-full"></div>
              </button>

              {/* Dropdown Menu */}
              {isDropdownOpen && (
                <div className="absolute top-full right-0 mt-2 bg-white/95 backdrop-blur-xl rounded-xl p-2 min-w-[180px] shadow-xl border border-white/20 z-50">
                  <div 
                    className="flex items-center gap-2 px-3 py-2 text-gray-700 hover:bg-purple-500/10 hover:text-purple-600 rounded-lg "
                    onClick={() => handleDropdownItemClick('profile')}
                  >
                         {/* Overlay per chiudere dropdown su mobile */} <span>👤</span>
                    {user.username}
                  </div>
                  <div className="h-px bg-gray-200 my-2"></div>
                  <div 
                    className="flex items-center gap-2 px-3 py-2 text-gray-700 hover:bg-red-500/10 hover:text-red-600 rounded-lg cursor-pointer transition-all duration-200 text-sm"
                    onClick={() => handleDropdownItemClick('logout')}
                  >
                    <span>🚪</span>
                    Logout
                  </div>
                </div>
              )}
            </div>
          </>
        ) : ""}
      </div>

      {isDropdownOpen && (
        <div 
          className="fixed inset-0 z-40"
          onClick={() => setIsDropdownOpen(false)}
        />
      )}
    </header>
  );
};