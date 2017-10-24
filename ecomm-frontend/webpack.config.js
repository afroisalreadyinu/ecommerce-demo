function getConfig(env, optionsMap) {
  return {
    entry: "./src/index.js",
    output: {
      path: `${__dirname}/dist`,
      filename: "bundle.js"
    }
  }
};

module.exports = getConfig
