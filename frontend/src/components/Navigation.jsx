import React from 'react';
import { Link, useLocation } from 'react-router-dom';

function Navigation() {
  const location = useLocation();

  const isActive = (path) => {
    return location.pathname === path;
  };

  return (
    <nav className="bg-white shadow-lg h-16 flex items-center px-6">
      <div className="flex justify-between items-center w-full">
        <div className="flex items-center">
          <Link to="/" className="text-xl font-bold text-gray-800 hover:text-blue-600 transition-colors">
            Home
          </Link>
        </div>
        
        <div className="hidden md:flex space-x-8">
          <Link 
            to="/" 
            className={`px-3 py-2 rounded-md text-sm font-medium transition-colors ${
              isActive('/') 
                ? 'bg-blue-100 text-blue-700' 
                : 'text-gray-600 hover:text-blue-600 hover:bg-blue-50'
            }`}
          >
            Home
          </Link>
          <Link 
            to="/past" 
            className={`px-3 py-2 rounded-md text-sm font-medium transition-colors ${
              isActive('/past') 
                ? 'bg-blue-100 text-blue-700' 
                : 'text-gray-600 hover:text-blue-600 hover:bg-blue-50'
            }`}
          >
            Past
          </Link>
          <Link 
            to="/behavior" 
            className={`px-3 py-2 rounded-md text-sm font-medium transition-colors ${
              isActive('/behavior') 
                ? 'bg-blue-100 text-blue-700' 
                : 'text-gray-600 hover:text-blue-600 hover:bg-blue-50'
            }`}
          >
            Behavior
          </Link>
          <Link 
            to="/technical" 
            className={`px-3 py-2 rounded-md text-sm font-medium transition-colors ${
              isActive('/technical') 
                ? 'bg-blue-100 text-blue-700' 
                : 'text-gray-600 hover:text-blue-600 hover:bg-blue-50'
            }`}
          >
            Technical
          </Link>
        </div>
        
        {/* Mobile menu button */}
        <div className="md:hidden">
          <button className="text-gray-600 hover:text-blue-600 focus:outline-none">
            <svg className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
            </svg>
          </button>
        </div>
      </div>
    </nav>
  );
}

export default Navigation;
