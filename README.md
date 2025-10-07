# 暗区突围：无限 战绩查询助手

这是一个基于 Flask 的 Web 应用程序，旨在帮助《暗区突围：无限》玩家通过输入游戏 Cookie 查询和查看他们的战绩数据。应用程序会获取用户数据，保存到本地，并生成个性化的战绩页面，界面友好且适配移动端。

## 功能

- **基于 Cookie 的数据获取**：用户输入游戏 Cookie 以获取战绩列表、详细战绩数据和角色信息。
- **数据存储**：将战绩列表、战绩数据和角色信息保存为 JSON 文件，同时存储用户头像。
- **动态 HTML 生成**：更新用户专属的 `index.html`，包含最新数据和个性化标题。
- **响应式设计**：针对桌面端和移动端优化，提供现代、简洁的界面。
- **OpenID 支持**：允许用户通过输入 OpenID 直接跳转到战绩页面。
- **错误处理**：验证 Cookie 的有效性，并为缺失或无效输入提供友好的错误提示。
- **静态文件服务**：安全地提供用户专属文件（如 JSON 数据和头像）。
- **数据不存在页面**：当用户数据缺失时，显示美化的错误页面，并自动跳转到首页。

## 前置条件

- Python 3.8+
- Flask（`pip install flask`）
- Requests 库（`pip install requests`）
- `getInfo.py` 模块，需包含以下函数：
  - `fetch_all_battlelist(cookie)`：获取战绩列表数据。
  - `fetch_battle_data(cookie)`：获取详细战绩数据。
  - `fetch_role_info(cookie)`：获取用户角色信息。

## 安装

1. 克隆仓库：
   ```bash
   git clone https://github.com/yourusername/arena-breakout-infinite-query.git
   cd arena-breakout-infinite-query
   ```

2. 安装依赖：
   ```bash
   pip install -r requirements.txt
   ```

3. 确保 `getInfo.py` 模块位于项目目录中。

4. 创建 `user_info` 目录以存储用户数据：
   ```bash
   mkdir user_info
   ```

5. 在项目根目录中创建 `index.html` 模板以支持动态更新（或自定义现有模板）。

## 使用方法

1. 运行 Flask 应用程序：
   ```bash
   python app.py
   ```

2. 打开浏览器，访问 `http://localhost:5000`。

3. 按照页面教程从 [WeGame](https://www.wegame.com.cn/helper/ca/#/) 获取游戏 Cookie，并粘贴到输入框中。

4. 提交 Cookie 以获取并保存战绩数据，成功后会跳转到提示页面，包含查看战绩的链接。

5. 或者，使用 `/jump` 路由输入 OpenID 直接跳转到战绩页面。

## 项目结构

```
arena-breakout-infinite-query/
├── app.py              # 主 Flask 应用程序
├── getInfo.py          # 获取游戏数据的模块（未包含）
├── user_info/          # 存储用户数据的目录（JSON 文件、头像和 HTML）
├── index.html          # 用户战绩页面的模板
└── README.md           # 本文件
```

## 路由

- `/`（GET, POST）：首页，包含 Cookie 输入表单和获取教程。
- `/jump`（GET, POST）：OpenID 输入页面，用于直接跳转到战绩页面。
- `/user_info/<openid>/index.html`：显示用户的战绩页面。
- `/user_info/<openid>/<filename>`：提供用户专属静态文件（如 JSON 或头像）。
- 404 页面：当用户数据不存在时，显示自定义错误页面并自动跳转到首页。

## 注意事项

- **Cookie 格式**：Cookie 必须包含 `tgp_id`、`tgp_ticket`、`tgp_env`、`tgp_user_type` 和 `tgp_third_openid`。无效或不完整的 Cookie 将返回错误。
- **数据获取**：假定 `getInfo.py` 模块处理与游戏服务器的 API 调用，请确保其正确实现。
- **安全性**：应用程序对文件访问进行验证，防止未授权的文件访问。
- **性能**：大量战绩数据可能需要最多 5 分钟处理时间，加载页面会显示相关提示。
- **自定义**：可修改 `index.html` 模板以增强战绩页面展示效果。

## 贡献

欢迎贡献！请提交 Pull Request 或创建 Issue 报告错误、提出功能请求或改进建议。

## 许可证

本项目采用 MIT 许可证，详情见 [LICENSE](LICENSE) 文件。
