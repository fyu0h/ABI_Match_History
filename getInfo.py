import requests
import json

# 获取所有对局记录 GetBattleList
def fetch_all_battlelist(cookie):
    url = "https://www.wegame.com.cn/api/v1/wegame.pallas.ca.CaBattle/GetBattleList"
    headers = {
        "accept": "*/*",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7",
        "content-type": "application/json",
        "origin": "https://www.wegame.com.cn",
        "priority": "u=1, i",
        "referer": "https://www.wegame.com.cn/helper/ca/",
        "sec-ch-ua": '"Chromium";v="140", "Not=A?Brand";v="24", "Google Chrome";v="140"',
        "sec-ch-ua-mobile": "?1",
        "sec-ch-ua-platform": '"Android"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Mobile Safari/537.36"
    }
    cookies = {pair.split("=", 1)[0]: pair.split("=", 1)[1] for pair in cookie.split("; ")}
    
    all_battles = []
    data = {"from_src": "ca_helper", "count": 11, "filters": []}
    eday = None
    
    while True:
        if eday:
            data["eday"] = eday
        
        try:
            response = requests.post(url, headers=headers, cookies=cookies, json=data)
            response.raise_for_status()
            json_data = response.json()
            battles = json_data.get("battles", [])
            
            if not isinstance(battles, list):
                raise ValueError("响应中的 'battles' 不是列表")
            
            all_battles.extend(battles)
            
            if len(battles) < 11 or len(battles) == 0:
                break
                
            if len(battles) < 2:
                raise ValueError("battles 长度不足 2，无法获取 eday")
                
            eday = battles[-2].get("dtEventTime")
            if not eday:
                raise ValueError("battles[-2] 缺少 'dtEventTime' 字段")
                
            print(f"已获取 {len(all_battles)} 条记录，下一页 eday: {eday}")
            
        except requests.RequestException as e:
            print(f"请求错误: {e}")
            break
        except ValueError as e:
            print(f"数据错误: {e}")
            break
            
    print(f"分页完成，总共获取 {len(all_battles)} 条战斗记录")
    return all_battles

# 获取单局对局详情 GetBattleData
def fetch_battle_data(cookie):
    try:
        print("开始获取对局列表...")
        battle_list = fetch_all_battlelist(cookie)
        print(f"获取到 {len(battle_list)} 条对局记录")
        
        if not isinstance(battle_list, list):
            raise ValueError("battle_list 不是列表")
            
        room_ids = [item.get('roomId') for item in battle_list if isinstance(item, dict) and item.get('roomId')]
        if not room_ids:
            raise ValueError("未找到任何 roomId")
            
        results = []
        url = "https://www.wegame.com.cn/api/v1/wegame.pallas.ca.CaBattle/GetBattleDetail"
        headers = {
            "accept": "*/*",
            "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7",
            "content-type": "application/json",
            "origin": "https://www.wegame.com.cn",
            "priority": "u=1, i",
            "referer": "https://www.wegame.com.cn/helper/ca/",
            "sec-ch-ua": '"Chromium";v="140", "Not=A?Brand";v="24", "Google Chrome";v="140"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36"
        }
        cookies = {pair.split("=", 1)[0]: pair.split("=", 1)[1] for pair in cookie.split("; ")}
        
        print(f"开始获取 {len(room_ids)} 个对局详情...")
        for i, room_id in enumerate(room_ids, 1):
            print(f"正在获取对局 {i}/{len(room_ids)} (roomId: {room_id})...")
            try:
                data = {"from_src": "ca_helper", "roomId": room_id}
                response = requests.post(url, headers=headers, cookies=cookies, json=data)
                response.raise_for_status()
                results.append(response.json())
                print(f"成功获取对局 {i}/{len(room_ids)} (roomId: {room_id})")
            except requests.RequestException as e:
                print(f"获取 roomId {room_id} 详情失败: {e}")
                continue
                
        print(f"对局详情获取完成，共获取 {len(results)} 条详情")
        return results
        
    except Exception as e:
        print(f"获取对局详情失败: {e}")
        return []

