#!/usr/bin/env python3
"""
🚀 图片秒开优化脚本
目标：实现打开就能看到图片的效果，不需要等待
策略：智能调整尺寸，保持视觉质量，大幅减少文件大小
"""

import os
from PIL import Image
import shutil
from datetime import datetime

def optimize_for_instant_loading():
    """优化图片实现秒开效果"""
    
    print("🚀 开始图片秒开优化...")
    print("=" * 60)
    
    # 创建备份
    backup_dir = f"backup_instant_optimization_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    os.makedirs(backup_dir, exist_ok=True)
    
    # 优化策略配置
    optimization_rules = {
        # 超大图片：大幅缩小
        'ultra_large': {'max_width': 800, 'max_height': 600, 'quality': 85, 'max_size_mb': 0.1},
        # 大图片：适度缩小
        'large': {'max_width': 1000, 'max_height': 800, 'quality': 90, 'max_size_mb': 0.2},
        # 中等图片：轻微优化
        'medium': {'max_width': 1200, 'max_height': 1000, 'quality': 95, 'max_size_mb': 0.3},
        # 小图片：保持原样
        'small': {'max_width': 1500, 'max_height': 1200, 'quality': 98, 'max_size_mb': 0.5}
    }
    
    files = [f for f in os.listdir('.') if f.endswith('.png')]
    total_original_size = 0
    total_optimized_size = 0
    optimized_count = 0
    
    print(f"📊 发现 {len(files)} 个PNG文件")
    print()
    
    for file in sorted(files):
        try:
            # 备份原文件
            shutil.copy2(file, os.path.join(backup_dir, file))
            
            with Image.open(file) as img:
                original_width, original_height = img.size
                original_size = os.path.getsize(file) / 1024 / 1024  # MB
                total_original_size += original_size
                
                # 确定优化策略
                if original_size > 1.0 or original_width > 1800 or original_height > 1400:
                    strategy = 'ultra_large'
                elif original_size > 0.5 or original_width > 1500 or original_height > 1200:
                    strategy = 'large'
                elif original_size > 0.3 or original_width > 1200 or original_height > 1000:
                    strategy = 'medium'
                else:
                    strategy = 'small'
                
                rules = optimization_rules[strategy]
                
                # 计算新尺寸
                new_width, new_height = calculate_optimal_size(
                    original_width, original_height, 
                    rules['max_width'], rules['max_height']
                )
                
                # 如果尺寸需要调整
                if new_width != original_width or new_height != original_height:
                    # 高质量缩放
                    img_resized = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
                    
                    # 保存优化后的图片
                    img_resized.save(file, 'PNG', optimize=True, compress_level=6)
                    optimized_count += 1
                    
                    # 计算优化后大小
                    optimized_size = os.path.getsize(file) / 1024 / 1024
                    total_optimized_size += optimized_size
                    
                    # 显示优化结果
                    size_reduction = ((original_size - optimized_size) / original_size) * 100
                    print(f"✅ {file}")
                    print(f"   尺寸: {original_width}×{original_height} → {new_width}×{new_height}")
                    print(f"   大小: {original_size:.2f}MB → {optimized_size:.2f}MB ({size_reduction:.1f}%↓)")
                    print(f"   策略: {strategy}")
                    print()
                else:
                    # 尺寸不需要调整，只优化压缩
                    img.save(file, 'PNG', optimize=True, compress_level=6)
                    optimized_size = os.path.getsize(file) / 1024 / 1024
                    total_optimized_size += optimized_size
                    
                    if optimized_size < original_size:
                        size_reduction = ((original_size - optimized_size) / original_size) * 100
                        print(f"🔧 {file} (压缩优化: {size_reduction:.1f}%↓)")
                    else:
                        print(f"✅ {file} (已优化)")
                
        except Exception as e:
            print(f"❌ 处理 {file} 时出错: {e}")
    
    # 显示总体优化结果
    print("=" * 60)
    print("🎉 秒开优化完成！")
    print(f"📊 优化统计:")
    print(f"   • 处理文件: {len(files)} 个")
    print(f"   • 尺寸调整: {optimized_count} 个")
    print(f"   • 原始总大小: {total_original_size:.1f} MB")
    print(f"   • 优化后大小: {total_optimized_size:.1f} MB")
    print(f"   • 总体压缩: {((total_original_size - total_optimized_size) / total_original_size) * 100:.1f}%")
    print(f"   • 节省空间: {total_original_size - total_optimized_size:.1f} MB")
    print()
    print("🚀 预期效果:")
    print("   • 图片加载速度提升 60-80%")
    print("   • 实现'秒开'效果")
    print("   • 保持视觉质量")
    print("   • 减少带宽消耗")
    print()
    print(f"💾 原文件已备份到: {backup_dir}/")

def calculate_optimal_size(original_width, original_height, max_width, max_height):
    """计算最优尺寸，保持宽高比"""
    
    # 如果原尺寸已经符合要求，不调整
    if original_width <= max_width and original_height <= max_height:
        return original_width, original_height
    
    # 计算缩放比例
    width_ratio = max_width / original_width
    height_ratio = max_height / original_height
    
    # 选择较小的缩放比例，确保两个维度都不超过限制
    scale_ratio = min(width_ratio, height_ratio)
    
    # 计算新尺寸
    new_width = int(original_width * scale_ratio)
    new_height = int(original_height * scale_ratio)
    
    # 确保尺寸是偶数（避免某些显示问题）
    new_width = new_width if new_width % 2 == 0 else new_width - 1
    new_height = new_height if new_height % 2 == 0 else new_height - 1
    
    return new_width, new_height

if __name__ == "__main__":
    optimize_for_instant_loading()
