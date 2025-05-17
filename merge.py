import json

# 两个源文件名
file1 = 'results_1-1514.json'
file2 = 'results_1515+.json'

# 合并后输出的文件名
output_file = 'ALL.json'

# 读取两个文件内容
with open(file1, 'r', encoding='utf-8') as f1, open(file2, 'r', encoding='utf-8') as f2:
    data1 = json.load(f1)
    data2 = json.load(f2)

# 合并两个列表
merged_data = data1 + data2

# 写入新文件
with open(output_file, 'w', encoding='utf-8') as fout:
    json.dump(merged_data, fout, indent=2, ensure_ascii=False)

print(f"Merged {len(data1)} + {len(data2)} entries into '{output_file}'")
