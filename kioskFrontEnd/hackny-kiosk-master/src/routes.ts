import { RouteConfig } from 'vue-router';
import VueRouter from 'vue-router';

import PageNotFoundComponent from './page-not-found-component.vue';
import HelloComponent from './kiosk.vue';

// Routes resolved in order
export const Routes: RouteConfig[] = [
    { path: '/kiosk', component: HelloComponent },
    { path: '**', component: PageNotFoundComponent }
];
