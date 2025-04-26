<template>
  <el-container>
    <el-header>
      <el-row type="flex" justify="space-between" align="middle">
        <el-col :span="24" style="text-align: right;">
          <div class="header-buttons">
            <el-button circle :icon="darkMode ? 'el-icon-sunny' : 'el-icon-moon'" @click="toggleDarkMode"></el-button>
            <el-button circle icon="el-icon-question" @click="introVisble=true"></el-button>
            <el-button circle icon="el-icon-user" @click="authorVisble=true"></el-button>
          </div>
        </el-col>
      </el-row>

      <!-- 规则介绍对话框 -->
      <el-dialog
          title="规则介绍"
          :visible.sync="introVisble"
          :width="isMobile ? '90%' : '50%'"
          :show-close=false
          custom-class="enhanced-dialog">
        <div class="intro-content">
          <p>输入一个宝可梦进行猜测。</p>
          <p>每次猜测后，你会获得你输入的宝可梦的信息。</p>

          <div class="hint-section">
            <div class="hint-item">
              <el-tag type="success" size="small">绿色高亮</el-tag>
              <span>表示该信息与你需要猜测的宝可梦完全相同</span>
            </div>
            <div class="hint-item">
              <el-tag type="warning" size="small">黄色高亮</el-tag>
              <span>表示该信息与你需要猜测的宝可梦比较接近</span>
            </div>
            <div class="hint-item">
              <span>"↑": 应该往高了猜；"↓": 应该往低了猜</span>
            </div>
          </div>

          <p>简单模式只会保留较为热门或携带其他标签的宝可梦。</p>
          <p><strong>世代选择：</strong>可以选择单个或多个世代组合进行游戏。</p>
        </div>

        <div slot="footer" class="dialog-footer">
          <el-button type="primary" @click="introVisble=false">确 定</el-button>
        </div>
      </el-dialog>
      <!-- 制作人员对话框（美化版） -->
      <el-dialog
          title="制作人员"
          :visible.sync="authorVisble"
          :width="isMobile ? '90%' : '50%'"
          :show-close="false"
          custom-class="enhanced-dialog">
        <div class="author-content">
          <div class="author-links">
            <el-button type="primary" size="small"
                       @click="openLink('https://www.bilibili.com/video/BV1XmLFz5E7Y/?spm_id_from=333.1387.homepage.video_card.click')">
              视频链接
            </el-button>
            <el-button type="info" size="small" @click="openLink('https://space.bilibili.com/38187048')">
              作者空间
            </el-button>
            <el-button type="success" size="small" @click="openLink('https://github.com/QuantAskk/pokemonle')">
              项目源地址
            </el-button>
          </div>
          <div class="author-cards">
            <el-card :body-style="{ padding: '0px' }" class="author-card">
              <img src="@/assets/img/QAHead.jpg" class="author-avatar">
              <div class="author-info">
                <span>QuantAsk</span>
                <br>
<<<<<<< HEAD
                <el-tag size="mini" type="info">作者</el-tag>
=======
                <el-tag size="mini" type="info">基础架构</el-tag>
>>>>>>> master
              </div>
            </el-card>
            <el-card :body-style="{ padding: '0px' }" class="author-card">
              <img src="@/assets/img/GengerHead.jpg" class="author-avatar">
              <div class="author-info">
                <span>流明Luminous</span>
                <br>
<<<<<<< HEAD
                <el-tag size="mini" type="info">UI优化</el-tag>
=======
                <el-tag size="mini" type="info">UI/功能</el-tag>
              </div>
            </el-card>
            <el-card :body-style="{ padding: '0px' }" class="author-card">
              <img src="@/assets/img/TyranitarX.png" class="author-avatar">
              <div class="author-info">
                <span>TyranitarX</span>
                <br>
                <el-tag size="mini" type="info">双人模式</el-tag>
>>>>>>> master
              </div>
            </el-card>
          </div>
        </div>
