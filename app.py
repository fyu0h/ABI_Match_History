from flask import Flask, request, url_for, send_from_directory, redirect
import os
import json
import datetime
from getInfo import fetch_all_battlelist, fetch_battle_data, fetch_role_info
import requests  # 用于下载图片

app = Flask(__name__)

# 主页：输入cookie的表单
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        cookie = request.form.get('cookie', '').strip()
        if not cookie:
            return "Cookie不能为空", 400

        # 解析 cookie
        try:
            cookies_dict = {}
            for pair in cookie.split(';'):
                pair = pair.strip()
                if pair and '=' in pair:
                    key, value = pair.split('=', 1)
                    cookies_dict[key.strip()] = value.strip()
        except Exception as e:
            return f"Cookie格式无效: {e}", 400

        required_keys = ['tgp_id', 'tgp_ticket', 'tgp_env', 'tgp_user_type', 'tgp_third_openid']
        missing_keys = [key for key in required_keys if key not in cookies_dict]
        if missing_keys:
            return f"Cookie缺少以下项: {', '.join(missing_keys)}", 400

        # 调用数据接口
        battle_list = fetch_all_battlelist(cookie)
        battle_data = fetch_battle_data(cookie)
        role_info = fetch_role_info(cookie)

        # 获取 openid 与头像链接
        openid = role_info.get("role_info", {}).get("openid", "unknown")
        username = role_info.get("role_info", {}).get("name", "未知用户")  # 获取用户名，默认为“未知用户”
        picture_url = role_info.get("role_info", {}).get("icon", "")

        user_dir = os.path.join('user_info', openid)
        os.makedirs(user_dir, exist_ok=True)

        # 保存数据
        with open(os.path.join(user_dir, 'battle_list.json'), 'w', encoding='utf-8') as f:
            json.dump(battle_list, f, ensure_ascii=False, indent=2)
        with open(os.path.join(user_dir, 'battle_data.json'), 'w', encoding='utf-8') as f:
            json.dump(battle_data, f, ensure_ascii=False, indent=2)
        with open(os.path.join(user_dir, 'role_info.json'), 'w', encoding='utf-8') as f:
            json.dump(role_info, f, ensure_ascii=False, indent=2)

        # 下载头像
        if picture_url:
            try:
                headers = {
                    "accept": "*/*",
                    "user-agent": "Mozilla/5.0"
                }
                response = requests.get(picture_url, headers=headers, cookies=cookies_dict)
                if response.status_code == 200:
                    with open(os.path.join(user_dir, 'avatar.jpg'), 'wb') as f:
                        f.write(response.content)
            except Exception:
                pass

        # 更新 index.html
        with open('index.html', 'r', encoding='utf-8') as f:
            html_content = f.read()
        current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        html_content = html_content.replace('更新时间: 2025-10-07', f'更新时间: {current_time}')
        html_content = html_content.replace('<title>暗区突围：无限 战绩查询助手</title>', f'<title>{username}对局记录</title>')  # 更新标题

        with open(os.path.join(user_dir, 'index.html'), 'w', encoding='utf-8') as f:
            f.write(html_content)

        view_url = url_for('view_user_info', openid=openid, _external=True)
        return f'''
        <!DOCTYPE html>
        <html lang="zh">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>提交成功</title>
            <style>
                body {{
                    font-family: "Segoe UI", Arial, sans-serif;
                    background: linear-gradient(135deg, #e0f7fa, #e3f2fd);
                    margin: 0;
                    padding: 0;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    min-height: 100vh;
                }}
                .container {{
                    max-width: 90%;
                    width: 500px;
                    margin: 20px;
                    background: white;
                    border-radius: 16px;
                    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
                    padding: 30px;
                    text-align: center;
                }}
                h1 {{
                    color: #1976d2;
                    font-size: 1.8rem;
                    margin-bottom: 20px;
                }}
                p {{
                    font-size: 1rem;
                    color: #333;
                }}
                a {{
                    color: #1565c0;
                    text-decoration: none;
                    font-weight: bold;
                }}
                a:hover {{
                    text-decoration: underline;
                }}
                @media (max-width: 600px) {{
                    .container {{
                        padding: 20px;
                    }}
                    h1 {{
                        font-size: 1.5rem;
                    }}
                    p {{
                        font-size: 0.9rem;
                    }}
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>数据获取成功！</h1>
                <p>您的战绩数据已成功保存！</p>
                <p><a href="{view_url}">点击查看您的战绩</a></p>
                <p><a href="{url_for('index', _external=True)}">返回首页</a></p>
            </div>
        </body>
        </html>
        '''

    # 美化后的输入页面（适配移动端）
    jump_url = url_for('jump', _external=True)  # Generate the URL for the /jump route
    return f'''
    <!DOCTYPE html>
    <html lang="zh">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>暗区突围：无限 战绩查询助手 - 输入 Cookie</title>
        <style>
            html, body {{
                font-family: "Segoe UI", Arial, sans-serif;
                background: linear-gradient(135deg, #e0f7fa, #e3f2fd);
                margin: 0;
                padding: 0;
                height: 100%; /* 确保 flex 居中生效 */
                display: flex;
                justify-content: center;
                align-items: center; /* 垂直居中 */
            }}
            .container {{
                max-width: 90%;
                width: 600px;
                background: white;
                border-radius: 16px;
                box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
                padding: 30px;
                text-align: center;
                margin: 0; /* 移除 margin，flex 已居中 */
            }}
            h1 {{
                color: #1976d2;
                font-size: 1.8rem;
                margin-bottom: 20px;
            }}
            textarea {{
                width: 100%;
                height: 100px;
                padding: 10px;
                border: 2px solid #90caf9;
                border-radius: 8px;
                font-size: 1rem;
                resize: vertical;
                outline: none;
                box-sizing: border-box;
                transition: border-color 0.3s;
            }}
            textarea:focus {{
                border-color: #1976d2;
                box-shadow: 0 0 5px rgba(25, 118, 210, 0.3);
            }}
            input[type="submit"] {{
                background-color: #1976d2;
                color: white;
                border: none;
                padding: 10px 30px;
                font-size: 1rem;
                border-radius: 6px;
                cursor: pointer;
                margin-top: 20px;
                transition: background-color 0.3s;
            }}
            input[type="submit"]:hover {{
                background-color: #0d47a1;
            }}
            #loading {{
                display: none;
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background: rgba(0, 0, 0, 0.6);
                color: white;
                font-size: 1.2rem;
                text-align: center;
                padding-top: 40%;
                z-index: 9999;
            }}
            .tutorial {{
                margin-top: 30px;
                text-align: left;
                background: #f9f9f9;
                padding: 20px;
                border-radius: 10px;
                border-left: 5px solid #42a5f5;
            }}
            .tutorial h2 {{
                color: #1976d2;
                font-size: 1.4rem;
                margin-bottom: 10px;
            }}
            .step {{
                margin-bottom: 10px;
                padding: 8px 10px;
                background: #e3f2fd;
                border-radius: 6px;
                transition: background 0.3s;
                font-size: 0.9rem;
            }}
            .step:hover {{
                background: #bbdefb;
            }}
            .step span {{
                font-weight: bold;
                color: #1565c0;
            }}
            a {{
                color: #1565c0;
                text-decoration: none;
            }}
            a:hover {{
                text-decoration: underline;
            }}
            .nav-link {{
                margin-top: 20px;
                display: block;
                font-size: 1rem;
            }}
            @media (max-width: 600px) {{
                .container {{
                    width: 90%;
                    padding: 20px;
                }}
                h1 {{
                    font-size: 1.5rem;
                }}
                textarea {{
                    font-size: 0.9rem;
                }}
                input[type="submit"] {{
                    font-size: 0.9rem;
                    padding: 8px 20px;
                }}
                .tutorial h2 {{
                    font-size: 1.2rem;
                }}
                .step {{
                    font-size: 0.85rem;
                }}
                #loading {{
                    font-size: 1rem;
                    padding-top: 50%;
                }}
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>暗区突围：无限 战绩查询助手</h1>
            <form method="post" onsubmit="showLoading()">
                <label for="cookie"><strong>请输入 Cookie：</strong></label><br>
                <textarea id="cookie" name="cookie" placeholder="请将完整 Cookie 粘贴在此处..."></textarea><br>
                <input type="submit" value="提交">
            </form>
            <a href="{jump_url}" class="nav-link">已有 OpenID？直接跳转到战绩页面</a>

            <div class="tutorial">
                <h2>🧭 获取 Cookie 教程</h2>
                <div class="step"><span>第一步：</span> 打开 <a href="https://www.wegame.com.cn/helper/ca/#/" target="_blank">https://www.wegame.com.cn/helper/ca/#/</a></div>
                <div class="step"><span>第二步：</span> 使用微信扫码登录。</div>
                <div class="step"><span>第三步：</span> 按下 <b>F12</b> 打开开发者工具，选择 <b>Network（网络）</b> 面板。</div>
                <div class="step"><span>第四步：</span> 按下 <b>F5</b> 刷新页面，在请求列表中找到 <b>ca/</b>，通常在最上面，点击它。</div>
                <div class="step"><span>第五步：</span> 在右侧的 <b>Headers（标头）</b> 选项卡中找到 <b>cookie</b> 字段，将其完整复制粘贴到上方输入框后点击提交即可。</div>
            </div>
        </div>

        <div id="loading">正在获取数据，如果对局数据较多耗时将比较长，预计在5分钟左右，请稍候...</div>
        <script>
            function showLoading() {{
                document.getElementById('loading').style.display = 'block';
            }}
        </script>
    </body>
    </html>
    '''

