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
            </ul>
        </nav>
    )
}