<<<<<<< HEAD

        <span slot="footer" class="dialog-footer">
                    <el-button type="primary" @click="authorVisble=false">确 定</el-button>
                </span>
      </el-dialog>
    </el-header>
    <el-main>
      <div class="guess">
        <div class="setting">
          <div class="setting-section">
            <div class="setting-title">游戏模式</div>
            <el-select v-model="settings.hardid" placeholder="请选择" size="small" style="width: 50%"
                       @change="updateSetting" :disabled="!this.cur_room||!this.host">
              <el-option
                  v-for="item in this.hards"
                  :key="item"
                  :label="item"
                  :value="item"
              >
              </el-option>
            </el-select>
          </div>
          <div v-if="!this.host||!this.cur_room" class="setting-section">
            <div class="setting-title">世代选择</div>
            <div class="gen-selection">
              <div class="gen-checkboxes">
                <el-checkbox
                    v-for="(gen, index) in genOptions"
                    :key="gen.value"
                    v-model="settings.selectedGens[index]"
                    @change="updateSetting" disabled>
                  {{ gen.label }}
                </el-checkbox>
              </div>
            </div>
          </div>
          <div v-if="this.cur_room&&this.host" class="setting-section">
            <div class="setting-title">世代选择</div>
            <div class="gen-selection">
              <div class="gen-checkboxes">
                <el-checkbox
                    v-for="(gen, index) in genOptions"
                    :key="gen.value"
                    v-model="settings.selectedGens[index]"
                    @change="updateSetting">
                  {{ gen.label }}
                </el-checkbox>
              </div>
            </div>
          </div>

          <div class="setting-section">
            <div class="setting-title">显示信息</div>
            <div class="switch-group">
              <el-switch
                  v-model="settings.battleOpen"
                  active-text="显示更多种族值信息"
                  @change="updateSetting"
                  :disabled="!this.cur_room||!this.host"
              >
              </el-switch>
              <el-switch
                  v-model="settings.shapeOpen"
                  active-text="显示更多外形信息"
                  @change="updateSetting"
                  :disabled="!this.cur_room||!this.host"
              >
              </el-switch>
              <el-switch
                  v-model="settings.catchOpen"
                  active-text="显示蛋组/捕获率信息"
                  @change="updateSetting"
                  :disabled="!this.cur_room||!this.host"
              >
              </el-switch>
              <el-switch
                  v-model="settings.showGenArrow"
                  active-text="开启世代箭头"
                  @change="updateSetting"
                  :disabled="!this.cur_room||!this.host"
              >
              </el-switch>
            </div>
          </div>

          <div class="setting-section">
            <div class="setting-title">卡片展示顺序</div>
            <el-switch
                v-model="settings.reverseDisplay"
                active-text="猜测反向显示"
                inactive-text="猜测正向显示"
                @change="updateSetting"
                :disabled="!this.cur_room||!this.host"
            >
            </el-switch>
          </div>

          <el-switch
              v-model="settings.cheatOpen"
              active-text="小小的恶作剧"
              @change="updateSetting"
              :disabled="!this.cur_room||!this.host"
          >
          </el-switch>
          <br>

          <div class="block">
            <span class="demonstration">猜测次数：{{ this.settings.maxguess }}</span>
            <el-slider
                v-model="settings.maxguess"
                :step="1"
                :max="15"
                :min="3"
                :show-tooltip="false"
                style="width: 100%"
                @change="updateSetting"
                :disabled="!this.cur_room||!this.host"
            >
            </el-slider>
          </div>
        </div>
        <el-row type="flex" justify="center" align="middle" gutter=20>
          <el-col :span="isMobile ? 12 : 6" class="input-col">
            <el-input
                class="username_input"
                v-model="username"
                placeholder="请输入用户名"
                :trigger-on-focus="false"
                style="width: 100%"></el-input>
          </el-col>
          <el-col :span="isMobile ? 12 : 6" class="input-col">
            <el-input
                class="username_input"
                v-model="room"
                placeholder="请输入房间号"
                :trigger-on-focus="false"
                :disabled="this.host"
                style="width: 100%"></el-input>
          </el-col>
        </el-row>
        <el-row type="flex" justify="center" align="middle" :gutter=20 class="button-row">
          <el-col :span="isMobile ? 12 : 6">
            <el-button type="primary" style="width: 100%" :disabled="this.gameover"
                       @click="initRoom()">
              创建房间
            </el-button>
          </el-col>
          <el-col :span="isMobile ? 12 : 6">
            <el-button type="primary" style="width: 100%" :disabled="this.gameover"
                       @click="joinRoom()">
              加入房间
            </el-button>
          </el-col>
        </el-row>
        <el-row type="flex" justify="center" align="middle" :gutter=20 class="button-row">
          <el-col :span="isMobile ? 12 : 6">
            <el-button v-if="(this.cur_room&&this.host)" :disabled="this.gameover"
                       type="primary"
                       style="width: 100%"
                       @click="initGame()">开始游戏
            </el-button>
          </el-col>
          <el-col :span="isMobile ? 12 : 6">
            <el-button
                v-if="this.cur_room&&this.host&&this.gameover||(this.times===this.settings.maxguess&&this.times2===this.settings.maxguess)"
                type="success" style="width: 100%"
                @click="RestartHostGame()">重新开始
            </el-button>
          </el-col>
        </el-row>
      </div>
    </el-main>
