const fs = require('fs');
const Papa = require('papaparse');

const monsterCsv = fs.readFileSync('data/モンスター(2024.7.11).csv', 'utf8');
const gunlanceCsv = fs.readFileSync('data/ガンランス(砲撃値).csv', 'utf8');

const monsterData = Papa.parse(monsterCsv, { header: true }).data;
const gunlanceData = Papa.parse(gunlanceCsv, { header: true }).data;

// モンスターデータを加工
const processedMonsters = monsterData.map(row => ({
    name: row['名前'],
    stars: {
        '星5': parseInt(row['星5']),
        '星6': parseInt(row['星6']),
        '星7': parseInt(row['星7']),
        '星8': parseInt(row['星8']),
        '星9': parseInt(row['星9']),
        '星10': parseInt(row['星10'])
    }
}));

// ガンランスデータを加工
const processedGunlances = gunlanceData.map(row => ({
    grade: row['名前'],
    normal: parseInt(row['放射型(通常)']),
    charged: parseInt(row['放射型(溜め)'])
}));

// calculate.jsにデータを埋め込む
const jsContent = `
const monsterData = ${JSON.stringify(processedMonsters, null, 2)};
const gunlanceData = ${JSON.stringify(processedGunlances, null, 2)};
`;

fs.writeFileSync('calculate.js', jsContent);

console.log('calculate.js updated with latest data.');
