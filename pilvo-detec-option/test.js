var plivo = require('plivo');
var express = require('express');
var app = express();
app.set('port', (process.env.PORT || 5000));
app.use(express.static(__dirname + '/public'));
//  Welcome message, first branch
// var WelcomeMessage = "Bienvenido a la demo de esteban guzman salazar. Press 1 for your account balance. Press 2 for your account status. Press 3 to speak to a representative"
var WelcomeMessage = "Bienvenido a la demo de esteban guzman salazar. Preciona 1 para español. Preciona 2 para ingles"
// Message for second branch
var RepresentativeBranch = "Press 1 for sales. Press 2 for support"
// Message that Plivo reads when the caller does nothing
var NoInput = "Sorry, I didn't catch that. Please hang up and try again"
// Message that Plivo reads when the caller presses a wrong digit
var WrongInput = "Sorry, that's not a valid input"

app.all('/multilevelivr/', function (request, response) {
	if (request.method == "GET") { 
		var r = new plivo.Response();
		const get_input = r.addGetInput(
			{
				'action': 'https://e5af-2806-2f0-8080-fbd1-dda-fa9f-3cfc-2120.ngrok-free.app/multilevelivr/firstbranch/',
				"method": 'POST',
				'inputType': 'dtmf',
				'digitEndTimeout': '5',
				'language': 'es-MX',
				'redirect': 'true'
			});
		// const get_input = r.addGetInput(
		// 	{
		// 		'action': 'https://3538-2806-2f0-8080-fbd1-dda-fa9f-3cfc-2120.ngrok-free.app/multilevelivr/firstbranch/',
		// 		'method': 'POST',
		// 		'interimSpeechResultsCallback': 'https://3538-2806-2f0-8080-fbd1-dda-fa9f-3cfc-2120.ngrok-free.app/multilevelivr/firstbranch/',
		// 		'interimSpeechResultsCallbackMethod': 'POST',
		// 		'inputType': 'speech',
		// 		'redirect': 'true',
		// 	});
		get_input.addSpeak(WelcomeMessage);
		r.addSpeak(NoInput);
		console.log(r.toXML());
		console.log('............--------------------------........')
		response.set({ 'Content-Type': 'text/xml' });
		response.end(r.toXML());
	}
});

app.all('/multilevelivr/firstbranch/', function (request, response) {
	var digits = request.query.Digits;
	console.log("Digit pressed", request.query)
	console.log('observador -=====>', request.query)
	var r = new plivo.Response();
	if (digits == "1") {
		console.log('has escogido la opcion 2')
		var BalMessage = "Your account balance is $20";
		r.addSpeak(BalMessage);
	}
	else if (digits == "2") {
		var StatMessage = "Your account status is active"
		r.addSpeak(StatMessage);
	}
	else if (digits == "3") {
		const get_input = r.addGetInput(
			{
				'action': 'https://<ngrok_identifier>.ngrok.io/multilevelivr/secondbranch/',
				"method": 'POST',
				'inputType': 'dtmf',
				'digitEndTimeout': '5',
				'language': 'en-US',
				'redirect': 'false',
				'profanityFilter': 'true'
			});
		get_input.addSpeak(RepresentativeBranch, voice = "Polly.Salli", language = "en-US");
		r.addSpeak(NoInput);
		console.log(r.toXML());
	}
	else {
		console.log('no ha escofigo la opcion')
		r.addSpeak(WrongInput);
	}
	response.set({ 'Content-Type': 'text/xml' });
	response.end(r.toXML());
});

app.all('/multilevelivr/secondbranch/', function (request, response) {
	var from_number = request.query.From;
	var digits = request.query.Digits;
	console.log("Digit pressed", digits)
	var r = new plivo.Response();
	var params = {
		'action': "https://<ngrok_identifier>.ngrok.io/multilevelivr/action/",
		'method': "POST",
		'redirect': "false",
		'callerId': from_number
	};
	var dial = r.addDial(params);
	if (digits == "1") {
		dial.addNumber("<number_1>");
		console.log(r.toXML());
	}
	else if (digits == "2") {
		dial.addNumber("<number_2>");
		console.log(r.toXML());
	}
	else {
		r.addSpeak(WrongInput);
	}
	response.set({ 'Content-Type': 'text/xml' });
	response.end(r.toXML());
});

app.listen(app.get('port'), function () {
	console.log('Node app is running on port', app.get('port'));
});