=======
		<div slot="footer" class="dialog-footer">
			<el-button type="primary" @click="authorVisble=false">确 定</el-button>
		</div>
		</el-dialog>

		<!-- 多人模式说明 -->
		<el-dialog
		title="多人模式测试说明"
		:visible.sync="dialogVisble"
		:width="isMobile ? '90%' : '50%'"
		:show-close=false
		custom-class="enhanced-dialog">
			<div class="intro-content">
				<p>此界面为双人对战模式的测试版本：</p>
				<p>双方进行有时限的猜题，在一定次数内最先猜出答案者获胜。</p>
				<p>由于版本测试中，可能会出现许多意料之外的bug。</p>
				<p>此时可以点击右上方找到作者进行反馈，祝您游玩愉快。</p>
				<p>（移动端UI适配尚未制作）</p>
			</div>
			<span slot="footer" class="dialog-footer">
						<el-button type="primary" @click="dialogVisble=false">确 定</el-button>
            </span>
      </el-dialog>
    </el-header>
    <el-container>
      <el-aside width="30%">
        <el-row type="flex" justify="center" align="middle">
			<el-col :span="isMobile ? 18 : 12" class="input-col">
                <el-autocomplete
                    class="inline-input"
                    v-model="username"
                    :fetch-suggestions="querySearch"
                    placeholder="请选择一个宝可梦作为用户名"
                    :trigger-on-focus="false"
                    popper-class="autocomplete-dropdown"
                    style="width: 100%"
					:disabled="this.gameover||this.cur_room||this.host">
				</el-autocomplete>
			</el-col>
        </el-row>
        <el-row type="flex" justify="center" align="middle" class="button-row">
			<el-col :span="isMobile ? 12 : 6">
				<el-button type="primary" style="width: 100%" :disabled="this.gameover||this.cur_room||this.host"
						@click="initRoom()">
				创建房间
				</el-button>
			</el-col>
        </el-row>
		<br>
        <el-row type="flex" justify="center" align="middle">
			<el-col :span="isMobile ? 18 : 12" class="input-col">
				<el-input
					v-model="room"
					placeholder="请输入房间号"
					:trigger-on-focus="false"
					:disabled="this.cur_room!=''"
					style="width: 100%"></el-input>
			</el-col>
		</el-row>
        <el-row type="flex" justify="center" align="middle" class="button-row">
			<el-col :span="isMobile ? 12 : 6">
				<el-button type="primary" style="width: 100%" :disabled="this.gameover||this.cur_room||this.host"
						@click="joinRoom()">
					加入房间
				</el-button>
			</el-col>
			<!-- <el-col :span="isMobile ? 12 : 6">
				<el-button type="success" style="width: 100%"
						@click="toClipboard()">
					复制房间号
				</el-button>
			</el-col> -->
        </el-row>
		
		<!-- 进入房间后才显示的 -->
		<div v-if="this.cur_room">
			<el-row type="flex" justify="center" align="middle">
				<el-col :span="12" class="input-container">
					<div class="player-box">
						<el-image style="width: 80px; height: 80px" :src="this.userimg" fit="contain"></el-image>
						<div class="pokemon-name">
							<el-tag>P1</el-tag>
							{{ this.username }}
						</div>
					  </div>
				</el-col>
				<el-col :span="12" class="input-container">
					<div class="player-box">
						<el-image style="width: 80px; height: 80px" :src="this.userimg2" fit="contain"></el-image>
						<div class="pokemon-name">
							<el-tag type="success">P2</el-tag>
							{{ this.username2==""?"等待玩家中":this.username2 }}
						</div>
					  </div>
				</el-col>
			</el-row>
			<el-row type="flex" justify="center" align="middle" class="button-row">
				<el-col :span="isMobile ? 12 : 6">
					<el-button :disabled="this.gameover"
							type="primary"
							style="width: 100%"
							@click="initGame()"
							v-if="(this.cur_room&&this.host)">
							开始游戏
					</el-button>	
				</el-col>
			</el-row>
			<el-row type="flex" justify="center" align="middle" class="button-row">
				<el-col :span="isMobile ? 12 : 6">
					<el-button :disabled="this.gameover"
							type="danger"
							style="width: 100%"
							@click="leaveRoom()">
							离开房间
					</el-button>	
				</el-col>
			</el-row>
		</div>
      </el-aside>

	  <!-- 设置部分 -->
      <el-main>
        <div class="guess">
          <div class="setting">
            <div class="setting-section">
              <div class="setting-title">游戏模式</div>
              <el-select v-model="settings.hardid" placeholder="请选择" size="small" style="width: 50%"
                        @change="updateSetting" :disabled="!this.cur_room||!this.host">
                <el-option
                    v-for="item in this.hards"
                    :key="item"
                    :label="item"
                    :value="item"
                >
                </el-option>
              </el-select>
            </div>
            <div v-if="!this.host||!this.cur_room" class="setting-section">
              <div class="setting-title">世代选择</div>
              <div class="gen-selection">
                <div class="gen-checkboxes">
                  <el-checkbox
                      v-for="(gen, index) in genOptions"
                      :key="gen.value"
                      v-model="settings.selectedGens[index]"
                      @change="updateSetting">
                    {{ gen.label }}
                  </el-checkbox>
                </div>
              </div>
            </div>
            <div v-if="this.cur_room&&this.host" class="setting-section">
              <div class="setting-title">世代选择</div>
              <div class="gen-selection">
                <div class="gen-checkboxes">
                  <el-checkbox
                      v-for="(gen, index) in genOptions"
                      :key="gen.value"
                      v-model="settings.selectedGens[index]"
                      @change="updateSetting">
                    {{ gen.label }}
                  </el-checkbox>
                </div>
              </div>
            </div>

            <div class="setting-section">
              <div class="setting-title">显示信息</div>
              <div class="switch-group">
                <el-switch
                    v-model="settings.battleOpen"
                    active-text="显示更多种族值信息"
                    @change="updateSetting"
                    :disabled="!this.cur_room||!this.host"
                >
                </el-switch>
                <el-switch
                    v-model="settings.shapeOpen"
                    active-text="显示更多外形信息"
                    @change="updateSetting"
                    :disabled="!this.cur_room||!this.host"
                >
                </el-switch>
                <el-switch
                    v-model="settings.catchOpen"
                    active-text="显示蛋组/捕获率信息"
                    @change="updateSetting"
                    :disabled="!this.cur_room||!this.host"
                >
                </el-switch>
                <el-switch
                    v-model="settings.showGenArrow"
                    active-text="开启世代箭头"
                    @change="updateSetting"
                    :disabled="!this.cur_room||!this.host"
                >
                </el-switch>
              </div>
            </div>

            <br>

            <div class="block">
              <span class="demonstration">猜测次数：{{ this.settings.maxguess }}</span>
              <el-slider
                  v-model="settings.maxguess"
                  :step="1"
                  :max="15"
                  :min="3"
                  :show-tooltip="false"
                  style="width: 100%"
                  @change="updateSetting"
                  :disabled="!this.cur_room||!this.host"
              >
              </el-slider>
            </div>
          </div>
        </div>
      </el-main>
    </el-container>
>>>>>>> master
  </el-container>
</template>

<script>
import axios from 'axios'
import io from 'socket.io-client';
import {v4 as uuidv4} from 'uuid';
import {ref} from "vue";


