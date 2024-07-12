# app.py

from flask import Flask, render_template, request
import pandas as pd
from tabulate import tabulate

app = Flask(__name__)

# データフレームの読み込み
df1 = pd.read_csv("モンスター(2024.7.11).csv", encoding="shift-jis")
df2 = pd.read_csv("ガンランス(砲撃値).csv")

# 砲術レベルに応じた補正値が格納された配列
gunnery = [1.1, 1.15, 1.2, 1.3, 1.4]

# メインページのルート
@app.route('/')
def index():
    return render_template('index.html')

# 結果を計算するページ
@app.route('/calculate', methods=['GET', 'POST'])
def calculate():
    if request.method == 'POST':
        grade = int(request.form['grade'])
        gunnery_level = int(request.form['gunnery_level'])
        monster_name = request.form['monster_name']

        # csvからグレードに応じたダメージ値(溜め砲撃)を取り込む
        damage = df2.iloc[grade - 1, 2]

        # 砲撃レベルに応じてダメージ値を補正する
        damage = damage * gunnery[gunnery_level - 1]

        # 名前が一致する行をフィルタリング
        filtered_df = df1[df1['名前'] == monster_name]

        if not filtered_df.empty:
            # 各列に対して計算を実行し、結果を準備
            result_dict = {'名前': monster_name}
            for column in filtered_df.columns:
                if column != '名前':  # 名前列を除外
                    result_dict[column] = round(filtered_df[column].values[0] / damage, 2)
            
            # 結果をテーブル形式で準備
            headers = result_dict.keys()
            rows = [result_dict.values()]

            return render_template('result.html', headers=headers, rows=rows)
        else:
            return render_template('not_found.html', monster_name=monster_name)

if __name__ == '__main__':
    app.run(debug=True)

