# 架构图索引 - AI-Trader

快速访问所有架构图的在线预览链接。

## 📊 架构图列表

### 1. 系统架构图
**文件**: `system_architecture.puml`

**预览**: [点击查看在线版本](http://www.plantuml.com/plantuml/uml/system_architecture.puml)

**描述**: 展示系统整体架构，包括入口层、Agent层、MCP工具链、数据层和外部服务的关系。

**关键要点**:
- main.py动态加载Agent
- BaseAgent vs BaseAgentAStock vs BaseAgentCrypto
- MCP工具的4个核心服务
- US/CN/Crypto三大市场数据隔离

---

### 2. 交易流程序列图
**文件**: `trading_flow.puml`

**预览**: [点击查看在线版本](http://www.plantuml.com/plantuml/uml/trading_flow.puml)

**描述**: 完整的交易执行流程，从程序启动到交易完成的全过程。

**关键阶段**:
1. 初始化阶段 - 加载配置和连接服务
2. 数据准备阶段 - 检查持仓和获取交易日
3. 交易执行阶段 - AI推理和工具调用循环
4. 结果输出阶段 - 生成交易摘要

---

### 3. 核心类图
**文件**: `class_diagram.puml`

**预览**: [点击查看在线版本](http://www.plantuml.com/plantuml/uml/class_diagram.puml)

**描述**: 核心类的结构、属性、方法和继承关系。

**主要类**:
- `BaseAgent` - 通用交易Agent (支持US/CN/Crypto)
- `BaseAgentAStock` - A股专用Agent (继承自BaseAgent)
- `BaseAgentCrypto` - 加密货币专用Agent (继承自BaseAgent)
- `DeepSeekChatOpenAI` - API适配器
- MCP工具类 - TradeTool, PriceTool, SearchTool, MathTool
- 工具类 - GeneralTools, PriceTools, ResultTools

---

### 4. 数据流图
**文件**: `data_flow.puml`

**预览**: [点击查看在线版本](http://www.plantuml.com/plantuml/uml/data_flow.puml)

**描述**: 数据在系统中的流动路径和存储结构。

**数据类型**:
- **配置数据**: .env → configs/*.json → runtime_env.json
- **市场数据**: Alpha Vantage/Tushare/Binance → merged.jsonl
- **持仓数据**: position.jsonl (追加写入，三大市场独立存储)
- **日志数据**: log/{date}/log.jsonl (AI推理过程，三大市场独立存储)

---

### 5. MCP工具交互图
**文件**: `mcp_interaction.puml`

**预览**: [点击查看在线版本](http://www.plantuml.com/plantuml/uml/mcp_interaction.puml)

**描述**: MCP工具的详细交互流程，展示每个工具如何工作。

**工具示例**:
- **价格查询**: 从merged.jsonl读取OHLCV数据
- **信息搜索**: 调用Jina AI API获取市场信息
- **买入交易**: 验证条件、更新持仓(带文件锁) - US股票示例
- **卖出交易**: 特别展示A股100股手数验证
- **加密货币交易**: BTC-USDT交易，展示小数精度和7×24小时交易
- **数学计算**: 安全的表达式计算

---

## 🔧 本地查看方法

### 方法1: VS Code (推荐)
```bash
# 1. 安装PlantUML插件
# 2. 打开.puml文件
# 3. 按 Alt+D 预览
```

### 方法2: 在线编辑器
1. 访问 http://www.plantuml.com/plantuml/uml/
2. 复制.puml文件内容
3. 粘贴到编辑器

### 方法3: 生成图片
```bash
# 进入架构图目录
cd docs/architecture

# 生成PNG图片
bash generate_diagrams.sh png

# 生成SVG图片(推荐，矢量图)
bash generate_diagrams.sh svg

# 同时生成PNG和SVG
bash generate_diagrams.sh both
```

---

## 📚 快速导航

| 关心的问题 | 推荐查看 |
|----------|---------|
| 系统整体结构是什么？ | → 系统架构图 |
| 交易是如何执行的？ | → 交易流程序列图 |
| 如何开发新功能？ | → 核心类图 |
| 数据存储在哪里？ | → 数据流图 |
| MCP工具如何工作？ | → MCP工具交互图 |
| 三大市场有什么区别？ | → 系统架构图 + MCP工具交互图 |
| US股票和A股有什么区别？ | → MCP工具交互图 (卖出A股示例) |
| 加密货币交易有何特点？ | → MCP工具交互图 (加密货币示例) + 数据流图 |
| 如何添加新的Agent？ | → 核心类图 |
| 持仓文件格式是什么？ | → 数据流图 |

---

## 📖 相关文档

- [架构图README](./README.md) - 详细的架构图说明
- [项目README](../../README.md) - 项目总体介绍
- [CLAUDE.md](../../CLAUDE.md) - 开发指南

---

**最后更新**: 2025-11-09
**维护**: AI-Trader Team

---

## 💡 提示

- 使用SVG格式可以无限缩放不失真
- 序列图最适合理解时序流程
- 类图最适合理解代码结构
- 组件图最适合理解系统架构
- 建议先看系统架构图，再看交易流程图

---

## 🎯 快速上手流程

**新手推荐阅读顺序**:

1. **系统架构图** - 了解系统全貌
2. **交易流程图** - 理解交易如何执行
3. **MCP工具交互图** - 理解工具如何工作
4. **数据流图** - 了解数据存储
5. **核心类图** - 深入代码细节

**开发者推荐阅读顺序**:

1. **核心类图** - 了解代码结构
2. **系统架构图** - 了解模块关系
3. **数据流图** - 了解数据管理
4. **MCP工具交互图** - 了解工具开发
5. **交易流程图** - 了解完整流程
