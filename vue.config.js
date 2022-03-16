//vue.config.js
module.exports = {
    chainWebpack: config => {
        config
            .plugin('html')
            .tap(args => {
                args[0].title = "Annotated SVG Creator";
                return args;
            })
    },
    devServer: {
        proxy: 'http://127.0.0.1:5000/',
    }
}