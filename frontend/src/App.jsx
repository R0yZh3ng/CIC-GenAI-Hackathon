import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Navigation from './components/Navigation';
import Home from './pages/Home';
import Past from './pages/Past';
import Behavior from './pages/Behavior';
import Technical from './pages/Technical';

function App() {
  return (
    <Router>
      <div className="h-screen w-full flex flex-col m-0 p-0">
        <Navigation />
        <div className="flex-1 overflow-hidden m-0 p-0">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/past" element={<Past />} />
            <Route path="/behavior" element={<Behavior />} />
            <Route path="/technical" element={<Technical />} />
          </Routes>
        </div>
      </div>
    </Router>
  );
}

export default App;
