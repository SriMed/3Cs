var path = require("path");
var child_process = require("child_process");

exports.ccc_home = function(req, res) {
  var render_dict = {
    message: "Welcome to 3Cs: Coffee, Covid, Cheer!"
  };
  res.render("ccc_home", render_dict);
};

function predict_cheer(req, res, next) {
  var coffee = req.query.coffee; //this is how you get input from ajax
  var pt = req.query.pt;
  
  
  var spawn = child_process.spawn;

  console.log("calling python script");
  var process = spawn("python", ["resources/get_prediction.py", coffee, pt]); 
  var result = "";
  
  console.log("python script spawned")
  
  process.stdout.on("data", function(data) {
    result = data.toString();
    console.log("Python script returned:" + result);

    res.locals.ac = result;
    console.log("res.locals arg");
    console.log(res.locals.ac);
    next();
  });
}

exports.render_prediction = [predict_cheer, function(req, res) {
    console.log("in render_prediction");
    var render_dict = {
      message: "Welcome to 3Cs: Coffee, Covid, Cheer!",
      prediction: res.locals.ac
    };
    res.render("prediction", render_dict); // #populate render_dict
  }
];