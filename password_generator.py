"""
密碼產生器 (Password Generator)
自動產生安全的隨機密碼
"""

import random
import string
import pyperclip

def generate_password(length=16, use_upper=True, use_lower=True, use_digits=True, use_symbols=True):
    """
    產生隨機密碼
    
    參數:
        length: 密碼長度（預設 16）
        use_upper: 包含大寫字母
        use_lower: 包含小寫字母
        use_digits: 包含數字
        use_symbols: 包含特殊符號
    
    回傳:
        產生的密碼字串
    """
    charset = ""
    guaranteed = []

    if use_upper:
        charset += string.ascii_uppercase
        guaranteed.append(random.choice(string.ascii_uppercase))
    if use_lower:
        charset += string.ascii_lowercase
        guaranteed.append(random.choice(string.ascii_lowercase))
    if use_digits:
        charset += string.digits
        guaranteed.append(random.choice(string.digits))
    if use_symbols:
        symbols = "!@#$%^&*()-_=+[]{}|;:,.<>?"
        charset += symbols
        guaranteed.append(random.choice(symbols))

    if not charset:
        print("❌ 請至少選擇一種字元類型！")
        return None

    remaining = [random.choice(charset) for _ in range(length - len(guaranteed))]
    password_list = guaranteed + remaining
    random.shuffle(password_list)
    
    return "".join(password_list)


def check_strength(password):
    """評估密碼強度"""
    score = 0
    feedback = []

    if len(password) >= 12:
        score += 1
    else:
        feedback.append("建議長度至少 12 字元")

    if any(c.isupper() for c in password):
        score += 1
    else:
        feedback.append("建議加入大寫字母")

    if any(c.islower() for c in password):
        score += 1
    else:
        feedback.append("建議加入小寫字母")

    if any(c.isdigit() for c in password):
        score += 1
    else:
        feedback.append("建議加入數字")

    if any(c in "!@#$%^&*()-_=+[]{}|;:,.<>?" for c in password):
        score += 1
    else:
        feedback.append("建議加入特殊符號")

    levels = {1: "❌ 非常弱", 2: "⚠️  弱", 3: "🟡 中等", 4: "🟢 強", 5: "💪 非常強"}
    return levels.get(score, "❌ 非常弱"), feedback


def main():
    print("=" * 50)
    print("  🔐 密碼產生器 Password Generator")
    print("=" * 50)

    while True:
        print("\n請設定密碼選項：")

        try:
            length = int(input("密碼長度（預設 16，建議 12~32）：").strip() or "16")
        except ValueError:
            length = 16

        upper   = input("包含大寫字母？(y/n，預設 y)：").strip().lower() != "n"
        lower   = input("包含小寫字母？(y/n，預設 y)：").strip().lower() != "n"
        digits  = input("包含數字？   (y/n，預設 y)：").strip().lower() != "n"
        symbols = input("包含符號？   (y/n，預設 y)：").strip().lower() != "n"

        try:
            count = int(input("產生幾組密碼？（預設 1）：").strip() or "1")
        except ValueError:
            count = 1

        print("\n" + "-" * 50)
        passwords = []
        for i in range(count):
            pwd = generate_password(length, upper, lower, digits, symbols)
            if pwd:
                strength, tips = check_strength(pwd)
                print(f"  [{i+1}] {pwd}")
                print(f"       強度：{strength}")
                if tips:
                    print(f"       建議：{' / '.join(tips)}")
                passwords.append(pwd)

        print("-" * 50)

        # 嘗試複製到剪貼簿
        if passwords:
            try:
                pyperclip.copy(passwords[0])
                print(f"\n✅ 第一組密碼已複製到剪貼簿！")
            except Exception:
                print(f"\n💡 提示：手動複製上方密碼使用")

        again = input("\n要再產生一批嗎？(y/n，預設 n)：").strip().lower()
        if again != "y":
            print("\n安全提醒：請使用密碼管理器儲存密碼，不要重複使用！\n")
            break


if __name__ == "__main__":
    main()
