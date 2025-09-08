#!/usr/bin/env python3
"""
HTML优化器 - 添加WebP支持、懒加载和渐进式加载
"""

import re
import os
import json
from pathlib import Path

class HTMLOptimizer:
    def __init__(self):
        self.html_file = "infimind_iclip3.0_sales.html"
        self.webp_dir = "images_webp"
        self.compressed_dir = "images_compressed"
        self.thumbnails_dir = "images_thumbnails"
        
    def get_webp_path(self, png_path):
        """获取WebP版本路径"""
        filename = os.path.basename(png_path)
        webp_filename = filename.replace('.png', '.webp')
        return os.path.join(self.webp_dir, webp_filename)
    
    def get_compressed_path(self, png_path):
        """获取压缩版本路径"""
        filename = os.path.basename(png_path)
        jpg_filename = filename.replace('.png', '.jpg')
        return os.path.join(self.compressed_dir, jpg_filename)
    
    def get_thumbnail_path(self, png_path):
        """获取缩略图路径"""
        filename = os.path.basename(png_path)
        thumb_filename = filename.replace('.png', '_thumb.jpg')
        return os.path.join(self.thumbnails_dir, thumb_filename)
    
    def create_optimized_img_tag(self, original_img_tag, png_path):
        """创建优化的图片标签"""
        # 提取原始属性
        src_match = re.search(r'src=["\']([^"\']+)["\']', original_img_tag)
        alt_match = re.search(r'alt=["\']([^"\']*)["\']', original_img_tag)
        class_match = re.search(r'class=["\']([^"\']*)["\']', original_img_tag)
        
        src = src_match.group(1) if src_match else png_path
        alt = alt_match.group(1) if alt_match else ""
        css_class = class_match.group(1) if class_match else ""
        
        # 获取优化后的路径
        webp_path = self.get_webp_path(png_path)
        compressed_path = self.get_compressed_path(png_path)
        thumbnail_path = self.get_thumbnail_path(png_path)
        
        # 创建优化的图片标签
        optimized_tag = f'''
        <picture class="lazy-load {css_class}">
            <source srcset="{webp_path}" type="image/webp">
            <source srcset="{compressed_path}" type="image/jpeg">
            <img 
                src="{thumbnail_path}" 
                data-src="{compressed_path}"
                data-webp="{webp_path}"
                alt="{alt}"
                class="lazy-img {css_class}"
                loading="lazy"
                decoding="async"
                style="transition: opacity 0.3s ease;"
            >
        </picture>'''
        
        return optimized_tag.strip()
    
    def add_lazy_loading_script(self, html_content):
        """添加懒加载脚本"""
        lazy_script = '''
    <script>
        // 懒加载和WebP支持
        document.addEventListener('DOMContentLoaded', function() {
            // 检测WebP支持
            function supportsWebP() {
                const canvas = document.createElement('canvas');
                canvas.width = 1;
                canvas.height = 1;
                return canvas.toDataURL('image/webp').indexOf('data:image/webp') === 0;
            }
            
            // 懒加载图片
            function lazyLoadImages() {
                const images = document.querySelectorAll('img[data-src]');
                const imageObserver = new IntersectionObserver((entries, observer) => {
                    entries.forEach(entry => {
                        if (entry.isIntersecting) {
                            const img = entry.target;
                            const webpSrc = img.getAttribute('data-webp');
                            const fallbackSrc = img.getAttribute('data-src');
                            
                            // 优先使用WebP
                            if (supportsWebP() && webpSrc) {
                                img.src = webpSrc;
                            } else {
                                img.src = fallbackSrc;
                            }
                            
                            // 添加加载完成效果
                            img.onload = function() {
                                img.style.opacity = '1';
                            };
                            
                            // 移除data属性
                            img.removeAttribute('data-src');
                            img.removeAttribute('data-webp');
                            
                            observer.unobserve(img);
                        }
                    });
                }, {
                    rootMargin: '50px 0px',
                    threshold: 0.01
                });
                
                images.forEach(img => {
                    imageObserver.observe(img);
                });
            }
            
            // 初始化懒加载
            lazyLoadImages();
            
            // 预加载关键图片
            function preloadCriticalImages() {
                const criticalImages = [
                    'images_webp/极睿直播智能体 iClip 3.0 - 短视频智能剪辑平台.webp',
                    'images_webp/产品全景图.webp'
                ];
                
                criticalImages.forEach(src => {
                    const link = document.createElement('link');
                    link.rel = 'preload';
                    link.as = 'image';
                    link.href = src;
                    document.head.appendChild(link);
                });
            }
            
            preloadCriticalImages();
        });
    </script>'''
        
        # 在</body>标签前插入脚本
        html_content = html_content.replace('</body>', lazy_script + '\n</body>')
        return html_content
    
    def add_loading_styles(self, html_content):
        """添加加载样式"""
        loading_styles = '''
        /* 懒加载样式 */
        .lazy-load {
            position: relative;
            overflow: hidden;
        }
        
        .lazy-img {
            opacity: 0;
            transition: opacity 0.3s ease;
            width: 100%;
            height: auto;
        }
        
        .lazy-img.loaded {
            opacity: 1;
        }
        
        /* 加载占位符 */
        .lazy-load::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, #f0f0f0 25%, #e0e0e0 50%, #f0f0f0 75%);
            background-size: 200% 100%;
            animation: loading 1.5s infinite;
            z-index: 1;
        }
        
        .lazy-img.loaded + .lazy-load::before {
            display: none;
        }
        
        @keyframes loading {
            0% { background-position: 200% 0; }
            100% { background-position: -200% 0; }
        }
        
        /* 图片容器优化 */
        picture {
            display: block;
            width: 100%;
        }
        
        /* 响应式图片 */
        @media (max-width: 768px) {
            .lazy-img {
                max-width: 100%;
                height: auto;
            }
        }'''
        
        # 在</style>标签前插入样式
        html_content = html_content.replace('</style>', loading_styles + '\n</style>')
        return html_content
    
    def optimize_html(self):
        """优化HTML文件"""
        print("🚀 开始优化HTML文件...")
        
        # 读取HTML文件
        with open(self.html_file, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        # 查找所有PNG图片引用
        png_pattern = r'<img[^>]*src=["\']([^"\']*\.png)["\'][^>]*>'
        png_matches = re.findall(png_pattern, html_content)
        
        print(f"📸 找到 {len(png_matches)} 个PNG图片引用")
        
        # 替换每个PNG图片
        for png_path in png_matches:
            # 查找对应的img标签
            img_pattern = rf'<img[^>]*src=["\']({re.escape(png_path)})["\'][^>]*>'
            img_match = re.search(img_pattern, html_content)
            
            if img_match:
                original_tag = img_match.group(0)
                optimized_tag = self.create_optimized_img_tag(original_tag, png_path)
                html_content = html_content.replace(original_tag, optimized_tag)
                print(f"   ✅ 优化: {os.path.basename(png_path)}")
        
        # 添加懒加载样式
        html_content = self.add_loading_styles(html_content)
        
        # 添加懒加载脚本
        html_content = self.add_lazy_loading_script(html_content)
        
        # 添加性能优化meta标签
        performance_meta = '''
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <meta name="theme-color" content="#0a1628">'''
        
        html_content = html_content.replace(
            '<meta name="viewport" content="width=device-width, initial-scale=1.0">',
            performance_meta
        )
        
        # 保存优化后的HTML
        output_file = "infimind_iclip3.0_sales_optimized.html"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"✅ HTML优化完成！保存为: {output_file}")
        return output_file

def main():
    optimizer = HTMLOptimizer()
    optimizer.optimize_html()

if __name__ == "__main__":
    main()
