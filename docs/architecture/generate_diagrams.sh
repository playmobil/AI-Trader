#!/bin/bash

# AI-Trader架构图生成脚本
# 用法: bash generate_diagrams.sh [png|svg|both]

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 获取脚本所在目录
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# 检查PlantUML是否安装
check_plantuml() {
    if ! command -v plantuml &> /dev/null; then
        echo -e "${RED}❌ PlantUML未安装${NC}"
        echo ""
        echo "请先安装PlantUML:"
        echo ""
        echo "  macOS:"
        echo "    brew install plantuml"
        echo ""
        echo "  Ubuntu/Debian:"
        echo "    sudo apt-get install plantuml"
        echo ""
        echo "  或下载jar文件:"
        echo "    https://plantuml.com/download"
        exit 1
    fi
}

# 生成图表
generate_diagrams() {
    local format=$1

    echo -e "${YELLOW}🎨 生成${format}格式架构图...${NC}"
    echo ""

    local puml_files=(
        "system_architecture.puml"
        "trading_flow.puml"
        "class_diagram.puml"
        "data_flow.puml"
        "mcp_interaction.puml"
    )

    local file_names=(
        "系统架构图"
        "交易流程图"
        "类图"
        "数据流图"
        "MCP工具交互图"
    )

    for i in "${!puml_files[@]}"; do
        local file="${puml_files[$i]}"
        local name="${file_names[$i]}"

        if [ -f "$file" ]; then
            echo -e "  📄 生成 ${name} (${file})..."

            if [ "$format" == "png" ]; then
                plantuml -tpng "$file" 2>&1
            elif [ "$format" == "svg" ]; then
                plantuml -tsvg "$file" 2>&1
            fi

            if [ $? -eq 0 ]; then
                echo -e "  ${GREEN}✓${NC} ${name} 生成成功"
            else
                echo -e "  ${RED}✗${NC} ${name} 生成失败"
            fi
        else
            echo -e "  ${RED}✗${NC} 文件不存在: $file"
        fi
        echo ""
    done
}

# 显示帮助信息
show_help() {
    echo "AI-Trader架构图生成脚本"
    echo ""
    echo "用法:"
    echo "  bash generate_diagrams.sh [png|svg|both]"
    echo ""
    echo "选项:"
    echo "  png   - 生成PNG格式图片 (默认)"
    echo "  svg   - 生成SVG格式图片 (矢量图，推荐)"
    echo "  both  - 同时生成PNG和SVG格式"
    echo ""
    echo "示例:"
    echo "  bash generate_diagrams.sh png"
    echo "  bash generate_diagrams.sh svg"
    echo "  bash generate_diagrams.sh both"
}

# 主函数
main() {
    echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${GREEN}  AI-Trader 架构图生成工具${NC}"
    echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo ""

    # 检查PlantUML
    check_plantuml

    # 获取格式参数
    local format="${1:-png}"

    # 验证参数
    if [[ ! "$format" =~ ^(png|svg|both)$ ]]; then
        echo -e "${RED}❌ 无效的格式: $format${NC}"
        echo ""
        show_help
        exit 1
    fi

    # 生成图表
    if [ "$format" == "both" ]; then
        generate_diagrams "png"
        echo ""
        generate_diagrams "svg"
    else
        generate_diagrams "$format"
    fi

    echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${GREEN}✅ 所有架构图生成完成！${NC}"
    echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo ""

    # 显示生成的文件
    echo "生成的文件:"
    if [ "$format" == "png" ] || [ "$format" == "both" ]; then
        ls -lh *.png 2>/dev/null | awk '{print "  📷 " $9 " (" $5 ")"}'
    fi
    if [ "$format" == "svg" ] || [ "$format" == "both" ]; then
        ls -lh *.svg 2>/dev/null | awk '{print "  🎨 " $9 " (" $5 ")"}'
    fi
    echo ""
}

# 运行主函数
main "$@"
