from flask import Flask, request, jsonify
from service import NameEnglish, Uppercase, Price, OtherCurrency, CurrencyToTWD

app = Flask(__name__)


@app.route("/api/orders", methods=["POST"])
def orders():
    requestData = request.get_json()

    order = {
        "oid": requestData["id"],
        "name": requestData["name"],
        "city": requestData["address"]["city"],
        "district": requestData["address"]["district"],
        "street": requestData["address"]["street"],
        "price": requestData["price"],
        "currency": requestData["currency"],
    }

    # uppercase = Uppercase()
    nameEnglish = NameEnglish(Uppercase(Price(OtherCurrency(CurrencyToTWD()))))

    response = nameEnglish.handle(order)

    if response['statusCode'] != 200:
        return (str(response['statusCode'] )+ ' - ' + response['msg']), response['statusCode']
    else:
        return jsonify(response['data'])


if __name__ == "__main__":
    app.run(debug=False, port=5000, host='0.0.0.0')
