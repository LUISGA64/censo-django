import { Controller, useForm } from 'react-hook-form';
import { getAllOrganizations } from '../../api/organizations.api.js';
import { useEffect, useState } from 'react';
import { OrganizationsList } from '../../components/organizations/OrganizationsList.jsx';
import { SelectOrganizations } from '../../components/organizations/SelectOrganizations.jsx';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import { Container } from 'react-bootstrap';

export function SidewalkFormPage() {
  const { control, handleSubmit, formState: { errors } } = useForm();

  const onSubmit = (data) => {
    console.log(data);
    // Aquí podrías realizar acciones adicionales en caso de que no haya errores en la validación
  };

  return (
    <Container>
      <Row className="justify-content-md-center">
        <form onSubmit={handleSubmit(onSubmit)}>
          <div>
            <label htmlFor="sidewalk_name">Vereda:</label>
            <Controller
              name="sidewalk_name"
              control={control}
              defaultValue=""
              rules={{ required: 'Este campo es obligatorio' }} // Mensaje de error personalizado
              render={({ field }) => <input {...field} />}
            />
            {errors.sidewalk_name && <span>{errors.sidewalk_name.message}</span>}
          </div>

          <div>
            <label htmlFor="organization_id">Organización</label>
            <Controller
              name="organization_id"
              control={control}
              rules={{ required: 'Selecciona una organización' }} // Mensaje de error personalizado
              render={({ field }) => <SelectOrganizations control={control} />}
            />
            {errors.organization_id && <span>{errors.organization_id.message}</span>}
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
