<template>
  <div>
    <el-card>
      <h4>Loan Application</h4>
      <hr />
      <el-form size="mini" :ref="form" :model="form">
        <el-row>
          <el-col :sm="24">
            <el-form-item label="Member">
              <el-select
                filterable
                style="width:100%;"
                v-model="form.member"
                placeholder="Select a member"
                @change="checkMemberHasLoan"
              >
                <el-option
                  v-for="(item, index) in members"
                  :value="item.id"
                  :label="item.fullname"
                  :key="index"
                ></el-option>
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="5">
          <el-col :sm="8">
            <el-form-item label="Cluster">
              <el-select
                filterable
                style="width:100%;"
                v-model="form.clustername"
                placeholder="Select cluster"
              >
                <el-option
                  v-for="(item, index) in clusters"
                  :value="item.id"
                  :label="item.name"
                  :key="index"
                ></el-option>
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :sm="8">
            <el-form-item label="Loan Type">
              <el-select
                filterable
                style="width:100%;"
                v-model="form.loan_mode"
                placeholder="Select a Loan Type"
              >
                <el-option
                  v-for="(item, index) in loan_modes"
                  :value="item.code"
                  :label="item.name"
                  :key="index"
                ></el-option>
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :sm="8">
            <el-form-item label="Loan Cycle">
              <el-input-number
                :disabled="form.member==''"
                style="width:100%;"
                v-model="form.loan_cycle"
              ></el-input-number>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="5">
          <el-col :sm="8">
            <el-form-item label="Interest Type">
              <el-select
                filterable
                style="width:100%;"
                v-model="form.loan_type"
                placeholder="Select a Interest Type"
              >
                <el-option
                  v-for="(item, index) in loan_types"
                  :value="item.code"
                  :label="item.name"
                  :key="index"
                ></el-option>
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :sm="8">
            <el-form-item label="Principal">
              <el-input-number
                style="width:100%;"
                :precision="2"
                :disabled="form.loan_type==''"
                v-model="form.principal"
              />
            </el-form-item>
          </el-col>
          <el-col :sm="8">
            <el-form-item label="Interest rate">
              <el-input-number
                style="width:100%;"
                :precision="2"
                placeholder="Enter interest rate"
                :disabled="form.principal==''"
                v-model="form.interest_rate"
              />
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="5">
          <el-col :sm="8">
            <el-form-item label="Mode of Payments">
              <el-select
                @change="calcInterest"
                :disabled="form.interest_rate==''"
                filterable
                style="width:100%;"
                v-model="form.payment_period"
                placeholder="Select a period"
              >
                <el-option
                  v-for="(item, index) in periods"
                  :value="item.code"
                  :label="item.name"
                  :key="index"
                ></el-option>
              </el-select>
            </el-form-item>
          </el-col>

          <el-col :sm="8">
            <el-form-item label="Term(in month)">
              <el-input-number
                style="width:100%;"
                @change="calcInterest"
                :disabled="form.payment_period==''"
                v-model="form.loan_period"
              />
            </el-form-item>
          </el-col>
          <el-col :sm="8">
            <el-form-item label="Interest">
              <el-input-number style="width:100%;" :precision="2" v-model="form.interest" />
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="5">
          <el-col :sm="8">
            <el-form-item label="Date Release">
              <el-date-picker
                @change="calcInterest"
                v-model="form.date_release"
                type="date"
                style="width:100%;"
                placeholder="Pick a day"
              ></el-date-picker>
            </el-form-item>
          </el-col>
          <el-col :sm="8">
            <el-form-item label="Processing Fee">
              <el-input-number
                style="width:100%;"
                :precision="2"
                placeholder="Enter Processing Fee"
                v-model="form.processing_fee"
              />
            </el-form-item>
          </el-col>
          <el-col :sm="8">
            <el-form-item label="(CBU)for New Member">
              <el-input-number
                style="width:100%;"
                :precision="2"
                placeholder="Enter CBU"
                v-model="form.cbu"
              />
            </el-form-item>
          </el-col>
          <el-col :sm="24">
            <el-form-item label="Witness Name">
              <el-input size="mini" placeholder="Enter Witness" v-model="form.loan_witness"></el-input>
            </el-form-item>
            <h4>Loan Payment Schedules</h4>
            <hr />
          </el-col>
        </el-row>
        <el-table :data="form.loanscheds" size="medium" style="width: 100%">
          <el-table-column type="index" :index="indexMethod"></el-table-column>
          <el-table-column prop="date" label="Date" width="180"></el-table-column>

          <el-table-column prop="principal" label="principal" width="180"></el-table-column>
          <el-table-column prop="interest" label="interest"></el-table-column>
          <el-table-column prop="total" label="Total"></el-table-column>
        </el-table>
      </el-form>
      <hr />
      <el-button
        icon="el-icon-notebook-1"
        size="small"
         :loading="isLoading"
        :disabled="form.loanscheds.length== 0 || form.member==''"
        @click="save"
        type="primary"
      >Update</el-button>
    </el-card>
  </div>
