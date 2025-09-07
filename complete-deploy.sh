#!/bin/bash

echo "🚀 完整部署 iClip 3.0 销售页面到 GitHub Pages"
echo "================================================"

# 检查Git状态
echo "📋 检查Git状态..."
git status

# 添加所有必要文件
echo "📁 添加所有必要文件..."
git add index.html
git add .nojekyll
git add infimind_iclip3.0_sales.html
git add infimind_iclip3.0_sales_pdf.html
git add MANUAL_UPLOAD_GUIDE.md
git add README.md
git add package.json
git add DEPLOYMENT_GUIDE.md

# 添加图片文件（分批添加避免超时）
echo "🖼️  添加图片文件..."
git add *.png

# 提交更改
echo "💾 提交更改..."
git commit -m "Complete deployment: Add all files for GitHub Pages

- Add index.html as main entry point
- Add .nojekyll to disable Jekyll processing
- Add all HTML pages and assets
- Add documentation and guides"

# 推送到GitHub
echo "🌐 推送到GitHub..."
git push origin main

echo "✅ 部署完成！"
echo ""
echo "🔧 接下来需要手动配置GitHub Pages："
echo "1. 访问: https://github.com/zxy36277-jpg/iclip3-sales-page"
echo "2. 点击 Settings 标签"
echo "3. 左侧菜单找到 Pages"
echo "4. 配置:"
echo "   - Source: Deploy from a branch"
echo "   - Branch: main"
echo "   - Folder: / (root)"
echo "5. 点击 Save"
echo ""
echo "🌍 配置完成后，网站将在以下地址可用："
echo "   https://zxy36277-jpg.github.io/iclip3-sales-page/"
echo ""
echo "⏰ 请等待2-3分钟让GitHub Pages完成部署"