export default {
<<<<<<< HEAD
  data() {
    var username = ""
    var username2 = ""
    var room = ""
    var host = false
    var socket = io(process.env.VUE_APP_API_BASE_URL);
    if ("username" in this.$route.params)
      username = this.$route.params.username
    if ("username2" in this.$route.params)
      username2 = this.$route.params.username2
    if ("room" in this.$route.params)
      room = this.$route.params.room
    if ("socket" in this.$route.params)
      socket = this.$route.params.socket
    if ("host" in this.$route.params)
      host = this.$route.params.host
    return {
      input: "",
      socket: socket,
      username: username,
      username2: username2,
      room: room,
      cur_room: room,
      authorVisble: false,
      tempdata: null,
      nameList: [],
      tableData: [],
      tableData2: [],
      temp: {},
      temp2: {},
      reply: {},
      times: 0,
      times2: 0,
      host: host,
      gameover: false,
      settingVisble: false,
      introVisble: false,
      genid: "全世代",
      hards: ["普通模式", "简单模式"],
      surrendered: false, // 新增：是否投降标记
      gens: ["全世代", "第一世代（红/黄/蓝/绿）", "第二世代（金/银）", "第三世代（红宝石/蓝宝石/绿宝石/火红/叶绿）", "第四世代（珍珠/钻石/白金/心金/魂银）", "第五世代（黑/白/黑2/白2）", "第六世代（X/Y/欧米伽红宝石/阿尔法蓝宝石）", "第七世代（日/月/究极之日/究极之月）", "第八世代（剑/盾）", "第九世代（朱/紫）"],
      genOptions: [
        {label: '第一世代（红/黄/蓝/绿）', value: 1, range: [0, 150]},  // 0001-0151
        {label: '第二世代（金/银）', value: 2, range: [151, 250]}, // 0152-0251
        {label: '第三世代（红宝石/蓝宝石/绿宝石/火红/叶绿）', value: 3, range: [251, 385]}, // 0252-0386
        {label: '第四世代（珍珠/钻石/白金/心金/魂银）', value: 4, range: [386, 492]}, // 0387-0493
        {label: '第五世代（黑/白/黑2/白2）', value: 5, range: [493, 648]}, // 0494-0649
        {label: '第六世代（X/Y/欧米伽红宝石/阿尔法蓝宝石）', value: 6, range: [649, 720]}, // 0650-0721
        {label: '第七世代（日/月/究极之日/究极之月）', value: 7, range: [721, 808]}, // 0722-0809
        {label: '第八世代（剑/盾）', value: 8, range: [809, 904]}, // 0810-0905
        {label: '第九世代（朱/紫）', value: 9, range: [905, 1024]} // 0906-1025
      ],
      maxguess: 10,
      settings: {
        hardid: "普通模式",
        genid: "全世代", // 保留以兼容旧数据
        selectedGens: [true, true, true, true, true, true, true, true, true], // 默认全选
        maxguess: 10,
        autodif: true,
        battleOpen: false,
        shapeOpen: false,
        catchOpen: false,
        showGenArrow: false,
        reverseDisplay: false,
        cheatOpen: false,
        baseGuessCount: 10  // 基础猜测次数
      },
      windowWidth: window.innerWidth,
      isMobile: window.innerWidth <= 768
    }

  },
  methods: {
    async initRoom() {
      this.username2 = ""
      this.times = 0
      this.times2 = 0
      this.gameover = false
      if (this.username === "") {
        this.$notify({
          title: '错误',
          message: '请输入用户名',
          type: "error"
        });
        return
      }
      if (this.cur_room !== "")
        this.socket.emit("leave", {"username": this.username, "host": this.host, "room": this.cur_room})
      this.room = ref(uuidv4())
      const username = this.username;
      this.socket.emit("join", {
        "username": username, "room": this.room, "action": "init", "hardid": this.settings.hardid,
        "selectedGens": this.settings.selectedGens,
        "battleOpen": this.settings.battleOpen,
        "shapeOpen": this.settings.shapeOpen,
        "catchOpen": this.settings.catchOpen,
        "showGenArrow": this.settings.showGenArrow,
        "cheatOpen": this.settings.cheatOpen,
        "reverseDisplay": this.settings.reverseDisplay,
        "maxGuess": this.settings.maxguess,
      });
      this.$notify({
        title: '成功',
        message: '创建房间成功',
        type: "success"
      });
    },
    async initGame() {
      if (this.username2 === "") {
        this.$notify({
          title: '失败',
          message: '游戏人数不足',
          type: "error"
        });
        return
      }
      const room_settings = {
        "hardid": this.settings.hardid,
        "selectedGens": this.settings.selectedGens,
        "battleOpen": this.settings.battleOpen,
        "shapeOpen": this.settings.shapeOpen,
        "catchOpen": this.settings.catchOpen,
        "showGenArrow": this.settings.showGenArrow,
        "cheatOpen": this.settings.cheatOpen,
        "reverseDisplay": this.settings.reverseDisplay,
        "maxGuess": this.settings.maxguess,
      }
      var gen = 10;
      for (let i = 0; i < 9; i++)
        if (this.settings.selectedGens[i]) gen += (1 << i);
      const dif = this.hards.indexOf(this.settings.hardid);
      this.socket.emit("room_game_init", {
        "difficulty": dif,
        "gen": gen,
        "room": this.room
      })
      if (!this.$route.path.includes("dualGuess")) {
        this.$router.push({
          name: 'dualGuess',
          params: {
            'room': this.cur_room,
            'host': this.host,
            'username': this.username,
            'username2': this.username2,
            'socket': this.socket,
            "settings": room_settings
          }
        })
      }
    },
    async joinRoom() {
      if (this.username === "") {
        this.$notify({
          title: '错误',
          message: '请输入用户名',
          type: "error"
        });
        return
      }
      if (this.cur_room !== "")
        this.socket.emit("leave", {"username": this.username, "host": this.host, "room": this.cur_room})
      try {
        const options = {
          method: 'GET',
          url: `${process.env.VUE_APP_API_BASE_URL}/findroom`,
          params: {room: this.room},
          responseType: 'json'
        };
        await axios.request(options).then((response) => {
              if (response.data.message !== "success") {
                this.$notify({
                  title: "错误",
                  message: response.data.message,
                  type: "error"
                });
              } else {
                const username = this.username;
                this.socket.emit("join", {"username": username, "room": this.room, "action": "join"});
                this.$notify({
                  title: '成功',
                  message: '加入房间成功',
                  type: "success"
                });
              }
            }
        ).catch(function (error) {
          console.error(error);
        });
      } catch
          (error) {
        console.error('寻找房间失败:', error);
      }

    }
    ,
    async updateSetting() {
      this.socket.emit("handle_config", {
        "hardid": this.settings.hardid,
        "selectedGens": this.settings.selectedGens,
        "battleOpen": this.settings.battleOpen,
        "shapeOpen": this.settings.shapeOpen,
        "catchOpen": this.settings.catchOpen,
        "showGenArrow": this.settings.showGenArrow,
        "cheatOpen": this.settings.cheatOpen,
        "reverseDisplay": this.settings.reverseDisplay,
        "maxGuess": this.settings.maxguess,
        "room": this.cur_room
      })
    },
    // 重构猜测次数计算逻辑
    updateGuessNumber() {
      //自动调整模式，不做任何改变
      if (!this.settings.autodif) return;

      // 基础猜测次数，默认为10
      let guessCount = 10;

      // 根据显示的信息数量调整难度
      if (this.settings.battleOpen) guessCount -= 2; // 显示战斗信息减2次
      if (this.settings.shapeOpen) guessCount -= 1; // 显示外形信息减1次
      if (this.settings.catchOpen) guessCount -= 1; // 显示捕获信息减1次

      // 根据选择的世代数量调整
      // 如果少于9个世代被选中，每少选一个世代减少1次猜测
      const missedGens = 9 - this.selectedGenCount;
      guessCount -= missedGens;

      // 确保猜测次数不低于3
      this.settings.maxguess = Math.max(3, guessCount);

      console.log("自动调整猜测次数为:", this.settings.maxguess);
    },
    handleBeforeUnload(event) {
      this.socket.emit("leave", {"username": this.username, "host": this.host, "room": this.cur_room})
    }
  },
  computed: {},
  mounted() {
    window.addEventListener('beforeunload', this.handleBeforeUnload)
    this.socket.on("join_event", (data) => {
      if (data.message === "host") {
        this.host = true
        this.cur_room = data.room
      }
      if (data.message === "join") {
        this.cur_room = data.room
        if (this.host === true) {
          this.username2 = data.username
          this.$notify({
            title: '参加',
            message: this.username2 + ' 加入房间',
            type: "success"
          });
        } else
          this.username2 = data.hostname

      }
    })
    this.socket.on("start_guess", (data) => {
      if (data.message === "success") {
        this.times = 0
        this.times2 = 0
        this.gameover = false
        const room_settings = {
          "hardid": this.settings.hardid,
          "selectedGens": this.settings.selectedGens,
          "battleOpen": this.settings.battleOpen,
          "shapeOpen": this.settings.shapeOpen,
          "catchOpen": this.settings.catchOpen,
          "showGenArrow": this.settings.showGenArrow,
          "cheatOpen": this.settings.cheatOpen,
          "reverseDisplay": this.settings.reverseDisplay,
          "maxGuess": this.settings.maxguess,
        }
        console.log(room_settings)
        if (!this.host && !this.$route.path.includes('dualGuess')) {
          this.$router.push({
            name: 'dualGuess',
            params: {
              'room': this.cur_room,
              'host': this.host,
              'username': this.username,
              'username2': this.username2,
              'socket': this.socket,
              'settings': room_settings
            }
          })
        }
      }
    })
    this.socket.on("leave_event", (data) => {
      if (data.host === true) {
        this.room = ""
        this.cur_room = ""
        this.username2 = ""
        this.times = 0
        this.times2 = 0
        this.gameover = false
        this.settings.battleOpen = false
      } else {
        this.username2 = ""
        this.times = 0
        this.times2 = 0
        this.gameover = false
        this.settings.battleOpen = false
      }
    })
    this.socket.on("setting_event", (data) => {
      console.log(data)
      if (!this.host) {
        {
          this.settings.hardid = data["hardid"]
          this.settings.selectedGens = data["selectedGens"]
          this.settings.battleOpen = data["battleOpen"]
          this.settings.shapeOpen = data["shapeOpen"]
          this.settings.catchOpen = data["catchOpen"]
          this.settings.showGenArrow = data["showGenArrow"]
          this.settings.cheatOpen = data["cheatOpen"]
          this.settings.reverseDisplay = data["reverseDisplay"]
          this.settings.maxguess = data["maxGuess"]
        }
      }
    })
  }
}
</script>

