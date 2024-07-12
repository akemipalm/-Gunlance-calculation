from flask import Flask, render_template, request
import pandas as pd
from tabulate import tabulate

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        grade = request.form['grade']
        gunnery_level = request.form['gunnery_level']
        monster_name = request.form['monster_name']

        df1 = pd.read_csv("csv/モンスター(2024.7.11).csv", encoding="shift-jis")
        df2 = pd.read_csv("csv/ガンランス(砲撃値).csv")

        gunnery = [1.1, 1.15, 1.2, 1.3, 1.4]

        damage = df2.iloc[(int(grade) - 1), 2]
        damage = damage * gunnery[int(gunnery_level) - 1]

        filtered_df = df1[df1['名前'] == monster_name]

        if not filtered_df.empty:
            result_dict = {'名前': monster_name}
            for column in filtered_df.columns:
                if column != '名前':
                    result_dict[column] = round(filtered_df[column].values[0] / damage, 2)

            result_df = pd.DataFrame([result_dict])
            result = tabulate(result_df, headers='keys', tablefmt='html', showindex=False)
            result_df.to_csv('result.csv', index=False)
        else:
            result = f"モンスター名 '{monster_name}' が見つかりませんでした。"
        return render_template('index.html', result=result)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
