var express = require("express");
var request = require("request");
var path = require("path");
var hbs = require("hbs");
var child_process = require("child_process");
var fs = require("fs");
var Chart = require("chart.js");


var app = express();
// 
var routes = require("./routes");
// -------------- express initialization -------------- //
app.set("trust proxy", 1); //trust first proxy?
app.set("port", process.env.PORT || 8080);

// tell express that the view engine is hbs
app.set("view engine", "hbs");
hbs.registerPartials(__dirname + "/views/partials");
app.use(express.static(__dirname + '/static'));

//express 'get' handles inside
routes.doSet(app);

// WILDCARD HANDLERS MUST COME AFTER ALL OTHER EXPLICIT ENDPOINTS
// -------------- listener -------------- //
// The listener is what keeps node 'alive.'

var listener = app.listen(app.get("port"), function() {
  console.log("Express server started on port: " + listener.address().port);
});
