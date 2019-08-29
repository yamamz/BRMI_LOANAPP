<template>
    <div>
        <el-card>
            <h5>Loan List</h5>
            <hr>
                      <v-client-table filterable="true" :columns="columns" :data="datas">
            <div  slot="action" slot-scope="props">
                 <el-button icon="el-icon-view" circle type="primary" size="mini" style="float:right;margin-left:10px;" @click="view(props.row.id)" ></el-button>

                  <el-button  icon="el-icon-edit" circle type="success" size="mini" style="float:right;" @click="edit(props.row.id)" ></el-button>
          
             <el-button  icon="el-icon-delete" circle type="danger" size="mini" style="float:right;" @click="del(props.row.id,props.$index)" ></el-button>
          
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
//let loans=res.data.sort((a, b) => a.hasMotor > b.hasMotor ? -1 : (a.hasMotor < b.hasMotor ? 1 : 0))
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
        },
        del(id,index){
            axios.get('/api/v1/searchPayments/'+id).then(response=>{
                    console.log(response.data.scheds)
                    if(response.data.scheds == 0 && response.data.payments == 0 ){
                          axios.delete('/api/v1/loans/'+id+'/').then(res=>{
                            this.$message.success('Delete successfully')
                                this.datas.splice(index, 1);     
                    })
                    }else{
                       this.$message.error('Please delete first the payments and schedules')
        
                    }

            })
          
        }
    },

}
</script>

<style>

</style>
