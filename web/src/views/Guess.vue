<template>
    <el-container>
        <el-header>
            <el-row type="flex" justify="space-between" align="middle">
                <el-col :span="24" style="text-align: right;">
                  <div class="header-buttons">
                    <el-button circle icon="el-icon-setting" @click="settingVisble=true"></el-button>
                    <el-button circle icon="el-icon-question" @click="introVisble=true"></el-button>
                    <el-link :underline="false" href="https://github.com/QuantAskk/pokemonle" style="margin-left:10px">
                        <el-button circle icon="el-icon-user"></el-button>
                    </el-link>
                  </div>
                </el-col>
            </el-row>

            <el-dialog
                title="设置"
                :visible.sync="settingVisble"
                width="30%"
                :show-close="false"
                :close-on-click-modal="false"
                :close-on-press-escape="false">
                <div class="setting">
                    模式：<el-select v-model="settings.hardid" placeholder="请选择" size="small" style="width: 50%">
                        <el-option
                        v-for="item in this.hards"
                        :key="item"
                        :label="item"
                        :value="item"
                        >
                        </el-option>
                    </el-select>
                    <br>
                    世代：<el-select v-model="settings.genid" placeholder="请选择" size="small" style="width: 50%"
                        @change="ReloadGuessNumber()">
                        <el-option
                        v-for="item in this.gens"
                        :key="item"
                        :label="item"
                        :value="item"
                        >
                        </el-option>
                    </el-select>
                    <br>
                    <el-switch
                    v-model="settings.battleOpen"
                    active-text="显示更多种族值信息"
                    @change="ReloadGuessNumber()">
                    </el-switch>
                    <el-switch
                    v-model="settings.shapeOpen"
                    active-text="显示更多外形信息"
                    @change="ReloadGuessNumber()">
                    </el-switch>
                    <el-switch
                    v-model="settings.catchOpen"
                    active-text="显示蛋组/捕获率信息"
                    @change="ReloadGuessNumber()">
                    </el-switch>
                    <br>
                    <el-switch
                    v-model="settings.autodif"
                    active-text="自动调整"
                    inactive-text="手动调整"
                    @change="ReloadGuessNumber()">
                    </el-switch>
                    <div class="block">
                        <span class="demonstration">猜测次数：{{this.settings.maxguess}}</span>
                        <el-slider
                        v-model="settings.maxguess"
                        :step="1"
                        :max="12"
                        :min="2"
                        :disabled="this.settings.autodif"
                        style="width: 100%">
                        </el-slider>
                    </div>
                </div>
                
                <span slot="footer" class="dialog-footer">
                    <el-button type="primary" @click="CloseSetting()">确 定</el-button>
                </span>
            </el-dialog>

            <el-dialog
                title="规则介绍"
                :visible.sync="introVisble"
                width="30%"
                :show-close=false>
                <div class="setting">
                    输入一个宝可梦进行猜测。
                    <br>
                    每次猜测后，你会获得你输入的宝可梦的信息。
                    <br>
                    <div>
                        <el-tag type="success" size="small">
                            绿色高亮
                        </el-tag>
                        表示该信息与你需要猜测的宝可梦完全相同；
                    </div>
                    <div>
                        <el-tag type="warning" size="small">
                            黄色高亮
                        </el-tag>
                        表示该信息与你需要猜测的宝可梦比较接近；
                    </div>
                    "↑": 应该往高了猜；"↓": 应该往低了猜；
                    <br>
                    简单模式只会保留较为热门或携带其他标签的宝可梦。
                </div>
                
                <span slot="footer" class="dialog-footer">
                    <el-button type="primary" @click="introVisble=false">确 定</el-button>
                </span>
            </el-dialog>

        </el-header>
        <el-main>
            <div class="guess">
                <el-row type="flex" justify="center" align="middle" gutter="20">
                    <el-col :span="7">
                        <el-autocomplete
                        class="inline-input"
                        v-model="input"
                        :fetch-suggestions="querySearch"
                        placeholder="请输入内容"
                        :trigger-on-focus="false"
                        style="width: 100%"></el-autocomplete>
                    </el-col>
                    <el-col :xs="5" :sm="4" :md="3" :lg="3" :xl="2">
                        <el-button type="primary" style="width: 100%" :disabled="this.gameover" @click="Guess()">
                            {{ this.gameover ? '已结束' : '确定' }}
                        </el-button>
                    </el-col>
                    <el-col :xs="5" :sm="4" :md="3" :lg="3" :xl="2">
                        <el-button type="success" style="width: 100%" @click="Restart()">重新开始</el-button>
                    </el-col>
                    <!-- <el-col :span="12"><div class="grid-content bg-purple">aaa</div></el-col>
                    <el-col :span="12"><div class="grid-content bg-purple-light">bbb</div></el-col> -->
                </el-row>
                <el-row class="times">
                    猜测次数：{{this.times}}/{{this.settings.maxguess}}
                </el-row>
                <el-table
                :data="tableData"
                style="width: 100%"
                empty-text=" ">

                    <el-table-column
                    label=""
                    min-width="70">
                        <template slot-scope="scope">
                                <el-image
                                style="width: 50px; height: 50px"
                                :src="scope.row.imgUrl"
                                :fit="fit"
                                ></el-image>
                        </template>
                    </el-table-column>

                    <el-table-column
                    label="宝可梦"
                    min-width="100"
                    align="center">
                        <template slot-scope="scope">
                            <p style="white-space: nowrap;">{{ scope.row.name }}</p>
                        </template>
                    </el-table-column>

                    
                    <el-table-column
                    label="外形"
                    min-width="100"
                    align="center"
                    v-if="settings.shapeOpen">
                        <template slot-scope="scope">
                            <el-tag style="font-size: 17px" :type="scope.row.shape.col">
                                {{ scope.row.shape.key }}
                            </el-tag>
                            <el-tag style="font-size: 17px" :type="scope.row.col.col">
                                {{ scope.row.col.key }}
                            </el-tag>
                        </template>
                    </el-table-column>

                    <el-table-column
                    label="属性"
                    min-width="100"
                    align="center">
                        <template slot-scope="scope">
                            <a v-for="item in scope.row.type">
                                <el-tag style="font-size: 17px" :type="item.col">
                                    {{ item.key }}
                                </el-tag>
                            </a>
                        </template>
                    </el-table-column>

                    <el-table-column
                    label="种族值"
                    min-width="150"
                    align="center">
                        <template slot-scope="scope">
                            <el-tag style="font-size: 17px" :type="scope.row.pow.col">
                                {{ ValueText(scope.row.pow.key,scope.row.pow.value) }}
                            </el-tag>
                            <el-tag style="font-size: 17px" :type="scope.row.speed.col" v-if="settings.battleOpen">
                                速度:{{ ValueText(scope.row.speed.key,scope.row.speed.value) }}
                            </el-tag>
                            <el-tag style="font-size: 17px" :type="scope.row.attack.col" v-if="settings.battleOpen">
                                {{ scope.row.attack.key }}
                            </el-tag>
                            <el-tag style="font-size: 17px" :type="scope.row.defense.col" v-if="settings.battleOpen">
                                {{ scope.row.defense.key }}
                            </el-tag>
                        </template>
                    </el-table-column>

                    <el-table-column
                    label="世代"
                    min-width="120"
                    align="center">
                        <template slot-scope="scope">
                            <el-tag style="font-size: 17px" :type="scope.row.gen.col">
                                {{ ValueText(scope.row.gen.key,scope.row.gen.value) }}
                            </el-tag>
                        </template>
                    </el-table-column>
                    
                    <el-table-column
                    label="特性"
                    min-width="150"
                    align="center">
                        <template slot-scope="scope">
                            <a v-for="item in scope.row.ability">
                                <el-tag style="font-size: 17px" :type="item.col">
                                    {{ item.key }}
                                </el-tag>
                            </a>
                        </template>
                    </el-table-column>

                    <el-table-column
                    label="进化条件"
                    min-width="170"
                    align="center">
                        <template slot-scope="scope">
                            <el-tag style="font-size: 17px" :type="scope.row.evo.col" v-if="scope.row.evo.key!=null">
                                {{ scope.row.evo.key }}
                            </el-tag>
                            <el-tag style="font-size: 17px" :type="scope.row.stage.col">
                                {{ scope.row.stage.key }}
                            </el-tag>
                        </template>
                    </el-table-column>

                    <el-table-column
                    label="蛋组/捕获率"
                    min-width="120"
                    align="center"
                    v-if="settings.catchOpen">
                        <template slot-scope="scope">
                            <a v-for="item in scope.row.egg">
                                <el-tag style="font-size: 17px" :type="item.col">
                                    {{ item.key }}
                                </el-tag>
                            </a>
                            <el-tag style="font-size: 17px" :type="scope.row.catrate.col">
                                捕获率:{{ ValueText(scope.row.catrate.key,scope.row.catrate.value) }}
                            </el-tag>
                        </template>
                    </el-table-column>

                    <el-table-column
                    label="其他"
                    min-width="200"
                    align="center">
                        <template slot-scope="scope">
                            <a v-for="item in scope.row.label">
                                <el-tag style="font-size: 17px" :type="item.col">
                                    {{ item.key }}
                                </el-tag>
                            </a>
                        </template>
                    </el-table-column>
                </el-table>
            </div>
        </el-main>
    </el-container>
