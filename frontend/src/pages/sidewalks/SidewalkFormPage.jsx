import { Controller, useForm } from 'react-hook-form';
import { useEffect, useState } from 'react';
import { SelectOrganizations } from '../../components/organizations/SelectOrganizations.jsx';
import Row from 'react-bootstrap/Row';
import { Container } from 'react-bootstrap';
import {createSidewalk} from '../../api/sidewalks.api'

export function SidewalkFormPage() {
  const { control, handleSubmit, formState: { errors } } = useForm();

  const onSubmit = async (data) => {
    await createSidewalk(data)
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
              render={({ field:{value} }) => <SelectOrganizations control={control} />}
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
