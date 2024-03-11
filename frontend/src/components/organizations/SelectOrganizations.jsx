export function SelectOrganizations(props) {
    return(
        <div>
            <select>
                <option value={props.id}>{props.name}</option>
            </select>
        </div>
    )
}