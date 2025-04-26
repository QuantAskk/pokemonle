<template>
	<el-container>
		<el-header>
			<el-row type="flex" justify="space-between" align="middle">
				<el-col :span="24" style="text-align: right;">
				<div class="header-buttons">
					<span class="game-type">房间号：{{ this.$route.params.room }}    </span>
					<el-button circle icon="el-icon-question" @click="introVisble=true"></el-button>
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
		</el-header>
		<el-main>
			<div class="guess">
				<!-- 统一居中的输入区域 -->
				<div class="input-container">
					<el-row type="flex" justify="center" align="middle" class="input-row">
						<el-col :span="isMobile ? 24 : 12" class="input-col">
							<el-autocomplete
							  class="inline-input"
							  v-model="input"
							  :fetch-suggestions="querySearch"
							  placeholder="请输入宝可梦名称"
							  :trigger-on-focus="false"
							  popper-class="autocomplete-dropdown"
							  style="width: 100%"></el-autocomplete>
						</el-col>
					</el-row>
					<el-row type="flex" justify="center" align="middle" class="input-row">
						<div style="width: 50%;">
							<el-progress :percentage="this.countdown/(this.settings.maxguess*12)*100" :format="countdownFormat"></el-progress>
						</div>
					</el-row>
					<!-- 增加按钮与输入框之间的间距 -->
					<el-row type="flex" justify="center" align="middle" class="button-row">
						<el-col v-if="!this.gameover" :span="isMobile ? 16 : 8" class="button-col">
							<el-button type="primary" class="action-button" :disabled="this.mygameover||!this.isReply"
										@click="Guess()">
								{{ this.mygameover ? '已结束' : '确定' }}
							</el-button>
						</el-col>
						<el-col v-if="this.host&&this.gameover" :span="isMobile ? 16 : 8" class="button-col">
							<el-button type="success" class="action-button" :disabled="!this.gameover"
								@click="RestartHostGame" v-if="!this.roundover">开始下一轮
							</el-button>
							<el-button type="success" class="action-button" :disabled="!this.gameover"
								@click="leaveRoomToHead" v-if="this.roundover">返回主页
							</el-button>
						</el-col>
						<el-col v-if="!this.host&&this.gameover" :span="isMobile ? 16 : 8" class="button-col">
							<el-button type="success" class="action-button" :disabled="true"
								v-if="!this.roundover">等待房主开启下一轮
							</el-button>
							<el-button type="success" class="action-button" :disabled="!this.gameover"
								@click="leaveRoomToHead" v-if="this.roundover">返回主页
							</el-button>
						</el-col>
					</el-row>
				</div>
				<el-row >
					<!-- 玩家1桌面端卡片水平布局 -->
					<el-col :span="16">
						<div class="score">
							<el-steps :active="this.score" finish-status="success">
								<el-step></el-step>
								<el-step></el-step>
								<el-step></el-step>
							</el-steps>
						</div>
						<div class="times">
							{{ this.username }} 猜测次数：{{ this.times }}/{{ this.settings.maxguess }}
						</div>
						<div class="pokemon-cards desktop-cards">
							<div v-for="(item, index) in (()=>displayedItems(this.tableData))()" :key="index"
								class="pokemon-card desktop-card">
								<div class="card-header">
									<div class="pokemon-image">
										<el-image style="width: 60px; height: 60px" :src="item.imgUrl" fit="contain"></el-image>
									</div>
									<div class="pokemon-name">{{ item.name }}</div>
								</div>
								<div class="desktop-card-content">
									<div class="desktop-section">
										<div class="section-title">属性</div>
										<div class="section-content">
											<el-tag v-for="(type, idx) in item.type" :key="'type-'+idx"
													size="small" :type="type.col" class="info-tag">
											{{ type.key }}
											</el-tag>
										</div>
									</div>

									<div class="desktop-section">
										<div class="section-title">种族值</div>
										<div class="section-content">
											<div>
												<el-tag size="small" :type="item.pow.col" class="info-tag">
													{{ ValueText(item.pow.key, item.pow.value) }}
												</el-tag>
												<el-tag size="small" :type="item.speed.col" class="info-tag" v-if="settings.battleOpen">
													速度:{{ ValueText(item.speed.key, item.speed.value) }}
												</el-tag>
											</div>
										</div>
									</div>

									<div v-if="settings.battleOpen" class="desktop-section">
										<div class="section-title">攻防</div>
										<div class="section-content">
											<el-tag size="small" :type="item.attack.col" class="info-tag">
											{{ item.attack.key }}
											</el-tag>
											<el-tag size="small" :type="item.defense.col" class="info-tag">
											{{ item.defense.key }}
											</el-tag>
										</div>
									</div>

									<div class="desktop-section">
										<div class="section-title">世代</div>
										<div class="section-content">
											<el-tag size="small" :type="item.gen.col" class="info-tag">
											{{ settings.showGenArrow ? ValueText(item.gen.key, item.gen.value) : item.gen.key }}
											</el-tag>
										</div>
									</div>

									<div class="desktop-section">
										<div class="section-title">特性</div>
										<div class="section-content">
											<el-tag v-for="(ability, idx) in item.ability" :key="'ability-'+idx"
													size="small" :type="ability.col" class="info-tag">
											{{ ability.key }}
											</el-tag>
										</div>
									</div>

									<div class="desktop-section">
										<div class="section-title">进化</div>
										<div class="section-content">
											<div>
												<el-tag v-if="item.evo.key != null" size="small" :type="item.evo.col" class="info-tag">
													{{ item.evo.key }}
												</el-tag>
												<el-tag size="small" :type="item.stage.col" class="info-tag">
													{{ item.stage.key }}
												</el-tag>
											</div>
										</div>
									</div>

									<div v-if="settings.shapeOpen" class="desktop-section">
										<div class="section-title">外形</div>
										<div class="section-content">
											<el-tag size="small" :type="item.shape.col" class="info-tag">
											{{ item.shape.key }}
											</el-tag>
											<el-tag size="small" :type="item.col.col" class="info-tag">
											{{ item.col.key }}
											</el-tag>
										</div>
									</div>

									<div v-if="settings.catchOpen" class="desktop-section">
										<div class="section-title">蛋组</div>
										<div class="section-content">
											<el-tag v-for="(egg, idx) in item.egg" :key="'egg-'+idx"
													size="small" :type="egg.col" class="info-tag">
											{{ egg.key }}
											</el-tag>
											<el-tag size="small" :type="item.catrate.col" class="info-tag">
											捕获率:{{ ValueText(item.catrate.key, item.catrate.value) }}
											</el-tag>
										</div>
									</div>

									<div class="desktop-section">
										<div class="section-title">其他</div>
										<div class="section-content">
											<el-tag v-for="(label, idx) in item.label" :key="'label-'+idx"
													size="small" :type="label.col" class="info-tag">
												{{ label.key }}
											</el-tag>
										</div>
									</div>
								</div>
							</div>
						</div>
					</el-col>

					<!-- 对手桌面端卡片水平布局 -->
					<el-col :span="7" :offset="1">
						<div class="score">
							<el-steps :active="this.score2" finish-status="success">
								<el-step></el-step>
								<el-step></el-step>
								<el-step></el-step>
							</el-steps>
						</div>
						<div class="times">
							{{ this.username2 }} 猜测次数：{{ this.times2 }}/{{ this.settings.maxguess }}
						</div>
						<div class="pokemon-cards p2-desktop-cards">
							<div v-for="(item, index) in (()=>displayedItems(tableData2))()" :key="index"
								class="pokemon-card p2-desktop-card">
								<div class="p2-desktop-card-content">
									<div class="p2-desktop-section">
										<div class="section-title">属性</div>
										<div class="section-content">
											<el-tag v-for="(type, idx) in item.type" :key="'type-'+idx"
													size="small" :type="type.col" class="info-tag" effect="dark">
											</el-tag>
										</div>
									</div>

									<div class="p2-desktop-section">
										<div class="section-title">种族值</div>
										<div class="section-content">
											<div>
											<el-tag size="small" :type="item.pow.col" class="info-tag" effect="dark"></el-tag>
											<el-tag v-if="settings.battleOpen" size="small" :type="item.speed.col" class="info-tag" effect="dark"></el-tag>
											</div>
										</div>
									</div>

									<div v-if="settings.battleOpen" class="p2-desktop-section">
										<div class="section-title">攻防</div>
										<div class="section-content">
											<el-tag size="small" :type="item.attack.col" class="info-tag" effect="dark"></el-tag>
											<el-tag size="small" :type="item.defense.col" class="info-tag" effect="dark"></el-tag>
										</div>
									</div>

									<div class="p2-desktop-section">
										<div class="section-title">世代</div>
										<div class="section-content">
											<el-tag size="small" :type="item.gen.col" class="info-tag" effect="dark"></el-tag>
										</div>
									</div>

									<div class="p2-desktop-section">
										<div class="section-title">特性</div>
										<div class="section-content">
											<el-tag v-for="(ability, idx) in item.ability" :key="'ability-'+idx"
													size="small" :type="ability.col" class="info-tag" effect="dark"></el-tag>
										</div>
									</div>

									<div class="p2-desktop-section">
										<div class="section-title">进化</div>
										<div class="section-content">
											<div>
												<el-tag v-if="item.evo.key != null" size="small" :type="item.evo.col" class="info-tag" effect="dark"></el-tag>
												<el-tag size="small" :type="item.stage.col" class="info-tag" effect="dark"></el-tag>
											</div>
										</div>
									</div>

									<div v-if="settings.shapeOpen" class="p2-desktop-section">
										<div class="section-title">外形</div>
										<div class="section-content">
											<el-tag size="small" :type="item.shape.col" class="info-tag" effect="dark"></el-tag>
											<el-tag size="small" :type="item.col.col" class="info-tag" effect="dark"></el-tag>
										</div>
									</div>

									<div v-if="settings.catchOpen" class="p2-desktop-section">
										<div class="section-title">蛋组</div>
										<div class="section-content">
											<el-tag v-for="(egg, idx) in item.egg" :key="'egg-'+idx"
													size="small" :type="egg.col" class="info-tag" effect="dark"></el-tag>
											<el-tag size="small" :type="item.catrate.col" class="info-tag" effect="dark"></el-tag>
										</div>
									</div>

									<div class="p2-desktop-section">
										<div class="section-title">其他</div>
										<div class="section-content">
											<el-tag v-for="(label, idx) in item.label" :key="'label-'+idx"
													size="small" :type="label.col" class="info-tag" effect="dark"></el-tag>
										</div>
									</div>
								</div>
							</div>
						</div>
					</el-col>
				</el-row>
			</div>
		</el-main>
	</el-container>
	</template>

	<script>
	import axios from 'axios'

	function truncateString(str, maxLength) {
	if (str.length > maxLength) {
		return str.slice(0, maxLength) + '...';
	}
	return str;
	}

	export default {
	data() {
		return {
			input: "",
			username: this.$route.params.username,
			username2: this.$route.params.username2,
			room: this.$route.params.room,
			tempdata: null,
			nameList: [],
			socket: this.$route.params.socket,
			tableData: [],
			tableData2: [],
			temp: {},
			temp2: {},
			reply: {},
			times: 0,
			times2: 0,
			score: 0,
			score2: 0,
			countdown: 0,
			timer: null,
			winner: 0,
			host: this.$route.params.host,
			gameover: false,
			mygameover: false,
			roundover: false,
			introVisble: false,
			hards: ["普通模式", "简单模式"],
			settings: {
				selectedGens: this.$route.params.settings.selectedGens,
				hardid: this.$route.params.settings.hardid,
				maxguess: this.$route.params.settings.maxGuess,
				battleOpen: this.$route.params.settings.battleOpen,
				shapeOpen: this.$route.params.settings.shapeOpen,
				catchOpen: this.$route.params.settings.catchOpen,
				showGenArrow: this.$route.params.settings.showGenArrow,
				cheatOpen: this.$route.params.settings.cheatOpen,
				reverseDisplay: this.$route.params.settings.reverseDisplay, // 控制卡片展示顺序
			},
			windowWidth: window.innerWidth,
			isMobile: window.innerWidth <= 768,
			useGitHubImages: true,
			isReply: true
		}
	},
	methods: {
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
		async initGame() {
			this.winner=0
			if (this.username2 === "") {
				this.$notify({
				title: '失败',
				message: '游戏人数不足',
				type: "error"
				});
				return
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
				await this.$router.push({
				name: 'dualGuess',
				params: {
					'room': this.room,
					'host': this.host,
					'username': this.username,
					'username2': this.username2,
					'socket': socket
				}
				})
			}
		},
		async RestartHostGame() {
			this.initGame()
		},
		async Guess() {
			try {
				const options = {
					method: 'GET',
					url: `${process.env.VUE_APP_API_BASE_URL}/guessDual`,
					params: {
						guess: this.input,
						room: this.room,
					}
				};
				this.isReply=false;
				await axios.request(options).then((response) => {
					this.tempdata = response.data;
				}).catch(function (error) {
					console.error(error);
					this.isReply=true;
				});
				const data = this.tempdata;
				if (data == "guess name error") {
					this.isReply=true;
					this.$notify({
						title: '提交错误',
						message: '不存在的宝可梦',
						type: "error"
					});
				} else {
					this.temp = {};

					this.temp.name = data.name;
					this.temp.answer = data.answer;

					// 属性
					this.temp.type = [];
					data.type.forEach((type, index) => {
						if (type.key != "无") {
						if (type.value == 'True')
							this.temp.type.push({key: type.key, col: "success"});
						else
							this.temp.type.push({key: type.key, col: "info"});
						}
					});

					// 种族值
					this.temp.pow = {};
					this.temp.pow.key = data.pow.key;
					this.temp.pow.value = data.pow.value;
					if (data.pow.value == "equiv")
						this.temp.pow.col = "success";
					else if (data.pow.dis == "far")
						this.temp.pow.col = "info";
					else
						this.temp.pow.col = "warning";

					// 速度
					this.temp.speed = {};
					this.temp.speed.key = data.speed.key;
					this.temp.speed.value = data.speed.value;
					if (data.speed.value == "equiv")
						this.temp.speed.col = "success";
					else if (data.speed.dis == "far")
						this.temp.speed.col = "info";
					else
						this.temp.speed.col = "warning";

					// 物特
					this.temp.attack = {};
					this.temp.attack.key = data.attack.key;
					this.temp.attack.value = data.attack.value;
					if (data.attack.value == 'True')
						this.temp.attack.col = "success";
					else
						this.temp.attack.col = "info";

					this.temp.defense = {};
					this.temp.defense.key = data.defense.key;
					this.temp.defense.value = data.defense.value;
					if (data.defense.value == 'True')
						this.temp.defense.col = "success";
					else
						this.temp.defense.col = "info";

					// 世代
					this.temp.gen = {};
					this.temp.gen.key = data.gen.key;
					this.temp.gen.value = data.gen.value;
					if (data.gen.value == 'equiv')
						this.temp.gen.col = "success";
					else if (data.gen.dis == 'far')
						this.temp.gen.col = "info";
					else this.temp.gen.col = "warning";

					// 特性
					this.temp.ability = [];
					data.ability.forEach((ability, index) => {
						if (ability.value == 'True')
						this.temp.ability.push({key: ability.key, col: "success"});
						else
						this.temp.ability.push({key: ability.key, col: "info"});
					});

					// 进化方式
					this.temp.evo = {};
					this.temp.evo.key = data.evo.key;
					if (this.temp.evo.key != null)
						this.temp.evo.key = truncateString(this.temp.evo.key, this.isMobile ? 6 : 12);
					if (data.evo.value == "far")
						this.temp.evo.col = "info";
					else if (data.evo.value == "near")
						this.temp.evo.col = "warning";
					else
						this.temp.evo.col = "success";

					// 阶段
					this.temp.stage = {};
					this.temp.stage.key = data.stage.key;
					this.temp.stage.value = data.stage.value;
					if (data.stage.value == 'True')
						this.temp.stage.col = "success";
					else
						this.temp.stage.col = "info";

					// 蛋组
					this.temp.egg = [];
					data.egg.forEach((egg, index) => {
						if (egg.value == 'True')
						this.temp.egg.push({key: egg.key, col: "success"});
						else
						this.temp.egg.push({key: egg.key, col: "info"});
					});

					// 捕获率
					this.temp.catrate = {};
					this.temp.catrate.key = data.catrate.key;
					this.temp.catrate.value = data.catrate.value;
					if (data.catrate.value == "equiv")
						this.temp.catrate.col = "success";
					else
						this.temp.catrate.col = "info";

					// 外形
					this.temp.shape = {};
					this.temp.shape.key = data.shape.key;
					this.temp.shape.value = data.shape.value;
					if (data.shape.value == 'True')
						this.temp.shape.col = "success";
					else
						this.temp.shape.col = "info";

					this.temp.col = {};
					this.temp.col.key = data.col.key;
					this.temp.col.value = data.col.value;
					if (data.col.value == 'True')
						this.temp.col.col = "success";
					else
						this.temp.col.col = "info";

					// 其他标签
					this.temp.label = [];
					data.label.forEach((label, index) => {
						if (label.value == 'True') {
						this.temp.label.push({key: label.key, col: "success"});
						} else if (label.similarity === "similar") {
						// 相似形态，标黄
						this.temp.label.push({key: label.key, col: "warning"});
						} else {
						this.temp.label.push({key: label.key, col: "info"});
						}
					});

					// 获取图片 - 使用开发者配置的图片源
					await this.loadPokemonImage(data, this.temp);

					// 清空输入框
					this.tableData.push(this.temp);
					this.times++;
					this.input = "";

					// 猜测结束
					if (this.times === this.settings.maxguess)
						this.mygameover = true
					if (this.times === this.settings.maxguess && this.times2 === this.settings.maxguess) {
						this.gameover = true
					}

					this.socket.emit("submit_answer", {"data": this.temp, "username": this.username, "room": this.room})
				}
			} catch (error) {
				console.error(error);
			}
		},
		async loadPokemonImage(data, tempObj) {
			try {
				if (this.useGitHubImages) {
				// 使用GitHub图片
				const id = parseInt(data.index);
				if (!isNaN(id)) {
					const githubUrl = `https://pokedata.archknowledge.com.cn/i/pokemon/${id}.png`;
					tempObj.imgUrl = githubUrl;

					// 检查图片是否可访问
					const imgCheck = new Image();
					imgCheck.onerror = async () => {
					console.log("GitHub图片加载失败，尝试使用API");
					tempObj.imgUrl = `https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/${id}.png`;
					};
					imgCheck.src = githubUrl;
				} else {
					console.warn("无效的宝可梦ID:", data.index);
					await this.loadApiImage(data.name, tempObj);
				}
				} else {
				// 直接使用API图片
				await this.loadApiImage(data.name, tempObj);
				}
			} catch (error) {
				console.error("图片加载错误:", error);
				// 设置默认图片或错误占位图
				//tempObj.imgUrl = require("@/assets/img/pokemon-placeholder.png");
			}
		},

		// API图片加载方法
		async loadApiImage(pokemonName, tempObj) {
			// try {
			// 	const options = {
			// 	method: 'GET',
			// 	url: `${process.env.VUE_APP_API_BASE_URL}/getimage`,
			// 	params: {pokemon: pokemonName},
			// 	responseType: 'blob'
			// 	};
			// 	const response = await axios.request(options);
			// 	const blob = new Blob([response.data]);
			// 	tempObj.imgUrl = URL.createObjectURL(blob);
			// } catch (error) {
			// 	console.error('API图片获取失败:', error);
			// 	// 设置默认图片
			// 	//tempObj.imgUrl = require("@/assets/img/pokemon-placeholder.png");
			// }
		},

		ValueText(key, value) {
			if (value == 'high')
				return String(key) + "↑"
			if (value == 'low')
				return String(key) + "↓"
			return String(key)
		}
		,
		async ReplayAnswer() {
			clearInterval(this.timer);
            this.timer = null;
			if(this.winner===1)this.score++;
			if(this.winner===2)this.score2++;
			if(this.score===3)this.roundover=true;
			if(this.score2===3)this.roundover=true;
			try {
				const options = {
					method: 'GET',
					url: `${process.env.VUE_APP_API_BASE_URL}/getanswerDual`,
					params: {
						room: this.room,
					}
				};
				await axios.request(options).then((response) => {
					this.tempdata = response.data;
					}).catch(function (error) {
					console.error(error);
				});
				const data = this.tempdata;
				console.log(data);

				// 创建临时对象用于加载图片
				const tempImageObj = {};
				await this.loadPokemonImage(data, tempImageObj);
				this.temp.imgUrl = tempImageObj.imgUrl;

				this.reply.type = "";
				data.type.forEach((tmp, index) => {
					if (index != 0) this.reply.type += "+";
					this.reply.type += tmp.key;
				});

				this.reply.ability = "";
				data.ability.forEach((tmp, index) => {
					if (index != 0) this.reply.ability += ",";
					this.reply.ability += tmp.key;
				});

				this.reply.label = "";
				data.label.forEach((tmp, index) => {
					if (index != 0) this.reply.label += ",";
					this.reply.label += tmp.key;
				});
				if (this.reply.label == "")
					this.reply.label = "无";

				// 提取世代号，避免重复
				let genNumber = data.gen.key;
				if (genNumber.startsWith('第') && genNumber.endsWith('世代')) {
					genNumber = genNumber.substring(1, genNumber.length - 2);
				}

				const h = this.$createElement;

				const resultContent = h('div', {class: 'result-dialog-container'}, [
				h('div', {class: 'result-dialog-header'}, [
					h('div', {class: 'result-image-container'}, [
					h('img', {
						attrs: {
						src: this.temp.imgUrl,
						alt: data.name
						},
						class: 'result-pokemon-image'
					})
					]),
					h('div', {class: 'result-title-container'}, [
					h('h2', {class: 'result-pokemon-name'}, data.name),
					h('p', {class: 'result-pokemon-gen'}, `第${genNumber}世代`)
					])
				]),
				h('div', {class: 'result-info-compact'}, [
					h('div', {class: 'result-info-row'}, [
					h('span', {class: 'result-info-label'}, '属性:'),
					h('div', {class: 'result-info-tags'},
						data.type.filter(type => type.key !== "无").map(type =>
							h('el-tag', {
								props: {size: 'mini', type: 'success'},
								class: 'result-tag'
							}, type.key)
						)
					)
					]),
					h('div', {class: 'result-info-row'}, [
					h('span', {class: 'result-info-label'}, '种族值:'),
					h('span', {class: 'result-info-value'}, data.pow.key)
					]),
					h('div', {class: 'result-info-row'}, [
					h('span', {class: 'result-info-label'}, '特性:'),
					h('div', {class: 'result-info-tags'},
						data.ability.map(ability =>
							h('el-tag', {
								props: {size: 'mini', type: 'info'},
								class: 'result-tag'
							}, ability.key)
						)
					)
					])
				]),
				h('div', {class: 'result-stats'}, [
					h('p', {class: 'result-guess-count'},
						this.winner<=0 ?
							'大家都没有猜对！' :
							`${this.winner===1?this.username:this.username2} 用了 ${this.winner===1?this.times:this.times2} 次尝试猜出正确答案`)
					])
				]);

				let dialogTitle = '本轮结束';
				if (this.winner==-1)dialogTitle='时间到';
				if (this.winner > 0) {
					if(!this.roundover){
						if(this.winner === 1){
							if (this.times <= 3) {
								dialogTitle = '太厉害了，鼓掌👏👏👏';
							} else {
								dialogTitle = '恭喜你猜对了！';
							}
						}else{
							dialogTitle = '对手更快，要加油了哦！';
						}
					}else{
						if(this.score===3)dialogTitle = '获胜了！鼓掌👏👏👏';
						if(this.score2===3)dialogTitle = '输掉了~再接再厉吧！'
					}
				}

				this.$alert(resultContent, dialogTitle, {
					customClass: 'result-dialog',
					dangerouslyUseHTMLString: true,
					center: true,
					showClose: false,
					closeOnClickModal: false,
					closeOnPressEscape: false,
					distinguishCancelAndClose: true,
				});
			} catch (error) {
				console.error(error);
			}
		},
		// 开始计时
		countdownStart(){
			if(this.timer!=null){
				clearInterval(this.timer);
				this.timer=null;
			}
			this.countdown=this.settings.maxguess*12;
			this.timer=setInterval(()=>{
				this.countdown-=1;
				if(this.countdown==0){
					this.winner=-1;
					this.gameover = true
					this.ReplayAnswer()
				}
			},1000);
		},
		countdownFormat(percentage){
			return `本轮剩余 ${this.countdown} 秒`;
		},
		displayedItems(curData) {
			return this.settings.reverseDisplay ? curData.slice().reverse() : curData;
		},
		handleBeforeUnload(event) {
			console.log("关闭连接");
			if(this.timer!=null){
				clearInterval(this.timer);
			}
			this.socket.emit("leave", {"username": this.username, "host": this.host, "room": this.room})
			this.socket.close(1000,'Closing normally');
		},
		async leaveRoomToHead(){
			this.socket.emit("leave", {"username": this.username, "host": this.host, "room": this.room})
			this.socket.close(1000,'Closing normally');
			await this.$router.push('/Guess')
		}
	},
	computed: {},
	beforeUnmount() {
    	window.removeEventListener('beforeunload', this.handleBeforeUnload);
 	},
	mounted() {
		this.$notify({
			title: '成功',
			message: '游戏开始',
			type: "success"
		});
		this.countdownStart()
		this.loadName();
		window.addEventListener('beforeunload', this.handleBeforeUnload)
		this.socket.on("start_guess", (data) => {
			if (data.message === "success") {
				this.$notify({
					title: '注意',
					message: '新的一轮已经开始',
					type: "warning"
				});
				this.times = 0
				this.times2 = 0
				this.gameover = false
				this.mygameover = false
				this.tableData = []
				this.tableData2 = []
				this.countdownStart()

				if (!this.host && !this.$route.path.includes('dualGuess')) {
				this.$router.push({
					name: 'dualGuess',
					params: {
						'room': this.room,
						'host': this.host,
						'username': this.username,
						'username2': this.username2,
						'socket': socket
					}
				})
				}
			}
		})
		this.socket.on("answer_result", (data) => {
			if (data.username === this.username2) {
				this.tableData2.push(data.result);
				this.times2++;
			}
			if(data.username===this.username)this.isReply=true;
			if (data.message === "success") {
				this.gameover = true
				if(data.username === this.username)this.winner=1;
				else this.winner = 2;
				this.ReplayAnswer()
			}
			else if (this.times2 === this.settings.maxguess && this.times === this.settings.maxguess) {
				this.gameover = true
				this.winner = 0;
				this.ReplayAnswer()
			}
		})
		this.socket.on("leave_event", (data) => {
			if (data.host === true) {
				if (!this.$route.path.includes('dualCreate')) {
					this.$router.push({
						name: 'dualCreate',
						params: {
							'room': this.room,
							'host': this.host,
							'username': this.username,
							'username2': this.username2,
							'socket': this.socket
						}
					})
				}
				this.$notify({
					title: '提示',
					message: '房间已解散',
					type: "info"
				});
			} else {
				if (!this.$route.path.includes('dualCreate')) {
					this.$router.push({
						name: 'dualCreate',
						params: {
							'room': this.room,
							'host': this.host,
							'username': this.username,
							'username2': this.username2,
							'socket': this.socket
						}
					})
				}
				this.$notify({
					title: '提示',
					message: data.username + '已离开房间',
					type: "info"
				});
			}
			this.leaveRoomToHead();
		})
	}
}
</script>

<style src="../assets/css/guess.css"></style>
