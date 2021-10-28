var express = require('express');
var app = express();

app.get('/listUsers', function (req, res) {
      console.log( "hello" );
      res.end( "hello" );
})

var server = app.listen(8081, function () {
   var host = server.address().address
   var port = server.address().port
   console.log("Example app listening at http://%s:%s", host, port)
})

