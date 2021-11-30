from flask import Flask, request, Response, json
from flask_restful import Resource, Api
import utils.rest_utils as rest_utils
import requests

app = Flask(__name__)
api = Api(app)


# PORTFOLIO_API_URL = 'http://127.0.0.2:5000'
PORTFOLIO_API_URL = 'http://localhost:5002'
PORTFOLIO_API_URL_BUY = '/api/buy/'
PORTFOLIO_API_URL_SELL = '/api/sell/'
PORTFOLIO_API_URL_USER_PORTFOLIO = '/api/user/'
PORTFOLIO_API_URL_USER_SHARE_QUANT_P1 = '/api/user/'
PORTFOLIO_API_URL_USER_SHARE_QUANT_P2 = '/stock/'
# MONEY_API_URL = 'http://127.0.0.3:5001'
MONEY_API_URL = 'http://localhost:5001'
MONEY_API_URL_ADD = '/money/'


class WelcomePage(Resource):
    def get(self):
        return 'Welcome to Stock Transaction Composition Service!'


class BuyTransaction(Resource):
    def post(self, _id: int):
        inputs = rest_utils.RESTContext(request)
        r_json = inputs.to_json()

        # get total money to be deducted
        money_amount = (r_json["data"]["quantity"])*(r_json["data"]["price"])
        money_payload = {
            "method": "deduction",
            "money_amount": money_amount
        }
        money_url = f"{MONEY_API_URL}{MONEY_API_URL_ADD}{str(_id)}"
        r_money = requests.put(money_url, json=money_payload)
        
        msg = r_money.json()
        del msg['links']

        if (msg['success']):
            # update stock portfolio if money successfully deducted
            porto_payload = {k: v for k, v in r_json["data"].items() if k!="price"}
            porto_url = f"{PORTFOLIO_API_URL}{PORTFOLIO_API_URL_BUY}{str(_id)}/"
            r_porto = requests.post(porto_url, json=porto_payload)

            msg['links'] = {
                'rel': "self",
                'href': f"/api/userPortfolio/{_id}"
            }
            # 201 CREATED
            rsp = Response(json.dumps(msg), status=201, content_type="application/json")
        else:
            # 422 BAD DATA
            rsp = Response(json.dumps(msg), status=422, content_type="application/json")

        return rsp


class SellTransaction(Resource):
    def post(self, _id: int):
        inputs = rest_utils.RESTContext(request)
        r_json = inputs.to_json()
        
        # update stock portfolio
        porto_payload = {k: v for k, v in r_json["data"].items() if k!="price"}
        porto_url = f"{PORTFOLIO_API_URL}{PORTFOLIO_API_URL_SELL}{str(_id)}/"
        r_porto = requests.post(porto_url, json=porto_payload)

        print(r_porto.json())

        msg = {}
        if r_porto.json():
            # receiving a message means that updating the stock portfolio fails
            msg['success'] = 0
            msg['cause_of_error'] = r_porto.json()['message']
            # 422 BAD DATA
            rsp = Response(json.dumps(msg), status=422, content_type="application/json")

        else:
            msg['success'] = 1
            
            # get total money to be added
            money_amount = (r_json["data"]["quantity"])*(r_json["data"]["price"])
            money_payload = {
                "method": "addition",
                "money_amount": money_amount
            }
            money_url = f"{MONEY_API_URL}{MONEY_API_URL_ADD}{str(_id)}"
            r_money = requests.put(money_url, json=money_payload)

            msg['links'] = {
                'rel': "self",
                'href': f"/api/userPortfolio/{_id}"
            }
            # 201 CREATED
            rsp = Response(json.dumps(msg), status=201, content_type="application/json")
            
        return rsp


class GetPortfolio(Resource):
    def get(self, _id: int):
        url = PORTFOLIO_API_URL + PORTFOLIO_API_URL_USER_PORTFOLIO + str(_id)
        r = requests.get(url)
        return r.json()


class GetUserStock(Resource):
    def get(self, _id: str, _ticker: str):
        url = PORTFOLIO_API_URL + PORTFOLIO_API_URL_USER_SHARE_QUANT_P1 + str(_id) + \
              PORTFOLIO_API_URL_USER_SHARE_QUANT_P2 + _ticker
        r = requests.get(url)
        return r.json()


api.add_resource(WelcomePage, '/')
api.add_resource(BuyTransaction, '/api/buy/<int:_id>/')
api.add_resource(SellTransaction, '/api/sell/<int:_id>/')
api.add_resource(GetPortfolio, '/api/userPortfolio/<int:_id>/')
api.add_resource(GetUserStock, '/api/userShareQuantity/<int:_id>/stock/<string:_ticker>/')


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5004, debug=True)
