# Tweets
 Tweets application

API for Twitter

Design a real-time API for Twitter that will operate at scale. The API will enable a user to subscribe using a keyword or phrase and (optional) location and radius. If a tweet contains the keyword or phrase and is within the area requested it will be streamed to the user. Keep in mind that not all tweets contain a location and those that do only have a name (e.g. Rome, Italy), not coordinates. 
You'll need to provide an authentication mechanism for the users. As input, assume you get a streaming feed of all tweets. Output will be a continuous stream of tweets matching the filter criteria.

Here's an example: a user subscribes to the phrase "I have arrived" with an area of radius 100km around Tel-Aviv. The following tweets are received by the system:
"I've arrived" with a location in Jerusalem.
"I have arrived" with no location.
"I don't know" with location in Tel-Aviv.
Only the first tweet is streamed to the user since it matches the phrase and location.

Assume you can use whichever ready made solutions you want (database, messaging infrastructure etc.), no need to create things from scratch. Please write code to implement the filtering component (only), in java.

When providing your solution please pay attention to the 5 pillars of the AWS well-architected framework, make sure you handle errors correctly and provide the DB schemas (if any) that you use. Think of any alternatives to the solution you came up with and why you preferred a specific solution over the others. 

Please send your design (with diagrams) and the code. We'll then discuss your solution.


Good luck!

