<template>
	<el-container>
		<el-header>
			<el-row type="flex" justify="space-between" align="middle">
				<el-col :span="24" style="text-align: right">
					<div class="header-buttons">
						<el-button
							circle
							icon="el-icon-setting"
							@click="settingVisble = true"
						></el-button>
						<el-button
							circle
							icon="el-icon-question"
							@click="introVisble = true"
						></el-button>
						<el-link
							:underline="false"
							href="https://github.com/QuantAskk/pokemonle"
							style="margin-left: 10px"
						>
							<el-button circle icon="el-icon-user"></el-button>
						</el-link>
					</div>
				</el-col>
			</el-row>

			<!-- 设置对话框 -->
			<el-dialog
				title="设置"
				:visible.sync="settingVisble"
				:width="isMobile ? '90%' : '50%'"
				:show-close="false"
				:close-on-click-modal="false"
				:close-on-press-escape="false"
				custom-class="enhanced-dialog"
			>
				<div class="setting">
					<div class="setting-section">
						<div class="setting-title">游戏模式</div>
						<el-select
							v-model="settings.hardid"
							placeholder="请选择"
							size="small"
							style="width: 50%"
						>
							<el-option
								v-for="item in this.hards"
								:key="item"
								:label="item"
								:value="item"
							>
							</el-option>
						</el-select>
					</div>

					<div class="setting-section">
						<div class="setting-title">世代选择</div>
						<div class="gen-selection">
							<div class="gen-checkboxes">
								<el-checkbox
									v-for="(gen, index) in genOptions"
									:key="gen.value"
									v-model="settings.selectedGens[index]"
									@change="handleGenChange(index)"
								>
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
								@change="updateGuessNumber"
							>
							</el-switch>
							<el-switch
								v-model="settings.shapeOpen"
								active-text="显示更多外形信息"
								@change="updateGuessNumber"
							>
							</el-switch>
							<el-switch
								v-model="settings.catchOpen"
								active-text="显示蛋组/捕获率信息"
								@change="updateGuessNumber"
							>
							</el-switch>
						</div>
					</div>

					<div class="setting-section">
						<div class="setting-title">猜测次数调整</div>
						<el-switch
							v-model="settings.autodif"
							active-text="自动调整"
							inactive-text="手动调整"
							@change="updateGuessNumber"
						>
						</el-switch>
						<div class="block">
							<span class="demonstration"
								>猜测次数：{{ this.settings.maxguess }}</span
							>
							<el-slider
								v-model="settings.maxguess"
								:step="1"
								:max="20"
								:min="3"
								:disabled="this.settings.autodif"
								style="width: 100%"
							>
							</el-slider>
						</div>
					</div>
				</div>

				<div slot="footer" class="dialog-footer">
					<el-button type="primary" @click="CloseSetting()">确 定</el-button>
				</div>
			</el-dialog>

			<!-- 规则介绍对话框 -->
			<el-dialog
				title="规则介绍"
				:visible.sync="introVisble"
				:width="isMobile ? '90%' : '50%'"
				:show-close="false"
				custom-class="enhanced-dialog"
			>
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
					<p>
						<strong>随机开局：</strong
						>帮你随机选择一个当前世代范围内的宝可梦作为第一次猜测。
					</p>
				</div>

				<div slot="footer" class="dialog-footer">
					<el-button type="primary" @click="introVisble = false"
						>确 定</el-button
					>
				</div>
			</el-dialog>
		</el-header>
		<el-main>
			<div class="guess">
				<!-- 修改：增加顶部间距并使用相对定位来确保下拉菜单不遮挡按钮 -->
				<div class="input-container">
					<el-row type="flex" justify="center" align="middle" class="input-row">
						<el-col :span="isMobile ? 24 : 16" class="input-col">
							<div class="autocomplete-wrapper">
								<el-autocomplete
									class="inline-input"
									v-model="input"
									:fetch-suggestions="querySearch"
									placeholder="请输入宝可梦名称"
									:trigger-on-focus="false"
									popper-class="autocomplete-dropdown"
									style="width: 100%"
								></el-autocomplete>
							</div>
						</el-col>
					</el-row>
					<!-- 增加按钮与输入框之间的间距 -->
					<el-row
						type="flex"
						justify="center"
						align="middle"
						:gutter="20"
						class="button-row"
					>
						<!-- 新增随机开局按钮 -->
						<el-col :span="isMobile ? 6 : 3" class="button-col">
							<el-button
								type="primary"
								class="action-button"
								:disabled="this.times > 0 || this.gameover"
								@click="RandomStart()"
								icon="el-icon-refresh-left"
							>
								随机开局
							</el-button>
						</el-col>
						<el-col :span="isMobile ? 6 : 3" class="button-col">
							<el-button
								type="primary"
								class="action-button"
								:disabled="this.gameover"
								@click="Guess()"
							>
								{{ this.gameover ? "已结束" : "确定" }}
							</el-button>
						</el-col>
						<el-col :span="isMobile ? 6 : 3" class="button-col">
							<el-button
								type="danger"
								class="action-button"
								:disabled="this.gameover"
								@click="Surrender()"
							>
								投降
							</el-button>
						</el-col>
						<el-col :span="isMobile ? 6 : 3" class="button-col">
							<el-button type="success" class="action-button" @click="Restart()"
								>重新开始</el-button
							>
						</el-col>
					</el-row>
				</div>

				<div class="times">
					猜测次数：{{ this.times }}/{{ this.settings.maxguess }}
				</div>

				<!-- 移动端卡片垂直布局 -->
				<div v-if="isMobile" class="pokemon-cards mobile-cards">
					<div
						v-for="(item, index) in tableData"
						:key="index"
						class="pokemon-card"
					>
						<div class="card-header">
							<div class="pokemon-image">
								<el-image
									style="width: 50px; height: 50px"
									:src="item.imgUrl"
									fit="contain"
								></el-image>
							</div>
							<div class="pokemon-name">{{ item.name }}</div>
						</div>

						<div class="card-section">
							<div class="section-title">属性</div>
							<div class="section-content">
								<el-tag
									v-for="(type, idx) in item.type"
									:key="'type-' + idx"
									size="mini"
									:type="type.col"
									class="info-tag"
								>
									{{ type.key }}
								</el-tag>
							</div>
						</div>

						<div class="card-section">
							<div class="section-title">种族值</div>
							<div class="section-content">
								<el-tag size="mini" :type="item.pow.col" class="info-tag">
									{{ ValueText(item.pow.key, item.pow.value) }}
								</el-tag>
								<el-tag
									v-if="settings.battleOpen"
									size="mini"
									:type="item.speed.col"
									class="info-tag"
								>
									速度:{{ ValueText(item.speed.key, item.speed.value) }}
								</el-tag>
							</div>
						</div>

						<div v-if="settings.battleOpen" class="card-section">
							<div class="section-title">攻防</div>
							<div class="section-content">
								<el-tag size="mini" :type="item.attack.col" class="info-tag">
									{{ item.attack.key }}
								</el-tag>
								<el-tag size="mini" :type="item.defense.col" class="info-tag">
									{{ item.defense.key }}
								</el-tag>
							</div>
						</div>

						<div class="card-section">
							<div class="section-title">世代</div>
							<div class="section-content">
								<el-tag size="mini" :type="item.gen.col" class="info-tag">
									{{ ValueText(item.gen.key, item.gen.value) }}
								</el-tag>
							</div>
						</div>

						<div class="card-section">
							<div class="section-title">特性</div>
							<div class="section-content">
								<el-tag
									v-for="(ability, idx) in item.ability"
									:key="'ability-' + idx"
									size="mini"
									:type="ability.col"
									class="info-tag"
								>
									{{ ability.key }}
								</el-tag>
							</div>
						</div>

						<div class="card-section">
							<div class="section-title">进化</div>
							<div class="section-content">
								<el-tag
									v-if="item.evo.key != null"
									size="mini"
									:type="item.evo.col"
									class="info-tag"
								>
									{{ item.evo.key }}
								</el-tag>
								<el-tag size="mini" :type="item.stage.col" class="info-tag">
									{{ item.stage.key }}
								</el-tag>
							</div>
						</div>

						<div v-if="settings.shapeOpen" class="card-section">
							<div class="section-title">外形</div>
							<div class="section-content">
								<el-tag size="mini" :type="item.shape.col" class="info-tag">
									{{ item.shape.key }}
								</el-tag>
								<el-tag size="mini" :type="item.col.col" class="info-tag">
									{{ item.col.key }}
								</el-tag>
							</div>
						</div>

						<div v-if="settings.catchOpen" class="card-section">
							<div class="section-title">蛋组/捕获率</div>
							<div class="section-content">
								<el-tag
									v-for="(egg, idx) in item.egg"
									:key="'egg-' + idx"
									size="mini"
									:type="egg.col"
									class="info-tag"
								>
									{{ egg.key }}
								</el-tag>
								<el-tag size="mini" :type="item.catrate.col" class="info-tag">
									捕获率:{{ ValueText(item.catrate.key, item.catrate.value) }}
								</el-tag>
							</div>
						</div>

						<div class="card-section">
							<div class="section-title">其他</div>
							<div class="section-content">
								<el-tag
									v-for="(label, idx) in item.label"
									:key="'label-' + idx"
									size="mini"
									:type="label.col"
									class="info-tag"
								>
									{{ label.key }}
								</el-tag>
							</div>
						</div>
					</div>
				</div>

				<!-- 桌面端卡片水平布局 - 修复布局 -->
				<div v-else class="pokemon-cards-container">
					<div class="pokemon-cards desktop-cards">
						<div
							v-for="(item, index) in tableData"
							:key="index"
							class="pokemon-card desktop-card"
						>
							<div class="card-header">
								<div class="pokemon-image">
									<el-image
										style="width: 60px; height: 60px"
										:src="item.imgUrl"
										fit="contain"
									></el-image>
								</div>
								<div class="pokemon-name">{{ item.name }}</div>
							</div>

							<div class="desktop-card-content">
								<div class="desktop-section">
									<div class="section-title">属性</div>
									<div class="section-content">
										<el-tag
											v-for="(type, idx) in item.type"
											:key="'type-' + idx"
											size="small"
											:type="type.col"
											class="info-tag"
										>
											{{ type.key }}
										</el-tag>
									</div>
								</div>

								<div class="desktop-section">
									<div class="section-title">种族值</div>
									<div class="section-content">
										<el-tag size="small" :type="item.pow.col" class="info-tag">
											{{ ValueText(item.pow.key, item.pow.value) }}
										</el-tag>
										<el-tag
											v-if="settings.battleOpen"
											size="small"
											:type="item.speed.col"
											class="info-tag"
										>
											速度:{{ ValueText(item.speed.key, item.speed.value) }}
										</el-tag>
									</div>
								</div>

								<div v-if="settings.battleOpen" class="desktop-section">
									<div class="section-title">攻防</div>
									<div class="section-content">
										<el-tag
											size="small"
											:type="item.attack.col"
											class="info-tag"
										>
											{{ item.attack.key }}
										</el-tag>
										<el-tag
											size="small"
											:type="item.defense.col"
											class="info-tag"
										>
											{{ item.defense.key }}
										</el-tag>
									</div>
								</div>

								<div class="desktop-section">
									<div class="section-title">世代</div>
									<div class="section-content">
										<el-tag size="small" :type="item.gen.col" class="info-tag">
											{{ ValueText(item.gen.key, item.gen.value) }}
										</el-tag>
									</div>
								</div>

								<div class="desktop-section">
									<div class="section-title">特性</div>
									<div class="section-content">
										<el-tag
											v-for="(ability, idx) in item.ability"
											:key="'ability-' + idx"
											size="small"
											:type="ability.col"
											class="info-tag"
										>
											{{ ability.key }}
										</el-tag>
									</div>
								</div>

								<div class="desktop-section">
									<div class="section-title">进化</div>
									<div class="section-content">
										<el-tag
											v-if="item.evo.key != null"
											size="small"
											:type="item.evo.col"
											class="info-tag"
										>
											{{ item.evo.key }}
										</el-tag>
										<el-tag
											size="small"
											:type="item.stage.col"
											class="info-tag"
										>
											{{ item.stage.key }}
										</el-tag>
									</div>
								</div>

								<div v-if="settings.shapeOpen" class="desktop-section">
									<div class="section-title">外形</div>
									<div class="section-content">
										<el-tag
											size="small"
											:type="item.shape.col"
											class="info-tag"
										>
											{{ item.shape.key }}
										</el-tag>
										<el-tag size="small" :type="item.col.col" class="info-tag">
											{{ item.col.key }}
										</el-tag>
									</div>
								</div>

								<div v-if="settings.catchOpen" class="desktop-section">
									<div class="section-title">蛋组/捕获率</div>
									<div class="section-content">
										<el-tag
											v-for="(egg, idx) in item.egg"
											:key="'egg-' + idx"
											size="small"
											:type="egg.col"
											class="info-tag"
										>
											{{ egg.key }}
										</el-tag>
										<el-tag
											size="small"
											:type="item.catrate.col"
											class="info-tag"
										>
											捕获率:{{
												ValueText(item.catrate.key, item.catrate.value)
											}}
										</el-tag>
									</div>
								</div>

								<div class="desktop-section">
									<div class="section-title">其他</div>
									<div class="section-content">
										<el-tag
											v-for="(label, idx) in item.label"
											:key="'label-' + idx"
											size="small"
											:type="label.col"
											class="info-tag"
										>
											{{ label.key }}
										</el-tag>
									</div>
								</div>
							</div>
						</div>
					</div>
				</div>
			</div>
		</el-main>
	</el-container>
