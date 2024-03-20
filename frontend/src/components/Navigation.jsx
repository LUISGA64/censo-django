import {Link} from 'react-router-dom';
export function Navigation() {
    return (
        <nav>
            <ul>
                <li>
                    <Link to="/sidewalks">Sidewalks</Link>
                </li>
                <li>
                    <Link to="/sidewalks-create">Create Sidewalk</Link>
                </li>
                <li>
                    <Link to="/organizations">Organizations</Link>
                </li>

                <li>
                    <Link to="/associations">Associations</Link>
                </li>

                <li>
                    <Link to="/associations-create">Crear Asociación</Link>
                </li>
            </ul>
        </nav>
    )
}