# OpenID 跳转页面
@app.route('/jump', methods=['GET', 'POST'])
def jump():
    if request.method == 'POST':
        openid = request.form.get('openid', '').strip()
        if not openid:
            return "OpenID 不能为空", 400
        return redirect(url_for('view_user_info', openid=openid))
    
    index_url = url_for('index', _external=True)  # 生成 / 路由的 URL
    return f'''
    <!DOCTYPE html>
    <html lang="zh">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>暗区突围：无限 战绩查询助手 - 输入 OpenID</title>
        <style>
            body {{
                font-family: "Segoe UI", Arial, sans-serif;
                background: linear-gradient(135deg, #e0f7fa, #e3f2fd);
                margin: 0;
                padding: 0;
                display: flex;
                justify-content: center;
                align-items: center;
                min-height: 100vh;
            }}
            .container {{
                max-width: 90%;
                width: 500px;
                margin: 20px;
                background: white;
                border-radius: 16px;
                box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
                padding: 30px;
                text-align: center;
            }}
            h1 {{
                color: #1976d2;
                font-size: 1.8rem;
                margin-bottom: 20px;
            }}
            input[type="text"] {{
                width: 100%;
                padding: 10px;
                border: 2px solid #90caf9;
                border-radius: 8px;
                font-size: 1rem;
                box-sizing: border-box;
                outline: none;
                transition: border-color 0.3s;
            }}
            input[type="text"]:focus {{
                border-color: #1976d2;
                box-shadow: 0 0 5px rgba(25, 118, 210, 0.3);
            }}
            input[type="submit"] {{
                background-color: #1976d2;
                color: white;
                border: none;
                padding: 10px 30px;
                font-size: 1rem;
                border-radius: 6px;
                cursor: pointer;
                margin-top: 20px;
                transition: background-color 0.3s;
            }}
            input[type="submit"]:hover {{
                background-color: #0d47a1;
            }}
            a {{
                color: #1565c0;
                text-decoration: none;
                display: block;
                margin-top: 20px;
                font-size: 1rem;
            }}
            a:hover {{
                text-decoration: underline;
            }}
            @media (max-width: 600px) {{
                .container {{
                    padding: 20px;
                }}
                h1 {{
                    font-size: 1.5rem;
                }}
                input[type="text"], input[type="submit"] {{
                    font-size: 0.9rem;
                }}
                a {{
                    font-size: 0.9rem;
                }}
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>输入 OpenID 查看战绩</h1>
            <form method="post">
                <label for="openid"><strong>请输入 OpenID：</strong></label><br>
                <input type="text" id="openid" name="openid" placeholder="请输入您的 OpenID..."><br>
                <input type="submit" value="跳转">
            </form>
            <a href="{index_url}">返回首页</a>
        </div>
    </body>
    </html>
    '''
