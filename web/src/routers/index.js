import VueRouter from 'vue-router';
import Vue from 'vue';

import Guess from '../views/Guess.vue';
import dualCreate from "@/views/dualCreate.vue";
import dualGuess from "@/views/dualGuess.vue";

Vue.use(VueRouter);

const router = new VueRouter({
    routes: [
        {path: '/Guess', name: 'Guess', component: Guess},
        {path: '/dualCreate', name: 'dualCreate', component: dualCreate},
        {path: '/dualGuess', name: 'dualGuess', component: dualGuess},
        {path: '*', component: Guess}
    ]
})

// router.beforeEach((to,from,next)=>{
//     if(to.path=='/login'){
//         if(store.getters.getToken=='')next();
//         else next('/home');
//     }
//     else if(to.meta.requireAuth){
//         if(store.getters.getToken=='')next('/login');
//         else next();
//     }
//     else next();
// })

export default router;