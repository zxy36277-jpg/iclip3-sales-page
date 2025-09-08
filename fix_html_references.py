#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复HTML文件中的图片引用问题
"""

import os
import re
from pathlib import Path

# 图片文件名映射表（包含不存在的.jpg文件）
IMAGE_MAPPING = {
    # 产品相关
    "产品全景图.png": "product-overview.png",
    "产品全景图.webp": "product-overview.webp", 
    "产品全景图_thumb.jpg": "product-overview-thumb.jpg",
    "产品全景图.jpg": "product-overview.png",  # 不存在的.jpg文件，指向.png
    
    # 功能相关
    "功能一.png": "feature-1.png",
    "功能一.webp": "feature-1.webp",
    "功能一_thumb.jpg": "feature-1-thumb.jpg",
    "功能一.jpg": "feature-1.png",  # 不存在的.jpg文件，指向.png
    
    "功能2.png": "feature-2.png",
    "功能2.webp": "feature-2.webp", 
    "功能2_thumb.jpg": "feature-2-thumb.jpg",
    "功能2.jpg": "feature-2.png",  # 不存在的.jpg文件，指向.png
    
    "功能3.png": "feature-3.png",
    "功能3.webp": "feature-3.webp",
    "功能3_thumb.jpg": "feature-3-thumb.jpg",
    "功能3.jpg": "feature-3.png",  # 不存在的.jpg文件，指向.png
    
    "功能4.png": "feature-4.png",
    "功能4.webp": "feature-4.webp",
    "功能4_thumb.jpg": "feature-4-thumb.jpg",
    "功能4.jpg": "feature-4.png",  # 不存在的.jpg文件，指向.png
    
    # 技术相关
    "技术.png": "technology.png",
    "技术.webp": "technology.webp",
    "技术_thumb.jpg": "technology-thumb.jpg",
    "技术.jpg": "technology.png",  # 不存在的.jpg文件，指向.png
    
    # 工作流相关
    "工作流对比.png": "workflow-comparison.png",
    "工作流对比.webp": "workflow-comparison.webp",
    "工作流对比_thumb.jpg": "workflow-comparison-thumb.jpg",
    "工作流对比.jpg": "workflow-comparison.png",  # 不存在的.jpg文件，指向.png
    
    "工作流程.png": "workflow-process.png",
    "工作流程.webp": "workflow-process.webp",
    "工作流程_thumb.jpg": "workflow-process-thumb.jpg",
    "工作流程.jpg": "workflow-process.png",  # 不存在的.jpg文件，指向.png
    
    # 界面相关
    "发布功能界面.png": "publish-interface.png",
    "发布功能界面.webp": "publish-interface.webp",
    "发布功能界面_thumb.jpg": "publish-interface-thumb.jpg",
    "发布功能界面.jpg": "publish-interface.png",  # 不存在的.jpg文件，指向.png
    
    "直播录制界面.png": "live-recording-interface.png",
    "直播录制界面.webp": "live-recording-interface.webp",
    "直播录制界面_thumb.jpg": "live-recording-interface-thumb.jpg",
    "直播录制界面.jpg": "live-recording-interface.png",  # 不存在的.jpg文件，指向.png
    
    "专有名称，敏感词配置.png": "tag-configuration.png",
    "专有名称，敏感词配置.webp": "tag-configuration.webp",
    "专有名称，敏感词配置_thumb.jpg": "tag-configuration-thumb.jpg",
    "专有名称，敏感词配置.jpg": "tag-configuration.png",  # 不存在的.jpg文件，指向.png
    
    # 案例相关
    "案例墙.png": "case-wall.png",
    "案例墙.webp": "case-wall.webp",
    "案例墙_thumb.jpg": "case-wall-thumb.jpg",
    "案例墙.jpg": "case-wall.png",  # 不存在的.jpg文件，指向.png
    
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

def fix_html_file(file_path):
    """修复HTML文件中的图片引用"""
    print(f"📝 修复 {file_path}")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    # 替换图片路径
    for old_name, new_name in IMAGE_MAPPING.items():
        # 替换各种可能的引用格式
        patterns = [
            f'images/{old_name}',
            f'"images/{old_name}"',
            f"'images/{old_name}'",
            f'images/{old_name}',
            f'=images/{old_name}',
            f'src="images/{old_name}"',
            f"src='images/{old_name}'",
            f'srcset="images/{old_name}"',
            f"srcset='images/{old_name}'",
        ]
        
        for pattern in patterns:
            if pattern in content:
                new_pattern = pattern.replace(old_name, new_name)
                content = content.replace(pattern, new_pattern)
                print(f"  ✅ {pattern} → {new_pattern}")
    
    # 检查是否有变化
    if content != original_content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ {file_path} 修复完成")
        return True
    else:
        print(f"ℹ️ {file_path} 无需修复")
        return False

def main():
    """主函数"""
    print("🔧 HTML图片引用修复工具")
    print("=" * 50)
    
    # 需要修复的HTML文件
    html_files = [
        "infimind_iclip3.0_sales.html",
        "infimind_iclip3.0_sales_fixed.html",
        "simple_test.html",
        "test_images.html",
        "english_filename_test.html"
    ]
    
    fixed_count = 0
    for html_file in html_files:
        if os.path.exists(html_file):
            if fix_html_file(html_file):
                fixed_count += 1
        else:
            print(f"⚠️ 文件不存在: {html_file}")
    
    print(f"\n🎉 修复完成！共修复 {fixed_count} 个文件")
    
    # 验证修复结果
    print("\n🔍 验证修复结果...")
    for html_file in html_files:
        if os.path.exists(html_file):
            with open(html_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 检查是否还有中文文件名引用
            chinese_refs = re.findall(r'images/[^"\'>\s]*[一-龟][^"\'>\s]*', content)
            if chinese_refs:
                print(f"⚠️ {html_file} 仍有中文引用: {chinese_refs}")
            else:
                print(f"✅ {html_file} 无中文引用")

if __name__ == "__main__":
    main()
