# 資料庫測驗
## 題目一
```SQL
SELECT bnb_id, name AS bnb_name, SUM(amount) AS may_amount FROM orders
JOIN bnbs ON bnbs.id = orders.bnb_id
WHERE currency = "TWD" AND created_at BETWEEN "2023-05-01 00:00:00" AND "2023-05-31 23:59:59"
GROUP BY bnb_id
ORDER BY may_amount DESC
LIMIT 10

```

## 題目二
可以透過新增索引(index)的方式對資料的查詢進行優化。以 WHERE 和 GROUP BY 這些需要查詢的欄位為主要新增索引的對象。GROUP BY 所使用的欄位是一個外來鍵，因此他原本就具有索引的特性，再額外建立索引反而會占用較多的儲存空間。  
比較適合新增索引的欄位包含 currency, created_at，這兩個欄位新增索引之後有可以避免再查詢時掃描整個資料庫。  


# API實作測驗
## 題目一
* ### SOLID
1. Single responsibility principle (SRP)  
   在 Service.py 中，每一個方法只負責他自己的工作，做完之後其他的工作會由其他的方法接續完成。

2. Open-Close principle (OCP)  
   當要新增其他規則時只要新增繼承 Servie 的 Class 就可以擴充現有的程式。

3. Liskov substitution principle (LSP)  
   在 service.py 中有五個類別繼承了 Service Class，而這些 Class 的功能都沒有超越父類別的功能。雖然並沒有單獨使用 Service Class 但是這五個 Class 是可以完整替代或呈現父類別 Servic Class 的。

4. Interface segregation principle (ISP)  
   所有功能都有獨立的介面，當不需要功能的時候不必使用。

5. Dependency inversion principle (DIP)  
   不符合此原則


* ### 設計模式
  **責任鏈模式:**  
  因為在這個程式中有很多需要判斷東西，就像是一個又一個的關卡。因此我認為適合使用**責任鏈模式**，將不同的


* ### 單元測試
  **測試分為兩個檔案，一個用來測試API，另一個用來測試Service的功能**  
  API測試內容與結果如下
  ```
   =============================================================== test session starts ================================================================
   platform win32 -- Python 3.10.5, pytest-8.3.3, pluggy-1.5.0
   rootdir: \api-test
   collected 22 items

   tests\testOrders.py


   (api) all correct
   status code = 200
   response = {'address': {'city': 'taipei-city', 'district': 'da-an-district', 'street': 'fuxing-south-road'}, 'currency': 'TWD', 'name': 'Test Name', 'oid': 'A0000001', 'price': '62000'}
   .

   (api) name non-english
   name = Test 測試
   status code = 400
   response = 400 - Name contains non-English characters
   .

   (api) name non-english
   name = 測試
   status code = 400
   response = 400 - Name contains non-English characters
   .

   (api) name non-english
   name = テスト
   status code = 400
   response = 400 - Name contains non-English characters
   .

   (api) name non-english
   name = тест
   status code = 400
   response = 400 - Name contains non-English characters
   .

   (api) name not capitalized
   name = Test name
   status code = 400
   response = 400 - Name is not capitalized
   .

   (api) name not capitalized
   name = test Name
   status code = 400
   response = 400 - Name is not capitalized
   .

   (api) name not capitalized
   name = test name
   status code = 400
   response = 400 - Name is not capitalized
   .

   (api) price over 2000
   price = 0
   status code = 200
   .

   (api) price over 2000
   price = 200
   status code = 200
   .

   (api) price over 2000
   price = 2000
   status code = 200
   .

   (api) price over 2000
   price = 2001
   status code = 400
   response = 400 - Price is over 2000
   .

   (api) price over 2000
   price = 3000
   status code = 400
   response = 400 - Price is over 2000
   .

   (api) price over 2000
   price = 20000
   status code = 400
   response = 400 - Price is over 2000
   .

   (api) price string in price
   price = abc
   status code = 400
   response = 400 - Price is not int
   .

   (api) other currency
   currency = TWD
   status code = 200
   .

   (api) other currency
   currency = USD
   status code = 200
   .

   (api) other currency
   currency = JPY
   status code = 400
   response = 400 - Currency format is wrong
   .

   (api) other currency
   currency = CNY
   status code = 400
   response = 400 - Currency format is wrong
   .

   (api) other currency
   currency = USD, price = 2000
   status code = 200
   response price= 62000
   .

   (api) other currency
   currency = USD, price = 100
   status code = 200
   response price= 3100
   .

   (api) other currency
   currency = TWD, price = 1000
   status code = 200
   response price= 1000
   .

   =============================================================== 22 passed in 44.98s ================================================================ 
   ```

   Service測試內容與結果如下
   ```
   =============================================================================== test session starts ================================================================================
   platform win32 -- Python 3.10.5, pytest-8.3.3, pluggy-1.5.0
   rootdir: \api-test
   collected 20 items

   tests\testService.py

   (service) name english
   name = English Name
   pass = True
   .

   (service) name english
   name = nom français
   pass = False
   .

   (service) name english
   name = 中文名字
   pass = False
   .

   (service) name english
   name = ชื่อไทย
   pass = False
   .

   (service) uppercase
   name = Test Name
   pass = True
   .

   (service) uppercase
   name = name
   pass = False
   .

   (service) uppercase
   name = test Name
   pass = False
   .

   (service) price
   price = 1
   pass = True
   .

   (service) price
   price = 2
   pass = True
   .

   (service) price
   price = 1000
   pass = True
   .

   (service) price
   price = 1999
   pass = True
   .

   (service) price
   price = 5000
   pass = False
   .

   (service) other currency
   currency = GBP
   pass = False
   .

   (service) other currency
   currency = KRW
   pass = False
   .

   (service) other currency
   currency = TWD
   pass = True
   .

   (service) other currency
   currency = USD
   pass = True
   .

   (service) currency to TWD
   currency = TWD
   price = 100
   pass = False
   {'statusCode': 200, 'data': {'oid': 'A0000001', 'name': 'Melody Holiday Inn', 'address': {'city': 'taipei-city', 'district': 'da-an-district', 'street': 'fuxing-south-road'}, 'price': '100', 'currency': 'TWD'}}
   .

   (service) currency to TWD
   currency = TWD
   price = 2000
   pass = False
   {'statusCode': 200, 'data': {'oid': 'A0000001', 'name': 'Melody Holiday Inn', 'address': {'city': 'taipei-city', 'district': 'da-an-district', 'street': 'fuxing-south-road'}, 'price': '2000', 'currency': 'TWD'}}
   .

   (service) currency to TWD
   currency = USD
   price = 100
   pass = False
   {'statusCode': 200, 'data': {'oid': 'A0000001', 'name': 'Melody Holiday Inn', 'address': {'city': 'taipei-city', 'district': 'da-an-district', 'street': 'fuxing-south-road'}, 'price': '3100', 'currency': 'TWD'}}
   .

   (service) currency to TWD
   currency = USD
   price = 2000
   pass = False
   {'statusCode': 200, 'data': {'oid': 'A0000001', 'name': 'Melody Holiday Inn', 'address': {'city': 'taipei-city', 'district': 'da-an-district', 'street': 'fuxing-south-road'}, 'price': '62000', 'currency': 'TWD'}}
   .

   ================================================================================ 20 passed in 0.05s ================================================================================
   ```