<style>
.guess {
  margin-top: 20px;
  margin-left: 5%;
  margin-right: 5%;
}

.enhanced-dialog .el-dialog__header {
  background-color: #f5f7fa !important;
  border-bottom: 1px solid #e4e7ed !important;
  padding: 15px 20px !important;
}

.enhanced-dialog .el-dialog__title {
  font-weight: 600 !important;
  color: #303133 !important;
}

.enhanced-dialog .el-dialog__body {
  padding: 20px !important;
}

/* 重要：确保弹窗底部按钮居中 */
.enhanced-dialog .el-dialog__footer {
  text-align: center !important;
  border-top: 1px solid #e4e7ed !important;
  padding: 15px 20px !important;
}

.enhanced-dialog .dialog-footer {
  width: 100% !important;
  text-align: center !important;
}

.enhanced-dialog .dialog-footer .el-button {
  min-width: 120px !important;
  margin: 0 !important;
}

/* 设置分区样式 */
.setting {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.setting-section {
  border-bottom: 1px dashed #EBEEF5;
  padding-bottom: 15px;
}

.setting-section:last-child {
  border-bottom: none;
  padding-bottom: 0;
}

.setting-title {
  font-weight: 600;
  color: #303133;
  margin-bottom: 10px;
}

.switch-group {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

/* 规则介绍样式 */
.intro-content {
  line-height: 1.6;
}

.hint-section {
  background-color: #f5f7fa;
  border-radius: 4px;
  padding: 12px 15px;
  margin: 15px 0;
}

.hint-item {
  display: flex;
  align-items: center;
  margin-bottom: 8px;
}

.hint-item:last-child {
  margin-bottom: 0;
}

.hint-item .el-tag {
  margin-right: 10px;
}

/* 世代选择样式 */
.gen-selection {
  margin: 10px 0;
}

.gen-checkboxes {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-top: 8px;
}

/* 输入区域相关样式调整 */
.input-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  max-width: 1200px;
  margin: 0 auto 20px;
  position: relative; /* 确保容器有相对定位，以便子元素绝对定位 */
}

/* 自动完成输入框包装器 */
.autocomplete-wrapper {
  position: relative;
  width: 100%;
  margin-bottom: 60px; /* 增加下方空间，确保下拉列表不会覆盖按钮 */
}

/* 输入行样式 */
.input-row {
  width: 100%;
  margin-bottom: 10px;
  position: relative;
  z-index: 10; /* 确保输入框在较高层级 */
}

/* 按钮行样式 */
.button-row {
  width: 100%;
  margin-top: 10px;
  position: relative;
  z-index: 5; /* 按钮在下拉菜单下方，但仍然可点击 */
}


.desktop-section .section-title {
  font-size: 14px;
  margin-bottom: 10px;
  border-bottom: 1px dashed #EBEEF5;
  padding-bottom: 5px;
  white-space: nowrap;
}

.desktop-section .section-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
}

