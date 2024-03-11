import {useForm} from 'react-hook-form'
function SidewalkFormPage() {
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
                <input type={"text"} id={"sidewalk_description"} name={"sidewalk_description"} />
            </div>
            <div>
                <button type={"submit"}>Create Sidewalk</button>
            </div>
        </form>
    </div>
  );
}
export default SidewalkFormPage;