import {useForm} from 'react-hook-form'
import {getAllOrganizations} from '../../api/organizations.api.js'
import {useEffect, useState} from "react";
import {OrganizationsList} from "../../components/organizations/OrganizationsList.jsx";
import {SelectOrganizations} from "../../components/organizations/SelectOrganizations.jsx";

export function SidewalkFormPage() {
    const {register} = useForm();


  return (
    <div>
        <form action={"/sidewalks"} method={"post"}>
            <div>
                <label htmlFor={"sidewalk_name"}>Sidewalk Name</label>
                <input type={"text"} id={"sidewalk_name"} name={"sidewalk_name"} placeholder={"Vereda"} />
            </div>
            <div>
                <label htmlFor={"sidewalk_description"}>Sidewalk Description</label>
                <OrganizationsList/>
            </div>
            <div>
                <button type={"submit"}>Create Sidewalk</button>
            </div>
        </form>
    </div>
  );
}

export default SidewalkFormPage;