from flask import Flask, request, json

app = Flask(__name__)


@app.route('/01-server')
def server01():
    return '这是服务器端响应内容'

@app.route('/02-server')
def srver02():
    cb = request.args['callback']
    dic = {
        'flightNo':'CA977',
        'from':'Beijing',
        'To':'LA',
        'Time':'00:30'
    }
    jsonStr = json.dumps(dic)
    return cb+'('+jsonStr+');'

@app.route('/03-jq-cross')
def jq_cross():
    cb = request.args.get('callback')
    dic = {
        'flightNo': 'CA977',
        'from': 'Beijing',
        'To': 'LA',
        'Time': '00:30'
    }
    jsonStr = json.dumps(dic)
    return cb+"("+jsonStr+")"





if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
