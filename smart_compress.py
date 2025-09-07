#!/usr/bin/env python3
"""
智能PNG压缩脚本 - 保持PNG格式，合理压缩
"""

import os
import sys
from PIL import Image, ImageOps
import glob

def smart_compress_png(input_path, output_path, max_width=1920, quality=85):
    """
    智能压缩PNG图片
    - 保持PNG格式
    - 合理调整尺寸
    - 优化压缩级别
    """
    try:
        # 打开图片
        with Image.open(input_path) as img:
            # 转换为RGB模式（去除透明度，减少文件大小）
            if img.mode in ('RGBA', 'LA', 'P'):
                # 创建白色背景
                background = Image.new('RGB', img.size, (255, 255, 255))
                if img.mode == 'P':
                    img = img.convert('RGBA')
                background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                img = background
            elif img.mode != 'RGB':
                img = img.convert('RGB')
            
            # 调整尺寸
            if img.width > max_width:
                ratio = max_width / img.width
                new_height = int(img.height * ratio)
                img = img.resize((max_width, new_height), Image.Resampling.LANCZOS)
            
            # 保存为PNG格式，使用优化压缩
            img.save(output_path, 'PNG', optimize=True, compress_level=6)
            
            return True
    except Exception as e:
        print(f"压缩失败 {input_path}: {e}")
        return False

def main():
    # 获取所有PNG文件
    png_files = glob.glob("*.png")
    
    if not png_files:
        print("没有找到PNG文件")
        return
    
    print(f"找到 {len(png_files)} 个PNG文件")
    
    # 创建备份目录
    backup_dir = "compressed_backup"
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)
    
    compressed_count = 0
    total_original_size = 0
    total_compressed_size = 0
    
    for png_file in png_files:
        # 获取原始文件大小
        original_size = os.path.getsize(png_file)
        total_original_size += original_size
        
        # 备份原文件
        backup_path = os.path.join(backup_dir, png_file)
        if not os.path.exists(backup_path):
            os.rename(png_file, backup_path)
        
        # 压缩文件
        if smart_compress_png(backup_path, png_file):
            compressed_size = os.path.getsize(png_file)
            total_compressed_size += compressed_size
            compressed_count += 1
            
            compression_ratio = (1 - compressed_size / original_size) * 100
            print(f"✅ {png_file}: {original_size/1024/1024:.1f}MB → {compressed_size/1024/1024:.1f}MB ({compression_ratio:.1f}% 压缩)")
        else:
            # 如果压缩失败，恢复原文件
            os.rename(backup_path, png_file)
            print(f"❌ {png_file}: 压缩失败，保持原文件")
    
    print(f"\n📊 压缩统计:")
    print(f"成功压缩: {compressed_count}/{len(png_files)} 个文件")
    print(f"原始总大小: {total_original_size/1024/1024:.1f}MB")
    print(f"压缩后总大小: {total_compressed_size/1024/1024:.1f}MB")
    print(f"总体压缩率: {(1 - total_compressed_size / total_original_size) * 100:.1f}%")
    print(f"节省空间: {(total_original_size - total_compressed_size)/1024/1024:.1f}MB")

if __name__ == "__main__":
    main()