# 用户信息页面
@app.route('/user_info/<openid>/index.html')
def view_user_info(openid):
    user_dir = os.path.join('user_info', openid)
    target_html = os.path.join(user_dir, 'index.html')
    if os.path.exists(target_html):
        with open(target_html, 'r', encoding='utf-8') as f:
            return f.read()
    # 文件不存在时返回美化页面
    return render_not_found_page()

# 静态文件服务
@app.route('/user_info/<openid>/<filename>')
def serve_user_file(openid, filename):
    user_dir = os.path.join('user_info', openid)
    allowed_files = ['role_info.json', 'battle_data.json', 'battle_list.json', 'avatar.jpg']
    file_path = os.path.join(user_dir, filename)
    if filename in allowed_files and os.path.exists(file_path):
        return send_from_directory(user_dir, filename)
    # 文件不存在时返回美化页面
    return render_not_found_page()


def render_not_found_page():
    home_url = url_for('index', _external=True)
    return f'''
    <!DOCTYPE html>
    <html lang="zh">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>数据不存在 - 暗区突围：无限 战绩查询助手</title>
        <style>
            body {{
                font-family: "Segoe UI", Arial, sans-serif;
                background: linear-gradient(135deg, #e0f7fa, #e3f2fd);
                margin: 0;
                padding: 0;
                display: flex;
                justify-content: center;
                align-items: center;
                min-height: 100vh;
                opacity: 0;
                animation: fadeIn 1s forwards;
            }}
            @keyframes fadeIn {{
                to {{ opacity: 1; }}
            }}
            .container {{
                max-width: 90%;
                width: 500px;
                background: white;
                border-radius: 16px;
                box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
                padding: 30px;
                text-align: center;
                transform: translateY(-20px);
                animation: slideIn 0.5s forwards;
            }}
            @keyframes slideIn {{
                to {{ transform: translateY(0); }}
            }}
            h1 {{
                color: #4caf50;
                font-size: 1.8rem;
                margin-bottom: 20px;
            }}
            p {{
                font-size: 1rem;
                color: #333;
                margin-bottom: 20px;
            }}
            a {{
                color: #1976d2;
                text-decoration: none;
                font-size: 1rem;
                transition: color 0.3s;
            }}
            a:hover {{
                color: #0d47a1;
                text-decoration: underline;
            }}
        </style>
        <script>
            // 3秒后跳转首页
            setTimeout(function(){{
                window.location.href = "{home_url}";
            }}, 3000);
        </script>
    </head>
    <body>
        <div class="container">
            <h1>❌ 该用户数据不存在</h1>
            <p>请返回首页重新获取</p>
            <a href="{home_url}">返回首页</a>
        </div>
    </body>
    </html>
    ''', 404

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)