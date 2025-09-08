#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
将HTML文件中的图片转换为base64内联编码，实现即时加载
"""

import os
import base64
import re
from pathlib import Path

def get_image_base64(image_path):
    """将图片文件转换为base64编码"""
    try:
        with open(image_path, 'rb') as img_file:
            img_data = img_file.read()
            base64_data = base64.b64encode(img_data).decode('utf-8')
            
            # 根据文件扩展名确定MIME类型
            ext = Path(image_path).suffix.lower()
            mime_types = {
                '.png': 'image/png',
                '.jpg': 'image/jpeg',
                '.jpeg': 'image/jpeg',
                '.gif': 'image/gif',
                '.webp': 'image/webp'
            }
            mime_type = mime_types.get(ext, 'image/png')
            
            return f"data:{mime_type};base64,{base64_data}"
    except Exception as e:
        print(f"错误：无法读取图片 {image_path}: {e}")
        return None

def find_image_file(image_name, search_dirs):
    """在指定目录中查找图片文件"""
    for search_dir in search_dirs:
        for ext in ['.png', '.jpg', '.jpeg', '.gif', '.webp']:
            image_path = os.path.join(search_dir, image_name + ext)
            if os.path.exists(image_path):
                return image_path
    return None

def convert_html_images_to_base64(html_file_path):
    """将HTML文件中的图片转换为base64内联编码"""
    
    # 搜索目录列表
    search_dirs = [
        '.',
        'images',
        'images_compressed', 
        'backup_instant_optimization_20250908_000948',
        'compressed_backup',
        'original_images_backup'
    ]
    
    # 读取HTML文件
    with open(html_file_path, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # 查找所有图片引用
    img_pattern = r'<img[^>]+src="([^"]+)"[^>]*>'
    matches = re.findall(img_pattern, html_content)
    
    print(f"找到 {len(matches)} 个图片引用")
    
    # 转换每个图片
    converted_count = 0
    for img_src in matches:
        # 提取文件名（不包含路径）
        img_name = os.path.basename(img_src)
        img_name_without_ext = os.path.splitext(img_name)[0]
        
        # 查找图片文件
        image_path = find_image_file(img_name_without_ext, search_dirs)
        
        if image_path:
            print(f"正在转换: {img_name} -> {image_path}")
            
            # 转换为base64
            base64_data = get_image_base64(image_path)
            
            if base64_data:
                # 替换HTML中的图片引用
                old_src = f'src="{img_src}"'
                new_src = f'src="{base64_data}"'
                html_content = html_content.replace(old_src, new_src)
                converted_count += 1
                print(f"✅ 成功转换: {img_name}")
            else:
                print(f"❌ 转换失败: {img_name}")
        else:
            print(f"⚠️  未找到图片文件: {img_name}")
    
    # 保存更新后的HTML文件
    output_file = html_file_path.replace('.html', '_instant.html')
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"\n🎉 转换完成！")
    print(f"✅ 成功转换 {converted_count} 个图片")
    print(f"📁 输出文件: {output_file}")
    
    # 计算文件大小
    original_size = os.path.getsize(html_file_path) / (1024 * 1024)
    new_size = os.path.getsize(output_file) / (1024 * 1024)
    
    print(f"📊 文件大小变化:")
    print(f"   原始: {original_size:.2f} MB")
    print(f"   新文件: {new_size:.2f} MB")
    print(f"   增加: {new_size - original_size:.2f} MB")
    
    return output_file

if __name__ == "__main__":
    html_file = "infimind_iclip3.0_sales.html"
    
    if os.path.exists(html_file):
        print("🚀 开始将图片转换为base64内联编码...")
        output_file = convert_html_images_to_base64(html_file)
        print(f"\n✨ 即时加载版本已创建: {output_file}")
        print("🌐 现在图片将立即显示，无需加载时间！")
    else:
        print(f"❌ 未找到HTML文件: {html_file}")
