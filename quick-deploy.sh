#!/bin/bash

echo "🚀 快速部署 iClip 3.0 销售页面到 GitHub Pages"
echo "================================================"

# 检查Git状态
echo "📋 检查Git状态..."
git status

# 添加关键文件
echo "📁 添加关键文件..."
git add index.html
git add .nojekyll
git add infimind_iclip3.0_sales_pdf.html
git add DEPLOYMENT_GUIDE.md
git add README.md
git add package.json

# 添加图片文件（排除超大文件）
echo "🖼️  添加图片文件..."
git add *.png
git add *.jpg
git add *.jpeg

# 提交更改
echo "💾 提交更改..."
git commit -m "Add index.html and essential files for GitHub Pages"

# 推送到GitHub
echo "🌐 推送到GitHub..."
git push origin main

echo "✅ 部署完成！"
echo "🌍 您的网站将在以下地址可用："
echo "   https://zxy36277-jpg.github.io/iclip3-sales-page/"
echo ""
echo "⏰ 请等待1-2分钟让GitHub Pages完成部署"
