var plivo = require('plivo');
var express = require('express');
var app = express();
app.set('port', (process.env.PORT || 5000));
app.use(express.static(__dirname + '/public'));
//  Welcome message - firstbranch
var WelcomeMessage = "piilvo test"
// This is the message that Plivo reads when the caller does nothing at all
var NoInput = "Sorry, I didn't catch that. Please hangup and try again later."
// This is the message that Plivo reads when the caller inputs a wrong digit.
var WrongInput = "airoman airaon arion"

app.all('/response/ivr/', function (request, response) {
	if (request.method == "GET") {
		var r = new plivo.Response();
		const get_input = r.addGetInput(
			{
				'action': 'https://'+request.hostname+'/multilevelivr/firstbranch/',
				'method': 'POST',
				'interimSpeechResultsCallback': 'https://'+request.hostname+'/multilevelivr/firstbranch/',
				'interimSpeechResultsCallbackMethod': 'POST',
				'inputType': 'speech',
				'redirect': 'true',
			});
		get_input.addSpeak(WelcomeMessage);
		r.addSpeak(NoInput);
		console.log(r.toXML());
		response.set({ 'Content-Type': 'text/xml' });
		response.end(r.toXML());
	}
});

app.all('/multilevelivr/firstbranch/', function (request, response) {
	// var from_number = request.query.From;
	// var speech = request.query.Speech;
	// console.log("Speech Input is:", speech)
	// var r = new plivo.Response();
	// var params = {
	// 	'action': 'https://'+request.hostname+'/multilevelivr/action/',
	// 	'method': 'POST',
	// 	'redirect': 'false',
	// 	'callerId': from_number
	// };
	// var dial = r.addDial(params);
	// if (speech == "sales") {
	// 	dial.addNumber("18667473658");
	// 	console.log(r.toXML());
	// }
	
	// else if (speech == "support") {
	// 	dial.addNumber("18667473658");
	// 	console.log(r.toXML());
	// }
	// else {
	// 	r.addSpeak(WrongInput);
	// }

	// r.addSpeak(WrongInput);
	// response.set({ 'Content-Type': 'text/xml' });
	// response.end(r.toXML());
	
    var r = new plivo.Response();
    var speak_body = "Hello, you just received your first call";
    r.addSpeak(speak_body);
    response.send(r.toXML());
});

app.listen(app.get('port'), function () {
	console.log('Node app is running on port', app.get('port'));
});