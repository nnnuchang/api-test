import pytest
import requests
import json

class TestOrders:
    def setup_method(self):
        self.url = 'http://localhost:5000/api/orders'

        self.headers = {
            'Content-Type': 'application/json'
        }


    def test_orders_all_correct(self):
        body = {
            "id": "A0000001",
            "name": "Test Name",
            "address": {
                "city": "taipei-city",
                "district": "da-an-district",
                "street": "fuxing-south-road"
            },
            "price": "2000",
            "currency": "USD"
        }
        
        response = requests.post(url= self.url, headers=self.headers, json = body)

        print('\n\n')
        print('(api) all correct')
        print('status code = ' + str(response.status_code))
        print('response = ' + str(response.json()))


        assert response.status_code == 200 and int(response.json()['price']) == int(body['price']) * 31
    
    @pytest.mark.parametrize('test_name', ['Test 測試', '測試', 'テスト', 'тест'])
    def test_order_name_non_english(self, test_name):
        body = {
            "id": "A0000001",
            "name": test_name,
            "address": {
                "city": "taipei-city",
                "district": "da-an-district",
                "street": "fuxing-south-road"
            },
            "price": "2000",
            "currency": "USD"
        }

        response = requests.post(url= self.url, headers=self.headers, json = body)

        print('\n')
        print('(api) name non-english')
        print('name = ' + body['name'])
        print('status code = ' + str(response.status_code))
        print('response = ' + response.text)


        assert response.text.strip() == '400 - Name contains non-English characters'

    @pytest.mark.parametrize('test_name', ['Test name', 'test Name', 'test name'])
    def test_order_name_not_capitalized(self, test_name):
        body = {
            "id": "A0000001",
            "name": test_name,
            "address": {
                "city": "taipei-city",
                "district": "da-an-district",
                "street": "fuxing-south-road"
            },
            "price": "2000",
            "currency": "USD"
        }

        response = requests.post(url= self.url, headers=self.headers, json = body)

        print('\n')
        print('(api) name not capitalized')
        print('name = ' + body['name'])
        print('status code = ' + str(response.status_code))
        print('response = ' + response.text)

        assert response.text.strip() == '400 - Name is not capitalized'

    @pytest.mark.parametrize('test_price', [0, 200, 2000, 2001, 3000, 20000])
    def test_order_name_over_2000(self, test_price):
        body = {
            "id": "A0000001",
            "name": "Test Name",
            "address": {
                "city": "taipei-city",
                "district": "da-an-district",
                "street": "fuxing-south-road"
            },
            "price": str(test_price),
            "currency": "USD"
        }

        response = requests.post(url= self.url, headers=self.headers, json = body)

        print('\n')
        print('(api) price over 2000')
        print('price = ' + body['price'])
        print('status code = ' + str(response.status_code))
        
        if test_price > 2000:
            print('response = ' + response.text)
            assert response.text.strip() == '400 - Price is over 2000'
        else:
            assert response.status_code != 400
    
    def test_order_string_price(self):
        body = {
            "id": "A0000001",
            "name": "Test Name",
            "address": {
                "city": "taipei-city",
                "district": "da-an-district",
                "street": "fuxing-south-road"
            },
            "price": "abc",
            "currency": "USD"
        }

        response = requests.post(url= self.url, headers=self.headers, json = body)

        print('\n')
        print('(api) price string in price')
        print('price = ' + body['price'])
        print('status code = ' + str(response.status_code))
        print('response = ' + response.text)
        
        assert response.status_code != 200

    @pytest.mark.parametrize('test_currency', ['TWD', 'USD', 'JPY', 'CNY'])
    def test_order_other_currency(self, test_currency):
        body = {
            "id": "A0000001",
            "name": "Test Name",
            "address": {
                "city": "taipei-city",
                "district": "da-an-district",
                "street": "fuxing-south-road"
            },
            "price": "2000",
            "currency": test_currency
        }

        response = requests.post(url= self.url, headers=self.headers, json = body)

        print('\n')
        print('(api) other currency')
        print('currency = ' + body['currency'])
        print('status code = ' + str(response.status_code))

        if test_currency != 'TWD' and test_currency != 'USD':
            print('response = ' + response.text)
            assert response.text.strip() == '400 - Currency format is wrong'
        else:
            assert response.status_code == 200

    @pytest.mark.parametrize('test_currency, test_price', [('USD', 2000), ('USD', 100), ('TWD', 1000)])
    def test_order_currency_USD(self, test_currency, test_price):
        body = {
            "id": "A0000001",
            "name": "Test Name",
            "address": {
                "city": "taipei-city",
                "district": "da-an-district",
                "street": "fuxing-south-road"
            },
            "price": str(test_price),
            "currency": test_currency
        }

        response = requests.post(url= self.url, headers=self.headers, json = body)

        print('\n')
        print('(api) other currency')
        print('currency = ' + body['currency'] + ', price = ' + body['price'])
        print('status code = ' + str(response.status_code))
        print('response price= ' + str(response.json()['price']))


        if test_currency == 'USD':
            assert response.status_code == 200 and int(response.json()['price']) == int(body['price']) * 31
        else:
            assert response.status_code == 200 and int(response.json()['price']) == int(body['price'])

    


