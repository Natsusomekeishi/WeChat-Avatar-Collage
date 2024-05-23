以下是更新后的 `README.md` 文件内容示例，包含你的项目地址和 GPL-3.0 许可证信息：

```markdown
# WeChat-Avatar-Collage

WeChat-Avatar-Collage 是一个可以读取从 [MemoTrace](https://github.com/LC044/WeChatMsg/) 导出的 CSV 文件并创建微信头像拼合图的工具。

## 描述

该工具可以从 MemoTrace 导出的 CSV 文件中提取微信头像链接，并将所有头像图片拼接成一张 16:9 的图片。同时，还会自动生成一个“你已被删”名单，用于识别被删除的好友。

## 功能

- 读取从 MemoTrace 导出的 CSV 文件。
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

2. 运行 `main.py` 脚本：

```bash
python main.py
```

3. 在弹出的窗口中，选择从 MemoTrace 导出的 CSV 文件。
4. 程序将开始下载头像图片并拼接成一张图片，最后会在指定位置保存生成的图片。

## 示例

运行程序后，选择 CSV 文件并等待下载和拼接完成。成功生成图片后，将弹出一个对话框，提示图片已保存，并显示“你已被删”名单。

## CSV 文件要求

- 第一列：微信用户 ID（包含 `wxid` 字符，不包含 `@chatroom` 字符）。
- 第三列：好友关系（不为数字 `0`）。
- 第四列：备注名（可选）。
- 第八列：头像链接（可选）。

## 过滤条件

- 仅处理第一列包含 `wxid` 字符且不包含 `@chatroom` 字符的行。
- 第三列不为 `0`。
- 第八列有头像链接。

## “你已被删”名单生成规则

- 第四列有字。
- 第一列不包含 `@chatroom` 字符。
- 第八列没有头像链接。

## 作者

Keishi

## 贡献

欢迎提交问题（issues）和请求（pull requests）来帮助改进此项目。

## 许可证

此项目基于 GPL-3.0 许可证开源。

## 参考

- [MemoTrace](https://github.com/LC044/WeChatMsg/)
```

将以上内容保存为 `README.md` 文件，放置在你的 GitHub 项目根目录中。这样可以为用户提供清晰的项目说明和使用指南。
