# WeChat-Avatar-Collage

WeChat-Avatar-Collage 是一个可以读取从 [MemoTrace](https://github.com/LC044/WeChatMsg/) 导出的联系人 CSV 文件并创建微信头像拼合图的工具。

## 功能

- 读取从 MemoTrace 导出的联系人 CSV 文件。
- 下载 CSV 文件中包含的微信头像链接。
- 将下载的头像图片拼接成一张 16:9 的图片。
- 自动生成“你已被删”名单，并在图片导出后显示。

## 安装

首先，确保你已经安装了所需的 Python 库。你可以使用以下命令安装这些库：

```bash
pip install pandas aiohttp nest_asyncio Pillow
```

## 使用方法

1. 克隆此仓库到本地：

```bash
git clone https://github.com/Natsusomekeishi/WeChat-Avatar-Collage.git
cd WeChat-Avatar-Collage
```

2. 运行 `WeChat.py` 脚本：

```bash
python WeChat.py
```

3. 点击 MemoTrace 程序左上角“数据”，再点击“导出联系人”。
4. 在弹出的窗口中，选择从 MemoTrace 导出的联系人 CSV 文件。
5. 程序将开始下载头像图片并拼接成一张图片，最后会在指定位置保存生成的图片。

## 过滤条件

- 仅处理第一列包含 `wxid` 字符且不包含 `@chatroom` 字符的行。
- 第三列不为 `0`。
- 第八列有头像链接。

## “你已被删”名单生成规则

- 第四列有字。
- 第一列不包含 `@chatroom` 字符。
- 第八列没有头像链接。
- 此名单经测试并不能包含所有相关用户，仅供娱乐。

## 作者

Keishi

## 贡献

欢迎提交问题（issues）和请求（pull requests）来帮助改进此项目。

## 许可证

此项目基于 GPL-3.0 许可证开源。

## 参考

- [MemoTrace](https://github.com/LC044/WeChatMsg/)