</template>

<script>
import axios from "axios";
import { MessageBox } from "element-ui";

function truncateString(str, maxLength) {
	if (str.length > maxLength) {
		return str.slice(0, maxLength) + "...";
	}
	return str;
}

export default {
	data() {
		return {
			input: "",
			tempdata: null,
			nameList: [],
			tableData: [],
			temp: {},
			reply: {},
			times: 0,
			gameover: false,
			settingVisble: false,
			introVisble: false,
			surrendered: false, // 新增：是否投降标记
			gens: [
				"全世代",
				"第一世代（红/黄/蓝/绿）",
				"第二世代（金/银）",
				"第三世代（红宝石/蓝宝石/绿宝石/火红/叶绿）",
				"第四世代（珍珠/钻石/白金/心金/魂银）",
				"第五世代（黑/白/黑2/白2）",
				"第六世代（X/Y/欧米伽红宝石/阿尔法蓝宝石）",
				"第七世代（日/月/究极之日/究极之月）",
				"第八世代（剑/盾）",
				"第九世代（朱/紫）",
			],
			genOptions: [
				{ label: "第一世代（红/黄/蓝/绿）", value: 1, range: [0, 150] }, // 0001-0151
				{ label: "第二世代（金/银）", value: 2, range: [151, 250] }, // 0152-0251
				{
					label: "第三世代（红宝石/蓝宝石/绿宝石/火红/叶绿）",
					value: 3,
					range: [251, 385],
				}, // 0252-0386
				{
					label: "第四世代（珍珠/钻石/白金/心金/魂银）",
					value: 4,
					range: [386, 492],
				}, // 0387-0493
				{ label: "第五世代（黑/白/黑2/白2）", value: 5, range: [493, 648] }, // 0494-0649
				{
					label: "第六世代（X/Y/欧米伽红宝石/阿尔法蓝宝石）",
					value: 6,
					range: [649, 720],
				}, // 0650-0721
				{
					label: "第七世代（日/月/究极之日/究极之月）",
					value: 7,
					range: [721, 808],
				}, // 0722-0809
				{ label: "第八世代（剑/盾）", value: 8, range: [809, 904] }, // 0810-0905
				{ label: "第九世代（朱/紫）", value: 9, range: [905, 1024] }, // 0906-1025
			],
			hards: ["普通模式", "简单模式"],
			settings: {
				hardid: "普通模式",
				genid: "全世代", // 保留以兼容旧数据
				selectedGens: [true, true, true, true, true, true, true, true, true], // 默认全选
				maxguess: 10,
				autodif: true,
				battleOpen: false,
				shapeOpen: false,
				catchOpen: false,
				baseGuessCount: 10, // 基础猜测次数
			},
			currentAnswerId: null, // 存储当前答案的ID
			currentGen: null,
			windowWidth: window.innerWidth,
			isMobile: window.innerWidth <= 768,
		};
	},
	computed: {
		// 计算当前选择的世代索引
		selectedGenIndices() {
			// 获取所有选中的世代索引+1（因为API索引从1开始，第一世代对应索引1）
			return this.settings.selectedGens
				.map((selected, index) => (selected ? index + 1 : null))
				.filter((index) => index !== null);
		},

		// 判断当前选择的宝可梦ID是否在所选世代范围内
		isPokemonInSelectedGens() {
			// 如果没有选择任何世代，默认选择全世代
			if (this.selectedGenIndices.length === 0) {
				return true;
			}

			// 获取当前答案ID对应的宝可梦编号（假设从0开始）
			const pokemonId = this.currentAnswerId;
			if (pokemonId === null) {
				return true; // 如果没有答案ID，默认返回true
			}

			// 检查宝可梦ID是否在任何选定的世代范围内
			return this.settings.selectedGens.some((selected, index) => {
				if (!selected) return false;
				return this.currentGen == index;
				// const range = this.genOptions[index].range;
				// return pokemonId >= range[0] && pokemonId <= range[1];
			});
		},

		// 计算已选择的世代数量
		selectedGenCount() {
			return this.settings.selectedGens.filter((selected) => selected).length;
		},
	},
	methods: {
		async createFilter(queryString) {
			if (this.nameList.length === 0) {
				await this.loadName();
			}
			const query = queryString.toLowerCase();

			return (item) => {
				const target = (item.value || "").toLowerCase();
				let qIndex = 0,
					tIndex = 0;

				while (qIndex < query.length && tIndex < target.length) {
					if (query[qIndex] === target[tIndex]) qIndex++;
					tIndex++;
				}
				return qIndex === query.length;
			};
		},

		querySearch(queryString, cb) {
			Promise.resolve(this.createFilter(queryString))
				.then((filter) => {
					const results = queryString
						? this.nameList.filter(filter)
						: this.nameList;
					cb(results);
				})
				.catch((err) => {
					console.error("Filter error:", err);
					cb([]);
				});
		},
		async loadName() {
			try {
				const options = {
					method: "GET",
					url: `${process.env.VUE_APP_API_BASE_URL}/nameget`,
				};

				await axios
					.request(options)
					.then((response) => {
						this.tempdata = response.data;
					})
					.catch(function (error) {
						console.error(error);
					});

				this.nameList = this.tempdata.map((item) => ({ value: item }));
			} catch (error) {
				console.error("请求失败", error);
			}
		},
		async Restart() {
			this.times = 0;
			this.gameover = false;
			this.surrendered = false; // 重设投降标志
			sessionStorage.removeItem("answer");
			this.tableData = [];
			console.log(`${process.env.VUE_APP_API_BASE_URL}/initget`);

			// 更新猜测次数
			this.updateGuessNumber();

			try {
				// 如果没有选择任何世代，默认全部选择
				if (this.selectedGenIndices.length === 0) {
					this.settings.selectedGens = [
						true,
						true,
						true,
						true,
						true,
						true,
						true,
						true,
						true,
					];
				}

				// 随机选择一个已选世代的索引
				const randomIndex = Math.floor(
					Math.random() * this.selectedGenIndices.length
				);
				const genValue = this.selectedGenIndices[randomIndex];

				const dif = this.hards.indexOf(this.settings.hardid);
				const options = {
					method: "GET",
					url: `${process.env.VUE_APP_API_BASE_URL}/initget`,
					params: {
						difficulty: dif,
						gen: genValue,
					},
				};

				await axios
					.request(options)
					.then((response) => {
						this.tempdata = response.data;
						console.log(this.tempdata);

						// 存储答案ID
						this.storeAnswerId(this.tempdata);

						// 检查答案是否在选定的世代范围内
						if (!this.isPokemonInSelectedGens) {
							// 如果答案不在选定的世代范围内，重新启动
							console.log("答案不在选定的世代范围内，重新获取...");
							this.Restart();
							return;
						}
					})
					.catch(function (error) {
						console.error(error);
					});
				sessionStorage.setItem("answer", this.tempdata.ans);
			} catch (error) {
				console.error(error);
			}
		},
		// 新增：随机开局功能
		// 随机开局功能修正 - 前端实现
		async RandomStart() {
			// 确保游戏已经初始化并且是第一次猜测
			if (this.times > 0 || this.gameover) return;

			try {
				// 确保名称列表已加载
				if (this.nameList.length === 0) {
					await this.loadName();
				}

				// 如果没有选择任何世代，默认选择全部世代
				if (this.selectedGenIndices.length === 0) {
					this.settings.selectedGens = [
						true,
						true,
						true,
						true,
						true,
						true,
						true,
						true,
						true,
					];
				}

				// 从已选世代范围内筛选宝可梦
				const eligiblePokemon = [];

				// 为每个宝可梦分配一个预估的世代（简化处理）
				this.nameList.forEach((pokemon, index) => {
					// 使用索引来估算宝可梦的世代范围
					// 这里假设nameList是按照图鉴编号排序的
					const pokemonId = index;

					// 检查该宝可梦是否在任何选定的世代范围内
					const inSelectedGen = this.settings.selectedGens.some(
						(selected, genIndex) => {
							if (!selected) return false;

							return this.currentGen == genIndex;
							// const range = this.genOptions[genIndex].range;
							// return pokemonId >= range[0] && pokemonId <= range[1];
						}
					);

					if (inSelectedGen) {
						eligiblePokemon.push(pokemon.value);
					}
				});

				// 如果没有符合条件的宝可梦，则使用所有宝可梦
				const pokemonPool =
					eligiblePokemon.length > 0
						? eligiblePokemon
						: this.nameList.map((p) => p.value);

				// 随机选择一个宝可梦
				const randomIndex = Math.floor(Math.random() * pokemonPool.length);
				const randomPokemon = pokemonPool[randomIndex];

				// 设置输入框值并提交
				this.input = randomPokemon;

				// 自动提交猜测
				this.$nextTick(() => {
					this.Guess();
				});
			} catch (error) {
				console.error("随机开局错误:", error);
				this.$notify({
					title: "随机失败",
					message: "无法随机选择宝可梦，请手动输入",
					type: "warning",
				});
			}
		},

		// 从答案中提取宝可梦ID
		storeAnswerId(answer) {
			try {
				// 这里需要根据实际API返回的格式来提取ID
				// 假设API返回的是宝可梦的编号或者某种可以转换为ID的形式
				this.currentAnswerId = parseInt(answer.ans);
				this.currentGen = parseInt(answer.gen);
			} catch (error) {
				console.error("无法解析答案ID", error);
				this.currentAnswerId = null;
			}
		},
		// 新增：投降功能
		async Surrender() {
			if (this.gameover) return; // 如果游戏已结束，不执行投降

			this.surrendered = true; // 标记为已投降
			this.gameover = true; // 设置游戏为结束状态

			// 直接显示答案
			this.ReplayAnswer();
		},
		async Guess() {
			const answer = sessionStorage.getItem("answer");
			if (answer == null) return;
			try {
				const options = {
					method: "GET",
					url: `${process.env.VUE_APP_API_BASE_URL}/guess`,
					params: {
						answer: answer,
						guess: this.input,
					},
				};
				await axios
					.request(options)
					.then((response) => {
						this.tempdata = response.data;
					})
					.catch(function (error) {
						console.error(error);
					});

				const data = this.tempdata;
				if (data == "guess name error") {
					this.$notify({
						title: "提交错误",
						message: "不存在的宝可梦",
						type: "error",
					});
				} else {
					this.temp = {};

					this.temp.name = data.name;
					this.temp.answer = data.answer;

					// 属性
					this.temp.type = [];
					data.type.forEach((type, index) => {
						if (type.key != "无") {
							if (type.value == "True")
								this.temp.type.push({ key: type.key, col: "success" });
							else this.temp.type.push({ key: type.key, col: "info" });
						}
					});

					// 种族值
					this.temp.pow = {};
					this.temp.pow.key = data.pow.key;
					this.temp.pow.value = data.pow.value;
					if (data.pow.value == "equiv") this.temp.pow.col = "success";
					else if (data.pow.dis == "far") this.temp.pow.col = "info";
					else this.temp.pow.col = "warning";

					//速度
					this.temp.speed = {};
					this.temp.speed.key = data.speed.key;
					this.temp.speed.value = data.speed.value;
					if (data.speed.value == "equiv") this.temp.speed.col = "success";
					else if (data.speed.dis == "far") this.temp.speed.col = "info";
					else this.temp.speed.col = "warning";

					//物特
					this.temp.attack = {};
					this.temp.attack.key = data.attack.key;
					this.temp.attack.value = data.attack.value;
					if (data.attack.value == "True") this.temp.attack.col = "success";
					else this.temp.attack.col = "info";

					this.temp.defense = {};
					this.temp.defense.key = data.defense.key;
					this.temp.defense.value = data.defense.value;
					if (data.defense.value == "True") this.temp.defense.col = "success";
					else this.temp.defense.col = "info";

					// 世代
					this.temp.gen = {};
					this.temp.gen.key = data.gen.key;
					this.temp.gen.value = data.gen.value;
					if (data.gen.value == "equiv") this.temp.gen.col = "success";
					else this.temp.gen.col = "info";

					// 特性
					this.temp.ability = [];
					data.ability.forEach((ability, index) => {
						if (ability.value == "True")
							this.temp.ability.push({ key: ability.key, col: "success" });
						else this.temp.ability.push({ key: ability.key, col: "info" });
					});

					// 进化方式
					this.temp.evo = {};
					this.temp.evo.key = data.evo.key;
					if (this.temp.evo.key != null)
						this.temp.evo.key = truncateString(
							this.temp.evo.key,
							this.isMobile ? 6 : 12
						);
					if (data.evo.value == "far") this.temp.evo.col = "info";
					else if (data.evo.value == "near") this.temp.evo.col = "warning";
					else this.temp.evo.col = "success";

					// 阶段
					this.temp.stage = {};
					this.temp.stage.key = data.stage.key;
					this.temp.stage.value = data.stage.value;
					if (data.stage.value == "True") this.temp.stage.col = "success";
					else this.temp.stage.col = "info";

					//蛋组
					this.temp.egg = [];
					data.egg.forEach((egg, index) => {
						if (egg.value == "True")
							this.temp.egg.push({ key: egg.key, col: "success" });
						else this.temp.egg.push({ key: egg.key, col: "info" });
					});

					//捕获率
					this.temp.catrate = {};
					this.temp.catrate.key = data.catrate.key;
					this.temp.catrate.value = data.catrate.value;
					if (data.catrate.value == "equiv") this.temp.catrate.col = "success";
					else this.temp.catrate.col = "info";

					//外形
					this.temp.shape = {};
					this.temp.shape.key = data.shape.key;
					this.temp.shape.value = data.shape.value;
					if (data.shape.value == "True") this.temp.shape.col = "success";
					else this.temp.shape.col = "info";

					this.temp.col = {};
					this.temp.col.key = data.col.key;
					this.temp.col.value = data.col.value;
					if (data.col.value == "True") this.temp.col.col = "success";
					else this.temp.col.col = "info";

					// 其他标签
					this.temp.label = [];
					data.label.forEach((label, index) => {
						if (label.value == "True")
							this.temp.label.push({ key: label.key, col: "success" });
						else this.temp.label.push({ key: label.key, col: "info" });
					});

					console.log(this.temp);

					// 获取图片
					try {
						const options = {
							method: "GET",
							url: `${process.env.VUE_APP_API_BASE_URL}/getimage`,
							params: { pokemon: this.temp.name },
							responseType: "blob",
						};
						await axios
							.request(options)
							.then((response) => {
								this.tempdata = response.data;
							})
							.catch(function (error) {
								console.error(error);
							});
						const blob = new Blob([this.tempdata]);
						this.temp.imgUrl = URL.createObjectURL(blob);
					} catch (error) {
						console.error("图片获取失败:", error);
					}

					// 修改：将最新猜测的宝可梦插入到数组的开头，而不是末尾
					this.tableData.unshift(this.temp);
					this.times++;

					// 清空输入框
					this.input = "";

					// 猜测结束
					if (
						this.temp.answer == "True" ||
						this.times == this.settings.maxguess
					) {
						this.gameover = true;
						this.ReplayAnswer();
					}
				}
			} catch (error) {
				console.error(error);
			}
		},
		ValueText(key, value) {
			if (value == "high") return String(key) + "↑";
			if (value == "low") return String(key) + "↓";
			return String(key);
		},
		// 修改 ReplayAnswer 方法 - 添加了根据猜测次数显示不同祝贺信息
		async ReplayAnswer() {
			const answer = sessionStorage.getItem("answer");
			if (answer == null) return;
			try {
				const options = {
					method: "GET",
					url: `${process.env.VUE_APP_API_BASE_URL}/getanswer`,
					params: {
						pokemon: answer,
					},
				};
				await axios
					.request(options)
					.then((response) => {
						this.tempdata = response.data;
					})
					.catch(function (error) {
						console.error(error);
					});
				const data = this.tempdata;
				console.log(data);

				try {
					const options = {
						method: "GET",
						url: `${process.env.VUE_APP_API_BASE_URL}/getimage`,
						params: { pokemon: data.name },
						responseType: "blob",
					};
					await axios
						.request(options)
						.then((response) => {
							this.tempdata = response.data;
						})
						.catch(function (error) {
							console.error(error);
						});
					const blob = new Blob([this.tempdata]);
					this.temp.imgUrl = URL.createObjectURL(blob);
				} catch (error) {
					console.error("图片获取失败:", error);
				}

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
				if (this.reply.label == "") this.reply.label = "无";

				// 提取世代号，避免重复
				let genNumber = data.gen.key;
				// 如果世代号已经包含"第"和"世代"，则提取中间的数字或文字
				if (genNumber.startsWith("第") && genNumber.endsWith("世代")) {
					genNumber = genNumber.substring(1, genNumber.length - 2);
				}

				const h = this.$createElement;

				// 创建简洁的结果内容
				const resultContent = h("div", { class: "result-dialog-container" }, [
					h("div", { class: "result-dialog-header" }, [
						h("div", { class: "result-image-container" }, [
							h("img", {
								attrs: {
									src: this.temp.imgUrl,
									alt: data.name,
								},
								class: "result-pokemon-image",
							}),
						]),
						h("div", { class: "result-title-container" }, [
							h("h2", { class: "result-pokemon-name" }, data.name),
							h("p", { class: "result-pokemon-gen" }, `第${genNumber}世代`),
						]),
					]),
					h("div", { class: "result-info-compact" }, [
						h("div", { class: "result-info-row" }, [
							h("span", { class: "result-info-label" }, "属性:"),
							h(
								"div",
								{ class: "result-info-tags" },
								data.type
									.filter((type) => type.key !== "无")
									.map((type) =>
										h(
											"el-tag",
											{
												props: { size: "mini", type: "success" },
												class: "result-tag",
											},
											type.key
										)
									)
							),
						]),
						h("div", { class: "result-info-row" }, [
							h("span", { class: "result-info-label" }, "种族值:"),
							h("span", { class: "result-info-value" }, data.pow.key),
						]),
						h("div", { class: "result-info-row" }, [
							h("span", { class: "result-info-label" }, "特性:"),
							h(
								"div",
								{ class: "result-info-tags" },
								data.ability.map((ability) =>
									h(
										"el-tag",
										{
											props: { size: "mini", type: "info" },
											class: "result-tag",
										},
										ability.key
									)
								)
							),
						]),
					]),
					h("div", { class: "result-stats" }, [
						h(
							"p",
							{ class: "result-guess-count" },
							this.surrendered
								? "你已投降，得不得行呀"
								: `你用了 ${this.times} 次尝试${
										this.temp.answer === "True" ? " 猜出正确答案" : ""
								  }`
						),
					]),
				]);

				// 根据条件设置不同的标题
				let dialogTitle = "游戏结束";

				if (!this.surrendered) {
					// 如果不是投降
					if (this.temp.answer === "True") {
						// 如果猜对了
						if (this.times <= 3) {
							// 三次及以内猜对
							dialogTitle = "太厉害了，鼓掌👏👏👏";
						} else {
							// 三次以上猜对
							dialogTitle = "恭喜你猜对了！";
						}
					}
				}

				// 使用this.$alert代替MessageBox，更好控制样式和位置
				this.$confirm(resultContent, dialogTitle, {
					confirmButtonText: "下一把",
					cancelButtonText: "返回",
					customClass: "result-dialog",
					dangerouslyUseHTMLString: true,
					center: true, // 确保弹窗居中
					showClose: false,
					closeOnClickModal: false,
					closeOnPressEscape: false,
					distinguishCancelAndClose: true,
					callback: (action) => {
						if (action === "confirm") {
							this.Restart();
						}
					},
				});
			} catch (error) {
				console.error(error);
			}
		},
		CloseSetting() {
			this.saveSettings();
			this.settingVisble = false;
			this.Restart();
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
		saveSettings() {
			console.log("保存设置中");
			try {
				// 保存当前设置状态
				localStorage.setItem("guessSettings", JSON.stringify(this.settings));
			} catch (e) {
				console.error("设置保存失败：", e);
			}
		},
		// 修改loadSettings方法，确保在加载设置后立即更新猜测次数
		loadSettings() {
			try {
				const savedSettings = localStorage.getItem("guessSettings");
				if (savedSettings) {
					const parsedSettings = JSON.parse(savedSettings);

					// 处理旧版本的设置
					if (parsedSettings.genid && !parsedSettings.selectedGens) {
						// 如果有旧版本的genid但没有selectedGens，初始化为全选
						parsedSettings.selectedGens = [
							true,
							true,
							true,
							true,
							true,
							true,
							true,
							true,
							true,
						];
					}

					// 确保有baseGuessCount属性
					if (parsedSettings.maxguess && !parsedSettings.baseGuessCount) {
						parsedSettings.baseGuessCount = parsedSettings.maxguess;
					} else if (!parsedSettings.baseGuessCount) {
						parsedSettings.baseGuessCount = 10;
					}

					// 更新设置
					this.settings = { ...this.settings, ...parsedSettings };
				}

				// 无论是否加载了已保存的设置，都确保在设置加载后立即更新猜测次数
				this.$nextTick(() => {
					this.updateGuessNumber();
				});
			} catch (e) {
				console.error("设置加载失败：", e);
				// 即使加载失败也要确保更新猜测次数
				this.$nextTick(() => {
					this.updateGuessNumber();
				});
			}
		},
		handleResize() {
			this.windowWidth = window.innerWidth;
			this.isMobile = window.innerWidth <= 768;
		},
		// 处理单个世代复选框变化
		handleGenChange(index) {
			// 获取当前选中的世代数量
			const selectedCount = this.settings.selectedGens.filter(
				(selected) => selected
			).length;

			// 如果用户试图取消所有选择（即当前只剩一个选中且用户要取消它）
			if (selectedCount === 0) {
				// 强制保持至少一个世代被选中
				this.$nextTick(() => {
					this.settings.selectedGens[index] = true;
					this.$message({
						message: "至少需要选择一个世代！",
						type: "warning",
					});
				});
			}

			// 更新猜测次数
			this.updateGuessNumber();
		},
	},
	mounted() {
		this.loadSettings(); // 加载设置会触发更新猜测次数
		// 如果初始化时还有问题，可以在这里再次调用
		this.$nextTick(() => {
			this.updateGuessNumber(); // 确保猜测次数已更新
			this.Restart(); // 然后重启游戏
		});
		window.addEventListener("resize", this.handleResize);
	},
	beforeDestroy() {
		// 移除事件监听，防止内存泄漏
		window.removeEventListener("resize", this.handleResize);
	},
};
</script>

<style>
.guess {
	margin-top: 20px;
	margin-left: 5%;
	margin-right: 5%;
}

.times {
	font-size: 1.2rem;
	margin: 20px 0;
	text-align: center;
}

/* 设置对话框样式 */
.enhanced-dialog {
	border-radius: 8px !important;
	overflow: hidden !important;
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
	border-bottom: 1px dashed #ebeef5;
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

/* 自动完成下拉菜单样式覆盖 */
.autocomplete-dropdown {
	z-index: 9 !important; /* 确保下拉菜单不会覆盖按钮 */
	max-height: 250px !important; /* 限制下拉菜单高度 */
	overflow-y: auto !important;
}

/* 桌面端卡片居中容器 */
.pokemon-cards-container {
	display: flex;
	justify-content: center;
	width: 100%;
}

/* 卡片基础样式 */
.pokemon-cards {
	display: flex;
	margin-bottom: 30px;
	max-width: 1200px; /* 限制最大宽度 */
	width: 100%;
}

.pokemon-card {
	border: 1px solid #ebeef5;
	border-radius: 8px;
	box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
	background-color: #fff;
	transition: all 0.3s ease;
}

.pokemon-card:hover {
	transform: translateY(-3px);
	box-shadow: 0 4px 16px 0 rgba(0, 0, 0, 0.15);
}

.card-header {
	display: flex;
	align-items: center;
	border-bottom: 1px solid #ebeef5;
}

.pokemon-image {
	margin-right: 15px;
}

.pokemon-name {
	font-weight: bold;
}

.section-title {
	color: #606266;
	font-weight: 500;
}

.section-content {
	display: flex;
	flex-wrap: wrap;
	gap: 5px;
}

.info-tag {
	margin: 2px;
}

/* 移动端卡片样式 */
.mobile-cards {
	flex-direction: column;
	gap: 15px;
}

.mobile-cards .pokemon-card {
	padding: 12px;
}

.mobile-cards .card-header {
	padding-bottom: 10px;
	margin-bottom: 10px;
}

.mobile-cards .pokemon-name {
	font-size: 16px;
}

.mobile-cards .card-section {
	margin-bottom: 8px;
	padding-bottom: 8px;
	border-bottom: 1px dashed #ebeef5;
}

.mobile-cards .card-section:last-child {
	border-bottom: none;
	margin-bottom: 0;
	padding-bottom: 0;
}

.mobile-cards .section-title {
	font-size: 14px;
	margin-bottom: 5px;
}

/* 桌面端卡片样式 - 水平布局 */
.desktop-cards {
	flex-direction: column;
	gap: 20px;
}

.desktop-card {
	display: flex;
	padding: 0;
	width: 100%;
}

.desktop-card .card-header {
	flex-direction: column;
	padding: 15px;
	border-bottom: none;
	border-right: 1px solid #ebeef5;
	align-items: center;
	justify-content: center;
	min-width: 100px;
}

.desktop-card .pokemon-image {
	margin-right: 0;
	margin-bottom: 10px;
}

.desktop-card .pokemon-name {
	font-size: 16px;
	text-align: center;
}

/* 桌面端卡片内容布局改进 - 平均分配空间 */
.desktop-card-content {
	display: flex;
	flex: 1;
	padding: 15px;
	overflow-x: auto;
	scrollbar-width: thin;
	justify-content: space-around;
}

.desktop-section {
	margin: 0 10px;
	min-width: 80px;
	text-align: center;
	flex: 1;
	max-width: 120px; /* 防止某些列过宽 */
}

.desktop-section .section-title {
	font-size: 14px;
	margin-bottom: 10px;
	border-bottom: 1px dashed #ebeef5;
	padding-bottom: 5px;
	white-space: nowrap;
}

.desktop-section .section-content {
	display: flex;
	flex-direction: column;
	align-items: center;
	gap: 8px;
}

/* 修复滚动条样式 */
.desktop-card-content::-webkit-scrollbar {
	height: 6px;
}

.desktop-card-content::-webkit-scrollbar-thumb {
	background-color: #c0c4cc;
	border-radius: 3px;
}

.desktop-card-content::-webkit-scrollbar-track {
	background-color: #f5f7fa;
}

/* 按钮样式优化 */
.button-col {
	display: flex;
	justify-content: center;
}

.action-button {
	width: 100%;
	height: 40px;
	display: flex;
	justify-content: center;
	align-items: center;
}

/* 按钮文字居中修复 */
.el-button {
	display: flex;
	justify-content: center;
	align-items: center;
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

/* 全局弹窗样式重置 */
.el-message-box {
	display: flex !important;
	flex-direction: column !important;
	max-height: 90vh !important;
	margin: 15vh auto !important; /* 确保垂直居中 */
	position: relative !important;
}

/* 结果对话框样式 */
.result-dialog {
	border-radius: 8px !important;
	box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2) !important;
	overflow: hidden !important;
}

.result-dialog .el-message-box__header {
	padding: 15px !important;
	background-color: #f5f7fa !important;
	border-bottom: 1px solid #e4e7ed !important;
	text-align: center !important;
}

.result-dialog .el-message-box__title {
	font-size: 18px !important;
	color: #303133 !important;
	font-weight: 600 !important;
}

.result-dialog .el-message-box__content {
	padding: 0 !important;
	margin: 0 !important;
}

.result-dialog .el-message-box__btns {
	padding: 10px 20px 15px !important;
	justify-content: center !important;
	text-align: center !important;
}

.result-dialog .el-button {
	width: 120px !important;
	margin: 0 !important;
}

.result-dialog-container {
	display: flex;
	flex-direction: column;
}

.result-dialog-header {
	display: flex;
	align-items: center;
	padding: 15px;
	background-color: #f5f7fa;
}

.result-image-container {
	margin-right: 15px;
	flex-shrink: 0;
}

.result-pokemon-image {
	width: 60px;
	height: 60px;
	object-fit: contain;
	border-radius: 50%;
	background-color: rgba(255, 255, 255, 0.7);
	padding: 5px;
	box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.result-title-container {
	flex: 1;
}

.result-pokemon-name {
	font-size: 20px;
	margin: 0 0 5px 0;
	color: #303133;
}

.result-pokemon-gen {
	margin: 0;
	color: #606266;
	font-size: 14px;
}

.result-info-compact {
	padding: 15px;
}

.result-info-row {
	display: flex;
	margin-bottom: 10px;
	align-items: flex-start;
}

.result-info-row:last-child {
	margin-bottom: 0;
}

.result-info-label {
	min-width: 60px;
	font-weight: 500;
	color: #606266;
}

.result-info-value {
	color: #303133;
}

.result-info-tags {
	display: flex;
	flex-wrap: wrap;
	gap: 5px;
}

.result-tag {
	margin: 2px;
}

.result-stats {
	text-align: center;
	padding: 10px 15px;
	color: #606266;
	border-top: 1px solid #e4e7ed;
	background-color: #f5f7fa;
}

.result-guess-count {
	font-size: 15px;
	margin: 0;
}

/* 移动端适配 */
@media screen and (max-width: 768px) {
	.guess {
		margin-left: 2%;
		margin-right: 2%;
	}

	.times {
		font-size: 1rem;
	}

	.el-message-box {
		width: 85% !important;
		max-width: 320px !important; /* 限制最大宽度 */
	}

	.result-dialog-header {
		padding: 12px;
	}

	.result-pokemon-image {
		width: 50px;
		height: 50px;
	}

	.result-pokemon-name {
		font-size: 18px;
	}

	.result-info-compact {
		padding: 12px;
	}

	.result-info-row {
		margin-bottom: 8px;
	}

	.result-info-label {
		min-width: 50px;
	}

	.enhanced-dialog .el-dialog__body {
		padding: 15px !important;
	}

	.setting-section {
		padding-bottom: 12px;
	}

	/* 移动端世代复选框优化 */
	.gen-checkboxes {
		flex-direction: column;
		gap: 5px;
	}

	/* 移动端输入框增强 */
	.autocomplete-wrapper {
		margin-bottom: 80px; /* 移动端增加更多下方空间 */
	}
}

/* 强制按钮居中的样式 */
.result-dialog .el-message-box__btns {
	display: flex !important;
	justify-content: center !important;
	padding: 10px 20px 15px !important;
	text-align: center !important;
}

.result-dialog .el-button {
	width: 120px !important;
	margin: 0 auto !important; /* 确保水平居中 */
	float: none !important; /* 防止浮动影响 */
	display: block !important; /* 确保按钮是块级元素 */
}

/* 覆盖Element UI可能的默认对齐 */
.result-dialog .el-message-box__btns button:nth-child(2) {
	margin-left: 0 !important;
}
/* 确保两个按钮并排显示 */
.result-dialog .el-message-box__btns {
	display: flex !important;
	justify-content: space-around !important;
	padding: 10px 20px 15px !important;
}

.result-dialog .el-button {
	width: 45% !important;
	margin: 0 5px !important;
}

/* 强制对话框底部按钮居中 */
.el-dialog__footer {
	text-align: center !important;
}

.dialog-footer {
	display: flex !important;
	justify-content: center !important;
	width: 100% !important;
}

/* 纠正输入框下拉菜单的层级和定位 */
.el-autocomplete-suggestion {
	max-height: 200px !important;
	margin-top: 5px !important;
	z-index: 100 !important;
}

.el-autocomplete-suggestion__wrap {
	max-height: 180px !important;
}

/* 确保按钮在移动端仍然可见和可点击 */
@media screen and (max-width: 768px) {
	.button-row {
		margin-top: 15px;
		z-index: 20; /* 在移动端提高按钮层级 */
	}

	.action-button {
		height: 44px; /* 移动端增大按钮高度 */
	}
}
</style>
