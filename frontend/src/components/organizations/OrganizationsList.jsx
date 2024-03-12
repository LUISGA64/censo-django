import {getAllOrganizations} from '../../api/organizations.api.js'
import {useState, useEffect} from 'react';
import {SelectOrganizations} from "./SelectOrganizations.jsx";


export function OrganizationsList() {

    const [organizations, setOrganizations] = useState([])

    useEffect(() => {
        async function loadOrganizations() {
            await getAllOrganizations().then((response) => {
                setOrganizations(response.data);
            });
        }

        loadOrganizations();

    }, []);

    return (
        <div>
            <h1>Hola mundo</h1>
        </div>
    )
}