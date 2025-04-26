<template>
  <el-container>
    <el-header>
      <el-row type="flex" justify="space-between" align="middle">
        <el-col :span="24" style="text-align: right;">
          <div class="header-buttons">
            <!-- 夜间/日间模式切换按钮 -->
            <el-button circle :icon="darkMode ? 'el-icon-sunny' : 'el-icon-moon'" @click="toggleDarkMode"></el-button>
            <el-button circle icon="el-icon-setting" @click="settingVisble=true"></el-button>
            <el-button circle icon="el-icon-question" @click="introVisble=true"></el-button>
            <el-button circle icon="el-icon-user" @click="authorVisble=true"></el-button>
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
        custom-class="enhanced-dialog">
        <div class="setting">
          <div class="setting-section">
            <div class="setting-title">游戏模式</div>
            <el-select v-model="settings.hardid" placeholder="请选择" size="small" style="width: 50%">
              <el-option
                v-for="item in hards"
                :key="item"
                :label="item"
                :value="item">
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
                  @change="handleGenChange(index)">
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
                active-text="显示更多种族值信息">
              </el-switch>
              <el-switch
                v-model="settings.shapeOpen"
                active-text="显示更多外形信息">
              </el-switch>
              <el-switch
                v-model="settings.catchOpen"
                active-text="显示蛋组/捕获率信息">
              </el-switch>
              <el-switch
                v-model="settings.showGenArrow"
                active-text="开启世代箭头">
              </el-switch>
            </div>
          </div>

          <div class="setting-section">
            <div class="setting-title">卡片展示顺序</div>
            <el-switch
              v-model="settings.reverseDisplay"
              active-text="猜测反向显示"
              inactive-text="猜测正向显示">
            </el-switch>
          </div>

          <el-switch
            v-model="settings.cheatOpen"
            active-text="小小的恶作剧">
          </el-switch>
          <br>

          <div class="block">
            <span class="demonstration">本轮猜测次数：{{ settings.maxguess }}</span>
            <el-slider
              v-model="settings.maxguess"
              :step="1"
              :max="15"
              :min="3"
              :show-tooltip="false"
              style="width: 100%">
            </el-slider>
          </div>
        </div>

        <span slot="footer" class="dialog-footer">
          <el-button type="primary" @click="CloseSetting()">确 定</el-button>
        </span>
      </el-dialog>

      <!-- 规则与功能介绍对话框 -->
      <el-dialog
        title="欢迎体验Pokémonle"
        :visible.sync="introVisble"
        :width="isMobile ? '90%' : '50%'"
        :show-close="false"
        custom-class="enhanced-dialog">
        <el-tabs v-model="activeTab" type="border-card">
          <el-tab-pane label="规则介绍" name="rules">
            <div class="intro-content">
              <p><strong>游戏目标：</strong>通过输入宝可梦名称进行猜测，找出目标宝可梦。每次猜测后，你将获得输入宝可梦的相关信息，帮助你逐步接近答案。</p>
              <p><strong>提示颜色说明：</strong></p>
              <div class="hint-section">
                <div class="hint-item">
                  <el-tag type="success" size="small">绿色高亮</el-tag>
                  <span>表示该信息与目标宝可梦完全相同。</span>
                </div>
                <div class="hint-item">
                  <el-tag type="warning" size="small">黄色高亮</el-tag>
                  <span>表示该信息与目标宝可梦接近但不完全相同。</span>
                </div>
              </div>
              <p><strong>黄色高亮的触发条件：</strong></p>
              <ul>
                <li>种族值总和：与目标宝可梦的差值 ≤ 50</li>
                <li>速度：与目标宝可梦的差值 ≤ 10</li>
                <li>世代：与目标世代相邻（差值 ≤ 1）</li>
                <li>进化方式：不完全相同但属于相似进化方式（例如使用物品、特定地点、等级、亲密度等）</li>
                <li>形态标签：两只宝可梦都有地区形态，特殊形态所属地区不同</li>
              </ul>
              <p><strong>上下箭头的作用：</strong></p>
              <p>在种族值总和、速度、世代等数值类信息中，箭头提示你猜测的方向是否正确：</p>
              <ul>
                <li><strong>↑：</strong>表示你输入的宝可梦的该数值低于目标宝可梦，建议下次猜测选择数值更高的宝可梦。</li>
                <li><strong>↓：</strong>表示你输入的宝可梦的该数值高于目标宝可梦，建议下次猜测选择数值更低的宝可梦。</li>
              </ul>
            </div>
          </el-tab-pane>
          <el-tab-pane label="功能介绍" name="features">
            <div class="intro-content">
              <p><strong>简单模式：</strong>只包含较为热门或带有特殊标签的宝可梦，适合新手玩家，降低猜测难度。</p>
              <p><strong>世代选择：</strong>允许选择单个或多个世代组合进行游戏，限定目标宝可梦的范围。例如，只选“第一世代”将只从红/绿/蓝/黄的宝可梦中选择目标。</p>
              <p><strong>随机开局：</strong>为首次猜测随机选择一个当前世代范围内的宝可梦，适合不想手动输入起手猜测的玩家。</p>
              <p><strong>小小的恶作剧：</strong>开启后，一只猥琐的宝可梦有概率随机隐藏某项信息（例如属性、种族值等）</p>
            </div>
          </el-tab-pane>
        </el-tabs>

        <span slot="footer" class="dialog-footer">
          <el-button type="primary" @click="introVisble=false">开始游戏</el-button>
        </span>
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
                <el-tag size="mini" type="info">基础架构</el-tag>
              </div>
            </el-card>
            <el-card :body-style="{ padding: '0px' }" class="author-card">
              <img src="@/assets/img/GengerHead.jpg" class="author-avatar">
              <div class="author-info">
                <span>流明Luminous</span>
                <br>
                <el-tag size="mini" type="info">UI/功能</el-tag>
              </div>
            </el-card>
            <el-card :body-style="{ padding: '0px' }" class="author-card">
              <img src="@/assets/img/TyranitarX.png" class="author-avatar">
              <div class="author-info">
                <span>TyranitarX</span>
                <br>
                <el-tag size="mini" type="info">双人模式</el-tag>
              </div>
            </el-card>
          </div>
        </div>
		<div slot="footer" class="dialog-footer">
			<el-button type="primary" @click="authorVisble=false">确 定</el-button>
		</div>
		</el-dialog>
		
    </el-header>
    <el-main>
      <div class="guess">
        <!-- 输入区域 -->
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
                  style="width: 100%"></el-autocomplete>
              </div>
            </el-col>
          </el-row>
          <el-row type="flex" justify="center" align="middle" :gutter="20" class="button-row">
            <el-col :span="isMobile ? 6 : 3" class="button-col">
              <el-button
                type="primary"
                class="action-button"
                :disabled="this.times > 0 || this.gameover"
                @click="RandomStart()"
                icon="el-icon-refresh-left">
                随机开局
              </el-button>
            </el-col>
            <el-col :span="isMobile ? 6 : 3" class="button-col">
              <el-button type="primary" class="action-button" :disabled="this.gameover" @click="Guess()">
                {{ this.gameover ? '已结束' : '确定' }}
              </el-button>
            </el-col>
            <el-col :span="isMobile ? 6 : 3" class="button-col">
              <el-button type="danger" class="action-button" :disabled="this.gameover" @click="Surrender()">
                投降
              </el-button>
            </el-col>
            <el-col :span="isMobile ? 6 : 3" class="button-col">
              <el-button type="success" class="action-button" @click="Restart()">重新开始</el-button>
            </el-col>
            <el-col :span="isMobile ? 6 : 3" class="button-col">
              <el-button class="action-button" @click="toDualCreate()">双人模式（测试）</el-button>
            </el-col>
          </el-row>
        </div>

        <div class="stats-container">
            <div class="stat-item">
                <i class="el-icon-tickets stat-icon"></i>
                <span class="stat-label">本轮猜测次数：</span>
                <span class="stat-value">{{ this.times }}/{{ this.settings.maxguess }}</span>
            </div>
            <div class="stat-item">
                <i class="el-icon-trophy stat-icon"></i>
                <span class="stat-label">连续猜对次数：</span>
                <span class="stat-value">{{ streakCount }}</span>
            </div>
            </div>

        <!-- 移动端卡片垂直布局 -->
        <div v-if="isMobile" class="pokemon-cards mobile-cards">
          <div v-for="(item, index) in displayedItems" :key="index" class="pokemon-card">
            <div class="card-header">
              <div class="pokemon-image">
                <el-image style="width: 50px; height: 50px" :src="item.imgUrl" fit="contain"></el-image>
              </div>
              <div class="pokemon-name">{{ item.name }}</div>
            </div>

            <div class="card-section">
              <div class="section-title">属性</div>
              <div class="section-content">
                <el-tag v-for="(type, idx) in item.type" :key="'type-'+idx"
                  size="mini" :type="type.col" class="info-tag"
                  v-if="item.cheat.id!=1">
                  {{ type.key }}
                </el-tag>
                <img :src="item.cheat.imgUrl" v-if="item.cheat.id==1">
              </div>
            </div>

            <div class="card-section">
              <div class="section-title">种族值</div>
              <div class="section-content">
                <div v-if="item.cheat.id!=2">
                  <el-tag size="mini" :type="item.pow.col" class="info-tag">
                    {{ ValueText(item.pow.key, item.pow.value) }}
                  </el-tag>
                  <el-tag v-if="settings.battleOpen" size="mini" :type="item.speed.col" class="info-tag">
                    速度:{{ ValueText(item.speed.key, item.speed.value) }}
                  </el-tag>
                </div>
                <img :src="item.cheat.imgUrl" v-if="item.cheat.id==2">
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
                <el-tag size="mini" :type="item.gen.col" class="info-tag"
                  v-if="item.cheat.id!=3">
                  {{ settings.showGenArrow ? ValueText(item.gen.key, item.gen.value) : item.gen.key }}
                </el-tag>
                <img :src="item.cheat.imgUrl" v-if="item.cheat.id==3">
              </div>
            </div>

            <div class="card-section">
              <div class="section-title">特性</div>
              <div class="section-content">
                <el-tag v-for="(ability, idx) in item.ability" :key="'ability-'+idx"
                  size="mini" :type="ability.col" class="info-tag"
                  v-if="item.cheat.id!=4">
                  {{ ability.key }}
                </el-tag>
                <img :src="item.cheat.imgUrl" v-if="item.cheat.id==4">
              </div>
            </div>

            <div class="card-section">
              <div class="section-title">进化</div>
              <div class="section-content">
                <div v-if="item.cheat.id!=5">
                  <el-tag v-if="item.evo.key != null" size="mini" :type="item.evo.col" class="info-tag">
                    {{ item.evo.key }}
                  </el-tag>
                  <el-tag size="mini" :type="item.stage.col" class="info-tag">
                    {{ item.stage.key }}
                  </el-tag>
                </div>
                <img :src="item.cheat.imgUrl" v-if="item.cheat.id==5">
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
                <el-tag v-for="(egg, idx) in item.egg" :key="'egg-'+idx"
                  size="mini" :type="egg.col" class="info-tag">
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
                <el-tag v-for="(label, idx) in item.label" :key="'label-'+idx"
                  size="mini" :type="label.col" class="info-tag"
                  v-if="item.cheat.id!=6">
                  {{ label.key }}
                </el-tag>
                <img :src="item.cheat.imgUrl" v-if="item.cheat.id==6">
              </div>
            </div>
          </div>
        </div>

        <!-- 桌面端卡片水平布局 -->
        <div v-else class="pokemon-cards desktop-cards">
          <div v-for="(item, index) in displayedItems" :key="index" class="pokemon-card desktop-card">
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
                    size="small" :type="type.col" class="info-tag"
                    v-if="item.cheat.id!=1">
                    {{ type.key }}
                  </el-tag>
                  <img :src="item.cheat.imgUrl" v-if="item.cheat.id==1">
                </div>
              </div>

              <div class="desktop-section">
                <div class="section-title">种族值</div>
                <div class="section-content">
                  <div v-if="item.cheat.id!=2">
                    <el-tag size="small" :type="item.pow.col" class="info-tag">
                      {{ ValueText(item.pow.key, item.pow.value) }}
                    </el-tag>
                    <el-tag v-if="settings.battleOpen" size="small" :type="item.speed.col" class="info-tag">
                      速度:{{ ValueText(item.speed.key, item.speed.value) }}
                    </el-tag>
                  </div>
                  <img :src="item.cheat.imgUrl" v-if="item.cheat.id==2">
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
                  <el-tag size="small" :type="item.gen.col" class="info-tag"
                    v-if="item.cheat.id!=3">
                    {{ settings.showGenArrow ? ValueText(item.gen.key, item.gen.value) : item.gen.key }}
                  </el-tag>
                  <img :src="item.cheat.imgUrl" v-if="item.cheat.id==3">
                </div>
              </div>

              <div class="desktop-section">
                <div class="section-title">特性</div>
                <div class="section-content">
                  <el-tag v-for="(ability, idx) in item.ability" :key="'ability-'+idx"
                    size="small" :type="ability.col" class="info-tag"
                    v-if="item.cheat.id!=4">
                    {{ ability.key }}
                  </el-tag>
                  <img :src="item.cheat.imgUrl" v-if="item.cheat.id==4">
                </div>
              </div>

              <div class="desktop-section">
                <div class="section-title">进化</div>
                <div class="section-content">
                  <div v-if="item.cheat.id!=5">
                    <el-tag v-if="item.evo.key != null" size="small" :type="item.evo.col" class="info-tag">
                      {{ item.evo.key }}
                    </el-tag>
                    <el-tag size="small" :type="item.stage.col" class="info-tag">
                      {{ item.stage.key }}
                    </el-tag>
                  </div>
                  <img :src="item.cheat.imgUrl" v-if="item.cheat.id==5">
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
                <div class="section-title">蛋组/捕获率</div>
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
                    size="small" :type="label.col" class="info-tag"
                    v-if="item.cheat.id!=6">
                    {{ label.key }}
                  </el-tag>
                  <img :src="item.cheat.imgUrl" v-if="item.cheat.id==6">
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
      tempdata: null,
      nameList: [],
      tableData: [],
      temp: {},
      reply: {},
      times: 0,
      gameover: false,
      settingVisble: false,
      authorVisble: false,
      introVisble: false,
      surrendered: false,
      darkMode: false,
      activeTab: 'rules',
      streakCount: 0,
      gens: ["全世代", "第一世代（红/黄/蓝/绿）", "第二世代（金/银）", "第三世代（红宝石/蓝宝石/绿宝石/火红/叶绿）", "第四世代（珍珠/钻石/白金/心金/魂银）", "第五世代（黑/白/黑2/白2）", "第六世代（X/Y/欧米伽红宝石/阿尔法蓝宝石）", "第七世代（日/月/究极之日/究极之月）", "第八世代（剑/盾）", "第九世代（朱/紫）"],
      genOptions: [
        { label: '第一世代（红/黄/蓝/绿）', value: 1, range: [0, 150] },
        { label: '第二世代（金/银）', value: 2, range: [151, 250] },
        { label: '第三世代（红宝石/蓝宝石/绿宝石/火红/叶绿）', value: 3, range: [251, 385] },
        { label: '第四世代（珍珠/钻石/白金/心金/魂银）', value: 4, range: [386, 492] },
        { label: '第五世代（黑/白/黑2/白2）', value: 5, range: [493, 648] },
        { label: '第六世代（X/Y/欧米伽红宝石/阿尔法蓝宝石）', value: 6, range: [649, 720] },
        { label: '第七世代（日/月/究极之日/究极之月）', value: 7, range: [721, 808] },
        { label: '第八世代（剑/盾）', value: 8, range: [809, 904] },
        { label: '第九世代（朱/紫）', value: 9, range: [905, 1024] }
      ],
      hards: ["普通模式", "简单模式"],
      cheaters: ["Amoonguss", "Sableye", "Smeargle", "Whimsicott"],
      settings: {
        genid: "全世代",
        selectedGens: [true, true, true, true, true, true, true, true, true],
        hardid: "普通模式",
        maxguess: 10,
        battleOpen: false,
        shapeOpen: false,
        catchOpen: false,
        cheatOpen: false,
        showGenArrow: true,
        reverseDisplay: true,
      },
      useGitHubImages: true,
      windowWidth: window.innerWidth,
      isMobile: window.innerWidth <= 768,
      tempSettings: null
    }
  },
  methods: {
	async toDualCreate() {
		await this.$router.push('/dualCreate')
	},
    toggleDarkMode() {
      this.darkMode = !this.darkMode;
      this.applyDarkMode();
      this.saveDarkModePreference();
    },
    applyDarkMode() {
      if (this.darkMode) {
        document.body.classList.add('dark-mode');
      } else {
        document.body.classList.remove('dark-mode');
      }
    },
    saveDarkModePreference() {
      try {
        localStorage.setItem('darkMode', JSON.stringify(this.darkMode));
      } catch(e) {
        console.error("保存夜间模式偏好失败:", e);
      }
    },
    loadDarkModePreference() {
      try {
        const savedMode = localStorage.getItem('darkMode');
        if (savedMode !== null) {
          this.darkMode = JSON.parse(savedMode);
          this.applyDarkMode();
        }
      } catch(e) {
        console.error("加载夜间模式偏好失败:", e);
      }
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
    async loadName() {
      try {
        this.tempdata = require(`@/assets/json/WordInfo.json`);
        this.nameList = this.tempdata.map(item => ({ value: item }));
		console.log(this.nameList)
        console.log("名称列表加载成功");
      } catch (error) {
        console.error("加载名称失败:", error);
        try {
          const options = {
            method: 'GET',
            url: `${process.env.VUE_APP_API_BASE_URL}/nameget`
          };
          await axios.request(options).then((response) => {
            this.tempdata = response.data;
            this.nameList = this.tempdata.map(item => ({ value: item }));
          }).catch(function (error) {
            console.error("API获取名称失败:", error);
          });
        } catch (apiError) {
          console.error("API获取名称失败:", apiError);
        }
      }
    },
    async Restart() {
      this.times = 0;
      this.gameover = false;
      this.surrendered = false;
      sessionStorage.removeItem('answer');
      this.tableData = [];
      try {
        var gen = 10;
        for (let i = 0; i < 9; i++)
          if (this.settings.selectedGens[i]) gen += (1 << i);
        const dif = this.hards.indexOf(this.settings.hardid);
        const options = {
          method: 'GET',
          url: `${process.env.VUE_APP_API_BASE_URL}/initget`,
          params: {
            difficulty: dif,
            gen: gen
          }
        };
        await axios.request(options).then((response) => {
          this.tempdata = response.data;
        }).catch(function (error) {
          console.error(error);
        });
        sessionStorage.setItem('answer', this.tempdata);
      } catch (error) {
        console.error(error);
      }
    },
    async Surrender() {
      if (this.gameover) return;
      this.surrendered = true;
      this.gameover = true;
      this.streakCount = 0;
      this.saveStreakCount();
      this.ReplayAnswer();
    },
    async Guess() {
      const answer = sessionStorage.getItem('answer');
      if (answer == null) return;
      try {
        const options = {
          method: 'GET',
          url: `${process.env.VUE_APP_API_BASE_URL}/guess`,
          params: {
            answer: answer,
            guess: this.input
          }
        };
        await axios.request(options).then((response) => {
          this.tempdata = response.data;
        }).catch(function (error) {
          console.error(error);
        });

        const data = this.tempdata;
        if (data == "guess name error") {
          this.$notify({
            title: '提交错误',
            message: '不存在的宝可梦',
            type: "error"
          });
        } else {
          this.temp = {};
          this.temp.name = data.name;
          this.temp.answer = data.answer;

          this.temp.type = [];
          data.type.forEach((type, index) => {
            if (type.key != "无") {
              if (type.value == 'True')
                this.temp.type.push({ key: type.key, col: "success" });
              else
                this.temp.type.push({ key: type.key, col: "info" });
            }
          });

          this.temp.pow = {};
          this.temp.pow.key = data.pow.key;
          this.temp.pow.value = data.pow.value;
          if (data.pow.value == "equiv")
            this.temp.pow.col = "success";
          else if (data.pow.dis == "far")
            this.temp.pow.col = "info";
          else
            this.temp.pow.col = "warning";

          this.temp.speed = {};
          this.temp.speed.key = data.speed.key;
          this.temp.speed.value = data.speed.value;
          if (data.speed.value == "equiv")
            this.temp.speed.col = "success";
          else if (data.speed.dis == "far")
            this.temp.speed.col = "info";
          else
            this.temp.speed.col = "warning";

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

          this.temp.gen = {};
          this.temp.gen.key = data.gen.key;
          this.temp.gen.value = data.gen.value;
          if (data.gen.value == 'equiv')
            this.temp.gen.col = "success";
          else if (data.gen.dis == 'far')
            this.temp.gen.col = "info";
          else this.temp.gen.col = "warning";

          this.temp.ability = [];
          data.ability.forEach((ability, index) => {
            if (ability.value == 'True')
              this.temp.ability.push({ key: ability.key, col: "success" });
            else
              this.temp.ability.push({ key: ability.key, col: "info" });
          });

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

          this.temp.stage = {};
          this.temp.stage.key = data.stage.key;
          this.temp.stage.value = data.stage.value;
          if (data.stage.value == 'True')
            this.temp.stage.col = "success";
          else
            this.temp.stage.col = "info";

          this.temp.egg = [];
          data.egg.forEach((egg, index) => {
            if (egg.value == 'True')
              this.temp.egg.push({ key: egg.key, col: "success" });
            else
              this.temp.egg.push({ key: egg.key, col: "info" });
          });

          this.temp.catrate = {};
          this.temp.catrate.key = data.catrate.key;
          this.temp.catrate.value = data.catrate.value;
          if (data.catrate.value == "equiv")
            this.temp.catrate.col = "success";
          else
            this.temp.catrate.col = "info";

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

          this.temp.label = [];
          data.label.forEach((label, index) => {
            if (label.value == 'True') {
              this.temp.label.push({ key: label.key, col: "success" });
            } else if (label.similarity === "similar") {
              this.temp.label.push({ key: label.key, col: "warning" });
            } else {
              this.temp.label.push({ key: label.key, col: "info" });
            }
          });

          await this.loadPokemonImage(data, this.temp);

          this.temp.cheat = {};
          const cheater = this.cheaters[Math.floor(Math.random() * this.cheaters.length)];
          this.temp.cheat.imgUrl = require(`@/assets/img/${cheater}.gif`);
          this.temp.cheat.id = 0;
          if (this.settings.cheatOpen)
            this.temp.cheat.id = 1 + Math.floor(Math.random() * 6);

          this.tableData.push(this.temp);
          this.times++;

          this.input = "";

          if (this.temp.answer == 'True') {
            this.gameover = true;
            this.streakCount++;
            this.saveStreakCount();
            this.ReplayAnswer();
          } else if (this.times == this.settings.maxguess) {
            this.gameover = true;
            this.streakCount = 0;
            this.saveStreakCount();
            this.ReplayAnswer();
          }
        }
      } catch (error) {
        console.error(error);
      }
    },
    async loadPokemonImage(data, tempObj) {
      try {
        if (this.useGitHubImages) {
          const id = parseInt(data.index);
          if (!isNaN(id)) {
            const githubUrl = `https://pokedata.archknowledge.com.cn/i/pokemon/${id}.png`;
            tempObj.imgUrl = githubUrl;
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
          await this.loadApiImage(data.name, tempObj);
        }
      } catch (error) {
        console.error("图片加载错误:", error);
      }
    },
    async loadApiImage(pokemonName, tempObj) {
      // try {
      //   const options = {
      //     method: 'GET',
      //     url: `${process.env.VUE_APP_API_BASE_URL}/getimage`,
      //     params: { pokemon: pokemonName },
      //     responseType: 'blob'
      //   };
      //   const response = await axios.request(options);
      //   const blob = new Blob([response.data]);
      //   tempObj.imgUrl = URL.createObjectURL(blob);
      // } catch (error) {
      //   console.error('API图片获取失败:', error);
      // }
    },
    ValueText(key, value) {
      if (value == 'high')
        return String(key) + "↑";
      if (value == 'low')
        return String(key) + "↓";
      return String(key);
    },
    async ReplayAnswer() {
      const answer = sessionStorage.getItem('answer');
      if (answer == null) return;
      try {
        const options = {
          method: 'GET',
          url: `${process.env.VUE_APP_API_BASE_URL}/getanswer`,
          params: {
            pokemon: answer
          }
        };
        await axios.request(options).then((response) => {
          this.tempdata = response.data;
        }).catch(function (error) {
          console.error(error);
        });
        const data = this.tempdata;
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

        let genNumber = data.gen.key;
        if (genNumber.startsWith('第') && genNumber.endsWith('世代')) {
          genNumber = genNumber.substring(1, genNumber.length - 2);
        }

        const h = this.$createElement;

        const resultContent = h('div', { class: 'result-dialog-container' }, [
          h('div', { class: 'result-dialog-header' }, [
            h('div', { class: 'result-image-container' }, [
              h('img', {
                attrs: {
                  src: this.temp.imgUrl,
                  alt: data.name
                },
                class: 'result-pokemon-image'
              })
            ]),
            h('div', { class: 'result-title-container' }, [
              h('h2', { class: 'result-pokemon-name' }, data.name),
              h('p', { class: 'result-pokemon-gen' }, `第${genNumber}世代`)
            ])
          ]),
          h('div', { class: 'result-info-compact' }, [
            h('div', { class: 'result-info-row' }, [
              h('span', { class: 'result-info-label' }, '属性:'),
              h('div', { class: 'result-info-tags' },
                data.type.filter(type => type.key !== "无").map(type =>
                  h('el-tag', {
                    props: { size: 'mini', type: 'success' },
                    class: 'result-tag'
                  }, type.key)
                )
              )
            ]),
            h('div', { class: 'result-info-row' }, [
              h('span', { class: 'result-info-label' }, '种族值:'),
              h('span', { class: 'result-info-value' }, data.pow.key)
            ]),
            h('div', { class: 'result-info-row' }, [
              h('span', { class: 'result-info-label' }, '特性:'),
              h('div', { class: 'result-info-tags' },
                data.ability.map(ability =>
                  h('el-tag', {
                    props: { size: 'mini', type: 'info' },
                    class: 'result-tag'
                  }, ability.key)
                )
              )
            ])
          ]),
          h('div', { class: 'result-stats' }, [
            h('p', { class: 'result-guess-count' },
              this.surrendered ?
              '你已投降，算不得英雄' :
              `你用了 ${this.times} 次尝试${this.temp.answer === 'True' ? ' 猜出正确答案' : ''}`)
          ])
        ]);

        let dialogTitle = '游戏结束';
        if (!this.surrendered) {
          if (this.temp.answer === 'True') {
            if (this.times <= 3) {
              dialogTitle = '太厉害了，鼓掌👏👏👏';
            } else {
              dialogTitle = '恭喜你猜对了！';
            }
          }
        }

        this.$confirm(resultContent, dialogTitle, {
          confirmButtonText: '再来一次',
          cancelButtonText: '返回',
          customClass: 'result-dialog',
          dangerouslyUseHTMLString: true,
          center: true,
          showClose: false,
          closeOnClickModal: false,
          closeOnPressEscape: false,
          distinguishCancelAndClose: true,
          callback: action => {
            if (action === 'confirm') {
              this.Restart();
            }
          }
        });
      } catch (error) {
        console.error(error);
      }
    },
    async RandomStart() {
      if (this.times > 0 || this.gameover) return;
      try {
        if (this.nameList.length === 0) {
          await this.loadName();
        }
        if (this.selectedGenIndices.length === 0) {
          this.settings.selectedGens = [true, true, true, true, true, true, true, true, true];
        }
        const eligiblePokemon = [];
        this.nameList.forEach((pokemon, index) => {
          const pokemonId = index;
          const inSelectedGen = this.settings.selectedGens.some((selected, genIndex) => {
            if (!selected) return false;
            const range = this.genOptions[genIndex].range;
            return pokemonId >= range[0] && pokemonId <= range[1];
          });
          if (inSelectedGen) {
            eligiblePokemon.push(pokemon.value);
          }
        });
        const pokemonPool = eligiblePokemon.length > 0 ? eligiblePokemon : this.nameList.map(p => p.value);
        const randomIndex = Math.floor(Math.random() * pokemonPool.length);
        const randomPokemon = pokemonPool[randomIndex];
        this.input = randomPokemon;
        this.$nextTick(() => {
          this.Guess();
        });
      } catch (error) {
        console.error("随机开局错误:", error);
        this.$notify({
          title: '随机失败',
          message: '无法随机选择宝可梦，请手动输入',
          type: "warning"
        });
      }
    },
    CloseSetting() {
      if (this.times > 0 || this.tableData.length > 0) {
        const oldSettings = this.tempSettings;
        const newSettings = JSON.parse(JSON.stringify(this.settings));

        const otherSettingsChanged = Object.keys(newSettings).some(key => {
          if (key === 'reverseDisplay') return false;
          if (Array.isArray(newSettings[key])) {
            return JSON.stringify(newSettings[key]) !== JSON.stringify(oldSettings[key]);
          }
          return newSettings[key] !== oldSettings[key];
        });

        this.saveSettings();

        if (!otherSettingsChanged) {
          this.settingVisble = false;
          return;
        }

        this.Restart();
      } else {
        this.saveSettings();
        this.Restart();
      }

      this.settingVisble = false;
    },
    saveSettings() {
      try {
        localStorage.setItem('guessSettings', JSON.stringify(this.settings));
      } catch (e) {
        console.error("设置保存失败：", e);
      }
    },
    loadSettings() {
      try {
        const savedSettings = localStorage.getItem("guessSettings");
        if (savedSettings) {
          const parsedSettings = JSON.parse(savedSettings);
          this.settings = { ...this.settings, ...parsedSettings };
        }
      } catch (e) {
        console.error("设置加载失败：", e);
      }
    },
    saveStreakCount() {
      try {
        localStorage.setItem('streakCount', JSON.stringify(this.streakCount));
      } catch (e) {
        console.error("连续猜对次数保存失败：", e);
      }
    },
    loadStreakCount() {
      // 不再自动加载，保留方法以防未来需要
    },
    handleResize() {
      this.windowWidth = window.innerWidth;
      this.isMobile = window.innerWidth <= 768;
    },
    handleGenChange(index) {
      const selectedCount = this.settings.selectedGens.filter(selected => selected).length;
      if (selectedCount === 0) {
        this.$nextTick(() => {
          this.settings.selectedGens[index] = true;
          this.$message({
            message: '至少需要选择一个世代！',
            type: 'warning'
          });
        });
      }
    },
    openLink(url) {
      window.open(url, '_blank');
    },
    saveTempSettings() {
      this.tempSettings = JSON.parse(JSON.stringify(this.settings));
    }
  },
  computed: {
    displayedItems() {
      return this.settings.reverseDisplay ? this.tableData.slice().reverse() : this.tableData;
    },
    selectedGenIndices() {
      return this.settings.selectedGens
        .map((selected, index) => selected ? index + 1 : null)
        .filter(index => index !== null);
    }
  },
  mounted() {
    this.loadSettings();
    this.loadDarkModePreference();
    // 清理 localStorage 中的 streakCount，确保页面刷新时重置
    try {
      localStorage.removeItem('streakCount');
    } catch (e) {
      console.error("清理连续猜对次数失败：", e);
    }
    this.$nextTick(() => {
      this.Restart();
    });
    window.addEventListener('resize', this.handleResize);
  },
  beforeDestroy() {
    window.removeEventListener('resize', this.handleResize);
  },
  watch: {
    settingVisble(newVal) {
      if (newVal) {
        this.saveTempSettings();
      }
    }
  }
}
</script>

<style>
.guess {
  margin-top: 20px;
  margin-left: 5%;
  margin-right: 5%;
}

/* 统计信息容器 */
.stats-container {
  display: flex;
  justify-content: center;
  align-items: center;
  margin: 20px auto; /* 居中，移除左右margin */
  padding: 15px;
  background-color: #f5f7fa;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  gap: 30px;
  flex-wrap: wrap;
  max-width: 1200px; /* 与.desktop-cards一致 */
  width: 100%; /* 确保占满父容器 */
  box-sizing: border-box; /* 确保padding不影响宽度 */
}

/* 统计项 */
.stat-item {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 1.1rem;
  color: #303133;
}

/* 统计图标 */
.stat-icon {
  font-size: 1.3rem;
  color: #409EFF;
}

/* 统计标签 */
.stat-label {
  font-weight: 600;
  color: #606266;
}

/* 统计值 */
.stat-value {
  font-weight: bold;
  color: #303133;
  transition: all 0.3s ease;
  animation: fadeIn 0.3s ease-in;
}

/* 桌面端卡片容器 */
.desktop-cards {
  flex-direction: column;
  gap: 20px;
  margin: 0 auto;
  max-width: 1200px; /* 与.stats-container一致 */
  width: 100%; /* 确保占满父容器 */
  box-sizing: border-box; /* 确保边距不影响宽度 */
}

/* 桌面端卡片 */
.desktop-card {
  display: flex;
  padding: 0;
  width: 100%; /* 占满父容器 */
  border: 1px solid #EBEEF5;
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  background-color: #fff;
  transition: all 0.3s ease;
  box-sizing: border-box; /* 确保边距不影响宽度 */
}

.desktop-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 4px 16px 0 rgba(0, 0, 0, 0.15);
}

