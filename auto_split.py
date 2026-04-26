import urllib.request
import os

# 1. 目标文件的 GitHub Raw 真实下载链接
url = "https://raw.githubusercontent.com/Skycnhe/IPDB/main/BestProxy/bestproxy%26country.txt"

# 2. 设置保存分类文件的文件夹名称
output_folder = "Proxies_By_Country"
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

print("正在从 GitHub 下载最新代理数据...")
try:
    # 模拟浏览器请求下载文件
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, timeout=15) as response:
        content = response.read().decode('utf-8')
except Exception as e:
    print(f"网络连接或下载失败: {e}")
    exit()

print("下载成功！正在自动按照国家分类...")

# 3. 按行解析数据
lines = content.strip().split('\n')
country_dict = {}

for line in lines:
    line = line.strip()
    if not line:
        continue
    
    # 将每一行按空格切分（通常格式为 "IP:端口 国家"）
    parts = line.split()
    if len(parts) >= 2:
        ip_proxy = parts[0]    # 第一部分是 IP:端口
        country = parts[-1]    # 最后一部分是 国家代码
        
        # 将 IP 加入对应国家的列表中
        if country not in country_dict:
            country_dict[country] = []
        country_dict[country].append(ip_proxy)

# 4. 按照国家分别生成 TXT 文件
for country, ips in country_dict.items():
    # 过滤掉可能导致文件名报错的特殊字符
    safe_country = "".join(c for c in country if c.isalnum())
    if not safe_country:
        continue
        
    file_path = os.path.join(output_folder, f"{safe_country}.txt")
    
    # 写入文件
    with open(file_path, "w", encoding="utf-8") as f:
        for ip in ips:
            f.write(ip + "\n")

print(f"分类完成！共识别出 {len(country_dict)} 个国家。")
print(f"所有的 TXT 文件已经保存在当前目录下的【{output_folder}】文件夹中。")
