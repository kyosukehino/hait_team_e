import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.externals import joblib
#from sklearn.metrics import classification_report, accuracy_score
# import pickle

# データ取得
df_hiyoshi = pd.read_excel('suumo_tamagawa.xlsx', sep='\t', encoding='utf-16')

#立地を「路線+駅」と「徒歩〜分」に分割
splitted1 = df_hiyoshi['立地1'].str.split('歩', expand=True)
splitted1.columns = ['立地11', '立地12']

#分割したカラムを結合
df_hiyoshi = pd.concat([df_hiyoshi, splitted1], axis=1)

#分割前のカラムは分析に使用しないので削除しておく
df_hiyoshi.drop(['立地1','立地11'], axis=1, inplace=True)

#エンコードをcp932に変更しておく（これをしないと、replaceできない）
df_hiyoshi['賃料'].str.encode('cp932')
df_hiyoshi['管理費'].str.encode('cp932')
df_hiyoshi['築年数'].str.encode('cp932')
df_hiyoshi['専有面積'].str.encode('cp932')
df_hiyoshi['立地12'].str.encode('cp932')

#数値として扱いたいので、不要な文字列を削除
df_hiyoshi['賃料'] = df_hiyoshi['賃料'].str.replace(u'万円', u'')
df_hiyoshi['管理費'] = df_hiyoshi['管理費'].str.replace(u'円', u'')
df_hiyoshi['築年数'] = df_hiyoshi['築年数'].str.replace(u'新築', u'0') #新築は築年数0年とする
df_hiyoshi['築年数'] = df_hiyoshi['築年数'].str.replace(u'築', u'')
df_hiyoshi['築年数'] = df_hiyoshi['築年数'].str.replace(u'年', u'')
df_hiyoshi['専有面積'] = df_hiyoshi['専有面積'].str.replace(u'm', u'')
df_hiyoshi['立地12'] = df_hiyoshi['立地12'].str.replace(u'分', u'')

#「-」を0に変換
df_hiyoshi['管理費'] = df_hiyoshi['管理費'].replace('-',0)

#文字列から数値に変換
df_hiyoshi['賃料'] = pd.to_numeric(df_hiyoshi['賃料'])
df_hiyoshi['管理費'] = pd.to_numeric(df_hiyoshi['管理費'])
df_hiyoshi['築年数'] = pd.to_numeric(df_hiyoshi['築年数'])
df_hiyoshi['専有面積'] = pd.to_numeric(df_hiyoshi['専有面積'])
df_hiyoshi['立地12'] = pd.to_numeric(df_hiyoshi['立地12'])

#単位を合わせるために、管理費以外を10000倍。
df_hiyoshi['賃料'] = df_hiyoshi['賃料'] * 10000

#管理費は実質的には賃料と同じく毎月支払うことになるため、「賃料+管理費」を家賃を見る指標とする
df_hiyoshi['賃料+管理費'] = df_hiyoshi['賃料'] + df_hiyoshi['管理費']

#階を数値化。地下はマイナスとして扱う
df_hiyoshi['階'].str.encode('cp932')
df_hiyoshi['階'] = df_hiyoshi['階'].str.replace(u'階', u'')
df_hiyoshi['階'] = df_hiyoshi['階'].str.replace(u'B', u'-')
df_hiyoshi['階'] = pd.to_numeric(df_hiyoshi['階'])

#建物高さを数値化。地下は無視。
df_hiyoshi['建物高さ'].str.encode('cp932')
df_hiyoshi['建物高さ'] = df_hiyoshi['建物高さ'].str.replace(u'地下1地上', u'')
df_hiyoshi['建物高さ'] = df_hiyoshi['建物高さ'].str.replace(u'地下2地上', u'')
df_hiyoshi['建物高さ'] = df_hiyoshi['建物高さ'].str.replace(u'地下3地上', u'')
df_hiyoshi['建物高さ'] = df_hiyoshi['建物高さ'].str.replace(u'地下4地上', u'')
df_hiyoshi['建物高さ'] = df_hiyoshi['建物高さ'].str.replace(u'地下5地上', u'')
df_hiyoshi['建物高さ'] = df_hiyoshi['建物高さ'].str.replace(u'地下6地上', u'')
df_hiyoshi['建物高さ'] = df_hiyoshi['建物高さ'].str.replace(u'地下7地上', u'')
df_hiyoshi['建物高さ'] = df_hiyoshi['建物高さ'].str.replace(u'地下8地上', u'')
df_hiyoshi['建物高さ'] = df_hiyoshi['建物高さ'].str.replace(u'地下9地上', u'')
df_hiyoshi['建物高さ'] = df_hiyoshi['建物高さ'].str.replace(u'平屋', u'1')
df_hiyoshi['建物高さ'] = df_hiyoshi['建物高さ'].str.replace(u'階建', u'')
df_hiyoshi['建物高さ'] = pd.to_numeric(df_hiyoshi['建物高さ'])

#分割前のカラムは分析に使用しないので削除しておく
df_hiyoshi.drop(['賃料','管理費'], axis=1, inplace=True)

#並べ替え
df_hiyoshi = df_hiyoshi[['築年数','建物高さ','階','専有面積','立地12','賃料+管理費']]

# 学習
X = np.array(df_hiyoshi.loc[:, ['築年数','専有面積','立地12']])
y = np.array(df_hiyoshi.loc[:, ['賃料+管理費']])

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=0)

# ランダムフォレストによる学習
#ランダムフォレストのクラスを読み込み
from sklearn.ensemble import RandomForestClassifier
#ランダムフォレストのインスタンスを生成
rfc = RandomForestClassifier(random_state=0, n_estimators=10)
#モデルを学習
rfc.fit(X_train, y_train)

# 学習済みモデルの保存
joblib.dump(rfc, "ml_tamagawa.pkl", compress=True)
