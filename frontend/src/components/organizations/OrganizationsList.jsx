import {getAllOrganizations} from '../../api/organizations.api.js'
import {useState, useEffect} from 'react';


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
            <h1>Resguardo</h1>
            <ul>
                {organizations.map((organization) => {
                    return <li key={organization.id}>{organization.organization_name}</li>;
                })}
            </ul>
        </div>
    );
}