</template>
  
<script>
    import axios from 'axios'
    import { MessageBox } from 'element-ui';

    function truncateString(str, maxLength) {
        if (str.length > maxLength) {
            return str.slice(0, maxLength) + '...';
        }
        return str;
    }

    export default{
        data(){
            return{
                input:"",
                tempdata:null,
                nameList:[],
                tableData: [],
                temp:{},
                reply:{},
                times:0,
                gameover:false,
                settingVisble:false,
                introVisble:false,
                gens:["全世代","第一世代","第二世代","第三世代","第四世代","第五世代","第六世代","第七世代","第八世代","第九世代"],
                hards:["普通模式","简单模式"],
                settings:{
                    genid:"全世代",
                    hardid:"普通模式",
                    maxguess:10,
                    autodif:true,
                    battleOpen:false,
                    shapeOpen:false,
                    catchOpen:false,
                },
            }
        },
        methods:{
            async createFilter(queryString) {
                if (this.nameList.length === 0) {  // 修复判断空数组的正确方式
                    await this.loadName();
                }
                const query = queryString.toLowerCase();
                
                return (item) => {  // 参数应为单个元素，而非整个数组
                    // 添加容错处理确保 value 存在
                    const target = (item.value || '').toLowerCase();
                    let qIndex = 0, tIndex = 0;
                    
                    // 子序列匹配核心逻辑
                    while (qIndex < query.length && tIndex < target.length) {
                    if (query[qIndex] === target[tIndex]) qIndex++;
                    tIndex++;
                    }
                    return qIndex === query.length; // 是否找到全部字符
                };
                },

                // 修改后的 querySearch 方法
                querySearch(queryString, cb) {
                // 保留原始引用避免异步问题
                const filterFn = this.createFilter(queryString);
                
                // 处理异步过滤
                Promise.resolve(filterFn).then(filter => {
                    const results = queryString 
                    ? this.nameList.filter(filter) 
                    : this.nameList;
                    cb(results);  // 注意保持回调参数格式
                }).catch(err => {
                    console.error('Filter error:', err);
                    cb([]);  // 异常时返回空数组
                });
            },
            async loadName(){
                try{
                    const options = {
                        method: 'GET',
                        url: `${process.env.VUE_APP_API_BASE_URL}/nameget`
                    };

                    await axios.request(options).then((response)=>{
                        this.tempdata=response.data
                    }).catch(function (error) {
                        console.error(error);
                    });
                    
                    this.nameList=this.tempdata.map(item=>({value:item}));
                    
                }catch(error){
                    console.error("请求失败",error)
                }
            },
            async Restart(){
                this.times=0
                this.gameover=false
                sessionStorage.removeItem('answer')
                this.tableData=[]
                console.log(`${process.env.VUE_APP_API_BASE_URL}/initget`)
                try{
                    const gen=this.gens.indexOf(this.settings.genid)
                    const dif=this.hards.indexOf(this.settings.hardid)
                    const options = {
                        method: 'GET',
                        url: `${process.env.VUE_APP_API_BASE_URL}/initget`,
                        params:{
                            difficulty:dif,
                            gen:gen
                        }   
                    };

                    await axios.request(options).then((response)=>{
                        this.tempdata=response.data
                        console.log(this.tempdata)
                    }).catch(function (error) {
                        console.error(error);
                    });
                    sessionStorage.setItem('answer',this.tempdata)
                }catch(error){
                    console.error(error)
                }
            },
            async Guess(){
                const answer=sessionStorage.getItem('answer')
                if(answer==null)return;
                try{
                    const options = {
                        method: 'GET',
                        url: `${process.env.VUE_APP_API_BASE_URL}/guess`,
                        params:{
                            answer:answer,
                            guess:this.input
                        }   
                    };
                    await axios.request(options).then((response)=>{
                        this.tempdata=response.data
                    }).catch(function (error) {
                        console.error(error);
                    });

                    const data=this.tempdata
                    if(data=="guess name error"){
                        this.$notify({
                            title: '提交错误',
                            message: '不存在的宝可梦',
                            type: "error"
                        });
                    }else{
                        this.temp={}

                        this.temp.name=data.name
                        this.temp.answer=data.answer

                        // 属性
                        this.temp.type=[]
                        data.type.forEach((type,index)=>{
                            if(type.key!="无"){
                                if(type.value=='True')
                                    this.temp.type.push({key:type.key,col:"success"})
                                else
                                    this.temp.type.push({key:type.key,col:"info"})
                            }
                        })

                        // 种族值
                        this.temp.pow={}
                        this.temp.pow.key=data.pow.key
                        this.temp.pow.value=data.pow.value
                        if(data.pow.value=="equiv")
                            this.temp.pow.col="success"
                        else if(data.pow.dis=="far")
                            this.temp.pow.col="info"
                        else
                            this.temp.pow.col="warning"

                        //速度
                        this.temp.speed={}
                        this.temp.speed.key=data.speed.key
                        this.temp.speed.value=data.speed.value
                        if(data.speed.value=="equiv")
                            this.temp.speed.col="success"
                        else if(data.speed.dis=="far")
                            this.temp.speed.col="info"
                        else
                            this.temp.speed.col="warning"
                        
                        //物特
                        this.temp.attack={}
                        this.temp.attack.key=data.attack.key
                        this.temp.attack.value=data.attack.value
                        if(data.attack.value=='True')
                            this.temp.attack.col="success"
                        else 
                            this.temp.attack.col="info"

                        this.temp.defense={}
                        this.temp.defense.key=data.defense.key
                        this.temp.defense.value=data.defense.value
                        if(data.defense.value=='True')
                            this.temp.defense.col="success"
                        else 
                            this.temp.defense.col="info"

                        // 世代
                        this.temp.gen={}
                        this.temp.gen.key=data.gen.key
                        this.temp.gen.value=data.gen.value
                        if(data.gen.value=='equiv')
                            this.temp.gen.col="success"
                        else 
                            this.temp.gen.col="info"

                        // 特性
                        this.temp.ability=[]
                        data.ability.forEach((ability,index)=>{
                            if(ability.value=='True')
                                this.temp.ability.push({key:ability.key,col:"success"})
                            else
                                this.temp.ability.push({key:ability.key,col:"info"})
                        })

                        // 进化方式
                        this.temp.evo={}
                        this.temp.evo.key=data.evo.key
                        if(this.temp.evo.key!=null)
                            this.temp.evo.key=truncateString(this.temp.evo.key,9)
                        if(data.evo.value=="far")
                            this.temp.evo.col="info"
                        else if(data.evo.value=="near")
                            this.temp.evo.col="warning"
                        else 
                            this.temp.evo.col="success"
  
                        // 阶段
                        this.temp.stage={}
                        this.temp.stage.key=data.stage.key
                        this.temp.stage.value=data.stage.value
                        if(data.stage.value=='True')
                            this.temp.stage.col="success"
                        else 
                            this.temp.stage.col="info"

                        //蛋组
                        this.temp.egg=[]
                        data.egg.forEach((egg,index)=>{
                            if(egg.value=='True')
                                this.temp.egg.push({key:egg.key,col:"success"})
                            else
                                this.temp.egg.push({key:egg.key,col:"info"})
                        })

                        //捕获率
                        this.temp.catrate={}
                        this.temp.catrate.key=data.catrate.key
                        this.temp.catrate.value=data.catrate.value
                        if(data.catrate.value=="equiv")
                            this.temp.catrate.col="success"
                        else
                            this.temp.catrate.col="info"
                        
                        //外形
                        this.temp.shape={}
                        this.temp.shape.key=data.shape.key
                        this.temp.shape.value=data.shape.value
                        if(data.shape.value=='True')
                            this.temp.shape.col="success"
                        else 
                            this.temp.shape.col="info"

                        this.temp.col={}
                        this.temp.col.key=data.col.key
                        this.temp.col.value=data.col.value
                        if(data.col.value=='True')
                            this.temp.col.col="success"
                        else 
                            this.temp.col.col="info"


                        // 其他标签
                        this.temp.label=[]
                        data.label.forEach((label,index)=>{
                            if(label.value=='True')
                                this.temp.label.push({key:label.key,col:"success"})
                            else
                                this.temp.label.push({key:label.key,col:"info"})
                        })

                        console.log(this.temp)

                        // 获取图片
                        try{
                            const options = {
                                method: 'GET',
                                url: `${process.env.VUE_APP_API_BASE_URL}/getimage`,
                                params: {pokemon: this.temp.name},
                                responseType:'blob'
                            };
                            await axios.request(options).then((response)=>{
                                this.tempdata=response.data
                            }).catch(function (error) {
                                console.error(error);
                            });
                            const blob=new Blob([this.tempdata]);
                            this.temp.imgUrl=URL.createObjectURL(blob);
                        }catch(error){
                            console.error('图片获取失败:',error);
                        }

                        this.tableData.push(this.temp);
                        this.times++;

                        // 猜测结束
                        if(this.temp.answer=='True'||this.times==this.settings.maxguess){
                            this.gameover=true
                            this.ReplayAnswer()
                        }
                    }
                }catch(error){
                    console.error(error)
                }
            },
            ValueText(key,value){
                if(value=='high')
                    return String(key)+"↑"
                if(value=='low')
                    return String(key)+"↓"
                return String(key)
            },
            async ReplayAnswer(){
                const answer=sessionStorage.getItem('answer')
                if(answer==null)return;
                try{
                    const options = {
                        method: 'GET',
                        url: `${process.env.VUE_APP_API_BASE_URL}/getanswer`,
                        params:{
                            pokemon:answer
                        } 
                    };
                    await axios.request(options).then((response)=>{
                        this.tempdata=response.data
                    }).catch(function (error) {
                        console.error(error);
                    });
                    const data=this.tempdata
                    console.log(data)


                    try{
                        const options = {
                            method: 'GET',
                            url: `${process.env.VUE_APP_API_BASE_URL}/getimage`,
                            params: {pokemon: data.name},
                            responseType:'blob'
                        };
                        await axios.request(options).then((response)=>{
                            this.tempdata=response.data
                        }).catch(function (error) {
                            console.error(error);
                        });
                        const blob=new Blob([this.tempdata]);
                        this.temp.imgUrl=URL.createObjectURL(blob);
                    }catch(error){
                        console.error('图片获取失败:',error);
                    }

                    this.reply.type=""
                    data.type.forEach((tmp,index)=>{
                        if(index!=0)this.reply.type+="+";
                        this.reply.type+=tmp.key;
                    })
                    
                    this.reply.ability=""
                    data.ability.forEach((tmp,index)=>{
                        if(index!=0)this.reply.ability+=",";
                        this.reply.ability+=tmp.key;
                    })
                    
                    this.reply.label=""
                    data.label.forEach((tmp,index)=>{
                        if(index!=0)this.reply.label+=",";
                        this.reply.label+=tmp.key;
                    })
                    if(this.reply.label=="")
                        this.reply.label="无"

                    const h = this.$createElement;
                    MessageBox({
                        title: '游戏结束',
                        message: h('el-container', null, [
                            h('el-aside',{attrs:{style: 'width:100px'}},[
                            h('img', {
                            attrs: {
                                src: this.temp.imgUrl,
                                style: 'width: 100px; height: 100px;'
                            }
                            })]),
                            h('el-container',null,[
                                h('el-header',null,[
                                    h('p',"宝可梦:"+data.name)
                                ]),
                                h('el-main',null,[
                                    h('p',"属性:"+this.reply.type),
                                    h('p',"种族值:"+data.pow.key),
                                    h('p',"特性:"+this.reply.ability),
                                    h('p',"其他标签:"+this.reply.label)
                                ])
                            ])
                        ]),
                        confirmButtonText: '下一把',
                    }).then(()=>{})
                    .catch(()=>{});
                }catch(error){
                    console.error(error)
                }
            },
            CloseSetting(){
                this.saveSettings();
                this.settingVisble=false;
                this.Restart();
            },
            ReloadGuessNumber(newvalue){
                if(this.settings.autodif==false)return true;
                this.settings.maxguess=10;
                var x=this.settings.battleOpen*2+this.settings.shapeOpen*2+this.settings.catchOpen;
                if(this.settings.genid!="全世代")this.settings.maxguess-=3,x+=(x<=3);
                if(x==1&&this.settings.catchOpen)x++;
                if(x==2&&this.settings.battleOpen)x++;
                else if(x>=3)x++;
                if(x>=6)this.settings.maxguess-=1;
                if(x>=5)this.settings.maxguess-=1;
                if(x>=4)this.settings.maxguess-=1;
                if(x>=3)this.settings.maxguess-=1;
                if(x>=2)this.settings.maxguess-=1;
                return true;
            },
            saveSettings(){
                console.log("保存设置中")
                try{
                    localStorage.setItem('guessSettings',JSON.stringify(this.settings));
                }catch(e){
                    console.error("设置保存失败：",e);
                }
            },
            loadSettings(){
                try{
                    const savedSettings=localStorage.getItem("guessSettings");
                    if(savedSettings){
                        this.settings=JSON.parse(savedSettings);
                    }
                }catch(e){
                    console.error("设置加载失败：",e);
                }
            }
        },
        computed:{
        },
        mounted() {
            this.loadSettings();
            this.Restart();
        }
    }
</script>

<style>

    .guess{
        margin-top: -2%;
        margin-left: 5%;
        margin-right: 5%;
        font-size: 3rem;
    }
    .inputlayout{
        display: flex;
        text-align: center;
        justify-content: center;
    }
    .inputbox{
        display: flex;
        justify-content: center;
        gap: 2rem;
        width: 60%;
    }
    .times{
        color: rgb(144, 147, 153);
        font-size: 1.5rem;
    }
    .setting{
        margin-left: 5%;
        margin-right: 5%;
        display: flex;
        flex-direction: column;
        gap: 8px;
    }
</style>