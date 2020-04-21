from django.shortcuts import render

# Create your views here.

from keras.preprocessing import image
from keras.models import Sequential
from keras.models import load_model
from keras.applications.resnet50 import preprocess_input, decode_predictions
from django.http import JsonResponse
import json
import numpy as np

# 加载模型
model = Sequential()
model = load_model('modelFile/model.h5')

def recognizePic(request):
    if request.method == "POST":
        req = json.loads(request.body)
        # 获取filePath图片
        filePath = req.get("filePath")
        # 更改图片格式
        img = image.load_img(filePath, target_size=(32, 32))
        # 把图片转化为数组
        x = image.img_to_array(img)
        # 合并数组
        x = np.expand_dims(x, axis=0)
        # 输出特征
        x = preprocess_input(x)

        # 预测得分
        preds = model.predict_classes(x)
        num = preds[0]
        # 打印出类别
        list = ['飞机', '汽车', '小鸟', '猫咪', '麋鹿', '狗', '青蛙', '马', '船', '卡车']
        return JsonResponse({"status": "200", "data": list[num]}, json_dumps_params={'ensure_ascii': False})
