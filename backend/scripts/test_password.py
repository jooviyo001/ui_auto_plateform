import bcrypt

# 数据库中的哈希密码
stored_hash = "$2b$12$TWDWtDK351uwGmfVvpxo1.NYRitNWxgQuNPf.7rt0L5KYu9rtF16i"

# 登录时输入的明文密码
password_input = "123456"

# 验证密码是否匹配
if bcrypt.checkpw(password_input.encode('utf-8'), stored_hash.encode('utf-8')):
    print("密码匹配")
else:
    print("密码不匹配")