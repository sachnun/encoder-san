from flask import Flask, Response
from flask_restful import Resource, Api, reqparse
from subtitle import Subtitle
from paste import KlgrthPaste

import requests

app = Flask(__name__)
api = Api(app)


class SubtitleAPI(Resource):
    def get(self):
        return {"hello": "world"}

    def post(self):
        # get data form request
        parser = reqparse.RequestParser()
        parser.add_argument("gd_id_ass", type=str, required=True, location="form")
        args = parser.parse_args()

        # generate subtitle
        try:
            url = "https://gdrive-index.dakunesu.workers.dev/?id=" + args["gd_id_ass"]
            res = requests.request(
                "COPY",
                url,
            )
            # return res.text
            if res.status_code == 200:
                subs = Subtitle(res.text)

                # return klgrth paste
                # klgrth = KlgrthPaste()
                # return {"url": klgrth.paste(subs.generate())}

                # return raw paste
                return Response(subs.generate(), mimetype="text/plain")
            else:
                return {"error": "subtitle not found"}, 404
        except Exception as e:
            return {"error": str(e)}, 500


api.add_resource(SubtitleAPI, "/")

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
