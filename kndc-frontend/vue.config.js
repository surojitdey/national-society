const BundleTracker = require('webpack-bundle-tracker');

module.exports = {
  transpileDependencies: [
    'vuetify'
  ],
  publicPath: process.env.BASE_URL,
  outputDir: './kndc/',
  runtimeCompiler: true,

  devServer: {
    public: 'localhost:8080',
    headers: {
      'Access-Control-Allow-Origin': '*'
    }
  },

  configureWebpack: {
    plugins: [
      new BundleTracker({path: __dirname, filename: 'webpack-stats.json'})
    ]
  },

  chainWebpack: config => {
    config
      .plugin('html')
      .tap(args => {
        args[0].title = "Kamakhya Nagar Society";
        return args;
      })
  },

  // pages: {
  //   index: {
  //     // entry for the page
  //     entry: 'src/main.js',
  //     title: 'Kamakhya Nagar Society',
  //   },
  // }

  // lintOnSave: false,
  // runtimeCompiler: true,
  // css: {
  //   loaderOptions: {
  //     sass: {
  //       data: `@import "@/styles/variables.scss";`,
  //     },
  //   },
  // },
}