.desktop-card .card-header {
  flex-direction: column;
  padding: 15px;
  border-bottom: none;
  border-right: 1px solid #EBEEF5;
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
  max-width: 120px;
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

/* 夜间模式适配 */
body.dark-mode .stats-container {
  background-color: #333333;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
}

body.dark-mode .stat-item {
  color: #e0e0e0;
}

body.dark-mode .stat-label {
  color: #c0c0c0;
}

body.dark-mode .stat-value {
  color: #e0e0e0;
}

body.dark-mode .stat-icon {
  color: #66b1ff;
}

body.dark-mode .desktop-card {
  background-color: #2a2a2a;
  border-color: #3a3a3a;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.3);
}

body.dark-mode .card-header {
  border-bottom-color: #3a3a3a;
  border-right-color: #3a3a3a;
}

/* 移动端适配（保持不变） */
@media screen and (max-width: 768px) {
  .stats-container {
    flex-direction: column;
    gap: 15px;
    padding: 12px;
    max-width: 100%; /* 移动端占满宽度 */
    margin: 20px 2%;
  }

  .stat-item {
    font-size: 1rem;
  }

  .stat-icon {
    font-size: 1.2rem;
  }

  .desktop-cards {
    display: none; /* 移动端使用.mobile-cards */
  }
}

/* 动画关键帧 */
@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(5px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
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

/* 规则与功能介绍样式 */
.intro-content {
  line-height: 1.6;
}

.intro-content ul {
  padding-left: 20px;
  margin: 10px 0;
}

.intro-content li {
  margin-bottom: 8px;
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

/* 制作人员样式 */
.author-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 20px;
}

.author-links {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
  justify-content: center;
  margin-bottom: 10px;
}

.author-links .el-button {
  min-width: 120px;
}

.author-cards {
  display: flex;
  justify-content: center;
  gap: 30px;
  flex-wrap: wrap;
  width: 100%;
}

.author-card {
  width: 120px;
  text-align: center;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.author-avatar {
  width: 120px;
  height: 120px;
  object-fit: cover;
}

.author-info {
  padding: 8px;
  background-color: #fff;
  text-align: center;
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

/* 输入区域样式 */
.input-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  max-width: 1200px;
  margin: 0 auto 20px;
  position: relative;
}

.autocomplete-wrapper {
  position: relative;
  width: 100%;
  margin-bottom: 60px;
}

.input-row {
  width: 100%;
  margin-bottom: 10px;
  position: relative;
  z-index: 10;
}

.button-row {
  width: 100%;
  margin-top: 10px;
  position: relative;
  z-index: 5;
}

.autocomplete-dropdown {
  z-index: 9 !important;
  max-height: 250px !important;
  overflow-y: auto !important;
}

/* 卡片样式 */
.pokemon-cards {
  display: flex;
  margin-bottom: 30px;
  max-width: 1200px;
  width: 100%;
}

.pokemon-card {
  border: 1px solid #EBEEF5;
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
  border-bottom: 1px solid #EBEEF5;
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

.section-content img {
  width: 40px;
  height: 40px;
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
  border-bottom: 1px dashed #EBEEF5;
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
  margin: 0 auto;
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
  border-right: 1px solid #EBEEF5;
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
  max-width: 120px;
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
  margin: 15vh auto !important;
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

/* 夜间模式样式 */
body.dark-mode {
  background-color: #1a1a1a;
  color: #e0e0e0;
}

body.dark-mode .pokemon-card {
  background-color: #2a2a2a;
  border-color: #3a3a3a;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.3);
}

body.dark-mode .card-header {
  border-bottom-color: #3a3a3a;
  border-right-color: #3a3a3a;
}

body.dark-mode .pokemon-name {
  color: #e0e0e0;
}

body.dark-mode .section-title {
  color: #c0c0c0;
}

body.dark-mode .card-section,
body.dark-mode .desktop-section .section-title {
  border-bottom-color: #3a3a3a;
}

body.dark-mode .el-dialog,
body.dark-mode .enhanced-dialog .el-dialog__header {
  background-color: #2a2a2a !important;
  border-color: #3a3a3a !important;
}

body.dark-mode .el-dialog__title,
body.dark-mode .setting-title {
  color: #e0e0e0 !important;
}

body.dark-mode .el-input__inner,
body.dark-mode .el-autocomplete .el-input__inner {
  background-color: #333333;
  color: #e0e0e0;
  border-color: #4a4a4a;
}

body.dark-mode .el-message-box {
  background-color: #2a2a2a;
  border-color: #3a3a3a;
}

body.dark-mode .el-message-box__title {
  color: #e0e0e0 !important;
}

body.dark-mode .el-message-box__content {
  color: #c0c0c0;
}

body.dark-mode .result-dialog-header,
body.dark-mode .result-stats {
  background-color: #333333;
}

body.dark-mode .result-pokemon-name {
  color: #e0e0e0;
}

body.dark-mode .result-pokemon-gen,
body.dark-mode .result-info-label {
  color: #c0c0c0;
}

body.dark-mode .result-info-value {
  color: #e0e0e0;
}

body.dark-mode .hint-section {
  background-color: #333333;
}

body.dark-mode .author-info {
  background-color: #2a2a2a;
  color: #e0e0e0;
}

body.dark-mode .el-checkbox__label {
  color: #c0c0c0;
}

body.dark-mode .el-switch__label {
  color: #c0c0c0;
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
    max-width: 320px !important;
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

  .gen-checkboxes {
    flex-direction: column;
    gap: 5px;
  }

  .autocomplete-wrapper {
    margin-bottom: 80px;
  }

  .author-cards {
    gap: 20px;
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
  margin: 0 auto !important;
  float: none !important;
  display: block !important;
}

.result-dialog .el-message-box__btns button:nth-child(2) {
  margin-left: 0 !important;
}

.result-dialog .el-message-box__btns {
  display: flex !important;
  justify-content: space-around !important;
  padding: 10px 20px 15px !important;
}

.result-dialog .el-button {
  width: 45% !important;
  margin: 0 5px !important;
}

.el-dialog__footer {
  text-align: center !important;
}

.dialog-footer {
  display: flex !important;
  justify-content: center !important;
  width: 100% !important;
}

.el-autocomplete-suggestion {
  max-height: 200px !important;
  margin-top: 5px !important;
  z-index: 100 !important;
}

.el-autocomplete-suggestion__wrap {
  max-height: 180px !important;
}

@media screen and (max-width: 768px) {
  .button-row {
    margin-top: 15px;
    z-index: 20;
  }

  .action-button {
    height: 44px;
  }
}

@media screen and (max-width: 768px) {
  .button-row {
    flex-wrap: wrap;
    gap: 10px;
  }

  .button-col {
    flex: 0 0 45%;
    max-width: 45%;
  }

  .action-button {
    height: 48px;
    font-size: 14px;
    padding: 0 10px;
    white-space: normal;
    line-height: 1.2;
  }

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
