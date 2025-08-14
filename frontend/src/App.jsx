import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Navigation from './components/Navigation';
import Home from './pages/Home';
import Past from './pages/Past';
import Behavior from './pages/Behavior';
import Technical from './pages/Technical';

function App() {
  return (
    <Router>
      <div className="min-h-screen">
        <Navigation />
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/past" element={<Past />} />
          <Route path="/behavior" element={<Behavior />} />
          <Route path="/technical" element={<Technical />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
