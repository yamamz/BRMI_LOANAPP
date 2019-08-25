<template>
    <div>
     
            <el-card>
                    <h5>Add Member</h5>
                    <hr>
                
                    <el-form size="mini" :ref="form" :model="form">
                        <el-row :gutter="5">
                            <el-col :md="8">
                                <el-form-item label="First name">
                                    <el-input placeholder="enter firstname" v-model="form.fname"></el-input>
                                </el-form-item>
                            </el-col>
                            <el-col :md="8">
                                <el-form-item label="Middle name">
                                    <el-input placeholder="enter middle name" v-model="form.mname"></el-input>
                                </el-form-item>
                            </el-col>
                            <el-col :md="8">
                                <el-form-item label="Last name">
                                    <el-input placeholder="enter lastname" v-model="form.lname"></el-input>
                                </el-form-item>
                            </el-col>
                        </el-row>
                        <el-row :gutter="5">
                            <el-col :md="16">
                                <el-form-item label="Address">
                                    <el-input placeholder="enter address"   v-model="form.address"></el-input>
                                </el-form-item>
                            </el-col>
                            <el-col :md="8">
                                <el-form-item label="Gender">
                                        <el-select style="width: 100%;" v-model="form.gender" placeholder="Select Gender">
                                                <el-option v-for="(item, index) in genders" :label="item" :value="item" :key="index"></el-option>
                                            </el-select>
                                </el-form-item>
                            </el-col>
                        </el-row>
                        <el-row :gutter="5">
                            <el-col :md="8">
                                    <el-form-item label="Mobile #">
                                            <el-input placeholder="enter mobile number" v-model="form.mobile_number"></el-input>
                                        </el-form-item>
                            </el-col >
                            <el-col :md="8">
                                    <el-form-item label="Age">
                                            <el-input type="number" style="width:100%;" placeholder="enter age" v-model="form.age"/>
                                        </el-form-item>
                            </el-col >
                            <el-col :md="8">
                                    <el-form-item label="Occupation">
                                            <el-input placeholder="enter occupation" v-model="form.occupation"></el-input>
                                    </el-form-item>
                            </el-col>
                        </el-row>
                        <el-row :gutter="5">
                            <el-col :md="8">
                                <el-form-item label="Civil Status">
                                        <el-select style="width: 100%;" v-model="form.civil_status" placeholder="Select Status">
                                                <el-option v-for="(item, index) in civil_statuses" :label="item" :value="item" :key="index"></el-option>
                                            </el-select>
                                </el-form-item>
                                
                            </el-col>
                            <el-col :md="8">
                                <el-form-item label="Husband's or Wife's Name">
                                    <el-input placeholder="enter fullname" v-model="form.partner_name" :disabled="form.civil_status=='' || form.civil_status=='widower' || form.civil_status=='single'"></el-input>
                                </el-form-item>
                            </el-col>
                            <el-col :md="8">
                                    <el-form-item label="Monthly Income">
                                        <el-input type="number" style="width:100%;" placeholder="monthly income here..."  v-model="form.monthly_income" />
                                    </el-form-item>
                                </el-col>
                        </el-row>
                    </el-form>
                    <hr>
                    <el-button @click="save" type="primary" size="small" icon="el-icon-edit">Save</el-button>
                </el-card>
    </div>


    
</template>
<style scoped>

    .el-form-item--small .el-form-item__content, .el-form-item--small .el-form-item__label {
        line-height: 10px;
    }
</style>

<script>
export default {
data(){
    return{
        genders:["male","female"],
        civil_statuses:['single','married','widower'],
        members:[],
        form:{
            account_number:'ACNT-'+Math.floor((Math.random() * 5000) + 1)+'-'+Math.floor((Math.random() * 9999) + 1),
            fname:'',
            mname:'',
            lname:'',
            age:null,
            gender:'',
            occupation:'',
            civil_status:'',
            partner_name:'',
            address:'',
            mobile_number:'',
            monthly_income:null
        }
    }
},
methods: {
    save(){
        console.log('x')
        let findMem = this.members.filter(e=> e.fname == this.form.fname && e.lname == this.form.lname)
        if(findMem.length == 0){
                   axios.post('/api/v1/members/',this.form).then(res=>{
            console.log(res.data)
               this.$message.success('Save data successfully')
            this.$router.push('/app/member/list')
        }).catch(err=>{
            console.log(err.response.status)
            if(err.response.status == 400){
                this.$message.error('Error occur please check data')
            }
            if(err.response.status==401)
            {
                console.log('xxx')
                          this.$message.error('Tokken expire and being refresh now please try again')
                      
            }
        }) 
        }else{
                      this.$message.error('Member already exists')
        }

    }  
},created(){
    axios.get('/api/v1/members').then(res=>{
        this.members= res.data
    })
}


}
</script>

<style>

</style>


