#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
图片文件重命名脚本 - 将中文文件名改为英文
"""

import os
import shutil
from pathlib import Path

# 图片文件名映射表
IMAGE_MAPPING = {
    # 产品相关
    "产品全景图.png": "product-overview.png",
    "产品全景图.webp": "product-overview.webp", 
    "产品全景图_thumb.jpg": "product-overview-thumb.jpg",
    
    # 功能相关
    "功能一.png": "feature-1.png",
    "功能一.webp": "feature-1.webp",
    "功能一_thumb.jpg": "feature-1-thumb.jpg",
    
    "功能2.png": "feature-2.png",
    "功能2.webp": "feature-2.webp", 
    "功能2_thumb.jpg": "feature-2-thumb.jpg",
    
    "功能3.png": "feature-3.png",
    "功能3.webp": "feature-3.webp",
    "功能3_thumb.jpg": "feature-3-thumb.jpg",
    
    "功能4.png": "feature-4.png",
    "功能4.webp": "feature-4.webp",
    "功能4_thumb.jpg": "feature-4-thumb.jpg",
    
    # 技术相关
    "技术.png": "technology.png",
    "技术.webp": "technology.webp",
    "技术_thumb.jpg": "technology-thumb.jpg",
    
    # 工作流相关
    "工作流对比.png": "workflow-comparison.png",
    "工作流对比.webp": "workflow-comparison.webp",
    "工作流对比_thumb.jpg": "workflow-comparison-thumb.jpg",
    
    "工作流程.png": "workflow-process.png",
    "工作流程.webp": "workflow-process.webp",
    "工作流程_thumb.jpg": "workflow-process-thumb.jpg",
    
    # 界面相关
    "发布功能界面.png": "publish-interface.png",
    "发布功能界面.webp": "publish-interface.webp",
    "发布功能界面_thumb.jpg": "publish-interface-thumb.jpg",
    
    "直播录制界面.png": "live-recording-interface.png",
    "直播录制界面.webp": "live-recording-interface.webp",
    "直播录制界面_thumb.jpg": "live-recording-interface-thumb.jpg",
    
    "专有名称，敏感词配置.png": "tag-configuration.png",
    "专有名称，敏感词配置.webp": "tag-configuration.webp",
    "专有名称，敏感词配置_thumb.jpg": "tag-configuration-thumb.jpg",
    
    # 案例相关
    "案例墙.png": "case-wall.png",
    "案例墙.webp": "case-wall.webp",
    "案例墙_thumb.jpg": "case-wall-thumb.jpg",
    
    # 主标题
    "极睿直播智能体 iClip 3.0 - 短视频智能剪辑平台.png": "main-title.png",
    "极睿直播智能体 iClip 3.0 - 短视频智能剪辑平台.webp": "main-title.webp",
    "极睿直播智能体 iClip 3.0 - 短视频智能剪辑平台_thumb.jpg": "main-title-thumb.jpg",
    
    # 其他文件
    "iclip3.0介绍.png": "iclip3-intro.png",
    "iclip3.0介绍.webp": "iclip3-intro.webp",
    "iclip3.0介绍_thumb.jpg": "iclip3-intro-thumb.jpg",
    
    "iClip3新功能介绍及后续迭代规划.png": "iclip3-features.png",
    "iClip3新功能介绍及后续迭代规划.webp": "iclip3-features.webp",
    "iClip3新功能介绍及后续迭代规划_thumb.jpg": "iclip3-features-thumb.jpg",
}

def rename_images():
    """重命名图片文件"""
    images_dir = Path("images")
    if not images_dir.exists():
        print("❌ images目录不存在")
        return
    
    print("🔄 开始重命名图片文件...")
    
    renamed_count = 0
    for old_name, new_name in IMAGE_MAPPING.items():
        old_path = images_dir / old_name
        new_path = images_dir / new_name
        
        if old_path.exists():
            try:
                shutil.move(str(old_path), str(new_path))
                print(f"✅ {old_name} → {new_name}")
                renamed_count += 1
            except Exception as e:
                print(f"❌ 重命名失败 {old_name}: {e}")
        else:
            print(f"⚠️ 文件不存在: {old_name}")
    
    print(f"\n🎉 重命名完成！共处理 {renamed_count} 个文件")

def update_html_files():
    """更新HTML文件中的图片路径"""
    html_files = [
        "infimind_iclip3.0_sales.html",
        "infimind_iclip3.0_sales_fixed.html",
        "simple_test.html",
        "test_images.html"
    ]
    
    print("\n🔄 更新HTML文件中的图片路径...")
    
    for html_file in html_files:
        if not os.path.exists(html_file):
            continue
            
        print(f"📝 更新 {html_file}")
        
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 替换图片路径
        for old_name, new_name in IMAGE_MAPPING.items():
            content = content.replace(f'images/{old_name}', f'images/{new_name}')
            content = content.replace(f'"images/{old_name}"', f'"images/{new_name}"')
            content = content.replace(f"'images/{old_name}'", f"'images/{new_name}'")
        
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ {html_file} 更新完成")

if __name__ == "__main__":
    print("🚀 图片文件重命名工具")
    print("=" * 50)
    
    # 重命名图片文件
    rename_images()
    
    # 更新HTML文件
    update_html_files()
    
    print("\n🎉 所有操作完成！")
    print("💡 建议提交更改并推送到GitHub Pages")
