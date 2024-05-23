import pandas as pd
import aiohttp
import asyncio
import nest_asyncio
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk
from io import BytesIO
import math
import sys

# 使当前事件循环能够嵌套运行
nest_asyncio.apply()

# 创建主窗口
root = tk.Tk()
root.title("微信头像拼合图工具")
root.geometry("500x150")

# 计数器
downloaded_count = 0
valid_count = 0
invalid_count = 0

async def download_image(session, url):
    global downloaded_count, valid_count, invalid_count
    try:
        async with session.get(url, timeout=10) as response:
            if response.status == 200:
                img_data = await response.read()
                img = Image.open(BytesIO(img_data))
                downloaded_count += 1
                if img.size == (132, 132):  # 只保留132x132的正方形头像
                    valid_count += 1
                else:
                    invalid_count += 1
            else:
                downloaded_count += 1
                invalid_count += 1
    except Exception as e:
        downloaded_count += 1
        invalid_count += 1
    finally:
        # 实时更新进度信息
        progress_var.set(f"已读取 {downloaded_count}/{total_count} 张图片，其中包含 {valid_count} 张有效， {invalid_count} 张无效。")
        root.update_idletasks()
    return img if img.size == (132, 132) else None

async def download_all_images(urls):
    async with aiohttp.ClientSession() as session:
        tasks = [download_image(session, url) for url in urls]
        images = await asyncio.gather(*tasks)
        return [img for img in images if img is not None]

def start_download():
    global downloaded_count, valid_count, invalid_count, total_count
    
    # 重置计数器
    downloaded_count = 0
    valid_count = 0
    invalid_count = 0

    # 获取文件路径
    file_path = filedialog.askopenfilename()
    if not file_path:
        return

    # 读取CSV文件
    try:
        df = pd.read_csv(file_path)
    except Exception as e:
        messagebox.showerror("错误", f"无法读取文件：{e}")
        return

    # 过滤掉第一列中包含@chatroom字符的行，第三列为数字0的行，并提取第八列的URL
    global urls
    df_filtered = df[~df.iloc[:, 0].str.contains('@chatroom', na=False)]
    df_filtered = df_filtered[df_filtered.iloc[:, 2] != 0]
    df_filtered = df_filtered[df_filtered.iloc[:, 7].notna()]
    df_filtered = df_filtered[df_filtered.iloc[:, 0].str.contains('wxid', na=False)]
    urls = df_filtered.iloc[:, 7].tolist()
    total_count = len(urls)

    # 开始异步下载
    loop = asyncio.get_event_loop()
    images = loop.run_until_complete(download_all_images(urls))

    # 确保至少下载到一张有效图片
    if valid_count == 0:
        messagebox.showerror("错误", "没有下载到任何有效图片。")
        return

    # 计算目标图片的尺寸
    img_width, img_height = 132, 132
    total_images = len(images)

    # 计算画布所需的尺寸
    aspect_ratio = 16 / 9
    rows = math.ceil(math.sqrt(total_images / aspect_ratio))
    cols = math.ceil(total_images / rows)

    output_width = cols * img_width
    output_height = rows * img_height

    # 创建空白画布
    output_image = Image.new('RGB', (output_width, output_height), (255, 255, 255))

    # 依次将头像图片拼接到画布上
    x_offset, y_offset = 0, 0
    for img in images:
        output_image.paste(img, (x_offset, y_offset))
        x_offset += img_width
        if x_offset >= output_width:
            x_offset = 0
            y_offset += img_height

    # 保存输出图片
    output_file_path = filedialog.asksaveasfilename(defaultextension=".jpg", initialfile="微信头像拼合图_Keishi制作", filetypes=[("JPEG files", "*.jpg"), ("All files", "*.*")])
    if output_file_path:
        output_image.save(output_file_path)

        # 查找"你已被删"名单
        deleted_list = df[
            (df.iloc[:, 3].notna()) &  # 第四列有字
            (~df.iloc[:, 0].str.contains('@chatroom', na=False)) &  # 第一列无@chatroom字符
            (df.iloc[:, 7].isna())  # 没有头像链接
        ][[df.columns[3], df.columns[4]]]

        # 生成名单文本
        if not deleted_list.empty:
            summary_text = "你已被删名单：\n" + "\n".join([f"备注名: {row[0]}, 微信名: {row[1]}" for index, row in deleted_list.iterrows()])
        else:
            summary_text = "没有发现符合条件的‘你已被删’名单。"

        # 弹出信息框
        messagebox.showinfo("完成", f"图片已保存至: {output_file_path}\n\n图片导出成功，同时给你一个小惊喜，这里是程序自动总结的‘你已被删’名单：\n（名单并非完全正确，仅能查找到部分用户）\n\n{summary_text}")

# 创建上传文件按钮
upload_button = ttk.Button(root, text="上传CSV文件并下载图片", command=start_download)
upload_button.pack(pady=10)

# 创建进度标签
progress_var = tk.StringVar()
progress_label = ttk.Label(root, textvariable=progress_var)
progress_label.pack(pady=5)

# 创建作者信息标签
author_label = ttk.Label(root, text="作者: Keishi")
author_label.pack()

# 创建GitHub主页标签
github_label = ttk.Label(root, text="GitHub: https://github.com/Natsusomekeishi", foreground="blue", cursor="hand2")
github_label.pack()

def open_github(event):
    import webbrowser
    webbrowser.open_new(r"https://github.com/Natsusomekeishi")

github_label.bind("<Button-1>", open_github)

# 启动主循环
root.mainloop()
