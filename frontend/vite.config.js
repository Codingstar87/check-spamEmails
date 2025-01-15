import { defineConfig } from 'vite';

export default defineConfig({
   
    server: {
        proxy: {
            '/auth': {
                target:'https://check-spamemails-2.onrender.com' , 
                   
                changeOrigin: true,
            },
        },
    },
});
