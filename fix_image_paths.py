#!/usr/bin/env python3
"""
修复HTML中的图片路径问题
"""

import re
import os

def fix_image_paths():
    html_file = "infimind_iclip3.0_sales.html"
    
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 修复所有 .jpg 扩展名为 .png
    content = re.sub(r'data-src="images/([^"]+)\.jpg"', r'data-src="images/\1.png"', content)
    
    # 修复WebP路径中的重复images前缀
    content = re.sub(r'data-webp="images/images_webp/', r'data-webp="images/', content)
    content = re.sub(r'srcset="images_webp/', r'srcset="images/', content)
    content = re.sub(r'srcset="images_compressed/', r'srcset="images/', content)
    
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ 图片路径修复完成")

if __name__ == "__main__":
    fix_image_paths()
