const path = require('path');

module.exports = {
  // ... other webpack config
  module: {
    rules: [
      {
        test: /\.js$/,
        enforce: 'pre',
        use: ['source-map-loader'],
        exclude: /node_modules\/react-zoom-pan-pinch/,
      },
    ],
  },
  ignoreWarnings: [/Failed to parse source map/],
}; 