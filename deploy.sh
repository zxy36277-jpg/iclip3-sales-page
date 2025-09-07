#!/bin/bash

echo "🚀 iClip 3.0 销售页面部署脚本"
echo "================================"

# 检查Git状态
if [ ! -d ".git" ]; then
    echo "❌ 未找到Git仓库，正在初始化..."
    git init
    git add .
    git commit -m "Initial commit: iClip 3.0 sales page"
fi

echo "📋 部署选项："
echo "1. GitHub Pages"
echo "2. Netlify Drop"
echo "3. Vercel"
echo "4. 本地预览"
echo ""

read -p "请选择部署方式 (1-4): " choice

case $choice in
    1)
        echo "🔧 GitHub Pages 部署步骤："
        echo "1. 访问 https://github.com/new"
        echo "2. 创建新仓库：iclip3-sales-page"
        echo "3. 运行以下命令："
        echo "   git remote add origin https://github.com/你的用户名/iclip3-sales-page.git"
        echo "   git branch -M main"
        echo "   git push -u origin main"
        echo "4. 在仓库设置中启用 GitHub Pages"
        echo ""
        echo "📁 当前文件已准备好上传到GitHub"
        ;;
    2)
        echo "🌐 Netlify Drop 部署："
        echo "1. 访问 https://app.netlify.com/drop"
        echo "2. 将当前文件夹拖拽到页面上"
        echo "3. 获得即时部署链接"
        echo ""
        echo "📁 当前文件夹已准备好上传到Netlify"
        ;;
    3)
        echo "⚡ Vercel 部署："
        echo "1. 访问 https://vercel.com"
        echo "2. 导入GitHub仓库或直接上传文件"
        echo "3. 自动部署完成"
        echo ""
        echo "📁 当前文件已准备好上传到Vercel"
        ;;
    4)
        echo "🏠 启动本地预览服务器..."
        if command -v npx &> /dev/null; then
            npx http-server . -p 8080 -o
        else
            echo "❌ 需要安装Node.js来运行本地服务器"
            echo "请访问 https://nodejs.org 安装Node.js"
        fi
        ;;
    *)
        echo "❌ 无效选择"
        ;;
esac

echo ""
echo "✅ 部署准备完成！"
echo "📄 主页面文件：infimind_iclip3.0_sales.html"
echo "📖 详细说明请查看 README.md"
