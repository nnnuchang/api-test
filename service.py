class Service:
    def __init__(self, successor=None):
        self._successor = successor

    def handle(self, request):
        handled = self._handle(request)

        # 處裡沒問題就傳給下一個
        if handled == True and self._successor:
            response = self._successor.handle(request)
        else:
            response = handled

        return response

    def _handle(self, request):
        raise NotImplementedError("not implemented in subclass")


class NameEnglish(Service):
    def _handle(self, request):
        try:
            name = request["name"]
            name.encode(encoding="utf-8").decode("ascii")
        except UnicodeDecodeError:
            return {"statusCode": 400, "msg": "Name contains non-English characters"}
        else:
            return True


class Uppercase(Service):
    def _handle(self, request):
        name = request["name"]

        nameWords = name.split()

        for nw in nameWords:
            if not nw[0].isupper():
                return {"statusCode": 400, "msg": "Name is not capitalized"}

        return True


class Price(Service):
    def _handle(self, request):
        price = request["price"]

        try:
            if int(price) > 2000:
                return {"statusCode": 400, "msg": "Price is over 2000"}
            else:
                return True
        except ValueError:
            return {"statusCode": 400, "msg": "Price is not int"}


class OtherCurrency(Service):
    def _handle(self, request):
        currency = request["currency"]

        if currency != "TWD" and currency != "USD":
            return {"statusCode": 400, "msg": "Currency format is wrong"}
        return True


class CurrencyToTWD(Service):
    def _handle(self, request):
        currency = request["currency"]
        price = int(request["price"])

        if currency == "USD":
            price = price * 31

        return {
            "statusCode": 200,
            "data": {
                "oid": request["oid"],
                "name": request["name"],
                "address": {
                    "city": request["city"],
                    "district": request["district"],
                    "street": request["street"],
                },
                "price": str(price),
                "currency": "TWD",
            },
        }
