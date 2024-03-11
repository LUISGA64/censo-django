// Code for the main application
import {BrowserRouter, Route, Routes, Navigate} from 'react-router-dom';
import {SidewalksPage} from './pages/sidewalks/SidewalksPage';
import SidewalkFormPage from "./pages/sidewalks/SidewalkFormPage.jsx";
import {Navigation} from './components/Navigation.jsx';
function App() {
    return (
        <BrowserRouter>
            <Navigation />
            <Routes>
                <Route path="/" element={<Navigate to={'/sidewalks'} />} />
                <Route path="/sidewalks" element={<SidewalksPage />} />
                <Route path="/sidewalks-create" element={<SidewalkFormPage />} />
            </Routes>
        </BrowserRouter>
    );
}
export default App;
