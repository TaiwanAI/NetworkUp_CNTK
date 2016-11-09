Guidance
=============


### How it works

comparisonHelper is a helper class that calculates the similarity between the user and other attendee and sends these information back to the server via a post request. It takes in three parameter, getUrl, postUrl and userId, all of which are used for what it means literally. First, it finds the user's information in the retrieved list from server with a loop that get its index. Then, dot product is used to determine how similar they are, and this value will be passed into the sigmoid helper function that maps this value onto a range between 0 and 1 (Here we assume that each feature is marked 1 if the attendee has this feature, otherwise, denoted by -1). After that, these information will be post to the server via a http post request and stored into the database.
