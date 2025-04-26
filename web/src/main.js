import Vue from 'vue';
import App from './App.vue';

import ElementUI from 'element-ui';
import 'element-ui/lib/theme-chalk/index.css';

import VueRouter from 'vue-router';
import router from './routers/index.js';

import VueMarkdownEditor from '@kangc/v-md-editor';
import '@kangc/v-md-editor/lib/style/base-editor.css';
import vuepressTheme from '@kangc/v-md-editor/lib/theme/vuepress.js';
import '@kangc/v-md-editor/lib/theme/style/vuepress.css';
import Prism from 'prismjs';
import createKatexPlugin from '@kangc/v-md-editor/lib/plugins/katex/cdn';

VueMarkdownEditor.use(vuepressTheme, {
    Prism,
    createKatexPlugin
});
VueMarkdownEditor.use(createKatexPlugin());

Vue.use(VueMarkdownEditor);
Vue.use(ElementUI);
Vue.use(VueRouter);
Vue.config.productionTip=false;

new Vue({
    el: '#app',
    render: h => h(App),
    router
});