</template>

<script>
import { ExcelFormulas } from "../../helper/loan.js";
import { Finance } from "financejs";

export default {
  data() {
    return {
      isLoading: false,
      is_updatescheds: false,
      members: [],
      clusters: [],
      loans: [],
      periods: [
        { code: 1, name: "weekly" },
        { code: 2, name: "semi-monthly" },
        { code: 3, name: "monthly" },
         { code: 4, name: "daily" }
      ],
      loan_types: [
        { code: 1, name: "Diminishing" },
        { code: 2, name: "flat rate" }
      ],
      loan_modes: [
        { code: 1, name: "Normal Loan" },
        { code: 2, name: "Emirgency Loan" }
      ],
      form: {
        loan_mode: 1,
        loan_cycle: "",
        member: "",
        loan_type: "",
        principal: "",
        interest: "",
        interest_rate: "",
        clustername: "",
        processing_fee: "",
        loan_period: "",
        payment_period: "",
        loan_witness: "",
        date_release: "",
        cbu: "",
        loanscheds: []
      }
    };
  },
  methods: {
    checkMemberHasLoan() {
      let loanmember = this.loans.filter(e => e.member.id == this.form.member);
      this.form.loan_cycle =
        this.loans.filter(e => e.member.id === this.form.member).length + 1;
      let loanamount = 0;
      let loanamountpaid = 0;
      console.log("sulod" + loanmember.length);
      if (loanmember.length > 0) {
        loanmember.forEach(e => {
          loanamount =
            loanamount + parseFloat(e.principal) + parseFloat(e.interest);
          e.loanpayments.forEach(el => {
            loanamountpaid =
              loanamountpaid +
              parseFloat(el.paid_principal) +
              parseFloat(el.paid_interest);
          });
        });
        let bal = loanamount - loanamountpaid;
        console.log(bal);
        if (bal > 0) {
          this.$message.error(
            "this member has outstanding balance in his/her loan"
          );
          //this.form.member = "";
        }
      }
    },
    save() {
      if (this.is_updatescheds) {
        axios
          .delete("/api/v1/deletescheds/" + this.$route.params.id, {})
          .then(res => {
            console.log("delete");
          });
        let date = new Date(this.form.date_release);
        this.form.date_release = `${date.getMonth() +
          1}-${date.getDate()}-${date.getFullYear()}`;
        console.log(this.form);
 this.isLoading=true
        axios
          .put("/api/v1/loans/" + this.$route.params.id + "/", this.form)
          .then(res => {
            this.isLoading=false
            this.$router.push("/app/loan/loanpayment/" + res.data.id);
            this.$message.success("Successfuly Updated");
          })
          .catch(err => {
            if (err.response.status == 401) {
              console.log("xxx");
              this.$message.error(
                "Tokken expire and being refresh now please try again"
              );
            }
          });
      } else {
        let date = new Date(this.form.date_release);
        this.form.date_release = `${date.getMonth() +
          1}-${date.getDate()}-${date.getFullYear()}`;
        console.log(this.form);
 this.isLoading=true
        axios
          .put("/api/v1/loans/" + this.$route.params.id + "/", this.form)
          .then(res => {
            this.isLoading=false
            this.$router.push("/app/loan/loanpayment/" + res.data.id);
            this.$message.success("Successfuly Updated");
          })
          .catch(err => {
            if (err.response.status == 401) {
              console.log("xxx");
              this.$message.error(
                "Tokken expire and being refresh now please try again"
              );
            }
          });
      }
    },
    indexMethod(index) {
      return index + 1;
    },

    calcInterest() {
      this.is_updatescheds = true;
      let finance = new Finance();

      if (this.form.loan_type == 1) {
        if (
          this.form.interest_rate != "" &&
          this.form.payment_period != "" &&
          this.form.loan_period != ""
        ) {
          let n = 0;
          let interest_rate = 0;
          let dateinc = 0;
          if (this.form.payment_period == 1) {
            n = this.form.loan_period * 4;
            interest_rate = this.form.interest_rate / 100 / 4;
            dateinc = 7;
            console.log("1");
          } else if (this.form.payment_period == 2) {
            n = this.form.loan_period * 2;
            interest_rate = this.form.interest_rate / 100 / 2;
            dateinc = 14;
            console.log("2");
            console.log(n);
          } 
          else if(this.form.payment_period == 4){
              n = this.form.loan_period * 29;
              interest_rate = this.form.interest_rate / 100 / 29;
              dateinc = 1;
              console.log("2");
              console.log(n);
              console.log("daily")
            }
          else {
            n = this.form.loan_period;
            interest_rate = this.form.interest_rate / 100;
            dateinc = 30;
            console.log("3");
          }

          let pmt = ExcelFormulas.PMT(interest_rate, n, this.form.principal);

          let abspmt = Math.abs(pmt);
          this.form.interest = Math.floor(abspmt) * n - this.form.principal;

          let currentprincipal = this.form.principal;
          this.form.loanscheds = [];
          console.log(abspmt);
          let totalprin = 0;
          let totalint = 0;

          let totaldateinc = 0;
          this.form.loanscheds = [];
          for (let i = 0; i < n; i++) {
            let date = new Date(this.form.date_release);
            totaldateinc = totaldateinc + dateinc;

            date.setDate(date.getUTCDate() + totaldateinc);
            console.log(date.getMonth());
            let pmt = ExcelFormulas.PMT(interest_rate, n, this.form.principal);
            let ipmt = ExcelFormulas.IPMT(
              currentprincipal,
              pmt,
              interest_rate,
              i
            );
            let ppmt = ExcelFormulas.PPMT(
              interest_rate,
              i + 1,
              n,
              currentprincipal
            );
            if (i == n - 1) {
              ppmt = this.form.principal - totalprin;

              console.log("nka abot dri");
            }

            totalprin = totalprin + Math.abs(ppmt);
            totalint = totalint + Math.abs(ipmt);

            //totalsum = totalsum + total
            let datestr = `${date.getMonth() +
              1}-${date.getDate()}-${date.getFullYear()}`;
            console.log(totalprin);
            this.form.loanscheds.push({
              date: datestr,
              datestr: date.toDateString(),
              principal: Math.floor(Math.abs(ppmt)).toFixed(2),
              interest: Math.floor(Math.abs(ipmt)).toFixed(2),
              total: (
                Math.floor(Math.abs(ppmt)) + Math.floor(Math.abs(ipmt))
              ).toFixed(2)
            });
          }
          this.form.interest = Math.round(totalint);
          console.log(Math.floor(totalprin));
          console.log(Math.floor(totalint));
        }
      } else {
        if (
          this.form.interest_rate != "" &&
          this.form.payment_period != "" &&
          this.form.loan_period != ""
        ) {
          let n = 0;
          let interest_rate = 0;
          let dateinc = 0;
          if (this.form.payment_period == 1) {
            n = this.form.loan_period * 4;
            dateinc = 7;

            console.log("1");
          } else if (this.form.payment_period == 2) {
            n = this.form.loan_period * 2;
            dateinc = 14;

            console.log("2");
            console.log(n);
          }
          else if(this.form.payment_period == 4){
              n = this.form.loan_period * 29;
              interest_rate = this.form.interest_rate / 100 / 29;
              dateinc = 1;
              console.log("2");
              console.log(n);
              console.log("daily")
            }
          else {
            n = this.form.loan_period;
            dateinc = 29;

            console.log("3");
          }
          let interest =
            ((this.form.principal *
              this.form.loan_period *
              (this.form.interest_rate / 100)) /
              n) *
            n;
          this.form.interest = Math.floor(interest);
          let principal = this.form.principal / n;
          let int = interest / n;
          this.form.loanscheds = [];
          let totaldateinc = 0;
          this.form.loanscheds = [];
          let totalinterest = 0;
          let totalprin = 0;
          for (let i = 1; i <= n; i++) {
            let date = new Date(this.form.date_release);
            totaldateinc = totaldateinc + dateinc;

            date.setDate(date.getUTCDate() + totaldateinc);
            console.log(date.getDate());
            let datestr = `${date.getUTCMonth() +
              1}-${date.getUTCDate()}-${date.getFullYear()}`;

            if (i != n) {
              this.form.loanscheds.push({
                date: datestr,
                datestr: date.toDateString(),
                principal: Math.floor(principal).toFixed(2),
                interest: Math.floor(int).toFixed(2),
                total: (Math.floor(int) + Math.floor(principal)).toFixed(2)
              });
            } else {
              this.form.loanscheds.push({
                date: datestr,
                datestr: date.toDateString(),
                principal: (
                  parseFloat(this.form.principal).toFixed(2) -
                  parseFloat(totalprin).toFixed(2)
                ).toFixed(2),
                interest: (
                  parseFloat(this.form.interest).toFixed(2) -
                  parseFloat(totalinterest).toFixed(2)
                ).toFixed(2),
                total: (Math.floor(int) + Math.floor(principal)).toFixed(2)
              });
            }
            totalinterest = totalinterest + Math.floor(int);
            totalprin = totalprin + Math.floor(principal);
            console.log("totint " + totalinterest + " ");
          }
        }
      }
    }
  },
  async created() {
    try {
      let resmembers = await axios.get("/api/v1/members");
      this.members = resmembers.data;
      this.members.forEach(el => {
        el.fullname = `${el.lname}, ${el.fname}`;
      });
      let loanres = await axios.get("/api/v1/loans/" + this.$route.params.id);
      loanres.data.loanscheds.forEach(e => {
        e.total = (parseFloat(e.interest) + parseFloat(e.principal)).toFixed(2);
        console.log(e.total)
      });
      this.form = loanres.data;
      let resclusters = await axios.get("/api/v1/clusters");
      this.clusters = resclusters.data;

      let resloans= await axios.get('/api/v1/loanss')
      this.loans = resloans.data
      this.form.loanscheds.forEach(e => {
          e.total = (parseFloat(e.interest) + parseFloat(e.principal)).toFixed(
            2
          );
    
      e.datestr = new Date(e.date).toDateString();
        });

    } catch (err) {
      if (err.response.status == 401) {
        this.$message.error(
          "Tokken is expired and being refresh now please try again"
        );
        this.$router.push("/");
      }
      console.log(err);
    }
  }
};
</script>

<style>
</style>
