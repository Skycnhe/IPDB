import requests
import re
import os

# GitHub Raw 文件的直接下载链接（%26 代表 '&'）
url = "https://raw.githubusercontent.com/Skycnhe/IPDB/main/BestProxy/bestproxy%26country.txt"
output_dir = "Proxies_By_Country" # 分类后文件的存放文件夹

def classify_proxies():
    print("正在从 GitHub 下载代理文件...")
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except Exception as e:
        print(f"下载失败，请检查网络或链接: {e}")
        return

    # 创建输出文件夹
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    classified_data = {}
    lines = response.text.splitlines()

    for line in lines:
        line = line.strip()
        if not line: continue

        # 假设格式是 "IP:端口 国家" 或 "IP:端口#国家" 或 "IP:端口,国家"
        # 这里用正则表达式分割常见的符号（空格、逗号、井号、制表符）
        parts = re.split(r'[\s#,]+', line)
        
        if len(parts) >= 2:
            proxy = parts[0]   # IP和端口
            country = parts[1] # 国家代码 (如 US, CN, SG 等)
            
            if country not in classified_data:
                classified_data[country] = []
            classified_data[country].append(proxy)

    # 将分类好的数据写入不同的 TXT 文件
    for country, proxies in classified_data.items():
        # 清理国家名称中的非法字符以防无法创建文件
        safe_country = re.sub(r'[\\/*?:"<>|]', "", country)
        file_path = os.path.join(output_dir, f"{safe_country}.txt")
        
        with open(file_path, 'w', encoding='utf-8') as f:
            for p in proxies:
                f.write(p + "\n")

    print(f"分类完成！共发现 {len(classified_data)} 个国家/地区。")
    print(f"文件已保存在当前目录下的 '{output_dir}' 文件夹中。")

if __name__ == "__main__":
    classify_proxies()
