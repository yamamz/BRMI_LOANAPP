<template>
  <div>
    <el-card>
      <h5>Member List</h5>
      <hr />
      <v-client-table filterable="true" :columns="columns" :data="datas">
        <div slot="action" slot-scope="props">
          <el-button
            icon="el-icon-edit"
            circle
            type="success"
            size="mini"
            style="float:right;"
            @click="edit(props.row.id)"
          ></el-button>
        </div>
      </v-client-table>
    </el-card>
  </div>
</template>

<script>
export default {
  data() {
    return {
      columns: [
        "fullname",
        "gender",
        "address",
        "mobile_number",
        "monthly_income",
        "action"
      ],
      datas: []
    };
  },
  async created() {
    try {
      let res = await axios.get("/api/v1/members");
      res.data.forEach(el => {
        el.fullname = `${el.lname}, ${el.fname} ${el.mname}`;
      });
      this.datas = res.data;
    } catch (err) {
      if (err.response.status == 401) {
        console.log("xxx");
        this.$message.error(
          "Tokken expire and being refresh now please try again"
        );
        this.$router.push("/");
      }
    }
  },
  methods: {
    edit(id) {
      this.$router.push("/app/member/edit/" + id);
    }
  }
};
</script>

<style>
</style>
