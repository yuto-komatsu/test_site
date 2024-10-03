import streamlit as st
import datetime
from datetime import date
from openpyxl import load_workbook
from io import BytesIO
import openpyxl
from openpyxl.styles import Border, Side, Font
from openpyxl.styles.alignment import Alignment

# セッション状態を初期化
if 'uploaded' not in st.session_state:
    st.session_state['uploaded'] = False
if 'kibou_uploaded' not in st.session_state:
    st.session_state['kibou_uploaded'] = False

# スタイルの設定（変数名は変更なし）
border_topthick = Border(top=Side(style='thick', color='000000'), left=Side(style='thick', color='000000'), right=Side(style='thick', color='000000'))
border_bottomthick = Border(bottom=Side(style='thick', color='000000'), left=Side(style='thick', color='000000'), right=Side(style='thick', color='000000'))
# 他のスタイルの設定はそのまま...

band_list = {}
week = {}
st.session_state["page_control"] = 0


def change_page():
    # ページ切り替えボタンコールバック
    st.session_state["page_control"] += 1

def band_list_making(sheet):
    i = 1
    while sheet.cell(row=5 + i, column=2).value:
        st.session_state[band_list[i]] = sheet.cell(row=5 + i, column=2).value
        i += 1
    band_sum = len(st.session_state[band_list])
    return band_sum

def option_select():
    max_practice = st.selectbox(
        '最大練習回数',
        [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        index=0,
        placeholder="練習回数を選択してください"
    )
    return max_practice

def input_date(start_day, end_day):
    book = openpyxl.Workbook()
    for i in range(1, band_sum + 1):
        book.create_sheet(index=0, title=band_list[i])
        sheet = book[band_list[i]]
        for t in range(1, 8):
            sheet.cell(row=2 + t, column=2).value = str(t) + "限"
        calc_day = start_day
        j = 1
        while calc_day <= end_day:
            sheet.cell(row=2, column=2 + j).value = str(calc_day.month) + "/" + str(calc_day.day)
            j += 1
            calc_day += datetime.timedelta(days=1)

    if 'Sheet' in book.sheetnames:
        book.remove(book['Sheet'])

    buffer = BytesIO()
    book.save(buffer)
    buffer.seek(0)

    st.download_button(
        label="ダウンロード",
        data=buffer,
        file_name='downloaded_file2.xlsx',
        mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )

# Webアプリのタイトル
st.title('シフトスケジュール最適化')

uploaded_file_path = 'シフト希望表.xlsx'

# ファイルをバイトとして読み込む
# with open(uploaded_file_path, 'rb') as file:
#     band_listfile = file.read()

st.header('１．参加バンドの登録')
st.caption('ダウンロードボタンからテンプレートをダウンロードして、出演バンドを記入してください。')
st.caption('記入を終えたファイルをアップロードしてください。')

# st.download_button(
#     label="テンプレートをダウンロード",
#     data=band_listfile,
#     file_name='downloaded_file.xlsx',
#     mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
# )

st.session_state["uploaded_file1"] = st.file_uploader("バンド名簿をアップロード", type=["xlsx"], on_change=change_page)


if "page_control" in st.session_state and st.session_state["page_control"] == 1:
    # st.session_state['uploaded'] = True
    st.header('２．ライブ情報の入力')
    book = load_workbook(st.session_state["uploaded_file1"])
    st.session_state["sheet"] = book["概要"]
    band_sum = band_list_making(st.session_state["sheet"])

    st.write(st.session_state[band_list])



#     start_day = st.date_input('シフト開始日を入力してください。', datetime.date(2024, 8, 22))
#     end_day = st.date_input('シフト終了日を入力してください。', datetime.date(2024, 9, 9))
#     if start_day > end_day:
#         st.error('開始日は終了日より後の日付を入力してください。')
#         st.stop()

#     day_sum = (end_day - start_day + datetime.timedelta(days=1)).days
#     max_practice = option_select()
#     vacation = st.toggle("長期休暇期間")
#     d = st.toggle("部室利用禁止日あり")

#     if st.button("入力完了"):
#         st.header('３．練習希望日時の入力')
#         input_date(start_day, end_day)
#         st.write("記入を終えたファイルをアップロードしてください。")

#         kibou_file = st.file_uploader("シフト希望表をアップロード", type=["xlsx"])
#         if kibou_file is not None:
#             st.session_state['kibou_uploaded'] = True
#             st.session_state['kibou_file'] = kibou_file  # ファイルをセッションに保存

# if st.session_state['kibou_uploaded']:
#     st.header('４．最適化の実行')
#     try:
#         # セッションからファイルを読み込む
#         kibou_file = st.session_state['kibou_file']
#         book = load_workbook(kibou_file)
#         st.success('ファイルが正常に読み込まれました。')
#         # 最適化の処理をここに追加
#     except Exception as e:
#         st.error(f'ファイルの読み込みに失敗しました: {e}')
