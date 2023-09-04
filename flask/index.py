#! / usr / bin / python
# -* - coding: utf - 8 -* -
from flask import Flask, Response, request, url_for
from plivo import plivoxml
# Welcome message, first branch
WelcomeMessage = ".Bienvenido a la demo de esteban guzman salazar. Preciona 1 para español. Preciona 2 para ingles"
# Message for second branch
RepresentativeBranch = "Press 1 for sales. Press 2 for support"
# Message that Plivo reads when the caller does nothing
NoInput = "Sorry, I didn't catch that. Please hang up and try again"
# Message that Plivo reads when the caller presses a wrong digit
WrongInput = "Sorry, that's not a valid input"
app = Flask(__name__)

@app.route("/call/", methods=["GET", "POST"])
def ivr():
    element = plivoxml.ResponseElement()
    if request.method == "GET":
        response = (
            element.add(
                plivoxml.GetInputElement()
                .set_action("https://2c38-2806-2f0-8080-fbd1-dda-fa9f-3cfc-2120.ngrok-free.app/multilevelivr/firstbranch/")
                .set_method("POST")
                .set_input_type("dtmf")
                .set_digit_end_timeout(5)
                .set_redirect(True)
                .set_language("es-MX")
                .add_speak(
                    content=WelcomeMessage, voice="Polly.Salli", language="en-US"
                )
            )
            .add_speak(content=NoInput)
            .to_string(False)
        )
    print('------------------------------------------')
    print(response)
    print('------------------------------------------')
    return Response(response, mimetype="text/xml")


@app.route("/multilevelivr/firstbranch/", methods=["GET", "POST"])
def firstbranch():
    response = plivoxml.ResponseElement()
    digit = request.form.get("Digits")
    print("digit pressed: {digit}")
    if digit == "1":
        text = "Your account balance is $20"
        params = {"language": "en-GB"}
        response.add(plivoxml.SpeakElement(text, ** params))
    elif digit == "2":
        text = "Your account status is active"
        params = {"language": "en-GB"}
        response.add(plivoxml.SpeakElement(text, ** params))
    elif digit == "3":
        element = plivoxml.ResponseElement()
        response = (
            element.add(
                plivoxml.GetInputElement()
                .set_action("https://<ngrok_identifier>.ngrok.io/multilevelivr/secondbranch/")
                .set_method("POST")
                .set_input_type("dtmf")
                .set_digit_end_timeout(5)
                .set_redirect(True)
                .set_language("en-US")
                .add_speak(
                    content=RepresentativeBranch, voice="Polly.Salli", language="en-US"
                )
            )
            .add_speak(content=NoInput)
            .to_string(False)
        )
        print(response)
        return Response(response, mimetype="text/xml")
    else:
        response.add(plivoxml.SpeakElement(WrongInput))
        print(response.to_string())
        return Response(response.to_string(), mimetype="text/xml")

@app.route("/multilevelivr/secondbranch/", methods=["GET", "POST"])
def secondbranch():
    response = plivoxml.ResponseElement()
    digit = request.form.get("Digits")
    from_number = request.form.get("From")
    print("digit pressed: {digit}")
    if digit == "1":
        response.add(
            plivoxml.DialElement(
                action="https://<ngrok_identifier>.ngrok.io/multilevelivr/action/",
                method="POST",
                redirect=False,
                caller_id=from_number,
            ).add(plivoxml.NumberElement("<number_1>"))
        )
        print(response.to_string())
        return Response(str(response), mimetype="text/xml")
    elif digit == "2":
        response.add(
            plivoxml.DialElement(
                action="https://<ngrok_identifier>.ngrok.io/multilevelivr/action/",
                method="POST",
                redirect=False,
                caller_id=from_number,
            ).add(plivoxml.NumberElement("<number_2>"))
        )
        print(response.to_string())
        return Response(str(response), mimetype="text/xml")
    else:
        response.add(plivoxml.SpeakElement(WrongInput))
        print(response.to_string())
        return Response(response.to_string(), mimetype="text/xml")


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)