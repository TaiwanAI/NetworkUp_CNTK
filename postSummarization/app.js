var express = require('express');
var app = express();
var PythonShell = require('python-shell');

/*
 * Landing Page
 */
app.get('/', function (req, res) {
  res.sendFile(__dirname + '/index.html');
});

/*
 * Summarize Request
 */
app.get('/myform', function(req, res){
  // Store the title and text from user input
  var myTitle = req.query.mytitle;
  var myText = req.query.mytext;

  // Prepare the summarizing data
  var options = {
    mode: 'json',
    pythonOptions: ['-u'],
    scriptPath: './',
    args: [myTitle, myText],
  };

  // Instantiate the pythonshell with the given data
  var test =  new PythonShell('summarize.py', options);

  /* 
   * Listening on the response.
   * The callback function displays the result on browser
   */
  test.on('message', function (message) {
    console.log(message);
    res.send('<b>Title: </b>' + message.title + '<br>' + '<b>Summary: </b>' + message.text);
  });

}); 

// Listening on port 3000
app.listen(3000, function () {
  console.log('Example app listening on port 3000!');
});
