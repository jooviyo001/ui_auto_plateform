import codecs

# 文件路径
file_path = 'main.py'

# 使用 UTF-16 读取文件
with codecs.open(file_path, 'r', encoding='utf-16') as file:
    content = file.read()

# 使用标准 UTF-8 编码写入文件
with codecs.open(file_path, 'w', encoding='utf-8') as file:
    file.write(content)

print('文件编码已成功从 UTF-16 转换为 UTF-8。')