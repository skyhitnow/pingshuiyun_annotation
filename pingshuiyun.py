import tkinter as tk
import json

CHINESE_SPACE="　"   # 全角空格，用于对齐

# 加载平水韵部字典
with open("dicmap.json", "r", encoding="utf8") as f:
    PING_SHUI_YUN = json.loads(f.read())



def get_yunbu(char)->str:
    """获取汉字对应的平水韵部，若多音字且分属不同韵部，则返回所有韵部；若无则返回'未知'"""
    catalog_final=""
    for collection,catalog in PING_SHUI_YUN.items():
        if char in collection:
            catalog_final+=catalog
    return f"【{catalog_final}】" if catalog_final else "未知"


def analyze_text():
    input_text = text_input.get("1.0", tk.END).strip()
    if not input_text:
        result_display.config(state=tk.NORMAL)
        result_display.delete("1.0", tk.END)
        result_display.insert(tk.END, "请输入汉字文本。")
        result_display.config(state=tk.DISABLED)
        return

    result_display.config(state=tk.NORMAL)
    result_display.delete("1.0", tk.END)

    for line in input_text.split('\n'):
        if not line:
            result_display.insert(tk.END, "\n\n")
            continue

        for char in line:
            if '\u4e00' <= char <= '\u9fff':  # 汉字
                yun = get_yunbu(char)
                yun_format=yun.center(7, CHINESE_SPACE)
                yun_set=set()
                for shengdiao in ["平声","上声","入声","去声"]:
                    if shengdiao in yun:
                        yun_set.add(shengdiao)
                if len(yun_set)>1:
                    if "平声" not in yun_set and "入声" not in yun_set:
                        result_display.insert(tk.END, yun_format, "yunbu_ze")
                        result_display.insert(tk.END, char, "hanzi_ze")
                    else:
                        result_display.insert(tk.END, yun_format, "yunbu_mul")
                        result_display.insert(tk.END, char, "hanzi_mul")
                elif "平声" in yun_set:
                    result_display.insert(tk.END, yun_format, "yunbu_ping")
                    result_display.insert(tk.END, char, "hanzi_ping")
                elif "入声" in yun_set:
                    result_display.insert(tk.END, yun_format, "yunbu_ru")
                    result_display.insert(tk.END, char, "hanzi_ru")
                elif "上声" in yun_set or "去声" in yun_set:
                    result_display.insert(tk.END, yun_format, "yunbu_ze")
                    result_display.insert(tk.END, char, "hanzi_ze")
                else:
                    result_display.insert(tk.END, yun_format, "yunbu_ping")
                    result_display.insert(tk.END, char, "hanzi_char")
            else:
                result_display.insert(tk.END, char+"\n", "hanzi_char")

    result_display.config(state=tk.DISABLED)

# 创建主窗口
root = tk.Tk()
root.title("平水韵标注")
root.iconbitmap("yun.ico")
root.geometry("800x600")

# 尝试使用等宽中文字体（按优先级）
SM_SIZE=8
fonts_to_try = [
    ("Microsoft YaHei Mono", SM_SIZE),
    ("FangSong", SM_SIZE),          # 仿宋在某些系统下接近等宽
    ("Courier New", SM_SIZE),
    ("Courier", SM_SIZE),
]

# 检测可用字体
import tkinter.font as tkFont
available_font = tkFont.Font(family="Courier", size=8, weight="normal")  # 默认字体
for f in fonts_to_try:
    if tkFont.families().count(f[0]):
        available_font = f
        break
bold_font=tkFont.Font(font=available_font)
bold_font.configure(weight="bold",size=SM_SIZE*2)

# 输入框
tk.Label(root, text="请输入汉字文本：").pack(anchor='w', padx=10, pady=(10, 0))
text_input = tk.Text(root, height=5, width=80, font=("SimSun", 12))
text_input.pack(fill=tk.BOTH, expand=True,padx=10, pady=5)
text_input.insert("1.0","白日依山尽，黄河入海流。欲穷千里目，更上一层楼。")

# 按钮
tk.Button(root, text="分析平水韵", command=analyze_text, font=("SimSun", 12)).pack(pady=5)

# 结果显示区
tk.Label(root, text="平水韵标注结果(红色-平声，蓝色-仄声，绿色-入声，紫色-多音字)：").pack(anchor='w', padx=10, pady=(10, 0))
result_display = tk.Text(
    root, 
    state=tk.DISABLED,
    wrap=tk.WORD, 
    font=available_font
)
result_display.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

# 配置样式：韵部小一点、灰色；汉字正常
result_display.tag_configure("yunbu_ping", font=available_font, foreground="gray50")
result_display.tag_configure("yunbu_ze", font=available_font, foreground="gray50")
result_display.tag_configure("hanzi_ping", font=bold_font, foreground="red")
result_display.tag_configure("hanzi_ze", font=bold_font, foreground="blue")
result_display.tag_configure("yunbu_ru", font=available_font, foreground="gray50")
result_display.tag_configure("hanzi_ru", font=bold_font, foreground="green")
result_display.tag_configure("yunbu_space", font=available_font)
result_display.tag_configure("hanzi_char", font=bold_font)
result_display.tag_configure("yunbu_mul", font=available_font, foreground="gray50")
result_display.tag_configure("hanzi_mul", font=bold_font, foreground="purple")

root.mainloop()
