#!/usr/bin/env python3
"""
修复超大图片文件
"""

import os
from PIL import Image, ImageOps

def fix_large_image():
    input_file = "极睿直播智能体 iClip 3.0 - 短视频智能剪辑平台.png"
    
    try:
        # 设置PIL的安全限制
        Image.MAX_IMAGE_PIXELS = None
        
        print(f"正在处理超大图片: {input_file}")
        
        with Image.open(input_file) as img:
            print(f"原始尺寸: {img.size}")
            print(f"原始模式: {img.mode}")
            
            # 如果图片太大，先大幅缩小
            max_dimension = 4000  # 最大边长4000像素
            if max(img.size) > max_dimension:
                ratio = max_dimension / max(img.size)
                new_size = (int(img.size[0] * ratio), int(img.size[1] * ratio))
                print(f"缩小到: {new_size}")
                img = img.resize(new_size, Image.Resampling.LANCZOS)
            
            # 转换为RGB模式
            if img.mode in ('RGBA', 'LA', 'P'):
                background = Image.new('RGB', img.size, (255, 255, 255))
                if img.mode == 'P':
                    img = img.convert('RGBA')
                background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                img = background
            elif img.mode != 'RGB':
                img = img.convert('RGB')
            
            # 保存为PNG
            output_file = "极睿直播智能体_compressed.png"
            img.save(output_file, 'PNG', optimize=True, compress_level=6)
            
            original_size = os.path.getsize(input_file)
            new_size = os.path.getsize(output_file)
            compression_ratio = (1 - new_size / original_size) * 100
            
            print(f"✅ 压缩成功!")
            print(f"原始大小: {original_size/1024/1024:.1f}MB")
            print(f"压缩后大小: {new_size/1024/1024:.1f}MB")
            print(f"压缩率: {compression_ratio:.1f}%")
            
            # 替换原文件
            os.rename(input_file, f"{input_file}.backup")
            os.rename(output_file, input_file)
            
            return True
            
    except Exception as e:
        print(f"❌ 处理失败: {e}")
        return False

if __name__ == "__main__":
    fix_large_image()
