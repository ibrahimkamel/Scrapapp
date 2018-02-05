from flask import Flask, request, jsonify,render_template
from scrapyd_api import ScrapydAPI
import re
from flask_pymongo import PyMongo
import urllib
from uuid import uuid4
app = Flask(__name__)



app.config['MONGO_DBNAME'] = 'amazonproducts'
mongo = PyMongo(app)
scrapyd = ScrapydAPI('http://localhost:6800')
def make_public_page(page):
    new_page = {}
    for field in page:
        if field == 'id':
            new_page['uri'] = url_for('get_page', page_id = page['id'], _external = True)
        else:
            new_page[field] = page[field]
    return new_page

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/api',methods=('POST','GET'))
def amazon_api():

    if request.method == "POST":
        urls = request.form.get("urls",None)
        if not urls:
            return jsonify("Url Not Found"),404
        if urls:
            url_list =  re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', urls)
            if not url_list:
                return jsonify("Invalid Url"),404

            for url in url_list:
                if "amazon.com" not in url:
                    return jsonify("Invalid Url must be for amazon website"),404
                unique_id = str(uuid4())
                settings = {'unique_id':unique_id}
                task = scrapyd.schedule('default', 'amazonspider', 
                        settings=settings, url=url,extra_attribute='unique_id='+unique_id, domain="amazon.com")
                status = scrapyd.job_status('default', task)
            return jsonify({'task_id': task, 'unique_id': unique_id, 'status': 'started' })
    else:
        urls = request.args.get("urls",None)
        task_id = request.args.get('task_id', None)
        unique_id = request.args.get('unique_id', None)
        if task_id:
            status = scrapyd.job_status('default', task_id)
            if status == 'finished':
                try:
                    # this is the unique_id that we created even before crawling started.
                    # item = ScrapyItem.objects.get(unique_id=unique_id) 
                    product = mongo.db.products.find_one({'unique_id': unique_id})
                    product = make_public_page({k:v for k, v in product.items() if k != '_id'})
                    return jsonify(product)
                except Exception as e:
                    return jsonify({'error': str(e)})
            else:
                return jsonify({'status': status})
        for url in urls:
            url = urllib.unquote(url).decode('utf8')
        if not urls:
            return jsonify("Url Not Found"),404
        if urls:
            url_list =  re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', urls)
            if not url_list:
                return jsonify("Invalid Url"),404

            for url in url_list:
                if "amazon.com" not in url:
                    return jsonify("Invalid Url must be for amazon website"),404
                
                
                products = mongo.db.products.find_one({'url': url})
                
                products = make_public_page({k:v for k, v in products.items() if k != '_id'})
                return jsonify(products)

if __name__ == '__main__':
    app.run(debug=True)
