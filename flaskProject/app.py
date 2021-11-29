from flask import Flask, request
from flask_restful import Resource, Api
import utils.rest_utils as rest_utils
import requests

app = Flask(__name__)
api = Api(app)


PORTFOLIO_API_URL = 'http://127.0.0.2:5000'
PORTFOLIO_API_URL_BUY = '/api/buy/'
PORTFOLIO_API_URL_SELL = '/api/sell/'
PORTFOLIO_API_URL_USER_PORTFOLIO = '/api/user/'
PORTFOLIO_API_URL_USER_SHARE_QUANT_P1 = '/api/user/'
PORTFOLIO_API_URL_USER_SHARE_QUANT_P2 = '/stock/'
MONEY_API_URL = 'http://127.0.0.3:5001'
MONEY_API_URL_ADD = '/money/<user_id>'


class WelcomePage(Resource):
    def get(self):
        return 'Welcome to Stock Transaction Composition Service!'


class BuyTransaction(Resource):
    def post(self, _id: int):
        inputs = rest_utils.RESTContext(request)
        r_json = inputs.to_json()
        payload = r_json["data"]
        url = PORTFOLIO_API_URL + PORTFOLIO_API_URL_BUY + str(_id)
        r = requests.post(url, json=payload)
        return r.text


class SellTransaction(Resource):
    def post(self, _id: int):
        inputs = rest_utils.RESTContext(request)
        r_json = inputs.to_json()
        payload = r_json["data"]
        url = PORTFOLIO_API_URL + PORTFOLIO_API_URL_SELL + str(_id)
        r = requests.post(url, json=payload)
        return r.text


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
    app.run()
