var express = require('express');
var app = express();
// Running python files
var PythonShell = require('python-shell');
// Using Twitter APIs
var Twitter = require('twitter');
// Using Http to open up URLs
var http = require('http');


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
  getSummarizationByTitleAndText(req.query.mytitle, req.query.mytext, function(message){
    console.log("python message received");
    // Send the HTML-like message back to the View
    var replyMessage = '<b>Title: </b>' + message.title + '<br>' + '<b>Summary: </b>' + message.text;
    res.send(replyMessage);
  });

});


/*
 * Get Tweets Request
 */
app.get('/mytweets', function(req, res){


  // Create a Twitter instance with ENV parameters given
  var client = new Twitter({
    consumer_key: req.query.consumer_key,
    consumer_secret: req.query.consumer_secret,
    access_token_key: req.query.access_token_key,
    access_token_secret: req.query.access_token_secret
  });

  // Given the target name
  var target_screen_name = req.query.screen_name; 

  // Retrieve all the tweets from the target user
  getUserTimelineByScreenName(target_screen_name, client, function(tweets){
    console.log("tweets callback OK");
    // Iterate through all the tweets and summarize each of their text
    tweets.forEach(function(tweet){
      //console.log("Original: " + tweet.user.name + ": " + tweet.text);
      getSummarizationByTitleAndText(tweet.user.name, tweet.text, function(message){
        console.log("Summarized: " + message.title + ": " + message.text);
      });
    });
    
  });

}); 


/*
 * Given the title and text, it processes the text by summarize.py
 * and then return the message object
 */
function getSummarizationByTitleAndText(title, text, callback){
  // Prepare the summarizing data
  var options = {
    mode: 'json',
    pythonOptions: ['-u'],
    scriptPath: './',
    args: [title, text],
  };

  // Instantiate the pythonshell with the given data
  var test =  new PythonShell('summarize.py', options);

  /* 
   * Listening on the response.
   * The callback function displays the result on browser
   */
  test.on('message', function (message) {
    callback(message);
  }); 
}


/*
 * Test twitter API
 */
function getUserTimelineByScreenName(target_screen_name, client, callback){

  var params = {screen_name: target_screen_name}; //screen_name: '@......'
  client.get('statuses/user_timeline', params, function(error, tweets, response) {
    if (!error) {
      console.log("tweets received");
      callback(tweets);

    } else {
      console.error("GET Method Error");
    }
  });
}





// Listening on port 3000
app.listen(3000, function () {
  console.log('Example app listening on port 3000!');
});
