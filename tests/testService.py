import pytest, sys
sys.path.append('.')
from service import NameEnglish, Uppercase, Price, OtherCurrency, CurrencyToTWD

class TestService:
    @pytest.mark.parametrize('name', ['English Name', 'nom français', '中文名字', 'ชื่อไทย'])
    def test_name_english(self, name):
        nameEnglish = NameEnglish()
        response = nameEnglish.handle({'name': name})

        print('\n')
        print('(service) name english')
        print('name = ' + name)
        print('pass = ' + str(response is True))

        if name == 'English Name':
            assert response
        else:
            assert response['statusCode'] == 400 and response['msg'] == 'Name contains non-English characters'
    
    @pytest.mark.parametrize('name', ['Test Name', 'name', 'test Name'])
    def test_uppercase(self, name):
        uppercase = Uppercase()
        response = uppercase.handle({'name': name})

        print('\n')
        print('(service) uppercase')
        print('name = ' + name)
        print('pass = ' + str(response is True))

        if name == 'Test Name':
            assert response
        else:
            assert response['statusCode'] == 400 and response['msg'] == 'Name is not capitalized'

    @pytest.mark.parametrize('prices', [1, 2, 1000, 1999, 5000])
    def test_price(self, prices):
        price = Price()
        response = price.handle({'price': str(prices)})

        print('\n')
        print('(service) price')
        print('price = ' + str(prices))
        print('pass = ' + str(response is True))

        if prices < 2000:
            assert response
        else:
            assert response['statusCode'] == 400 and response['msg'] == 'Price is over 2000'

    @pytest.mark.parametrize('currency', ['GBP', 'KRW', 'TWD', 'USD'])
    def test_other_currency(self, currency):
        otherCurrency = OtherCurrency()
        response = otherCurrency.handle({'currency': currency})

        print('\n')
        print('(service) other currency')
        print('currency = ' + currency)
        print('pass = ' + str(response is True))


        if currency == 'TWD' or currency == 'USD':
            assert response
        else:
            assert response['statusCode'] == 400 and response['msg'] == 'Currency format is wrong'
    
    @pytest.mark.parametrize('currency, price', [('TWD', 100), ('TWD', 2000), ('USD', 100), ('USD', 2000)])
    def test_currency_to_twd(self, currency, price):
        order = {
            "oid": "A0000001",
            "name": "Melody Holiday Inn",
            "city": "taipei-city",
            "district": "da-an-district",
            "street": "fuxing-south-road",
            "price": str(price),
            "currency": currency,
        }

        currencyToTwd = CurrencyToTWD()
        response = currencyToTwd.handle(order)

        print('\n')
        print('(service) currency to TWD')
        print('currency = ' + currency)
        print('price = ' + str(price))
        print('pass = ' + str(response is True))
        print(response)

        if currency == 'USD':
            assert response['statusCode'] == 200 and int(response['data']['price']) == int(order['price']) * 31 and response['data']['currency'] == 'TWD'
        else:
            assert response['statusCode'] == 200 and int(response['data']['price']) == int(order['price']) and response['data']['currency'] == 'TWD'