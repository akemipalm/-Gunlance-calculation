from flask import Flask, render_template, request, jsonify
import pandas as pd
from tabulate import tabulate

app = Flask(__name__)

# CSVファイルの読み込み
df1 = pd.read_csv("csv/モンスター(2024.7.11).csv", encoding="shift-jis")
df2 = pd.read_csv("csv/ガンランス(砲撃値).csv")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    grade = int(request.form['grade'])
    gunnery_level = int(request.form['gunnery_level'])
    monster_name = request.form['monster_name']

    gunnery = [1.1, 1.15, 1.2, 1.3, 1.4]
    damage = df2.iloc[(grade - 1), 2]
    damage = damage * gunnery[gunnery_level - 1]

    filtered_df = df1[df1['名前'] == monster_name]

    if not filtered_df.empty:
        result_dict = {'名前': monster_name}
        for column in filtered_df.columns:
            if column != '名前':
                result_dict[column] = round(filtered_df[column].values[0] / damage, 2)

        result_df = pd.DataFrame([result_dict])
        result_html = tabulate(result_df, headers='keys', tablefmt='html', showindex=False)

        return jsonify({'result': result_html})
    else:
        return jsonify({'error': f"モンスター名 '{monster_name}' が見つかりませんでした。"})

if __name__ == '__main__':
    app.run(debug=True)
