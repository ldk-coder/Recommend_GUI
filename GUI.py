import tkinter as tk
from tkinter import messagebox
import argparse
import os
import time
import numpy as np
import torch
import csv
import test
from Dataset import TrainingDataset, data_load

data_path ='movielens'
num_user, num_item, train_edge, user_item_dict, v_feat, a_feat, t_feat = data_load(data_path)

data_list = []
with open('title.csv', mode='r', newline='', encoding='GBK') as file:
    reader = csv.reader(file)
    for row in reader:
        data_list.append(row)
data_list = [item for sublist in data_list for item in sublist]
class Application(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.master = master
        self.pack()
        self.createWidget()
        self.config(bg="white")
        test.main()
        self.pred_results = test.get_pred_results()
        self.user_item_dict=user_item_dict
        self.data_list=data_list
        # print(" self.pred_results", self.pred_results)
    def createWidget(self):
        self.lable1 = tk.Label(self, text="欢迎进入MMGCN推荐系统", width=40, height=6, font=("黑体", 30), bg="white")
        self.lable1.pack()

        self.button1 = tk.Button(self, text="进入系统", command=self.open_new_window, width=18, height=3, bg="white",
                                 font=("黑体", 16))
        self.button1.pack()

        self.button2 = tk.Button(self, text="退出", command=root.destroy, width=16, height=2, bg="white",
                                 font=("黑体", 12))
        self.button2.pack()

        global photo
        photo = tk.PhotoImage(file="./Data/movielens/logo.gif")
        self.lable2 = tk.Label(self, image=photo, bg="white")
        self.lable2.pack()

    def open_new_window(self):
        messagebox.showinfo("MMGCN视频推荐系统", "欢迎进入MMGCN视频推荐系统!")
        new_window = tk.Toplevel(self.master)  # 创建一个新的窗口
        new_window.title("MMGCN推荐系统")  # 设置新窗口的标题
        new_window.geometry("800x1200")  # 设置新窗口的大小

        label = tk.Label(new_window, text="MMGCN推荐系统!", font=("黑体", 16))
        label.pack(pady=50)

        label_input = tk.Label(new_window, text="请输入用户ID：", font=("黑体", 16))
        label_input.pack(pady=20)

        self.entry = tk.Entry(new_window, font=("黑体", 16))  # 将 entry 作为实例属性
        self.entry.pack(pady=10)
        print_button = tk.Button(new_window, text="获取推荐", command=self.print_number, font=("黑体", 16))
        print_button.pack()
        self.result_label1 = tk.Label(new_window, text="", font=("黑体", 10), bg="white",wraplength=800)  # 将 result_label 作为实例属性
        self.result_label1.pack(pady=20)

        self.result_label = tk.Label(new_window, text="", font=("黑体", 10), bg="white",wraplength=700)  # 将 result_label 作为实例属性
        self.result_label.pack(pady=20)

        close_button = tk.Button(new_window, text="关闭页面", command=new_window.destroy, font=("黑体", 16))
        close_button.pack()

    def print_number(self):
        try:
            # 获取输入的号码
            user_input = self.entry.get()
            recommended_dict, user_item_dict_number = self.recommend_number(user_input)

            # 如果 recommended_dict 是一个字典，提取所有的推荐电影ID
            recommended_numbers = list(recommended_dict)
            print(recommended_numbers, user_item_dict_number)
            print(len(self.data_list))

            # 根据推荐的电影ID列表来获取电影标题
            recommended_movies = ', '.join(
                [self.data_list[idx] for idx in recommended_numbers if 0 <= idx < len(self.data_list)]
            ) if recommended_numbers else "无推荐电影"

            if isinstance(user_item_dict_number, list):
                watched_movies = ', '.join(
                    [self.data_list[idx] for idx in user_item_dict_number if 0 <= idx < len(self.data_list)]
                )
            else:
                watched_movies = "该用户没有观看记录"

            # 显示推荐的电影和曾经看过的电影
            self.result_label.config(text=f"推荐电影: {recommended_movies}")
            self.result_label1.config(text=f"曾经看过电影: {watched_movies}")

        except Exception as e:
            messagebox.showerror("错误", f"输入无效，请重新输入号码！\n{str(e)}")

    def recommend_number(self, input_number):
        try:
            input_number = int(input_number)
            Pred_results = self.pred_results
            user_item_dict = self.user_item_dict
            user_item_dict_number = user_item_dict.get(input_number, [])

            # 确保返回的是整数索引或者默认值
            recommended_number = Pred_results.get(input_number, {})
            return recommended_number, user_item_dict_number

        except ValueError:
            return {}, []  # 如果输入不是数字，返回空字典和空列表
def say_hello():
    messagebox.showinfo("MMGCN视频推荐系统", "欢迎进入MMGCN视频推荐系统!")  # 显示一个窗口，出现内容

root = tk.Tk()  # 创建一个页面
root.title("MMGCN视频推荐系统")  # 第一个界面的名称
root.geometry("600x600")
root.config(bg="white")
app = Application(master=root)
root.mainloop()
