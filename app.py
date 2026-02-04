import pandas as pd
import numpy as np
from flask import Flask,jsonify,request
from flasgger import Swagger

df = pd.read_excel("/Users/yoyukawa/Documents/PythonPractice/Sampledata.xlsx")
    #print(type(df)) -> <class 'pandas.core.frame.DataFrame'>

app = Flask(__name__)
swagger = Swagger(app)

@app.route('/hello')
def hello():
    """
    Hello endpoint
    ---
    responses:
     200:
        description: "hello worldを返す"
        examples:
         text/plain: hello world
    """
    return "hello world"


@app.route('/check')
def check():
    """
    check endpoint
    ---
    responses:
     200:
        description: "リストをチェックする"
        examples:
         text/plain: リストチェック
    """
    return jsonify(df.to_dict(orient='records'))


@app.route('/test',methods=['GET'])
def test():
    """
    test endpoint
    ---
    parameters:
      - name: item
        in: query
        type: string
        required: true
        description: 検索したい商品名
    responses:
      200:
        description: "excelのデータを返す"
        examples:
        examples:
         text/plain: return excel
    """
    #inputデータを受け取る処理
    item = request.args.get("item", "")
        #print(type(item)) -> <class 'str'>
    
    #itemをカンマ区切りでリストに格納する
    itemlist = item.split(",")

    #for文でDFからソート、最安値検索処理
    cheapest_stores={}
    for i in itemlist:
        result = df[df["商品名"] == i]
        cheapest_price = result["価格"].min()
        cheapest_store = result[result["価格"] == cheapest_price]
        cheapest_stores[i] = cheapest_store.to_dict(orient='records')
    return jsonify(cheapest_stores)

if __name__=='__main__':
    app.run(debug=True)