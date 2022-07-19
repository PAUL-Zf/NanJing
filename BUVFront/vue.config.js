module.exports = {
  lintOnSave: false,
  devServer: {
    historyApiFallback: true,//不用花生壳则去掉，有报错
    allowedHosts: "all",//不用花生壳则去掉，有报错
    port: 8080, // default frontend port
    proxy: {
      "/api": {
        target: "http://localhost:5000", // backend url
        changeOrigin: true,
        secure: true,
        pathRewrite: {
          "^/api": "api",
        },
      },
    },
  },
};
