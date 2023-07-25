import tkinter as tk
from tkcalendar import Calendar
from tkinter import ttk, Entry, Button, Label, Text, Checkbutton, IntVar, messagebox
import datetime
import pymysql.cursors

# 保存日程的列表
schedules = []

# 连接数据库
def connect_db():
    return pymysql.connect(host='10.10.10.3', user='kali', password='19841122Cy!', db='scheduleDB', charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)

# 显示日程的函数
def show_schedules(frame):
    for widget in frame.winfo_children():
        widget.destroy()
    for schedule in schedules:
        var = IntVar()
        schedule['var'] = var
        Checkbutton(frame, text=f"{schedule['start']} - {schedule['end']}: {schedule['note']}", variable=var).pack(anchor="w")

# 从数据库中读取日程
def load_schedules(frame):
    schedules.clear()  # 清除旧的日程
    with connect_db().cursor() as cursor:
        cursor.execute("SELECT id, start_time, end_time, note FROM schedules")
        for row in cursor.fetchall():
            schedules.append({'id': row['id'], 'start': row['start_time'], 'end': row['end_time'], 'note': row['note']})
    show_schedules(frame)

# 添加日程的函数
def add_schedule(frame):
    def add_schedule_ok():
        start, end, note = start_time_text.get(), end_time_text.get(), note_entry.get()
        schedules.append({'start': start, 'end': end, 'note': note})

        # 插入到数据库中
        with connect_db().cursor() as cursor:
            cursor.execute("INSERT INTO schedules (start_time, end_time, note) VALUES (%s, %s, %s)", (start, end, note))
        dialog.destroy()
        load_schedules(frame)  # 重新加载日程

    def start_calendar(entry_widget):
        def print_sel():
            entry_widget.configure(state="normal")
            entry_widget.delete(0, tk.END)
            entry_widget.insert("0", str(cal.selection_get()) + " " + str(hour.get()) + ":" + str(minute.get()))
            entry_widget.configure(state="disabled")
            top.destroy()

        top = tk.Toplevel()
        top.geometry("300x250")
        cal = Calendar(top, font="Arial 14", selectmode='day', locale='zh_CN')
        cal.place(x=0, y=0, width=300, height=200)
        values = [f"{i:02d}" for i in range(60)]
        hour = ttk.Combobox(master=top, values=values[:24], state="readonly", width=5)
        hour.place(x=10, y=220)
        hour.current(datetime.datetime.now().hour)  # 设置默认的小时为当前的小时
        Label(top, text="小时").place(x=70, y=220)
        minute = ttk.Combobox(master=top, values=values, state="readonly", width=5)
        minute.place(x=100, y=220)
        minute.current(datetime.datetime.now().minute)  # 设置默认的分钟为当前的分钟
        Label(top, text="分钟").place(x=160, y=220)
        Button(top, text="OK", command=print_sel).place(x=240, y=220)

    dialog = tk.Toplevel(root)
    dialog.geometry("400x200")
    start_time = Button(dialog, text="Start Time", command=lambda: start_calendar(start_time_text)).place(x=10, y=10)
    start_time_text = Entry(dialog, width=20, state="disabled")
    start_time_text.place(x=100, y=10)
    end_time = Button(dialog, text="End Time", command=lambda: start_calendar(end_time_text)).place(x=10, y=40)
    end_time_text = Entry(dialog, width=20, state="disabled")
    end_time_text.place(x=100, y=40)
    Label(dialog, text="Note").place(x=10, y=70)
    note_entry = Entry(dialog, width=20)
    note_entry.place(x=100, y=70)
    Button(dialog, text='OK', command=add_schedule_ok).place(x=150, y=100)

# 删除选定的日程
def delete_schedules(frame):
    selected_schedules = [schedule for schedule in schedules if schedule['var'].get() > 0]
    if len(selected_schedules) == 0:
        return
    if messagebox.askyesno("Delete schedules", "Do you want to delete the selected schedules?"):
        with connect_db().cursor() as cursor:
            for schedule in selected_schedules:
                cursor.execute("DELETE FROM schedules WHERE id=%s", (schedule['id'],))
                schedules.remove(schedule)
        load_schedules(frame)  # 重新加载日程

# root = tk.Tk()
# root.geometry("400x400")
# root.resizable(False, False)  # 禁止调整窗口大小
# frame = tk.Frame(root)
# frame.pack()


root = tk.Tk()
root.geometry("500x500")
root.resizable(False, False)  # 禁止调整窗口大小
frame = tk.Frame(root, bd=2, relief='sunken', highlightbackground="red")
frame.place(x=50, y=50, width=400, height=300)

Button(root, text="Delete selected schedules", command=lambda: delete_schedules(frame)).pack(side='bottom')
Button(root, text="Add schedule", command=lambda: add_schedule(frame)).pack(side='bottom')

load_schedules(frame)
root.mainloop()
