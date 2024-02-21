from flask_restful import Resource


class IndexApi(Resource):
    def get(self):
        return {'response': 'steph app'}, 200
