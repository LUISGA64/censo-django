<script>
import axios from "axios";
export default {
  data() {
    return {
      fields: [
        {key: 'id', label: 'ID'},
        {key: 'sidewalk_name', label: 'Name'},
        {key: 'organization_id', label: 'Description'},
      ],
      sidewalks: []
    }
  },
  mounted() {
    axios.get('http://localhost:8000/api/sidewalks/')
      .then(response => {
        this.sidewalks = response.data;
      })
      .catch(error => {
        console.log(error);
      });
  }
}
</script>

<template>
  <div class="container">
    <div class="row">
      <div class="col text-left">
        <h1>List Sidewalks</h1>
        <div class="col-md-12">
          <b-table striped hover :items="sidewalks" :fields="fields">

          </b-table>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>

</style>
