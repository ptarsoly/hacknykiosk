import Vue from 'vue';
import VueRouter from 'vue-router';

Vue.use(VueRouter);

import './styles/styles.scss';

import { Routes } from './routes';

export const router = new VueRouter({
    mode: 'history',
    routes: Routes
});

router.beforeEach((to, from, next) => {
    console.log(to, from);
    next();
});

const app = new Vue({
    router
}).$mount('#app');