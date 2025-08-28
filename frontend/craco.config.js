module.exports = {
  webpack: {
    configure: (webpackConfig) => {
      // Disable source-map-loader for react-zoom-pan-pinch
      webpackConfig.module.rules.forEach((rule) => {
        if (rule.enforce === 'pre' && rule.use && rule.use.some(use => use.loader === 'source-map-loader')) {
          rule.exclude = /node_modules\/react-zoom-pan-pinch/;
        }
      });

      // Ignore source map warnings
      webpackConfig.ignoreWarnings = [
        function ignoreSourcemapsloaderWarnings(warning) {
          return (
            warning.module &&
            warning.module.resource &&
            warning.module.resource.includes('react-zoom-pan-pinch')
          );
        }
      ];

      return webpackConfig;
    },
  },
  devServer: {
    historyApiFallback: true,
    hot: true,
  },
}; 