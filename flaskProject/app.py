from flask import Flask
from flask_restful import Resource, Api
import utils.rest_utils as rest_utils

app = Flask(__name__)
api = Api(app)


PORTFOLIO_API_URL = 'http://127.0.0.2:5000'
PORTFOLIO_API_URL_BUY = '/api/buy/<user_id>'
MONEY_API_URL = 'http://127.0.0.3:5001'
MONEY_API_URL_ADD = '/money/<user_id>'


class WelcomePage(Resource):
    def get(self):
        return 'Welcome to Stock Transaction Composition Service!'


class BuyTransaction(Resource):
    def post(self, _id: int):
        inputs = rest_utils.RESTContext(request)
        r_json = inputs.to_json()
        params = r_json["data"]
        params["user_id"] = _id
        pass


class SellTransaction(Resource):
    def post(self, _id: int):
        inputs = rest_utils.RESTContext(request)
        r_json = inputs.to_json()
        params = r_json["data"]
        params["user_id"] = _id
        pass


class GetPortfolio(Resource):
    def get(self, _id: int):
        pass


class GetUserStock(Resource):
    def get(self, _id: str, _ticker: str):
        pass


api.add_resource(WelcomePage, '/')
api.add_resource(BuyTransaction, '/api/buy/<int:_id>/')
api.add_resource(SellTransaction, '/api/sell/<int:_id>/')
api.add_resource(GetPortfolio, '/api/get/<int:_id>/')
api.add_resource(GetUserStock, '/api/getUserStock/<int:_id>/stock/<string:_ticker>/')


if __name__ == '__main__':
    app.run()
