<template>
    <div>
        <el-card>
            <h5>Loan List</h5>
            <hr>
                      <v-client-table filterable="true" :columns="columns" :data="datas">
            <div  slot="action" slot-scope="props">
                 <el-button icon="el-icon-view" round type="primary" size="mini" style="float:right;" @click="view(props.row.id)" >view</el-button>
                  <el-button icon="el-icon-view" round type="primary" size="mini" style="float:right;" @click="edit(props.row.id)" >edit</el-button>
          
          
            </div>
                    </v-client-table>
        </el-card>
    </div>
</template>

<script>
export default {
 data(){
        return{
            columns:['account_number','loan_cycle','fullname','interest_rate','principal','interest','balance','action'],
            datas:[]
        }
    },async created() {
        try{
             let res=await axios.get('/api/v1/loanss')
             this.datas=res.data
               this.datas.forEach(el=>{

                   el.account_number = el.member.account_number
              
                     el.fullname = `${el.member.lname}, ${el.member.fname}`
                     let totalinterestPaid=0
                     let totalprincipalpaid=0

                     el.loanpayments.forEach(e=>{
                        totalinterestPaid = totalinterestPaid + parseFloat(e.paid_interest)
                        totalprincipalpaid= totalprincipalpaid + parseFloat(e.paid_principal)
                     })
                     el.balance = (parseFloat(el.principal)+ parseFloat(el.interest)) - (totalinterestPaid + totalprincipalpaid)
               
               
             })

        }catch(err){
             if(err.response.status==401)
            {
                console.log('xxx')
                          this.$message.error('Tokken expire and being refresh now please try again')
                          this.$router.push('/')
            }
        }
      
    },
    methods: {
        view(id){
            this.$router.push('/app/loan/loanpayment/'+id)
        },
        edit(id){
            this.$router.push('/app/loan/edit/'+id)
        }
    },

}
</script>

<style>

</style>
