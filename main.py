import initializePlateTemperature4AF
import calculatePlateTemperature4AF
import initializeDelta_t4AF
import numpy as np
from flask import Flask, request
from waitress import serve

app = Flask(__name__)

tt = initializePlateTemperature4AF.initialize()
bb = calculatePlateTemperature4AF.initialize()
cc = initializeDelta_t4AF.initialize()


# 初始化数据接口
@app.route('/init', methods=['POST'])
def init():
    json_data = request.json
    length = np.mat([json_data["length"]], float)
    width = np.mat([json_data["width"]], float)
    thickness = np.mat([json_data["thickness"]], float)
    init_temp = np.mat([json_data["initial_hot_temp"]], float)

    wow = tt.initializePlateTemperature4AF(json_data["plate_no"], json_data["plate_grade"], length, width, thickness, init_temp)
    ok = cc.initializeDelta_t4AF(json_data["plate_no"], json_data["plate_grade"], length, width, thickness, init_temp)
    return {"temp": wow[0].toarray().tolist(), "step": ok}


# 计算接口
@app.route('/calc', methods=['POST'])
def calc():
    json_data = request.json

    length = np.mat([json_data["length"]], float)
    width = np.mat([json_data["width"]], float)
    thickness = np.mat([json_data["thickness"]], float)
    speed = np.mat([json_data["speed"]], float)
    head_location = np.mat([json_data["head_location"]], float)
    up = np.mat(json_data["up"], float)
    down = np.mat(json_data["down"], float)
    delt = np.mat([json_data["delt"]], float)
    target = np.mat([json_data["target"]], float)
    pre_temp = np.mat(json_data["pre_temp"], float)

    ojb = bb.calculatePlateTemperature4AF(json_data["id"], json_data["grade"], length, width, thickness, speed, head_location, up, down,
                                          delt, target, pre_temp)
    return {"temp": ojb[0].toarray().tolist()}


if __name__ == "__main__":
    serve(app, host='127.0.0.1', port=5000)
    # app.run(port=5000, debug=True)

    tt.terminate()
    bb.terminate()
    cc.terminate()
    tt.exit()
    bb.exit()
    cc.exit()
