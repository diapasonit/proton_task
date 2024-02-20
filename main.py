import flask
from flask import request, Response
from flask_cors import CORS, cross_origin

from service.order_service import OrderService

app = flask.Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route('/orders/', methods=['GET'])
@cross_origin()
def get_orders():
    page = request.args.get('page', default=1, type=int)
    size = request.args.get('size', default=100, type=int)
    orders = OrderService.get_orders(page, size)
    return orders.to_json()


@app.route('/orders/<order_id>', methods=['GET'])
@cross_origin()
def get_order(order_id: int):
    order_details = OrderService.get_order_details(order_id)
    if order_details is None:
        return Response('', status=404)
    return order_details.to_json()


@app.route('/orders/follow-up/', methods=['GET'])
@cross_origin()
def get_follow_up_orders():
    return OrderService.get_follow_up_orders().to_json()


@app.route('/orders/follow-up/<order_id>', methods=['POST'])
@cross_origin()
def follow_up_order(order_id):
    if not OrderService.follow_up_order(order_id):
        return Response('', status=404)

    return Response('{}', status=201, mimetype='application/json')


@app.route('/orders/unfollow-up/<order_id>', methods=['POST'])
@cross_origin()
def unfollow_up_order(order_id):
    if not OrderService.unfollow_up_order(order_id):
        return Response('', status=404)
    return Response('{}', status=201, mimetype='application/json')


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, use_reloader=True, debug=True)
