<template>
  <div>
    <el-card>
      <h5>Loan Details</h5>
      <el-form size="mini" :ref="loan" :model="loan">
        <el-row :gutter="5">
          <el-col :sm="8">
            <el-form-item label="Cluster">
              <el-select
                disabled
                filterable
                style="width:100%;"
                v-model="loan.clustername"
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
            <el-form-item label="Member">
              <el-select
                disabled
                filterable
                style="width:100%;"
                v-model="loan.member"
                placeholder="Select a member"
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
          <el-col :sm="8">
            <el-form-item label="Loan Cycle">
              <el-input-number disabled style="width:100%;" v-model="loan.loan_cycle"></el-input-number>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="5">
          <el-col :sm="8">
            <el-form-item label="Loan Type">
              <el-select
                filterable
                disabled
                style="width:100%;"
                v-model="loan.loan_type"
                placeholder="Select a Loan Type"
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
                disabled
                style="width:100%;"
                :precision="2"
                v-model="loan.principal"
              />
            </el-form-item>
          </el-col>
          <el-col :sm="8">
            <el-form-item label="Interest rate">
              <el-input-number
                style="width:100%;"
                :precision="2"
                placeholder="Enter interest rate"
                disabled
                v-model="loan.interest_rate"
              />
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="5">
          <el-col :sm="8">
            <el-form-item label="Loan Payment period">
              <el-select
                disabled
                @change="calcInterest"
                filterable
                style="width:100%;"
                v-model="loan.payment_period"
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
                disabled
                style="width:100%;"
                @change="calcInterest"
                v-model="loan.loan_period"
              />
            </el-form-item>
          </el-col>
          <el-col :sm="8">
            <el-form-item label="Interest">
              <el-input-number disabled style="width:100%;" :precision="2" v-model="loan.interest" />
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="5">
          <el-col :sm="8">
            <el-form-item label="Date Release">
              <el-date-picker
                disabled
                v-model="loan.date_release"
                type="date"
                style="width:100%;"
                placeholder="Pick a day"
              ></el-date-picker>
            </el-form-item>
          </el-col>
          <el-col :sm="8">
            <el-form-item label="Processing Fee">
              <el-input-number
                disabled
                style="width:100%;"
                :precision="2"
                placeholder="Enter Processing Fee"
                v-model="loan.processing_fee"
              />
            </el-form-item>
          </el-col>
          <el-col :sm="8">
            <el-form-item label="(CBU)for New Member">
              <el-input-number
                disabled
                style="width:100%;"
                :precision="2"
                placeholder="Enter CBU"
                v-model="loan.cbu"
              />
            </el-form-item>
          </el-col>
          <el-col :sm="24">
            <el-form-item label="Witness Name">
              <el-input
                disabled
                size="mini"
                placeholder="Enter Witness"
                v-model="loan.loan_witness"
              ></el-input>
            </el-form-item>
          </el-col>
        </el-row>
      </el-form>
    </el-card>
    <el-card></el-card>

    <el-tabs type="border-card">
      <el-tab-pane>
        <span slot="label">
          <i class="el-icon-notebook-2"></i> Payment History
        </span>
        <el-card>
          <div slot="header" class="clearfix">
            <el-button
              type="success"
              :disabled="form.ending_balance<0"
              style="float:right; margin:2px;"
              @click="openDialog"
              size="small"
              icon="el-icon-tickets"
            >Add Payment</el-button>
            <el-button
              type="primary"
              style="float:right; margin:2px;"
              @click="printLoanDetails(loan)"
              icon="el-icon-printer"
              size="small"
            >Print</el-button>
          </div>
          <br />
          <el-row>
            <el-col>
              <el-table
                :row-class-name="tableRowClassName"
                size="mini"
                :data="payments"
                stripe
                border
                style="width: 100%"
              >
                <el-table-column type="index" :index="indexMethod"></el-table-column>
                <el-table-column prop="date_of_payment" label="Date" width="180"></el-table-column>
                <el-table-column prop="beginning_balance" label="Beginning Balance" width="180"></el-table-column>
                <el-table-column prop="paid_interest" label="Paid Interest"></el-table-column>
                <el-table-column prop="paid_principal" label="Paid Principal"></el-table-column>
                <el-table-column prop="ending_balance" label="Ending Balance"></el-table-column>

                <el-table-column label="action">
                  <template slot-scope="scope">
                    <el-button
                     :loading="isLoading"
                      style="float:right;"
                      type="danger"
                      @click="deletePayment(scope.row.id,scope.$index)"
                      size="mini"
                      icon="el-icon-delete"
                      round
                    >delete</el-button>
                  </template>
                </el-table-column>
              </el-table>
            </el-col>
          </el-row>

          <el-row>
            <el-col>
              <h6 style="float:right;">Interest Balance : {{(caltotInterest).toFixed(2)}}</h6>
            </el-col>
            <el-col>
              <h6 style="float:right;">Principal Balance: {{(calcTotprincipalPaid).toFixed(2)}}</h6>
            </el-col>
            <el-col>
              <h6
                style="float:right;"
              >Total Balance: {{(caltotInterest + calcTotprincipalPaid).toFixed(2)}}</h6>
            </el-col>
          </el-row>
        </el-card>
      </el-tab-pane>
      <el-tab-pane>
        <span slot="label">
          <i class="el-icon-date"></i> Payment Schedules
        </span>

        <el-table
          :row-class-name="tableRowClassName"
          :data="loan.loanscheds"
          size="mini"
          style="width: 100%"
        >
          <el-table-column type="index" :index="indexMethod"></el-table-column>
          <el-table-column prop="datestr" label="Date" width="180"></el-table-column>

          <el-table-column prop="principal" label="principal" width="180"></el-table-column>
          <el-table-column prop="interest" label="interest"></el-table-column>
          <el-table-column prop="total" label="Total"></el-table-column>
          <el-table-column label="Operations">
            <template slot-scope="scope">
              <el-button
                :loading="isLoading"
                size="mini"
                round
                icon="el-icon-delete"
                type="danger"
                style="float:right;"
                @click="deleteScheds(scope.$index, scope.row.id)"
              >Delete</el-button>
            </template>
          </el-table-column>
        </el-table>
      </el-tab-pane>
    </el-tabs>

    <el-dialog title="Add Payment" :visible.sync="dialogAdd" width="40%">
      <el-form ref="form" :model="form" size="mini" label-position="top">
        <el-row :gutter="5">
          <el-col :md="12">
            <el-form-item label="payment date">
              <el-date-picker
                style="width:100%;"
                v-model="form.date_of_payment"
                type="date"
                placeholder="Please Select date"
              ></el-date-picker>
            </el-form-item>
          </el-col>
          <el-col :md="12">
            <el-form-item label="Beginning Balance">
              <el-input v-model="form.beginning_balance" :value="calculateBeginningbal"></el-input>
            </el-form-item>
          </el-col>
          <el-col :md="12">
            <el-form-item label="Paid Interest">
              <el-input v-model="form.paid_interest" :value="caltotInterest"></el-input>
            </el-form-item>
          </el-col>
          <el-col :md="12">
            <el-form-item label="Paid Principal">
              <el-input v-model="form.paid_principal" :value="calcTotprincipalPaid"></el-input>
            </el-form-item>
          </el-col>
          <el-col :md="12">
            <el-form-item label="Total Due">
              <el-input :value="total_Due" v-model="form.total_monthly_due"></el-input>
            </el-form-item>
          </el-col>
          <el-col :md="12">
            <el-form-item label="Ending Balance">
              <el-input :value="calculateEndingBal" v-model="form.ending_balance"></el-input>
            </el-form-item>
          </el-col>
          <el-col>
            <el-button
              :loading="isLoading"
              :disabled="form.total_monthly_due==0"
              type="primary"
              size="small"
              @click="savePayment"
            >Save Payment</el-button>
          </el-col>
        </el-row>
      </el-form>
    </el-dialog>
  </div>
