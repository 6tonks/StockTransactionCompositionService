from flask import Flask
from flask_restful import Resource, Api

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
    def post(self):
        pass


class SellTransaction(Resource):
    def post(self):
        pass


class GetPortfolio(Resource):
    def get(self):
        pass


class GetUserStock(Resource):
    def get(self):
        pass


api.add_resource(WelcomePage, '/')
api.add_resource(BuyTransaction, '/api/buy/<user_id>')
api.add_resource(SellTransaction, '/api/sell/<user_id>')
api.add_resource(GetPortfolio, '/api/get/<user_id>')
api.add_resource(GetUserStock, '/api/getUserStock/<user_id>')




if __name__ == '__main__':
    app.run()
