import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

DATA_FILE = "expenses.json"

# データを読み込む
def load_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as file:
                return json.load(file)
        except:
            pass
    return {"budget": 30000, "expenses": []}

data = load_data()
budget = data.get("budget", 30000)
expenses = data.get("expenses", [])

# データを保存する
def save_data():
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump({"budget": budget, "expenses": expenses},
                  file, ensure_ascii=False, indent=2)

# 画面を更新する
def refresh():
    expense_list.delete(0, tk.END)
    total = 0

    for item in expenses:
        total += item["amount"]
        expense_list.insert(
            tk.END,
            f'{item["category"]} | ¥{item["amount"]:,} | {item["memo"]}'
        )

    total_label.config(text=f"今月の支出：¥{total:,}")
    remaining = budget - total
    remaining_label.config(text=f"予算残り：¥{remaining:,}")

    if total >= budget:
        status_label.config(text="予算を超えています！", fg="#ff7777")
    elif total >= budget * 0.8:
        status_label.config(text="予算の80%を使いました", fg="#f4c542")
    else:
        status_label.config(text="順調です！", fg="#7ee787")

# 支出を登録する
def add_expense():
    amount_text = amount_entry.get().strip()
    memo = memo_entry.get().strip()
    category = category_box.get()

    if not amount_text:
        messagebox.showwarning("入力エラー", "金額を入力してください")
        return

    try:
        amount = int(amount_text)
        if amount <= 0:
            raise ValueError
    except ValueError:
        messagebox.showwarning("入力エラー", "正しい金額を入力してください")
        return

    expenses.append({
        "amount": amount,
        "category": category,
        "memo": memo
    })

    save_data()
    amount_entry.delete(0, tk.END)
    memo_entry.delete(0, tk.END)
    refresh()

# 支出を削除する
def delete_expense():
    selected = expense_list.curselection()

    if not selected:
        messagebox.showinfo("お知らせ", "削除する支出を選んでください")
        return

    expenses.pop(selected[0])
    save_data()
    refresh()

# 予算を変更する
def change_budget():
    global budget

    try:
        new_budget = int(budget_entry.get())
        if new_budget <= 0:
            raise ValueError
    except ValueError:
        messagebox.showwarning("入力エラー", "正しい予算を入力してください")
        return

    budget = new_budget
    save_data()
    budget_entry.delete(0, tk.END)
    refresh()

# ウィンドウを作る
root = tk.Tk()
root.title("SpendNote")
root.geometry("520x600")
root.configure(bg="#101410")

style = ttk.Style()
style.theme_use("clam")

# タイトル
tk.Label(
    root, text="SpendNote",
    font=("Arial", 24, "bold"),
    bg="#101410", fg="#69d18a"
).pack(pady=15)

tk.Label(
    root, text="毎日の支出を、かんたんに記録。",
    bg="#101410", fg="#b8c5ba"
).pack()

# 入力欄
input_frame = tk.Frame(root, bg="#18231b", padx=15, pady=15)
input_frame.pack(fill="x", padx=20, pady=15)

tk.Label(input_frame, text="金額（円）", bg="#18231b", fg="white").grid(
    row=0, column=0, sticky="w", pady=5
)

amount_entry = tk.Entry(
    input_frame, bg="#202a22", fg="white", insertbackground="white"
)
amount_entry.grid(row=0, column=1, sticky="ew", pady=5)

tk.Label(input_frame, text="カテゴリ", bg="#18231b", fg="white").grid(
    row=1, column=0, sticky="w", pady=5
)

category_box = ttk.Combobox(
    input_frame,
    values=["食費", "交通費", "買い物", "娯楽", "その他"],
    state="readonly"
)
category_box.current(0)
category_box.grid(row=1, column=1, sticky="ew", pady=5)

tk.Label(input_frame, text="メモ", bg="#18231b", fg="white").grid(
    row=2, column=0, sticky="w", pady=5
)

memo_entry = tk.Entry(
    input_frame, bg="#202a22", fg="white", insertbackground="white"
)
memo_entry.grid(row=2, column=1, sticky="ew", pady=5)

input_frame.columnconfigure(1, weight=1)

tk.Button(
    input_frame, text="支出を登録",
    command=add_expense,
    bg="#287a45", fg="white",
    relief="flat", pady=7
).grid(row=3, column=0, columnspan=2, sticky="ew", pady=10)

# 支出一覧
tk.Label(
    root, text="支出一覧",
    bg="#101410", fg="white",
    font=("Arial", 13, "bold")
).pack(anchor="w", padx=20)

expense_list = tk.Listbox(
    root, bg="#202a22", fg="white",
    selectbackground="#287a45",
    relief="flat", height=9
)
expense_list.pack(fill="both", expand=True, padx=20, pady=5)

tk.Button(
    root, text="選択した支出を削除",
    command=delete_expense,
    bg="#6b3030", fg="white",
    relief="flat"
).pack(fill="x", padx=20, pady=5)

# 合計
total_label = tk.Label(
    root, bg="#101410", fg="#69d18a",
    font=("Arial", 13, "bold")
)
total_label.pack(pady=5)

remaining_label = tk.Label(
    root, bg="#101410", fg="white",
    font=("Arial", 12)
)
remaining_label.pack()

status_label = tk.Label(
    root, bg="#101410",
    font=("Arial", 11, "bold")
)
status_label.pack(pady=5)

# 予算
budget_frame = tk.Frame(root, bg="#101410")
budget_frame.pack(pady=10)

tk.Label(
    budget_frame, text="予算（円）",
    bg="#101410", fg="white"
).pack(side="left")

budget_entry = tk.Entry(
    budget_frame, width=12,
    bg="#202a22", fg="white",
    insertbackground="white"
)
budget_entry.pack(side="left", padx=5)
budget_entry.insert(0, str(budget))

tk.Button(
    budget_frame, text="変更",
    command=change_budget,
    bg="#287a45", fg="white",
    relief="flat"
).pack(side="left")

refresh()
root.mainloop()