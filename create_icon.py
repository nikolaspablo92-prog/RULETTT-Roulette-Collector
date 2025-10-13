#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Генератор иконки для RULETTT Desktop
Создает icon.ico размером 256x256 с символом рулетки
"""

from PIL import Image, ImageDraw, ImageFont
import os

def create_roulette_icon(size=256):
    """Создание иконки с символом рулетки"""
    
    # Создаем изображение с прозрачным фоном
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Параметры
    center = size // 2
    outer_radius = size // 2 - 10
    inner_radius = outer_radius - 30
    
    # Фон - темно-зеленый круг (как стол рулетки)
    draw.ellipse(
        [(10, 10), (size-10, size-10)],
        fill=(20, 100, 50, 255),
        outline=(200, 150, 0, 255),
        width=5
    )
    
    # Внутренний круг
    draw.ellipse(
        [(center - inner_radius, center - inner_radius),
         (center + inner_radius, center + inner_radius)],
        fill=(150, 0, 0, 255),
        outline=(255, 255, 255, 255),
        width=3
    )
    
    # Рисуем секции (как на рулетке)
    import math
    num_sections = 12
    for i in range(num_sections):
        angle1 = (i * 360 / num_sections) * math.pi / 180
        angle2 = ((i + 0.5) * 360 / num_sections) * math.pi / 180
        
        x1 = center + inner_radius * math.cos(angle1)
        y1 = center + inner_radius * math.sin(angle1)
        x2 = center + outer_radius * math.cos(angle2)
        y2 = center + outer_radius * math.sin(angle2)
        
        color = (255, 255, 255, 255) if i % 2 == 0 else (0, 0, 0, 255)
        draw.line([(center, center), (x2, y2)], fill=color, width=2)
    
    # Центральная точка (шарик)
    ball_radius = 15
    draw.ellipse(
        [(center - ball_radius, center - ball_radius),
         (center + ball_radius, center + ball_radius)],
        fill=(255, 255, 255, 255),
        outline=(0, 0, 0, 255),
        width=2
    )
    
    # Добавляем текст "R" в центре
    try:
        # Пытаемся использовать жирный шрифт
        font_size = 20
        font = ImageFont.truetype("arial.ttf", font_size)
    except:
        font = ImageFont.load_default()
    
    text = "R"
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    text_x = center - text_width // 2
    text_y = center - text_height // 2
    
    draw.text((text_x, text_y), text, fill=(0, 0, 0, 255), font=font)
    
    return img

def main():
    """Создание иконки в разных размерах"""
    
    print("🎨 Создание иконки RULETTT Desktop...")
    
    # Создаем иконку 256x256
    icon_256 = create_roulette_icon(256)
    
    # Создаем дополнительные размеры для .ico
    sizes = [256, 128, 64, 48, 32, 16]
    images = []
    
    for size in sizes:
        if size == 256:
            images.append(icon_256)
        else:
            resized = icon_256.resize((size, size), Image.Resampling.LANCZOS)
            images.append(resized)
        print(f"  ✅ Создан размер: {size}x{size}")
    
    # Сохраняем как .ico
    icon_path = "icon.ico"
    images[0].save(
        icon_path,
        format='ICO',
        sizes=[(img.width, img.height) for img in images],
        append_images=images[1:]
    )
    
    print(f"\n✅ Иконка сохранена: {icon_path}")
    print(f"📊 Размеры: {', '.join([f'{s}x{s}' for s in sizes])}")
    print(f"💾 Размер файла: {os.path.getsize(icon_path) / 1024:.1f} KB")
    
    # Создаем также PNG для превью
    png_path = "icon_preview.png"
    icon_256.save(png_path, "PNG")
    print(f"🖼️ Превью сохранено: {png_path}")
    
    print("\n🎉 Готово! Используйте icon.ico для сборки приложения.")

if __name__ == "__main__":
    main()
