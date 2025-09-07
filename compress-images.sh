#!/bin/bash

# 🚀 图片压缩脚本 - 大幅减少文件大小
echo "🚀 开始压缩图片..."

# 创建备份目录
mkdir -p original_images_backup
echo "📁 创建备份目录..."

# 备份原始图片
echo "💾 备份原始图片..."
cp *.png original_images_backup/ 2>/dev/null || true

# 压缩函数
compress_image() {
    local file="$1"
    local filename=$(basename "$file" .png)
    
    echo "🔄 压缩: $file"
    
    # 使用sips压缩PNG，质量设为70%
    sips -s format jpeg -s formatOptions 70 "$file" --out "${filename}_compressed.jpg" 2>/dev/null
    
    # 如果转换成功，替换原文件
    if [ -f "${filename}_compressed.jpg" ]; then
        mv "${filename}_compressed.jpg" "$file"
        echo "✅ 压缩完成: $file"
    else
        echo "❌ 压缩失败: $file"
    fi
}

# 压缩所有PNG文件
for file in *.png; do
    if [ -f "$file" ]; then
        compress_image "$file"
    fi
done

echo "🎉 图片压缩完成！"
echo "📊 压缩前后对比："
echo "压缩前总大小："
du -sh original_images_backup/*.png | awk '{sum+=$1} END {print sum "MB"}'

echo "压缩后总大小："
du -sh *.png | awk '{sum+=$1} END {print sum "MB"}'