.el-button span {
  display: inline-flex;
  align-items: center;
  justify-content: center;
}

/* 优化头部按钮 */
.header-buttons {
  display: flex;
  justify-content: flex-end;
  margin-bottom: 10px;
}

.header-buttons .el-button {
  margin-left: 10px;
}


/* 移动端适配 */
@media screen and (max-width: 768px) {
  .guess {
    margin-left: 2%;
    margin-right: 2%;
  }

  .setting-section {
    padding-bottom: 12px;
  }

  /* 移动端世代复选框优化 */
  .gen-checkboxes {
    flex-direction: column;
    gap: 5px;
  }

}

/* 覆盖Element UI可能的默认对齐 */
.result-dialog .el-message-box__btns button:nth-child(2) {
  margin-left: 0 !important;
}


.dialog-footer {
  display: flex !important;
  justify-content: center !important;
  width: 100% !important;
}


/* 确保按钮在移动端仍然可见和可点击 */
@media screen and (max-width: 768px) {
  .button-row {
    margin-top: 15px;
    z-index: 20; /* 在移动端提高按钮层级 */
  }
}

/* 移动端按钮样式优化 */
@media screen and (max-width: 768px) {
  .button-row {
    flex-wrap: wrap; /* 允许按钮换行，避免挤压 */
    gap: 10px; /* 增加按钮间距 */
  }

  /* 确保按钮文字居中且不被截断 */
  .el-button span {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 100%;
    height: 100%;
    text-align: center;
  }
}
</style>
=======
	data() {
		var username = ""
		var username2 = ""
		var room = ""
		var host = false
		var socket = io(process.env.VUE_APP_API_BASE_URL);
		if ("username" in this.$route.params){
			username = this.$route.params.username
			const id1=nameKey.indexOf(this.username)
			this.userimg=`https://pokedata.archknowledge.com.cn/i/pokemon/${id1+1}.png`;
		}
		if ("username2" in this.$route.params){
			username2 = this.$route.params.username2
			const id2=nameKey.indexOf(this.username2)
			this.userimg2=`https://pokedata.archknowledge.com.cn/i/pokemon/${id2+1}.png`;
		}
		if ("room" in this.$route.params)
			room = this.$route.params.room
		if ("socket" in this.$route.params)
			socket = this.$route.params.socket
		if ("host" in this.$route.params)
			host = this.$route.params.host
		return {
			input: "",
			socket: socket,
			username: username,
			username2: username2,
			userimg:"",
			userimg2:"",
			room: room,
			cur_room: room,
			authorVisble: false,
			dialogVisble: true,
			tempdata: null,
			nameList: [],
			tableData: [],
			tableData2: [],
			temp: {},
			temp2: {},
			reply: {},
			times: 0,
			times2: 0,
			host: host,
			gameover: false,
			settingVisble: false,
			introVisble: false,
			genid: "全世代",
			hards: ["普通模式", "简单模式"],
			surrendered: false, // 新增：是否投降标记
			gens: ["全世代", "第一世代（红/黄/蓝/绿）", "第二世代（金/银）", "第三世代（红宝石/蓝宝石/绿宝石/火红/叶绿）", "第四世代（珍珠/钻石/白金/心金/魂银）", "第五世代（黑/白/黑2/白2）", "第六世代（X/Y/欧米伽红宝石/阿尔法蓝宝石）", "第七世代（日/月/究极之日/究极之月）", "第八世代（剑/盾）", "第九世代（朱/紫）"],
			genOptions: [
				{label: '第一世代（红/黄/蓝/绿）', value: 1, range: [0, 150]},  // 0001-0151
				{label: '第二世代（金/银）', value: 2, range: [151, 250]}, // 0152-0251
				{label: '第三世代（红宝石/蓝宝石/绿宝石/火红/叶绿）', value: 3, range: [251, 385]}, // 0252-0386
				{label: '第四世代（珍珠/钻石/白金/心金/魂银）', value: 4, range: [386, 492]}, // 0387-0493
				{label: '第五世代（黑/白/黑2/白2）', value: 5, range: [493, 648]}, // 0494-0649
				{label: '第六世代（X/Y/欧米伽红宝石/阿尔法蓝宝石）', value: 6, range: [649, 720]}, // 0650-0721
				{label: '第七世代（日/月/究极之日/究极之月）', value: 7, range: [721, 808]}, // 0722-0809
				{label: '第八世代（剑/盾）', value: 8, range: [809, 904]}, // 0810-0905
				{label: '第九世代（朱/紫）', value: 9, range: [905, 1024]} // 0906-1025
			],
			maxguess: 10,
			settings: {
				hardid: "普通模式",
				genid: "全世代", // 保留以兼容旧数据
				selectedGens: [true, true, true, true, true, true, true, true, true], // 默认全选
				maxguess: 10,
				autodif: true,
				battleOpen: false,
				shapeOpen: false,
				catchOpen: false,
				showGenArrow: false,
				reverseDisplay: true,
				cheatOpen: false,
				baseGuessCount: 10  // 基础猜测次数
			},
			windowWidth: window.innerWidth,
			isMobile: window.innerWidth <= 768,
			darkMode: false,
		}

	},
	methods: {
		generateNumericRoomId() {
			// 生成4组4位数字
			const part1 = Math.floor(1000 + Math.random() * 9000); // 1000-9999
			const part2 = Math.floor(1000 + Math.random() * 9000);
			const part3 = Math.floor(1000 + Math.random() * 9000);
			
			// 组合成 XXXX-XXXX-XXXX 格式
			return `${part1}-${part2}-${part3}`;
		},
		toClipboard(){
			navigator.clipboard.writeText(this.room)
		},
		// 新增：加载夜间模式偏好
		loadDarkModePreference() {
			try {
				const savedMode = localStorage.getItem('darkMode');
				if (savedMode !== null) {
				this.darkMode = JSON.parse(savedMode);
				this.applyDarkMode();
				}
			} catch (e) {
				console.error("加载夜间模式偏好失败:", e);
			}
		},
		toggleDarkMode() {
			this.darkMode = !this.darkMode;
			this.applyDarkMode();
			this.saveDarkModePreference();
			},

			// 新增：应用夜间模式
			applyDarkMode() {
			if (this.darkMode) {
				document.body.classList.add('dark-mode');
			} else {
				document.body.classList.remove('dark-mode');
			}
		},
		async loadName() {
			try {
				this.tempdata = require(`@/assets/json/WordInfo.json`);
				this.nameList = this.tempdata.map(item => ({value: item}));
				console.log("名称列表加载成功");
			} catch (error) {
				console.error("加载名称失败:", error);
				// 如果本地加载失败，尝试通过API获取
				try {
				const options = {
					method: 'GET',
					url: `${process.env.VUE_APP_API_BASE_URL}/nameget`
				};
				await axios.request(options).then((response) => {
					this.tempdata = response.data;
					this.nameList = this.tempdata.map(item => ({value: item}));
				}).catch(function (error) {
					console.error("API获取名称失败:", error);
				});
				} catch (apiError) {
					console.error("API获取名称失败:", apiError);
				}
			}
			return;
		},
		async createFilter(queryString) {
			if (this.nameList.length === 0) {
				await this.loadName();
			}
			const query = queryString.toLowerCase();

			return (item) => {
				const target = (item.value || '').toLowerCase();
				let qIndex = 0, tIndex = 0;

				while (qIndex < query.length && tIndex < target.length) {
				if (query[qIndex] === target[tIndex]) qIndex++;
				tIndex++;
				}
				return qIndex === query.length;
			};
		},
		querySearch(queryString, cb) {
			Promise.resolve(this.createFilter(queryString)).then(filter => {
				const results = queryString
					? this.nameList.filter(filter)
					: this.nameList;
				cb(results);
			}).catch(err => {
				console.error('Filter error:', err);
				cb([]);
			});
		},
		async initRoom() {
			this.username2 = ""
			this.times = 0
			this.times2 = 0
			this.gameover = false
			const nameKey=this.nameList.map(item=>item.value)
			const id=nameKey.indexOf(this.username)
			if (this.username === "" || id==-1) {
				this.$notify({
				title: '错误',
				message: '用户名错误',
				type: "error"
				});
				return
			}
			if (this.cur_room !== "")
				this.socket.emit("leave", {"username": this.username, "host": this.host, "room": this.cur_room})
			this.room = ref(this.generateNumericRoomId())
			const username = this.username;
			this.socket.emit("join", {
				"username": username,
				"room": this.room,
				"action": "init",
				"hardid": this.settings.hardid,
				"selectedGens": this.settings.selectedGens,
				"battleOpen": this.settings.battleOpen,
				"shapeOpen": this.settings.shapeOpen,
				"catchOpen": this.settings.catchOpen,
				"showGenArrow": this.settings.showGenArrow,
				"cheatOpen": this.settings.cheatOpen,
				"reverseDisplay": this.settings.reverseDisplay,
				"maxGuess": this.settings.maxguess,
			});
			this.userimg=`https://pokedata.archknowledge.com.cn/i/pokemon/${id+1}.png`;
			this.$notify({
				title: '成功',
				message: '创建房间成功',
				type: "success"
			});
		},
		async initGame() {
			if (this.username2 === "") {
				this.$notify({
				title: '失败',
				message: '游戏人数不足',
				type: "error"
				});
			return
			}
			const room_settings = {
				"hardid": this.settings.hardid,
				"selectedGens": this.settings.selectedGens,
				"battleOpen": this.settings.battleOpen,
				"shapeOpen": this.settings.shapeOpen,
				"catchOpen": this.settings.catchOpen,
				"showGenArrow": this.settings.showGenArrow,
				"cheatOpen": this.settings.cheatOpen,
				"reverseDisplay": this.settings.reverseDisplay,
				"maxGuess": this.settings.maxguess,
			}
			var gen = 10;
			for (let i = 0; i < 9; i++)
				if (this.settings.selectedGens[i]) gen += (1 << i);
			const dif = this.hards.indexOf(this.settings.hardid);
			this.socket.emit("room_game_init", {
				"difficulty": dif,
				"gen": gen,
				"room": this.room
			})
			if (!this.$route.path.includes("dualGuess")) {
				this.$router.push({
				name: 'dualGuess',
				params: {
					'room': this.cur_room,
					'host': this.host,
					'username': this.username,
					'username2': this.username2,
					'socket': this.socket,
					"settings": room_settings
				}
				})
			}
		},
		async leaveRoom(){
			if(this.cur_room!=="")
				this.socket.emit("leave", {"username": this.username, "host": this.host, "room": this.cur_room})
			this.username2=""
			this.room=this.cur_room=""
			this.host=false
		},
		async joinRoom() {
			if (this.username === "") {
				this.$notify({
				title: '错误',
				message: '请输入用户名',
				type: "error"
				});
				return
			}
			const nameKey=this.nameList.map(item=>item.value)
			const id=nameKey.indexOf(this.username)
			if(id==-1){
				this.$notify({
				title: '错误',
				message: '请以一个宝可梦名字作为用户名',
				type: "error"
				});
				return
			}
			if (this.cur_room !== "")
				this.socket.emit("leave", {"username": this.username, "host": this.host, "room": this.cur_room})
			try {
				const options = {
				method: 'GET',
				url: `${process.env.VUE_APP_API_BASE_URL}/findroom`,
				params: {room: this.room},
				responseType: 'json'
				};
				await axios.request(options).then((response) => {
					if (response.data.message !== "success") {
						this.$notify({
						title: "错误",
						message: response.data.message,
						type: "error"
						});
					} else {
						const username = this.username;
						this.socket.emit("join", {"username": username, "room": this.room, "action": "join"});
						this.$notify({
							title: '成功',
							message: '加入房间成功',
							type: "success"
						});
					}
					}
				).catch(function (error) {
					console.error(error);
				});
			} catch
				(error) {
				console.error('寻找房间失败:', error);
			}
		}
		,
		async updateSetting() {
			this.socket.emit("handle_config", {
				"hardid": this.settings.hardid,
				"selectedGens": this.settings.selectedGens,
				"battleOpen": this.settings.battleOpen,
				"shapeOpen": this.settings.shapeOpen,
				"catchOpen": this.settings.catchOpen,
				"showGenArrow": this.settings.showGenArrow,
				"cheatOpen": this.settings.cheatOpen,
				"reverseDisplay": this.settings.reverseDisplay,
				"maxGuess": this.settings.maxguess,
				"room": this.cur_room
			})
		},
		// 重构猜测次数计算逻辑
		updateGuessNumber() {
			//自动调整模式，不做任何改变
			if (!this.settings.autodif) return;

			// 基础猜测次数，默认为10
			let guessCount = 10;

			// 根据显示的信息数量调整难度
			if (this.settings.battleOpen) guessCount -= 2; // 显示战斗信息减2次
			if (this.settings.shapeOpen) guessCount -= 1; // 显示外形信息减1次
			if (this.settings.catchOpen) guessCount -= 1; // 显示捕获信息减1次

			// 根据选择的世代数量调整
			// 如果少于9个世代被选中，每少选一个世代减少1次猜测
			const missedGens = 9 - this.selectedGenCount;
			guessCount -= missedGens;

			// 确保猜测次数不低于3
			this.settings.maxguess = Math.max(3, guessCount);

			console.log("自动调整猜测次数为:", this.settings.maxguess);
		},
		handleBeforeUnload(event) {
			console.log("关闭连接");
			this.socket.emit("leave", {"username": this.username, "host": this.host, "room": this.room})
			this.socket.close(1000,'Closing normally');
		},
	},
	computed: {},
	beforeUnmount(){
    	window.removeEventListener('beforeunload', this.handleBeforeUnload);
	},
	mounted() {
		this.userimg=this.userimg2=require("@/assets/img/Ditto.png")
		window.addEventListener('beforeunload', this.handleBeforeUnload);
		this.socket.on("join_event", (data) => {
			if (data.message === "host") {
				this.host = true
				this.cur_room = data.room
			}
			if (data.message === "join") {
				this.cur_room = data.room
				console.log(data)
				if(data.hostname===this.username && this.host===false){
					this.leaveRoom()
					this.$notify({
						title: '离开',
						message: '与房主重名',
						type: "error"
					});
				}
				else{
					if (this.host === true) {
						this.username2 = data.username
						this.$notify({
							title: '参加',
							message: this.username2 + ' 加入房间',
							type: "success"
						});
					} 
					else this.username2 = data.hostname
					const nameKey=this.nameList.map(item=>item.value)
					const id1=nameKey.indexOf(this.username)
					this.userimg=`https://pokedata.archknowledge.com.cn/i/pokemon/${id1+1}.png`;
					const id2=nameKey.indexOf(this.username2)
					this.userimg2=`https://pokedata.archknowledge.com.cn/i/pokemon/${id2+1}.png`;
				}
			}
		})
		this.socket.on("start_guess", (data) => {
		if (data.message === "success") {
			this.times = 0
			this.times2 = 0
			this.gameover = false
			const room_settings = {
			"hardid": this.settings.hardid,
			"selectedGens": this.settings.selectedGens,
			"battleOpen": this.settings.battleOpen,
			"shapeOpen": this.settings.shapeOpen,
			"catchOpen": this.settings.catchOpen,
			"showGenArrow": this.settings.showGenArrow,
			"cheatOpen": this.settings.cheatOpen,
			"reverseDisplay": this.settings.reverseDisplay,
			"maxGuess": this.settings.maxguess,
			}
			console.log(room_settings)
			if (!this.host && !this.$route.path.includes('dualGuess')) {
			this.$router.push({
				name: 'dualGuess',
				params: {
				'room': this.cur_room,
				'host': this.host,
				'username': this.username,
				'username2': this.username2,
				'socket': this.socket,
				'settings': room_settings
				}
			})
			}
		}
		})
		this.socket.on("leave_event", (data) => {
			if (data.host === true) {
				this.room = ""
				this.cur_room = ""
				this.username2 = ""
				this.userimg2 = require("@/assets/img/Ditto.png")
				this.times = 0
				this.times2 = 0
				this.gameover = false
				this.settings.battleOpen = false
			} else {
				this.username2 = ""
				this.userimg2 = require("@/assets/img/Ditto.png")
				this.times = 0
				this.times2 = 0
				this.gameover = false
				this.settings.battleOpen = false
			}
		})
		this.socket.on("setting_event", (data) => {
		console.log(data)
		if (!this.host) {
			{
			this.settings.hardid = data["hardid"]
			this.settings.selectedGens = data["selectedGens"]
			this.settings.battleOpen = data["battleOpen"]
			this.settings.shapeOpen = data["shapeOpen"]
			this.settings.catchOpen = data["catchOpen"]
			this.settings.showGenArrow = data["showGenArrow"]
			this.settings.cheatOpen = data["cheatOpen"]
			this.settings.reverseDisplay = data["reverseDisplay"]
			this.settings.maxguess = data["maxGuess"]
			}
		}
		})
	}
}
</script>

<style src="../assets/css/guess.css"></style>
>>>>>>> master
