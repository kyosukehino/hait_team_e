from flask import Flask, render_template, request
from wtforms import Form, FloatField, SubmitField, validators, ValidationError
import numpy as np
from sklearn.externals import joblib

# 学習モデルを読み込み予測する
def predict(parameters):
    # モデル読み込み
    model = joblib.load('./ml_hiyoshi.pkl')
    params = parameters.reshape(1,-1)
    pred = model.predict(params)
    pred = int(pred[0])
    return pred

app = Flask(__name__)

# Flaskとwtformsを使い、index.html側で表示させるフォームを構築する
class HousePriceForm(Form):
    Age = IntergerField("Age(年)(築年数)",
                     [validators.InputRequired("この項目は入力必須です"),
                     validators.NumberRange(min=0, max=150)])

    Area  = FloatField("Area(㎡)(専有面積)",
                     [validators.InputRequired("この項目は入力必須です"),
                     validators.NumberRange(min=0, max=100)])

    Time = IntergerField("Time(分)(最寄駅までの徒歩の所要時間)",
                     [validators.InputRequired("この項目は入力必須です"),
                     validators.NumberRange(min=0, max=60)])

# html側で表示するsubmitボタンの表示
    submit = SubmitField("判定")

@app.route('/', methods = ['GET', 'POST'])
def predicts():
    form = HousePriceForm(request.form)
    if request.method == 'POST':
        if form.validate() == False:
            return render_template('index.html', form=form)
        else:
            Age = float(request.form["Age"])
            Area  = float(request.form["Area"])
            Time = float(request.form["Time"])

            x = np.array([Age, Area, Time])
            pred = predict(x)

            return render_template('result.html', pred=pred)
    elif request.method == 'GET':

        return render_template('index.html', form=form)

if __name__ == "__main__":
    app.run()
