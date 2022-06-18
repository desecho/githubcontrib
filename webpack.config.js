const webpack = require('webpack');
const path = require('path');
const MiniCssExtractPlugin = require('mini-css-extract-plugin');

const basePath = path.resolve(__dirname, 'src', 'githubcontrib');
const jsPath = path.join(basePath, 'js');
const vendorPackages = ['vue-flash-message/dist/vue-flash-message.min.css',
  'bootstrap/dist/css/bootstrap.min.css', 'bootstrap/dist/js/bootstrap.min.js',
  'axios-progress-bar/dist/nprogress.css', 'popper.js/dist/umd/popper.min.js',
  'bootstrap-social/bootstrap-social.css',
];

function getBundle(filename) {
  return [path.join(jsPath, 'init.js'), path.join(jsPath, filename), path.join(jsPath, 'set_axios_settings.js')];
}

module.exports = {
  entry: {
    myRepos: getBundle('my_repos.js'),
    preferences: getBundle('preferences.js'),
    app: [path.join(jsPath, 'init.js'), path.join(jsPath, 'app.js')],
    style: path.join(basePath, 'styles', 'styles.scss'),
    vendor: vendorPackages,
  },
  watchOptions: {
    poll: true,
  },
  resolve: {
    alias: {
      vue: 'vue/dist/vue.min.js',
    },
  },
  output: {
    filename: 'js/[name].js',
    path: path.join(basePath, 'static'),
  },
  module: {
    rules: [
      {
        test: /\.css$/,
        use: [MiniCssExtractPlugin.loader, 'css-loader'],
      },
      {
        test: /\.scss$/,
        use: [MiniCssExtractPlugin.loader, 'css-loader', 'sass-loader'],
      },
    ],
  },
  plugins: [
    new MiniCssExtractPlugin(),
    new webpack.ProvidePlugin({
      '$': 'jquery',
      'Vue': 'vue',
      'jQuery': 'jquery',
      'window.jQuery': 'jquery',
      'Tether': 'tether',
      'Popper': 'popper.js',
      'window.Tether': 'tether',
      'Alert': 'exports-loader?Alert!bootstrap/js/dist/alert',
      'Button': 'exports-loader?Button!bootstrap/js/dist/button',
      'Carousel': 'exports-loader?Carousel!bootstrap/js/dist/carousel',
      'Collapse': 'exports-loader?Collapse!bootstrap/js/dist/collapse',
      'Dropdown': 'exports-loader?Dropdown!bootstrap/js/dist/dropdown',
      'Modal': 'exports-loader?Modal!bootstrap/js/dist/modal',
      'Popover': 'exports-loader?Popover!bootstrap/js/dist/popover',
      'Scrollspy': 'exports-loader?Scrollspy!bootstrap/js/dist/scrollspy',
      'Tab': 'exports-loader?Tab!bootstrap/js/dist/tab',
      'Tooltip': 'exports-loader?Tooltip!bootstrap/js/dist/tooltip',
      'Util': 'exports-loader?Util!bootstrap/js/dist/util',
    }),
  ],
  optimization: {
    splitChunks: {
      minSize: 0,
    },
  },
};
