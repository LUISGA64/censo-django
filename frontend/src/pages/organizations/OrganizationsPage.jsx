import {OrganizationsList} from '../../components/organizations/OrganizationsList.jsx';
import {SelectOrganizations} from "../../components/organizations/SelectOrganizations.jsx";

export function OrganizationsPage() {
    return (
        <div>
            <h1>Listado</h1>
            <OrganizationsList />
        </div>
    );
}