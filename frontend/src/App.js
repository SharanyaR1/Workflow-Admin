import './App.css';
import { DndProvider } from 'react-dnd';
import { HTML5Backend } from 'react-dnd-html5-backend';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Home from './pages/Home';
import LeftMenu from './components/LeftMenu';
import NavBar from './components/NavBar';
import Upload from './pages/Upload';
import Modify from './pages/Modify';

function App() {
  const pages =[
    { title: 'Home', path :'/'},
    { title: 'Upload Artifacts', path: '/Upload' },
    { title: 'Manage Bundle',path: '/Modify'},
    { title: 'Service provider',path :'http://localhost:3000'}
 
  ]
  return (
    <DndProvider backend={HTML5Backend}>
    <Router>
        <div className="app">
          <div className="header">
            <NavBar />
          </div>

          <div className="content">
            <LeftMenu pages={pages} />
            <Routes>
              <Route path="/" element={<Home />} />
              <Route path="/Upload" element={<Upload/>}/>
              <Route path="/Modify" element={<Modify/>}/> 
            </Routes>
          </div>
        </div>
    </Router>
  </DndProvider>

  );
}

export default App;
