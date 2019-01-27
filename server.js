var express = require('express');
var bodyParser = require('body-parser');
var app     = express();

//Note that in version 4 of express, express.bodyParser() was
//deprecated in favor of a separate 'body-parser' module.
app.use(bodyParser.urlencoded({ extended: true })); 

//app.use(express.bodyParser());

app.post('/myaction', function(req, res) {
    console.log('test');
    var response = 'Name: ' + req.body.name + ' Zip: ' + req.body.zip + ' Phone: ' + req.body.phone + ' Low: ' + req.body.cold + ' High: ' + req.body.hot + ' Rain: ' + req.body.rain + ' Snow: ' + req.body.snow
    res.send(response);
});

app.listen(8080, function() {
  console.log('Server running at http://127.0.0.1:8080/');
});

