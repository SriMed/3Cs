var ccc = require("./ccc");

exports.doSet = function(app) {
  //-------express 'get' handlers
  app.get("/", ccc.ccc_home);
  app.get("/predict", ccc.render_prediction);
};

