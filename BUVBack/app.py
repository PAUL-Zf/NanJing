from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os

FILE_ABS_PATH = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
CORS(app)


@app.route('/api/test/counter/', methods=['POST'])
def update_counter():
    params = request.json
    counter = int(params['counter'])

    counter += 1

    resp = {'counter': counter}
    return jsonify(resp), 200, {"Content-Type": "application/json"}


@app.route('/api/test/hello/', methods=['POST'])
def hello_resp():
    params = request.json
    msg = int(params['msg'])
    print(msg)
    return "hello VUE"


@app.route('/api/test/fetchAllData/', methods=['POST'])
def fetch_data():
    # people & people-id切换
    data_path = '{}/data/people-id-figure-type-id.json'.format(FILE_ABS_PATH)
    with open(data_path, 'r', encoding='gbk') as input_file:
        data = json.load(input_file)
        return data


@app.route('/api/test/queryByName/', methods=['POST'])
def queryByName():
    params = request.json
    query_name = params['name']
    data_path = '{}/data/people.json'.format(FILE_ABS_PATH)
    with open(data_path, "r", encoding='utf-8') as f:
        data = json.load(f)

    # query certain person by name
    for person in data:
        if(person["人物"]["通用名称"]["值"] == query_name):
            target = person
            break

    # extract location and time
    experiences = target["人物"]["经历"]["事件"]
    events = []
    for ex in experiences:
        if "地点起止" not in ex:
            continue
        event = {}
        event['time'] = ex["时间起止"]["时间点"][0]
        event['name'] = ex["地点起止"]["时态点"][0]["通用名称"]
        event['location'] = ex["地点起止"]["时态点"][0]["坐标"].split(',')
        event['content'] = ex["概要"]
        events.append(event)

    return json.dumps(events, ensure_ascii=False)


if __name__ == '__main__':
    app.run()
