# Scrapapp
requirments:
   use pip install -r requirments.txt
   must run localy mongodb server or provide setting in AmazonSpider settings.py for DB configs
run:
  1- run scrapyd in AmazonSpider directory 
  2- run python app.py in SpiderApi directory
  3- put amazon product link like https://www.amazon.com/Amazon-Echo-Dot-Portable-Bluetooth-Speaker-with-Alexa-Black/dp/B01DFKC2SO/
  4- to get status or json result call api in one of these ways:
      a- http://127.0.0.1:5000/api?urls=https://www.amazon.com/Amazon-Echo-Dot-Portable-Bluetooth-Speaker-with-Alexa-Black/dp/B01DFKC2SO/
      b- http://127.0.0.1:5000/api?task_id=d599268f0a7711e8bd56ec9a7459f54b&unique_id=95cd9030-0ed0-4860-a24d-b2d19d92bdb1
