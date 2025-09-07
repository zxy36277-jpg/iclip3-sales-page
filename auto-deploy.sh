#!/bin/bash

# iClip 3.0 自动部署脚本
# 此脚本将自动完成GitHub Pages部署的所有步骤

set -e  # 遇到错误时退出

echo "🚀 开始自动部署 iClip 3.0 销售页面到 GitHub Pages..."

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 函数：打印带颜色的消息
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 检查是否在正确的目录
if [ ! -f "infimind_iclip3.0_sales.html" ]; then
    print_error "请在项目根目录运行此脚本"
    exit 1
fi

# 获取GitHub用户名
echo ""
print_status "请输入您的GitHub用户名："
read -r GITHUB_USERNAME

if [ -z "$GITHUB_USERNAME" ]; then
    print_error "GitHub用户名不能为空"
    exit 1
fi

REPO_NAME="iclip3-sales-page"
REPO_URL="https://github.com/${GITHUB_USERNAME}/${REPO_NAME}.git"

echo ""
print_status "将创建仓库: ${REPO_URL}"

# 检查是否已经存在远程仓库
if git remote get-url origin >/dev/null 2>&1; then
    print_warning "远程仓库已存在，将更新URL"
    git remote set-url origin "$REPO_URL"
else
    print_status "添加远程仓库..."
    git remote add origin "$REPO_URL"
fi

# 设置主分支
print_status "设置主分支为 main..."
git branch -M main

# 推送代码到GitHub
print_status "推送代码到GitHub..."
if git push -u origin main; then
    print_success "代码已成功推送到GitHub！"
else
    print_error "推送失败，请检查网络连接和GitHub访问权限"
    print_warning "您可能需要："
    echo "1. 在GitHub上手动创建仓库: https://github.com/new"
    echo "2. 仓库名称: ${REPO_NAME}"
    echo "3. 设置为公开仓库"
    echo "4. 不要添加README、.gitignore或license"
    echo "5. 创建后重新运行此脚本"
    exit 1
fi

echo ""
print_success "🎉 部署完成！"
echo ""
print_status "接下来请手动完成以下步骤："
echo "1. 访问: https://github.com/${GITHUB_USERNAME}/${REPO_NAME}/settings/pages"
echo "2. Source 选择: 'Deploy from a branch'"
echo "3. Branch 选择: 'main'"
echo "4. Folder 选择: '/ (root)'"
echo "5. 点击 'Save'"
echo ""
print_status "部署完成后，您的网站将在以下地址可用："
echo "https://${GITHUB_USERNAME}.github.io/${REPO_NAME}/"
echo ""
print_success "部署脚本执行完成！"
