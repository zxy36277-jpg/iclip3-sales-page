#!/usr/bin/env python3
"""
终极图片优化器 - 实现WebP转换、懒加载和渐进式加载
"""

import os
import sys
from PIL import Image, ImageOps
import subprocess
import json
from pathlib import Path

class UltimateImageOptimizer:
    def __init__(self):
        self.original_dir = "original_images_backup"
        self.webp_dir = "images_webp"
        self.compressed_dir = "images_compressed"
        self.thumbnails_dir = "images_thumbnails"
        self.optimization_log = []
        
    def create_directories(self):
        """创建必要的目录"""
        for dir_name in [self.webp_dir, self.compressed_dir, self.thumbnails_dir]:
            os.makedirs(dir_name, exist_ok=True)
        print("✅ 创建优化目录完成")
    
    def get_image_files(self):
        """获取所有PNG图片文件"""
        png_files = [f for f in os.listdir('.') if f.endswith('.png')]
        return png_files
    
    def optimize_image_quality(self, input_path, output_path, quality=85, max_width=1200):
        """优化图片质量和尺寸"""
        try:
            with Image.open(input_path) as img:
                # 转换为RGB模式（去除透明度）
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
                
                # 保存优化后的图片
                img.save(output_path, 'JPEG', quality=quality, optimize=True, progressive=True)
                
                original_size = os.path.getsize(input_path)
                new_size = os.path.getsize(output_path)
                compression_ratio = (1 - new_size / original_size) * 100
                
                return {
                    'original_size': original_size,
                    'new_size': new_size,
                    'compression_ratio': compression_ratio,
                    'dimensions': f"{img.width}x{img.height}"
                }
        except Exception as e:
            print(f"❌ 优化图片失败 {input_path}: {e}")
            return None
    
    def create_webp_version(self, input_path, output_path, quality=80):
        """创建WebP版本"""
        try:
            with Image.open(input_path) as img:
                # 转换为RGB模式
                if img.mode in ('RGBA', 'LA', 'P'):
                    background = Image.new('RGB', img.size, (255, 255, 255))
                    if img.mode == 'P':
                        img = img.convert('RGBA')
                    background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                    img = background
                elif img.mode != 'RGB':
                    img = img.convert('RGB')
                
                # 保存为WebP
                img.save(output_path, 'WebP', quality=quality, optimize=True)
                
                original_size = os.path.getsize(input_path)
                webp_size = os.path.getsize(output_path)
                compression_ratio = (1 - webp_size / original_size) * 100
                
                return {
                    'original_size': original_size,
                    'webp_size': webp_size,
                    'compression_ratio': compression_ratio
                }
        except Exception as e:
            print(f"❌ 创建WebP失败 {input_path}: {e}")
            return None
    
    def create_thumbnail(self, input_path, output_path, max_size=300):
        """创建缩略图"""
        try:
            with Image.open(input_path) as img:
                # 创建缩略图
                img.thumbnail((max_size, max_size), Image.Resampling.LANCZOS)
                
                # 转换为RGB
                if img.mode in ('RGBA', 'LA', 'P'):
                    background = Image.new('RGB', img.size, (255, 255, 255))
                    if img.mode == 'P':
                        img = img.convert('RGBA')
                    background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                    img = background
                elif img.mode != 'RGB':
                    img = img.convert('RGB')
                
                # 保存缩略图
                img.save(output_path, 'JPEG', quality=75, optimize=True)
                
                return os.path.getsize(output_path)
        except Exception as e:
            print(f"❌ 创建缩略图失败 {input_path}: {e}")
            return None
    
    def optimize_all_images(self):
        """优化所有图片"""
        print("🚀 开始终极图片优化...")
        self.create_directories()
        
        png_files = self.get_image_files()
        total_original_size = 0
        total_compressed_size = 0
        total_webp_size = 0
        
        for i, png_file in enumerate(png_files, 1):
            print(f"📸 处理图片 {i}/{len(png_files)}: {png_file}")
            
            # 记录原始大小
            original_size = os.path.getsize(png_file)
            total_original_size += original_size
            
            # 创建压缩版本
            compressed_path = os.path.join(self.compressed_dir, png_file.replace('.png', '.jpg'))
            compressed_result = self.optimize_image_quality(png_file, compressed_path, quality=85, max_width=1200)
            
            if compressed_result:
                total_compressed_size += compressed_result['new_size']
                print(f"   📦 压缩版本: {compressed_result['new_size']/1024:.1f}KB ({compressed_result['compression_ratio']:.1f}% 压缩)")
            
            # 创建WebP版本
            webp_path = os.path.join(self.webp_dir, png_file.replace('.png', '.webp'))
            webp_result = self.create_webp_version(png_file, webp_path, quality=80)
            
            if webp_result:
                total_webp_size += webp_result['webp_size']
                print(f"   🌐 WebP版本: {webp_result['webp_size']/1024:.1f}KB ({webp_result['compression_ratio']:.1f}% 压缩)")
            
            # 创建缩略图
            thumbnail_path = os.path.join(self.thumbnails_dir, png_file.replace('.png', '_thumb.jpg'))
            thumbnail_size = self.create_thumbnail(png_file, thumbnail_path, max_size=300)
            
            if thumbnail_size:
                print(f"   🖼️  缩略图: {thumbnail_size/1024:.1f}KB")
            
            # 记录优化信息
            self.optimization_log.append({
                'file': png_file,
                'original_size': original_size,
                'compressed_size': compressed_result['new_size'] if compressed_result else 0,
                'webp_size': webp_result['webp_size'] if webp_result else 0,
                'thumbnail_size': thumbnail_size or 0
            })
        
        # 输出统计信息
        print("\n📊 优化统计:")
        print(f"   原始总大小: {total_original_size/1024/1024:.1f}MB")
        print(f"   压缩后大小: {total_compressed_size/1024/1024:.1f}MB")
        print(f"   WebP大小: {total_webp_size/1024/1024:.1f}MB")
        print(f"   压缩率: {(1-total_compressed_size/total_original_size)*100:.1f}%")
        print(f"   WebP压缩率: {(1-total_webp_size/total_original_size)*100:.1f}%")
        
        # 保存优化日志
        with open('optimization_log.json', 'w', encoding='utf-8') as f:
            json.dump(self.optimization_log, f, ensure_ascii=False, indent=2)
        
        print("✅ 图片优化完成！")
        return self.optimization_log

def main():
    optimizer = UltimateImageOptimizer()
    optimizer.optimize_all_images()

if __name__ == "__main__":
    main()
