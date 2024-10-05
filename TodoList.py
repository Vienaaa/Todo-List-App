import tkinter as tk
from tkinter import ttk, messagebox
from ttkbootstrap import Style
import json


class TodoListApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Todo List App")
        self.geometry("500x500")
        style = Style(theme="flatly")
        style.configure("Custon.TEntry", foreground="gray")

        # Tạo trường để nhập thêm các tasks
        self.task_input = ttk.Entry(self, font=("TkDefaultFont", 16), width=30, style="Custon.TEntry")
        self.task_input.pack(pady=10)

        # Set placeholder
        self.task_input.insert(0, "Nhấp vào để thêm...")

        # Ẩn placeholder khi nhấp chuột vào input
        self.task_input.bind("<FocusIn>", self.clear_placeholder)

        # Hiện lại placeholder khi click ra ngoài input
        self.task_input.bind("<FocusOut>", self.restore_placeholder)

        # tạo nút thêm task
        ttk.Button(self, text="Thêm", command=self.add_task).pack(pady=5)

        # Tạo hộp thoại hiển thị danh sách nhiệm vụ đã thêm
        self.task_list = tk.Listbox(self, font=("TkDefaultFont", 16), height=10, selectmode=tk.NONE)
        self.task_list.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Tạo nút đánh dấu các nhiệm vụ đã hoàn thành
        ttk.Button(self, text="Hoàn thành", style="success.TButton",
                   command=self.mark_done).pack(side=tk.LEFT, padx=10, pady=10)
        ttk.Button(self, text="Xóa", style="danger.TButton",
                   command=self.delete_task).pack(side=tk.RIGHT, padx=10, pady=10)
        
        # Tạo nút hiển thị các công việc đã hoàn thành
        ttk.Button(self, text="Xem công việc", style="info.TButton",
                   command=self.view_stats).pack(side=tk.BOTTOM, pady=10)
        
        self.load_tasks()
    
    def view_stats(self):
        done_count = 0
        total_count = self.task_list.size()
        for i in range(total_count):
            if self.task_list.itemcget(i, "fg") == "green":
                done_count += 1
        messagebox.showinfo("Bảng thống kê công việc", f"Số lượng: {total_count}\nĐã hoàn thành: {done_count}")

    def add_task(self):
        task = self.task_input.get()
        if task != "Enter your todo here...":
            self.task_list.insert(tk.END, task)
            self.task_list.itemconfig(tk.END, fg="orange")
            self.task_input.delete(0, tk.END)
            self.save_tasks()

    def mark_done(self):
        task_index = self.task_list.curselection()
        if task_index:
            self.task_list.itemconfig(task_index, fg="green")
            self.save_tasks()
    
    def delete_task(self):
        task_index = self.task_list.curselection()
        if task_index:
            self.task_list.delete(task_index)
            self.save_tasks()
    
    def clear_placeholder(self, event):
        if self.task_input.get() == "Nhấp vào để thêm...":
            self.task_input.delete(0, tk.END)
            self.task_input.configure(style="TEntry")

    def restore_placeholder(self, event):
        if self.task_input.get() == "":
            self.task_input.insert(0, "Nhấp vào để thêm...")
            self.task_input.configure(style="Custom.TEntry")

    def load_tasks(self):
        try:
            with open("tasks.json", "r") as f:
                data = json.load(f)
                for task in data:
                    self.task_list.insert(tk.END, task["text"])
                    self.task_list.itemconfig(tk.END, fg=task["color"])
        except FileNotFoundError:
            pass
    
    def save_tasks(self):
        data = []
        for i in range(self.task_list.size()):
            text = self.task_list.get(i)
            color = self.task_list.itemcget(i, "fg")
            data.append({"text": text, "color": color})
        with open("tasks.json", "w") as f:
            json.dump(data, f)

if __name__ == '__main__':
    app = TodoListApp()
    app.mainloop()
