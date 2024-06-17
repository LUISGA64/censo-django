// Code for the main application
import {BrowserRouter, Route, Routes, Navigate} from 'react-router-dom';
import {SidewalksPage} from './pages/sidewalks/SidewalksPage';
import SidewalkFormPage from "./pages/sidewalks/SidewalkFormPage.jsx";
import {Navigation} from './components/Navigation.jsx';
import {OrganizationsPage} from "./pages/organizations/OrganizationsPage.jsx";
import {Toaster} from 'react-hot-toast';
import {AssociationList} from "./components/association/AssociationList.jsx";
import {AssociationPage} from "./pages/association/AssociationPage.jsx";
import {AssociationForm} from "./pages/association/AssociationForm.jsx";
import './App.css';

function App() {
    return (
        <>
            <div className="mx-auto ">
                <BrowserRouter>
                    <Navigation/>
                    <Routes>
                        <Route path="/" element={<Navigate to={'/sidewalks'}/>}/>
                        <Route path="/sidewalks" element={<SidewalksPage/>}/>
                        <Route path="/sidewalks-create" element={<SidewalkFormPage/>}/>
                        <Route path="/sidewalks/:id" element={<SidewalkFormPage/>}/>
                        <Route path="/organizations" element={<OrganizationsPage/>}/>
                        <Route path="/associations" element={<AssociationPage/>}/>
                        <Route path="/associations-create" element={<AssociationForm/>}/>
                    </Routes>
                    <Toaster/>
                </BrowserRouter>
            </div>
        </>
    );
}

export default App;
