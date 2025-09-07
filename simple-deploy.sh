#!/bin/bash

# 简化的部署脚本
echo "🚀 iClip 3.0 销售页面部署助手"
echo "=================================="
echo ""

# 获取GitHub用户名
echo "请输入您的GitHub用户名："
read -r GITHUB_USERNAME

if [ -z "$GITHUB_USERNAME" ]; then
    echo "❌ GitHub用户名不能为空"
    exit 1
fi

REPO_NAME="iclip3-sales-page"
REPO_URL="https://github.com/${GITHUB_USERNAME}/${REPO_NAME}.git"

echo ""
echo "📋 部署信息："
echo "   仓库名称: ${REPO_NAME}"
echo "   仓库地址: ${REPO_URL}"
echo "   网站地址: https://${GITHUB_USERNAME}.github.io/${REPO_NAME}/"
echo ""

# 设置远程仓库
echo "🔗 配置Git远程仓库..."
if git remote get-url origin >/dev/null 2>&1; then
    git remote set-url origin "$REPO_URL"
    echo "✅ 已更新远程仓库URL"
else
    git remote add origin "$REPO_URL"
    echo "✅ 已添加远程仓库"
fi

# 设置主分支
echo "🌿 设置主分支..."
git branch -M main

echo ""
echo "📝 接下来请按以下步骤操作："
echo ""
echo "1️⃣ 在浏览器中打开: https://github.com/new"
echo "2️⃣ 仓库名称填写: ${REPO_NAME}"
echo "3️⃣ 描述填写: iClip 3.0 短视频智能剪辑平台销售页面"
echo "4️⃣ 选择: Public (公开)"
echo "5️⃣ 不要勾选任何选项 (README, .gitignore, license)"
echo "6️⃣ 点击 'Create repository'"
echo ""
echo "创建完成后，按回车键继续推送代码..."
read -r

echo "🚀 推送代码到GitHub..."
if git push -u origin main; then
    echo "✅ 代码推送成功！"
    echo ""
    echo "🎉 最后一步 - 启用GitHub Pages："
    echo "1️⃣ 访问: https://github.com/${GITHUB_USERNAME}/${REPO_NAME}/settings/pages"
    echo "2️⃣ Source 选择: 'Deploy from a branch'"
    echo "3️⃣ Branch 选择: 'main'"
    echo "4️⃣ Folder 选择: '/ (root)'"
    echo "5️⃣ 点击 'Save'"
    echo ""
    echo "⏳ 等待1-2分钟部署完成"
    echo "🌐 您的网站将在以下地址可用："
    echo "   https://${GITHUB_USERNAME}.github.io/${REPO_NAME}/"
else
    echo "❌ 推送失败，请检查："
    echo "   - 网络连接"
    echo "   - GitHub仓库是否已创建"
    echo "   - 仓库名称是否正确"
fi

echo ""
echo "✨ 部署助手完成！"
