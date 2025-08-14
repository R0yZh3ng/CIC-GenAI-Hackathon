import logo from './logo.svg';

function App() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center">
      <div className="bg-white rounded-lg shadow-xl p-8 max-w-md w-full mx-4">
        <header className="text-center">
          <img src={logo} className="h-24 w-24 mx-auto mb-6 animate-spin" alt="logo" />
          <h1 className="text-3xl font-bold text-gray-800 mb-4">
            Welcome to React + Tailwind
          </h1>
          <p className="text-gray-600 mb-6">
            Edit <code className="bg-gray-100 px-2 py-1 rounded text-sm font-mono">src/App.js</code> and save to reload.
          </p>
          <a
            className="inline-block bg-blue-600 hover:bg-blue-700 text-white font-semibold py-3 px-6 rounded-lg transition-colors duration-200"
            href="https://reactjs.org"
            target="_blank"
            rel="noopener noreferrer"
          >
            Learn React
          </a>
        </header>
      </div>
    </div>
  );
}

export default App;
