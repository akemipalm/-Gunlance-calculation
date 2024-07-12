import Tabulator from 'tabulator-tables';

// モンスターデータのCSV読み込み
fetch('/data/モンスター(2024.7.11).csv')
    .then(response => response.text())
    .then(data => {
        const monsterData = Papa.parse(data, { header: true }).data;

        // ガンランスデータのCSV読み込み
        fetch('/data/ガンランス(砲撃値).csv')
            .then(response => response.text())
            .then(data => {
                const gunlanceData = Papa.parse(data, { header: true }).data;

                // 砲術レベルに応じた補正値
                const gunnery = [1.1, 1.15, 1.2, 1.3, 1.4];

                // 溜め砲撃のダメージ計算
                function calculateDamage(grade, gunneryLevel) {
                    const damage = gunlanceData[grade - 1]['放射型(溜め)'];
                    return parseFloat(damage) * gunnery[gunneryLevel - 1];
                }

                // モンスターの討伐に必要な溜め砲撃数を計算
                function calculateMonsterKillCount(grade, gunneryLevel, monsterName) {
                    const damage = calculateDamage(grade, gunneryLevel);
                    const monster = monsterData.find(entry => entry['名前'] === monsterName);
                    
                    if (!monster) {
                        console.log(`モンスター名 '${monsterName}' が見つかりませんでした。`);
                        return null;
                    }

                    const result = {};
                    result['名前'] = monsterName;
                    Object.keys(monster).forEach(key => {
                        if (key !== '名前') {
                            result[key] = parseFloat((monster[key] / damage).toFixed(2));
                        }
                    });

                    return result;
                }

                // HTMLからの入力を受け取り、計算結果を表示する関数
                function calculateAndDisplay() {
                    const grade = parseInt(document.getElementById('grade').value);
                    const gunneryLevel = parseInt(document.getElementById('gunneryLevel').value);
                    const monsterName = document.getElementById('monsterName').value.trim();

                    const result = calculateMonsterKillCount(grade, gunneryLevel, monsterName);

                    if (result) {
                        // Tabulatorで表を作成する
                        const table = new Tabulator('#result', {
                            data: [result],
                            layout: 'fitColumns',
                            columns: [
                                { title: '名前', field: '名前', headerFilter: true },
                                { title: '星5', field: '星5', headerFilter: true },
                                { title: '星6', field: '星6', headerFilter: true },
                                { title: '星7', field: '星7', headerFilter: true },
                                { title: '星8', field: '星8', headerFilter: true },
                                { title: '星9', field: '星9', headerFilter: true },
                                { title: '星10', field: '星10', headerFilter: true }
                            ]
                        });
                    }
                }

                // 計算ボタンのイベントリスナーを設定
                document.getElementById('calculateButton').addEventListener('click', calculateAndDisplay);
            });
    });
