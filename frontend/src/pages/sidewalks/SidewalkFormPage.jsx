import {useForm} from 'react-hook-form'
import {getAllOrganizations} from '../../api/organizations.api.js'
import {useEffect, useState} from "react";
import {OrganizationsList} from "../../components/organizations/OrganizationsList.jsx";
import {SelectOrganizations} from "../../components/organizations/SelectOrganizations.jsx";
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import {Container} from "react-bootstrap";

export function SidewalkFormPage() {

    /*Crear Select para Organización*/

    const {register, handleSubmit,
        watch, formState: {errors}} = useForm();
    const onSubmit = data => console.log(data);


  return (
    <Container>
        <Row className="justify-content-md-center">
            <form onSubmit={handleSubmit(onSubmit)}>
                <div>
                    <label htmlFor={"sidewalk_name"}>Vereda:</label>
                    <input {...register("sidewalk_name", {required: true})}/>

                </div>
                <div>
                    <label htmlFor={"sidewalk_description"}>Organización</label>
                    <SelectOrganizations/>
                </div>
                <div>
                    <button type="submit">Save</button>
                </div>
            </form>
        </Row>
    </Container>
  );
}

export default SidewalkFormPage;