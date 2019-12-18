from flask import Flask, render_template, request
from wtforms import Form, IntegerField, StringField, FloatField, SubmitField, validators, ValidationError
import numpy as np
from sklearn.externals import joblib

app = Flask(__name__)

# Flaskとwtformsを使い、index.html側で表示させるフォームを構築する
class HousePriceForm(Form):
    Station = StringField("Station(最寄駅)",
                     [validators.InputRequired("この項目は入力必須です")])


    Age = IntegerField("Age(年)(築年数)",
                     [validators.InputRequired("この項目は入力必須です"),
                     validators.NumberRange(min=0, max=150)])

    Area  = FloatField("Area(㎡)(専有面積)",
                     [validators.InputRequired("この項目は入力必須です"),
                     validators.NumberRange(min=0, max=100)])

    Time = IntegerField("Time(分)(最寄駅までの徒歩の所要時間)",
                     [validators.InputRequired("この項目は入力必須です"),
                     validators.NumberRange(min=0, max=60)])

# html側で表示するsubmitボタンの表示
    submit = SubmitField("判定")

# 学習モデルを読み込み予測する
def predict(parameters, Station):
    # モデル読み込み
    if Station == "日吉":
        model = joblib.load('./ml_hiyoshi.pkl')
        params = parameters.reshape(1,-1)
        pred = model.predict(params)
        pred = int(pred[0])
        return pred
    
    if Station == "目黒":
        model =  joblib.load('./ml_meguro.pkl')
        params = parameters.reshape(1,-1)
        pred = model.predict(params)
        pred = int(pred[0])
        return pred

    if Station == "多摩川":
        model = joblib.load('./ml_tamagawa.pkl')
        params = parameters.reshape(1,-1)
        pred = model.predict(params)
        pred = int(pred[0])
        return pred

    if Station == "武蔵小杉":
        model = joblib.load('./ml_musashikosugi.pkl')
        params = parameters.reshape(1,-1)
        pred = model.predict(params)
        pred = int(pred[0])
        return pred

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
            Station = str(request.form["Station"])
            x = np.array([Age, Area, Time])
            pred = predict(x, Station)
            return render_template('result.html', pred=pred)
    elif request.method == 'GET':

        return render_template('index.html', form=form)

if __name__ == "__main__":
    app.run()