# 获取用户个人信息 GetRoleInfo
def fetch_role_info(cookie):
    url = "https://www.wegame.com.cn/api/v1/wegame.pallas.ca.CaBattle/GetRoleInfo"
    headers = {
        "accept": "*/*",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7",
        "content-type": "application/json",
        "origin": "https://www.wegame.com.cn",
        "priority": "u=1, i",
        "referer": "https://www.wegame.com.cn/helper/ca/",
        "sec-ch-ua": '"Chromium";v="140", "Not=A?Brand";v="24", "Google Chrome";v="140"',
        "sec-ch-ua-mobile": "?1",
        "sec-ch-ua-platform": '"Android"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Mobile Safari/537.36"
    }
    cookies = {pair.split("=", 1)[0]: pair.split("=", 1)[1] for pair in cookie.split("; ")}
    data = {"from_src": "ca_helper"}
    
    try:
        response = requests.post(url, headers=headers, cookies=cookies, json=data)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"获取用户信息失败: {e}")
        return {}
    except ValueError as e:
        print(f"无效的 JSON 响应: {e}")
        return {}

# 获取用户头像
def download_image(cookie, picture_url, openid):
    headers = {
        "accept": "*/*",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7",
        "origin": "https://www.wegame.com.cn",
        "referer": "https://www.wegame.com.cn/helper/ca/",
        "sec-ch-ua": '"Chromium";v="140", "Not=A?Brand";v="24", "Google Chrome";v="140"',
        "sec-ch-ua-mobile": "?1",
        "sec-ch-ua-platform": '"Android"',
        "sec-fetch-dest": "image",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Mobile Safari/537.36"
    }
    cookies = {pair.split("=", 1)[0]: pair.split("=", 1)[1] for pair in cookie.split("; ")}
    
    try:
        response = requests.get(picture_url, headers=headers, cookies=cookies)
        response.raise_for_status()
        filename = f"avatar.jpg"
        with open(filename, "wb") as f:
            f.write(response.content)
        return f"图片已下载为 {filename}"
    except requests.RequestException as e:
        return f"下载图片失败: {e}"
    except IOError as e:
        return f"保存图片失败: {e}"
    
#获取个人战斗信息
def fetch_battle_report(cookies):
    import requests
    import json

    url = "https://www.wegame.com.cn/api/v1/wegame.pallas.ca.CaBattle/GetBattleReport"

    headers = {
        "accept": "*/*",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7",
        "cache-control": "no-cache",
        "content-type": "application/json",
        "origin": "https://www.wegame.com.cn",
        "pragma": "no-cache",
        "priority": "u=1, i",
        "referer": "https://www.wegame.com.cn/helper/ca/",
        "sec-ch-ua": '"Chromium";v="140", "Not=A?Brand";v="24", "Google Chrome";v="140"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36"
    }

    data = {
        "from_src": "ca_helper"
    }

    response = requests.post(url, headers=headers, cookies=cookies, json=data)

    if response.status_code == 200:
        return response.json()
    else:
        return {"error": f"Request failed with status code: {response.status_code}", "details": response.text}

if __name__ == "__main__":
    cookie = "ts_refer=www.google.com/; pgv_pvid=3597051623; ts_uid=2178193520; tgp_id=2029000207; tgp_ticket=D7762B0D118D4BD0467E04D6DED81DDD9ECAF9A29A4DB6BE3F0391C8A15A7DB9CE7ECA2939CCB5CF41C2BBE0846E2947335BFCDAF923489048F5ECF5A4D3F57FF93716E80ABA0BEAB606D88DB7128FFE3BC0DC84EFB62B99977033A7A06EAF73F7BAD776097D663039D51889FEF14BE602FE7528F985897434F105AB2D575DC3F7803DE9EE1A27C6780442326FD9260371FA4730DF094000F71A9C08F01BD0AB; tgp_env=online; tgp_user_type=1; tgp_third_openid=oPXtF0oGQTzFsGmG9ZeXPwdCdL_I; _qimei_uuid42=19a041519151002087132a1ce1fbb4747fde180be7; _qimei_fingerprint=540e35db61d2b5969af0c382111ccbfe"
    
    try:
        # 获取对局列表
        battlelist_result = fetch_all_battlelist(cookie)
        print("对局列表:", json.dumps(battlelist_result, indent=2, ensure_ascii=False))
        
        # 获取对局详情
        battle_report_result = fetch_battle_data(cookie)
        print("对局详情:", json.dumps(battle_report_result, indent=2, ensure_ascii=False))
        
        # 获取用户信息
        role_info_result = fetch_role_info(cookie)
        print("用户信息:", json.dumps(role_info_result, indent=2, ensure_ascii=False))
        
        # 下载头像
        openid = role_info_result.get("role_info", {}).get("openid", "unknown")
        picture_url = role_info_result.get("role_info", {}).get("icon", "")
        if picture_url:
            result = download_image(cookie, picture_url, openid)
            print(result)
        else:
            print("未找到头像 URL")
            
    except Exception as e:
        print(f"主程序错误: {e}")