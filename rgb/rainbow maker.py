def generate_rainbow():
    rainbow = []
    # بخش اول: رنگ‌های گرادیان از قرمز به زرد و سبز
    for r, g in zip(range(126, -1, -3), range(0, 123, 3)):
        rainbow.append((r, g, 0))

    # بخش دوم: رنگ‌های گرادیان از سبز به آبی
    for g, b in zip(range(126, -1, -3), range(0, 126, 3)):
        rainbow.append((0, g, b))

    # بخش سوم: رنگ‌های گرادیان از آبی به قرمز
    for b, r in zip(range(126, -1, -3), range(0, 126, 3)):
        rainbow.append((r, 0, b))

    return rainbow

# فراخوانی تابع و چاپ لیست
rainbow = generate_rainbow()
print(rainbow)