</template>
<style>
.el-table .warning-row {
  background: oldlace;
}

.el-table .success-row {
  background: #f0f9eb;
}
</style>

<script>
import pdfMake from "pdfmake/build/pdfmake";
import pdfFonts from "pdfmake/build/vfs_fonts";
import { ExcelFormulas } from "../../helper/loan.js";
pdfMake.vfs = pdfFonts.pdfMake.vfs;

export default {
  data() {
    return {
      isLoading: false,
      payment_period: "",
      loan_percentage_type: "",
      loan: {
        member: { name: "" }
      },
      members: [],
      clusters: [],
      periods: [
        { code: 1, name: "weekly" },
        { code: 2, name: "semi-monthly" },
        { code: 3, name: "monthly" }
      ],
      loan_types: [
        { code: 1, name: "Diminishing" },
        { code: 2, name: "flat rate" }
      ],
      form: {
        date_of_payment: new Date(),
        beginning_balance: 0.0,
        paid_interest: 0.0,
        paid_principal: 0.0,
        ending_balance: 0.0,
        loan: this.$route.params.id,
        total_monthly_due: 0.0
      },
      dialogAdd: false,
      payments: []
    };
  },
  methods: {
    tableRowClassName({ row, rowIndex }) {
      if (rowIndex % 2 === 1) {
        return "success-row";
      } else {
        return "";
      }
      return "";
    },
    deleteScheds(index, id) {
      this.isLoading = true
      axios.delete("/api/v1/loanpaymentscheds/" + id).then(res => {
        this.loan.loanscheds.splice(index, 1);
       this.$message.success('Delete successfully')
       this.isLoading = false
      }).catch(err=>{
        this.isLoading = flase
           this.$message.error('there is an error please try again')
      });
    },
    deletePayment(id, index) {
      this.isLoading = true
      axios.delete("/api/v1/loanpayment/" + id).then(res => {
        this.payments.splice(index, 1);
       this.$message.success('Delete successfully')
       this.isLoading = false
      }).catch(err=>{
           this.$message.error('there is an error please try again')
           this.isLoading = false
      });
    },
    printLoanDetails(obj) {
      var dd = {
        pageOrientation: "portrait",
        content: [
          {
            margin: [0, 0, 0, 0],
            columns: [
              {
                width: "auto",
                margin: [130, 0, 0, 0],
                stack: [
                  {
                    width: 55,
                    height: 50,
                    image:
                      "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAfQAAAHFCAYAAAAE8AuCAAAAGXRFWHRTb2Z0d2FyZQBBZG9iZSBJbWFnZVJlYWR5ccllPAAAAyFpVFh0WE1MOmNvbS5hZG9iZS54bXAAAAAAADw/eHBhY2tldCBiZWdpbj0i77u/IiBpZD0iVzVNME1wQ2VoaUh6cmVTek5UY3prYzlkIj8+IDx4OnhtcG1ldGEgeG1sbnM6eD0iYWRvYmU6bnM6bWV0YS8iIHg6eG1wdGs9IkFkb2JlIFhNUCBDb3JlIDUuNi1jMTQyIDc5LjE2MDkyNCwgMjAxNy8wNy8xMy0wMTowNjozOSAgICAgICAgIj4gPHJkZjpSREYgeG1sbnM6cmRmPSJodHRwOi8vd3d3LnczLm9yZy8xOTk5LzAyLzIyLXJkZi1zeW50YXgtbnMjIj4gPHJkZjpEZXNjcmlwdGlvbiByZGY6YWJvdXQ9IiIgeG1sbnM6eG1wPSJodHRwOi8vbnMuYWRvYmUuY29tL3hhcC8xLjAvIiB4bWxuczp4bXBNTT0iaHR0cDovL25zLmFkb2JlLmNvbS94YXAvMS4wL21tLyIgeG1sbnM6c3RSZWY9Imh0dHA6Ly9ucy5hZG9iZS5jb20veGFwLzEuMC9zVHlwZS9SZXNvdXJjZVJlZiMiIHhtcDpDcmVhdG9yVG9vbD0iQWRvYmUgUGhvdG9zaG9wIENDIChXaW5kb3dzKSIgeG1wTU06SW5zdGFuY2VJRD0ieG1wLmlpZDozNTI5MkVBOUM0Q0YxMUU5OEZCNERCNDU5OTMyRkZFNCIgeG1wTU06RG9jdW1lbnRJRD0ieG1wLmRpZDozNTI5MkVBQUM0Q0YxMUU5OEZCNERCNDU5OTMyRkZFNCI+IDx4bXBNTTpEZXJpdmVkRnJvbSBzdFJlZjppbnN0YW5jZUlEPSJ4bXAuaWlkOjM1MjkyRUE3QzRDRjExRTk4RkI0REI0NTk5MzJGRkU0IiBzdFJlZjpkb2N1bWVudElEPSJ4bXAuZGlkOjM1MjkyRUE4QzRDRjExRTk4RkI0REI0NTk5MzJGRkU0Ii8+IDwvcmRmOkRlc2NyaXB0aW9uPiA8L3JkZjpSREY+IDwveDp4bXBtZXRhPiA8P3hwYWNrZXQgZW5kPSJyIj8+frSX6wAARG5JREFUeNrsnQdgHNWd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"
                  }
                ]
              },
              {
                width: 180,
                alignment: "center",
                text: [
                  {
                    text: "Visayan Riders Ministry Inc.",
                    fontSize: 12,
                    bold: true
                  },
                  "\n       Poblacion, Inabanga, Bohol",

                  {
                    text: " \n      Mobile No: 09361224834\n     Tel.: 038-5120290",
                    bold: true,
                    fontSize: 10
                  },
                  {
                    text: "\n\n Loan Card",
                    bold: true,
                    fontSize: 12
                  }
                ]
              }
            ]
          },
          {
            margins: [0, 0, 10, 0],
            columns: [
              {
                width: 250,
                fontSize: 9,
                text: [
                  { text: `Fullname: `, bold: true },
                  `${this.loan.member.lname}, ${this.loan.member.fname} ${
                    this.loan.member.mname != null ? this.loan.member.mname : ""
                  }`
                ]
              },
              {
                fontSize: 9,
                width: 150,
                text: [
                  { text: `Account No.: `, bold: true },
                  `${this.loan.member.account_number}`
                ]
              },
              {
                fontSize: 9,
                width: 200,
                text: [
                  { text: `Gender: `, bold: true },
                  this.loan.member.gender
                ]
              }
            ]
          },
          {
            columns: [
              {
                fontSize: 9,
                width: 250,
                text: [
                  { text: `Mode of Payment: `, bold: true },
                  this.payment_period
                ]
              },
              {
                fontSize: 9,
                width: 150,
                text: [
                  { text: `Term(month): `, bold: true },
                  this.loan.loan_period
                ]
              },
              {
                fontSize: 9,
                width: 200,
                text: [
                  { text: `Interest Rate: `, bold: true },
                  `${this.loan.interest_rate} %(${
                    this.loan_types.find(e => e.code == this.loan.loan_type)
                      .name
                  })`
                ]
              }
            ]
          },
          {
            columns: [
              {
                fontSize: 9,
                width: 250,
                text: [
                  { text: `Principal Amount: `, bold: true },
                  this.loan.principal.toFixed(2)
                ]
              },
              {
                fontSize: 9,
                width: 150,
                text: [
                  { text: `Interest Amount: `, bold: true },
                  this.loan.interest.toFixed(2)
                ]
              },
              {
                fontSize: 9,
                width: 150,
                text: [
                  { text: `Loan Cycle: `, bold: true },
                  this.loan.loan_cycle
                ]
              }
            ]
          },
          {
            margin: [0, 10, 0, 0],
            columns: [
              {
                fontSize: 9,
                width: 250,
                text: [{ text: `Acknoledgement: `, bold: true }]
              }
            ]
          },
          {
            margin: [0, 5, 0, 0],
            text:
              "I acknowledge that the loan indicated in this contract was disburse as of " +
              this.loan.date_release +
              ", and that I recieved the proceeds outline in the disclosure statement",
            fontSize: 9
          },
          {
            margin: [0, 10, 0, 0],
            columns: [
              {
                fontSize: 9,
                width: 150,
               
                text: [
                  { text: `Client Signature: `, bold: true },
                  "_______________"
                ]
              },
              {
                 alignment: "center",
                fontSize: 9,
                width: 130,
                text: [
                  { text: `_________________ \n`, bold: true },
                  "Disbursed by"
                ]
              },
              {
                 alignment: "center",
                fontSize: 9,
                width: 130,
                text: [
                  { text: `______________________ \n`, bold: true },
                  "Witness Signature"
                ]
              },
              {
                 alignment: "center",
                fontSize: 9,
                width: 130,
                text: [{ text: `_________________ \n`, bold: true }, "Date"]
              }
            ]
          },

          {
            margin: [0, 10, 0, 0],
            columns: [
              {
                width: 220,
                fontSize: 9,
                bold: true,
                text: "Schedule of Payments:"
              },
              {
                width: 250,
                fontSize: 9,
                bold: true,
                text: "Actual Payments:"
              }
            ]
          },

          {
            style: "tableExample",

            table: {
              widths: [50, 35, 35, 40, 45, 50, 50, 50, 50, 50],
              body: [
                [
                  { text: "Date", bold: true, style: "tableHeader" },
                  { text: "Principal", bold: true, style: "tableHeader" },

                  {
                    text: "Interest",
                    alignment: "center",
                    bold: true,
                    style: "tableHeader"
                  },
                  {
                    text: "Total",
                    alignment: "center",
                    bold: true,
                    style: "tableHeader"
                  },
                  {
                    text: "Date paid",
                    alignment: "center",
                    bold: true,
                    style: "tableHeader"
                  },
                  {
                    text: "Amnt. Col.",
                    alignment: "center",
                    bold: true,
                    style: "tableHeader"
                  },
                  {
                    text: "Variance",
                    alignment: "center",
                    bold: true,
                    style: "tableHeader"
                  },
                  {
                    text: "Principal Bal.",
                    alignment: "center",
                    bold: true,
                    style: "tableHeader"
                  },
                  {
                    text: "Interest Bal.",
                    alignment: "center",
                    bold: true,
                    style: "tableHeader"
                  },
                  {
                    text: "Officer Sig.",
                    alignment: "center",
                    bold: true,
                    style: "tableHeader"
                  }
                ]
              ]
            },
            layout: {
              hLineWidth: function(i, node) {
                return i === 0 || i === node.table.body.length ? 0.5 : 0.5;
              },
              vLineWidth: function(i, node) {
                return i === 0 || i === node.table.widths.length ? 0.5 : 0.5;
              },
              hLineColor: function(i, node) {
                return i === 0 || i === node.table.body.length
                  ? "black"
                  : "gray";
              },
              vLineColor: function(i, node) {
                return i === 0 || i === node.table.widths.length
                  ? "black"
                  : "gray";
              }
            }
          }
        ],

        styles: {
          header: {
            fontSize: 30,
            bold: true,
            alignment: "left",
            margin: [0, 0, 0, 20]
          },
          subheader: {
            fontSize: 16,
            bold: true,
            margin: [0, 10, 0, 5]
          },
          tableExample: {
            margin: [0, 5, 0, 15]
          },
          tableHeader: {
            bold: true,
            fontSize: 8,
            color: "black"
          }
        },
        defaultStyle: {
          // alignment: 'justify'
        }
      };

      let totalint = 0;
      let totalprin = 0;
      this.loan.loanscheds.forEach((el, i) => {
        let payments_array_size = this.payments.length - 1;

        if (i <= payments_array_size) {
          console.log(this.payments);
          totalint = totalint + parseFloat(this.payments[i].paid_interest);
          totalprin = totalprin + parseFloat(this.payments[i].paid_principal);
          let date=new Date(this.payments[i].date_of_payment)
          let fdate=`${date.getMonth()+1}-${date.getDate()}-${date.getFullYear()}`
          dd.content[8].table.body.push([
            { text: el.date, style: "tableHeader" },
            { text: el.principal, alignment: "right", style: "tableHeader" },
            { text: el.interest, alignment: "right", style: "tableHeader" },
            { text: el.total, alignment: "right", style: "tableHeader" },
            {
              text: fdate,
              alignment: "right",
              style: "tableHeader"
            },
            {
              text: (
                parseFloat(this.payments[i].paid_interest) +
                parseFloat(this.payments[i].paid_principal)
              ).toFixed(2),
              alignment: "right",
              style: "tableHeader"
            },
            {
              text: (
                parseFloat(el.total) -
                (parseFloat(this.payments[i].paid_interest) +
                  parseFloat(this.payments[i].paid_principal))
              ).toFixed(2),
              alignment: "right",
              style: "tableHeader"
            },
            {
              text: (parseFloat(this.loan.principal) - totalprin).toFixed(2),
              alignment: "right",
              style: "tableHeader"
            },
            {
              text: (parseFloat(this.loan.interest) - totalint).toFixed(2),
              alignment: "right",
              style: "tableHeader"
            },
            { text: "", alignment: "right", style: "tableHeader" }
          ]);
        } else {
          dd.content[8].table.body.push([
            { text: el.date, style: "tableHeader" },
            { text: el.principal, alignment: "right", style: "tableHeader" },
            { text: el.interest, alignment: "right", style: "tableHeader" },
            { text: el.total, alignment: "right", style: "tableHeader" },
            { text: "", alignment: "right", style: "tableHeader" },
            { text: "", alignment: "right", style: "tableHeader" },
            { text: "", alignment: "right", style: "tableHeader" },
            { text: "", alignment: "right", style: "tableHeader" },
            { text: "", alignment: "right", style: "tableHeader" },
            { text: "", alignment: "right", style: "tableHeader" }
          ]);
        }
      });
      for (let i = 0; i < 15; i++) {
        dd.content[8].table.body.push([
          { text: "-", style: "tableHeader",color:"white" },
          { text: "-", alignment: "right", style: "tableHeader",color:"white" },
          { text: "-", alignment: "right", style: "tableHeader",color:"white" },
          { text: "-", alignment: "right", style: "tableHeader",color:"white" },
          { text: "", alignment: "right", style: "tableHeader" },
          { text: "", alignment: "right", style: "tableHeader" },
          { text: "", alignment: "right", style: "tableHeader" },
          { text: "", alignment: "right", style: "tableHeader" },
          { text: "", alignment: "right", style: "tableHeader" },
          { text: "", alignment: "right", style: "tableHeader" }
        ]);
      }

      pdfMake.createPdf(dd).open();
    },
    openDialog() {
      this.dialogAdd = true;
    },

    calcInterest() {
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
          } else {
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
              principal: Math.round(Math.abs(ppmt)).toFixed(2),
              interest: Math.round(Math.abs(ipmt)).toFixed(2),
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
          } else {
            n = this.form.loan_period;
            dateinc = 29;

            console.log("3");
          }
          let interest =
            Math.round(
              (this.form.principal *
                this.form.loan_period *
                (this.form.interest_rate / 100)) /
                n
            ) * n;
          this.form.interest = interest;
          let principal = this.form.principal / n;
          let int = interest / n;
          this.form.loanscheds = [];
          let totaldateinc = 0;
          for (let i = 1; i <= n; i++) {
            let date = new Date(this.form.date_release);
            totaldateinc = totaldateinc + dateinc;

            date.setDate(date.getUTCDate() + totaldateinc);
            console.log(date.getDate());
            let datestr = `${date.getUTCMonth() +
              1}-${date.getUTCDate()}-${date.getFullYear()}`;
            this.form.loanscheds.push({
              date: datestr,
              datestr: date.toDateString(),
              principal: Math.round(principal).toFixed(2),
              interest: Math.round(int).toFixed(2),
              total: (Math.round(int) + Math.round(principal)).toFixed(2)
            });
          }
        }
      }
    },

    indexMethod(index) {
      return index + 1;
    },
    calBeginingBal() {
      let total_interest_paid = 0;
      let total_principal_paid = 0;
      this.payments.forEach(el => {
        total_interest_paid =
          parseFloat(el.paid_interest) + parseFloat(total_interest_paid);
        total_principal_paid =
          parseFloat(total_principal_paid) + parseFloat(el.paid_principal);
      });
      this.form.beginning_balance =
        parseFloat(this.loan.total_amount_due) -
        (parseFloat(total_interest_paid) + parseFloat(total_principal_paid));
    },
    savePayment() {
      let date = new Date(this.form.date_of_payment);
      this.form.date_of_payment = `${date.getMonth() +
        1}-${date.getDate()}-${date.getFullYear()}`;
      this.isLoading = true;
      axios
        .post("/api/v1/loanpayment/", this.form)
        .then(res => {
          this.isLoading = false;
          this.payments.push(res.data);

          this.dialogAdd = false;

          this.form = {
            date_of_payment: new Date(),
            beginning_balance: 0.0,
            paid_interest: 0.0,
            paid_principal: 0.0,
            ending_balance: 0.0,
            loan: this.$route.params.id
          };
        })
        .catch(err => {
          if (err.response.status == 401) {
            this.$message.error(
              "Tokken expire and being refresh now please try again"
            );
          }
        });
    }
  },

  computed: {
    total_Due() {
      let total = this.form.paid_principal + this.form.paid_interest;
      this.form.total_monthly_due = total;
      return total;
    },
    calculateEndingBal() {
      let total;
      try {
        total =
          parseFloat(this.form.beginning_balance) -
          (parseFloat(this.form.paid_interest) +
            parseFloat(this.form.paid_principal));
        console.log(total);
      } catch (err) {
        total = 0;
      }

      this.form.ending_balance = total;
      return total;
    },
    calculateBeginningbal() {
      let total_interest_paid = 0;
      let total_principal_paid = 0;
      this.payments.forEach(el => {
        total_interest_paid =
          parseFloat(el.paid_interest) + parseFloat(total_interest_paid);
        total_principal_paid =
          parseFloat(total_principal_paid) + parseFloat(el.paid_principal);
      });

      this.form.beginning_balance =
        parseFloat(this.loan.total_amount_due) -
        (parseFloat(total_interest_paid) + parseFloat(total_principal_paid));

      return total_interest_paid + total_principal_paid;
    },
    caltotInterest() {
      let total_interest_paid = 0;
      let n = 0;
      let interest_rate = 0;
      let i = this.payments.length != 0 ? this.payments.length : 0;
      this.payments.forEach(el => {
        total_interest_paid =
          parseFloat(el.paid_interest) + parseFloat(total_interest_paid);
      });
      console.log(total_interest_paid);
      if (this.loan.loan_type == 1) {
        if (this.loan.payment_period == 1) {
          n = this.loan.loan_period * 4;
          interest_rate = parseFloat(this.loan.interest_rate) / 100 / 4;

          console.log("1");
        } else if (this.loan.payment_period == 2) {
          n = this.loan.loan_period * 2;
          interest_rate = parseFloat(this.loan.interest_rate) / 100 / 2;

          console.log("2");
          console.log(n);
        } else {
          n = this.loan.loan_period;
          interest_rate = parseFloat(this.loan.interest_rate) / 100;

          console.log("3");
        }

        let bal = parseFloat(this.loan.interest) - total_interest_paid;

        let pmt = ExcelFormulas.PMT(
          interest_rate,
          n,
          parseInt(this.loan.principal)
        );

        let ipmt = ExcelFormulas.IPMT(
          parseFloat(this.loan.principal),
          parseFloat(pmt),
          interest_rate,
          i
        );
        console.log("ipmt " + pmt);

        if (bal >= ipmt) {
          this.form.paid_interest = Math.round(Math.abs(ipmt));
          // return (parseFloat(this.loan.principal_amount) * parseFloat(this.loan.interest_rate))/parseFloat(this.loan.term_id)
        } else {
          this.form.paid_interest = Math.ceil(bal);
          //return bal
        }
        return bal;
      } else {
        if (this.loan.payment_period == 1) {
          n = this.loan.loan_period * 4;

          console.log("1");
        } else if (this.loan.payment_period == 2) {
          n = this.loan.loan_period * 2;

          console.log("2");
          console.log(n);
        } else {
          n = this.loan.loan_period;

          console.log("3");
        }

        let bal = parseFloat(this.loan.interest) - total_interest_paid;

        let interest = Math.floor(
          (parseFloat(this.loan.principal) *
            parseFloat(this.loan.loan_period) *
            (parseFloat(this.loan.interest_rate) / 100)) /
            n
        );

        if (bal >= interest) {
          //   console.log('diri')
          this.form.paid_interest = Math.floor(
            (parseFloat(this.loan.principal) *
              parseFloat(this.loan.loan_period) *
              (parseFloat(this.loan.interest_rate) / 100)) /
              n
          );
          // return (parseFloat(this.loan.principal_amount) * parseFloat(this.loan.interest_rate))/parseFloat(this.loan.term_id)
        } else {
          this.form.paid_interest = Math.floor(bal);
          //return bal
        }
        return bal;
      }
    },
    calcTotprincipalPaid() {
      let total_principal_paid = 0;
      this.payments.forEach(el => {
        total_principal_paid =
          parseFloat(el.paid_principal) + parseFloat(total_principal_paid);
      });
      let n = 0;
      let interest_rate = 0;
      let i = this.payments.length != 0 ? this.payments.length + 1 : 1;
      if (this.loan.loan_type == 1) {
        if (this.loan.payment_period == 1) {
          n = this.loan.loan_period * 4;
          interest_rate = parseFloat(this.loan.interest_rate) / 100 / 4;

          console.log("1");
        } else if (this.loan.payment_period == 2) {
          n = this.loan.loan_period * 2;
          interest_rate = parseFloat(this.loan.interest_rate) / 100 / 2;

          console.log("2");
          console.log(n);
        } else {
          n = this.loan.loan_period;
          interest_rate = parseFloat(this.loan.interest_rate) / 100;

          console.log("3");
        }
        let bal = parseFloat(this.loan.principal) - total_principal_paid;
        let ppmt = ExcelFormulas.PPMT(
          interest_rate,
          i,
          n,
          parseFloat(this.loan.principal)
        );
        console.log(ppmt);

        if (bal >= Math.abs(ppmt)) {
          this.form.paid_principal = Math.floor(Math.abs(ppmt));
          //  return principal_monthly
        } else {
          this.form.paid_principal = Math.ceil(bal);
          //  return bal
        }

        return bal;
      } else {
        if (this.loan.payment_period == 1) {
          n = this.loan.loan_period * 4;

          console.log("1");
        } else if (this.loan.payment_period == 2) {
          n = this.loan.loan_period * 2;

          console.log("2");
          console.log(n);
        } else {
          n = this.loan.loan_period;

          console.log("3");
        }

        let bal = parseFloat(this.loan.principal) - total_principal_paid;
        let principal = parseFloat(this.loan.principal) / n;

        if (bal >= principal) {
          console.log("diri");
          this.form.paid_principal = Math.floor(principal);
          //  return principal_monthly
        } else {
          this.form.paid_principal = Math.floor(bal);
          //  return bal
        }

        return bal;
      }
    }
  },
  mounted() {
    axios
      .get("/api/v1/loanss/" + this.$route.params.id)
      .then(res => {
        this.loan = res.data;
        console.log(res.data);
        this.loan.name = `${this.loan.member.lname}, ${this.loan.member.fname}`;
        this.payment_period = this.periods.find(
          e => e.code == this.loan.payment_period
        ).name;
        this.loan.loanscheds.forEach(e => {
          e.total = (parseFloat(e.interest) + parseFloat(e.principal)).toFixed(
            2
          );
          e.datestr = new Date(e.date).toDateString();
        });

        this.members.push(res.data.member);
        this.clusters.push(res.data.clustername);
        this.members.forEach(e => {
          e.fullname = `${e.lname}, ${e.fname}`;
        });

        // this.loan.principal = (this.loan.principal).toFixed(2);
        this.loan.total_amount_due = (
          parseFloat(this.loan.principal) + parseFloat(this.loan.interest)
        ).toFixed(2);
      })
      .catch(err => {
        if (err.response.status == 401) {
          console.log("xxx");
          this.$message.error(
            "Tokken expire and being refresh now please try again"
          );
        }
      });
    axios.get("/api/v1/loanpaymentlist/" + this.$route.params.id).then(res => {
      if (res.data.length > 0) {
        this.payments = res.data;
        // this.form.paid_interest=(parseFloat(this.loan.principal_amount) * parseFloat(this.loan.interest_rate))/parseFloat(this.loan.term_id)
        //this.form.paid_principal=((parseFloat(this.loan.total_amount_due))-(parseFloat(this.loan.principal_amount) * parseFloat(this.loan.interest_rate)))/parseFloat(this.loan.term_id)

        this.calBeginingBal();
      }
    });
  }
};
</script>

<style>
</style>
