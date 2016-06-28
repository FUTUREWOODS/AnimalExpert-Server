import time
import sqlite3

conn = sqlite3.connect("./animal.db")
cur = conn.cursor()

coordinates_data = [
    ['ジャイアントパンダ', '35.71642608370434', '139.77241694927215']
    , ['シロフクロウ', '35.71735000000000', '139.77222300000000']
    , ['オオタカ', '35.71736500000000', '139.77225900000000']
    , ['オジロワシ', '35.71764700000000', '139.77231800000000']
    , ['オオワシ', '35.71757300000000', '139.77227800000000']
    , ['ダルマワシ', '35.71751900000000', '139.77226000000000']
    , ['コンドル', '35.71733700000000', '139.77226500000000']
    , ['インドライオン', '35.71786500000000', '139.77160300000000']
    , ['スマトラトラ', '35.71799400000000', '139.77155600000000']
    , ['シロテテナガザル', '35.71814400000000', '139.77126100000000']
    , ['ニシローランドゴリラ', '35.71795429033892', '139.77045893669128']
    , ['ミナミコアリクイ', '35.71766800000000', '139.77067800000000']
    , ['アフリカクロトキ', '35.71711400000000', '139.77142800000000']
    , ['アジアゾウ', '35.71655729176538', '139.77163106203080']
    , ['アビシニアコロブス', '35.71624800000000', '139.77146600000000']
    , ['オグロプレーリードッグ', '35.71617800000000', '139.77139500000000']
    , ['ニホンザル', '35.71639886208784', '139.77082170546055']
    , ['アメリカバク', '35.71751600000000', '139.77104300000000']
    , ['ホッキョクグマ', '35.71662900000000', '139.77043200000000']
    , ['シュモクドリ', '35.71694800000000', '139.77085700000000']
    , ['オグロヅル', '35.71702400000000', '139.77094400000000']
    , ['ヘビクイワシ', '35.71708300000000', '139.77103200000000']
    , ['タンチョウ', '35.71712600000000', '139.77113600000000']
    , ['ワライカワセミ', '35.71732000000000', '139.77044100000000']
    , ['オニオオハシ', '35.71727500000000', '139.77034800000000']
    , ['カンムリシロムク', '35.71726300000000', '139.77047600000000']
    , ['エゾヒグマ', '35.71681700000000', '139.77090600000000']
    , ['ニホンツキノワグマ', '35.71684900000000', '139.77113200000000']
    , ['マレーグマ', '35.71706100000000', '139.77128000000000']
    , ['コツメカワウソ', '35.71708000000000', '139.77124300000000']
    , ['アカガシラカラスバト', '35.71710800000000', '139.77211200000000']
    , ['スバールバルライチョウ', '35.71663700000000', '139.77021700000000']
    , ['カリフォルニアアシカ', '35.71674900000000', '139.77035200000000']
    , ['ニホンアナグマ', '35.71691700000000', '139.77118300000000']
    , ['パラワンコクジャク', '35.71719200000000', '139.77027900000000']
    , ['シロハラハイイロエボシドリ', '35.71726300000000', '139.77047600000000']
    , ['ゼニガタアザラシ', '35.71674900000000', '139.77035200000000']
    , ['ハダカデバネズミ', '35.71477900000000', '139.76918400000000']
    , ['コビトマングース', '35.71477900000000', '139.76918400000000']
    , ['ケープハイラックス', '35.71477900000000', '139.76918400000000']
    , ['オリイオオコウモリ', '35.71477900000000', '139.76918400000000']
    , ['マタコミツオビアルマジロ', '35.71477900000000', '139.76918400000000']
    , ['セバタンビヘラコウモリ', '35.71498000000000', '139.76923500000000']
    , ['カナダヤマアラシ', '35.71498000000000', '139.72623500000000']
    , ['カバ', '35.71492016990860', '139.76857736706734']
    , ['コビトカバ', '35.71498900000000', '139.76873500000000']
    , ['キリン', '35.71438879223247', '139.76825751364230']
    , ['アイアイ', '35.71323700000000', '139.76927100000000']
    , ['ハイイロジェントルキツネザル', '35.71323700000000', '139.76927100000000']
    , ['オカピ', '35.71411439089776', '139.76828902959824']
    , ['ヒガシクロサイ', '35.71466300000000', '139.76854300000000']
    , ['ハシビロコウ', '35.71415400000000', '139.76906300000000']
    , ['クロシロエリマキキツネザル', '35.71330700000000', '139.76854300000000']
    , ['ワオキツネザル', '35.71377500000000', '139.76960700000000']
    , ['フォッサ', '35.71337100000000', '139.76962400000000']
    , ['ホウシャガメ', '35.71359934139698', '139.76961135864258']
    , ['オオカンガルー', '35.71433500000000', '139.76951700000000']
    , ['タテガミオオカミ', '35.71438000000000', '139.76948300000000']
    , ['ケープペンギン', '35.71412500000000', '139.76954100000000']
    , ['ベニイロフラミンゴ', '35.71408700000000', '139.76912400000000']
    , ['アカカワイノシシ', '35.71453500000000', '139.76922000000000']
    , ['ニホンコウノトリ', '35.71425900000000', '139.77066100000000']
    , ['レッサーパンダ', '35.71421800000000', '139.77095900000000']
    , ['アフリカタテガミヤマアラシ', '35.71415200000000', '139.77069500000000']
    , ['キンカジュー', '35.71477900000000', '139.76918400000000']
    , ['ミーアキャット', '35.71477900000000', '139.76918400000000']
    , ['ショウガラゴ', '35.71477900000000', '139.76918400000000']
    , ['ワタボウシタマリン', '35.71477900000000', '139.76918400000000']
    , ['ハートマンヤマシマウマ', '35.71499000000000', '139.76891200000000']
    , ['バーバリーシープ', '35.71499000000000', '139.76891200000000']
    , ['オオサンショウウオ', '35.71469400000000', '139.76874000000000']
    , ['イリエワニ', '35.71359000000000', '139.76893400000000']
    , ['オーストラリアハイギョ', '35.71352200000000', '139.76880900000000']
    , ['スッポンモドキ', '35.71346500000000', '139.76880000000000']
    , ['ガラパゴスゾウガメ', '35.71329700000000', '139.76885600000000']
    , ['ボールニシキヘビ', '35.71343300000000', '139.76872300000000']
    , ['グリーンイグアナ', '35.71345000000000', '139.76866200000000']
    , ['ニシアフリカコガタワニ', '35.71352300000000', '139.76887200000000']
    , ['オオアナコンダ', '35.71347300000000', '139.76876000000000']
    , ['ハゲガオホウカンチョウ', '35.71699900000000', '139.77208300000000']
    , ['ハクビシン', '35.71707700000000', '139.77136400000000']
    , ['ユーラシアカワウソ', '35.71735000000000', '139.77207400000000']
    , ['コサンケイ', '35.71790700000000', '139.77162560000000']
    , ['ニホンキジ', '35.71714400000000', '139.77215500000000']
    , ['ジェフロイクモザル', '35.71615000000000', '139.77124600000000']
    , ['アミメニシキヘビ', '35.71340700000000', '139.76875800000000']
]

sql = "SELECT id FROM animals"
cur.execute(sql)

dummy_id = 999000

for coordinates in coordinates_data:
    sql = "SELECT name FROM animals WHERE name = ?"
    cur.execute(sql, [coordinates[0]])

    if len(cur.fetchall()) != 1:
        print("not exist in DB: {} ".format(coordinates[0]))
        sql = "INSERT INTO animals(id, name, longitude, latitude) VALUES(?,?,?,?)"
        cur.execute(sql, [dummy_id, coordinates[0], coordinates[1], coordinates[2]])
        dummy_id += 1

    else:
        sql = "UPDATE animals SET " \
              "longitude=?," \
              "latitude=?" \
              "WHERE name = ?"
        cur.execute(sql, [coordinates[1], coordinates[2], coordinates[0]])
    time.sleep(0.5)

conn.commit()
conn.close()