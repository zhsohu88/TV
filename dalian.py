import requests  # 用于发送HTTP请求的库
import re  # 用于处理正则表达式的库
import time  # 用于处理时间相关的函数

def fetch_playlist_url():
    idn = {  # 定义频道名称与对应的频道ID
        "大连新闻综合": "tcb3IB5",
        "大连生活": "JzcFkF4",
        "大连文体": "hxT7Fc3",
        "大连影视": "8cuL6wa",
        "大连少儿": "q6tZ6Ba",
        "大连购物": "N4S4uAj",
    }
    headers = {  # 定义请求头，以模拟浏览器的请求
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    output_lines = [
        "# 这是本地源列表，一行一个源，格式为：频道名称,接口地址",
        "# 支持设置白名单：接口后添加$!",
        "# The local source list, one line per source, format: channel name, interface address",
        "# Support setting whitelist: add $! after the interface"
    ]  # 添加注释行
    for channel_name, channel_id in idn.items():  # 遍历每个频道名称及其对应的频道ID
        url = f"https://dlyapp.dltv.cn/apiv4.5/api/m3u8_notoken?channelid={channel_id}"  # 构建请求URL
        for _ in range(3):  # 尝试三次
            try:
                response = requests.get(url, headers=headers)  # 发送HTTP GET请求
                if response.status_code == 200:  # 如果请求成功，退出重试循环
                    break
            except requests.exceptions.RequestException as e:
                print(f"Failed to fetch URL for {channel_name}: {url}, retrying...")  # 捕获请求异常并重试
                time.sleep(5)  # 等待5秒钟后重试
        else:
            print(f"Failed to fetch URL for {channel_name}: {url}")  # 如果三次重试都失败，记录失败信息
            output_lines.append(channel_name)  # 只添加频道名称，不带逗号
            continue
        info = response.text  # 获取响应的文本内容
        match = re.search(r'"address":"(.*?)"', info)  # 使用正则表达式提取播放地址
        if not match or match.group(1) == "":  # 如果没有匹配到播放地址或地址为空
            output_lines.append(channel_name)  # 只添加频道名称，不带逗号
            continue
        playlist_url = match.group(1).replace('\\/', '/')  # 替换地址中的转义斜杠
        output_lines.append(f"{channel_name},{playlist_url}$!")  # 添加频道名称和播放地址，并在链接后面加上$!
        
    # 去掉注释就可以使用下面的功能
    # # 获取指定地址的播放列表并添加新的频道，取指定分组的频道
    # # target_groups = ["松视正版"]  # 指定需要的分组名称
    # # new_source_url = "https://codeberg.org/weidi/AV18_X18/raw/branch/master/xh"    
    # target_groups = ["咪咕视频"]  # 指定需要的分组名称
    # new_source_url = "https://4708.kstore.space/svip/ITV.txt"
    # try:
    #     response = requests.get(new_source_url, headers=headers)  # 发送HTTP GET请求获取新源地址列表
    #     if response.status_code == 200:  # 如果请求成功
    #         info = response.content.decode('utf-8')  # 获取响应的文本内容并进行UTF-8解码
    #         # print(info)  # 打印获取的内容
    #         current_group = None  # 当前处理的分组名称
    #         for line in info.splitlines():  # 遍历每行内容
    #             if ",#genre#" in line:  # 如果是分组名称行
    #                 current_group = line.split(",")[0]  # 提取分组名称
    #                 # print(f"Current group: {current_group}")  # 打印当前分组名称
    #             elif current_group and any(group in current_group for group in target_groups) and "," in line:  # 如果当前分组包含需要的分组名称且是频道行
    #                 channel_name, playlist_url = line.split(",", 1)  # 分割频道名称和播放地址
    #                 output_lines.append(f"{channel_name},{playlist_url}$!")  # 添加频道名称和播放地址，并在链接后面加上$!
    #                 # print(f"Matched line: {line}")  # 打印匹配的行
    #     else:
    #         print(f"Failed to fetch additional channels: {new_source_url} with status code {response.status_code}")  # 捕获请求异常
    # except requests.exceptions.RequestException as e:
    #     print(f"Failed to fetch additional channels: {new_source_url}. Error: {e}")  # 捕获请求异常

    with open("config/user_local.txt", "w") as file:  # 将结果写入文件
        file.write("\n".join(output_lines))

if __name__ == "__main__":
    fetch_playlist_url()  # 调用函数