import {getAllAssociations} from '../../api/associations.api.js'
import {useEffect, useState} from "react";
export function AssociationList() {

    const [associations, setAssociations] = useState([])

    useEffect(() => {
        async function loadAssociations() {
            await getAllAssociations().then((response) => {
                setAssociations(response.data);
                console.log(response.data);
            });
        }

        loadAssociations();
    }, []);

    return (
        <div>
            <ul>
                {associations.map((association) => {
                //     mostrar todos los datos de association
                    return <li key={association.id}>
                        <p>{association.association_name}</p>
                        <p>{association.association_address}</p>
                        <p>{association.association_phone}</p>
                        <p>{association.association_email}</p>
                        <p>{association.association_contact}</p>
                        <p>{association.association_contact_phone}</p>
                        <p>{association.association_contact_email}</p>
                        <p>{association.association_description}</p>
                        <p>{association.association_logo}</p>
                    </li>;
                })}
            </ul>
        </div>
    );
}