# AI-Trader 架构图文档

本目录包含AI-Trader系统的PlantUML架构图，帮助理解系统的整体架构和工作流程。

## 📁 架构图列表

### 1. 系统架构图 (system_architecture.puml)
**用途**: 展示系统的整体架构和各组件之间的关系

**包含内容**:
- 入口层 (main.py)
- Agent层 (BaseAgent, BaseAgentAStock, BaseAgentCrypto)
- MCP工具链 (trade, price, search, math)
- 数据层 (US股票、A股、加密货币数据)
- 工具层 (general_tools, price_tools, result_tools)
- 外部服务 (OpenAI, Jina AI, Alpha Vantage, Tushare, Binance)

**适用场景**:
- 快速了解系统整体结构
- 理解各模块职责划分
- 查看三大市场数据流向

### 2. 交易流程图 (trading_flow.puml)
**用途**: 展示从启动到完成交易的完整流程序列图

**流程阶段**:
1. 初始化阶段 - 加载配置、创建Agent、连接MCP
2. 数据准备阶段 - 检查持仓、获取交易日列表
3. 交易执行阶段 - AI推理循环、工具调用、持仓更新
4. 结果输出阶段 - 生成交易摘要

**适用场景**:
- 理解交易执行的完整流程
- 调试交易问题
- 了解AI决策过程

### 3. 类图 (class_diagram.puml)
**用途**: 展示核心类的结构、属性、方法和关系

**主要类**:
- BaseAgent - 通用交易Agent (支持US/CN/Crypto)
- BaseAgentAStock - A股专用Agent
- BaseAgentCrypto - 加密货币专用Agent
- DeepSeekChatOpenAI - DeepSeek API适配器
- MCP工具类 (TradeTool, PriceTool, SearchTool, MathTool)
- 工具类 (GeneralTools, PriceTools, ResultTools)
- AgentPrompt - 提示词管理

**适用场景**:
- 开发新功能
- 理解类的设计
- 查看继承和依赖关系
- 了解三种Agent的差异

### 4. 数据流图 (data_flow.puml)
**用途**: 展示数据如何在系统中流动

**数据类型**:
- 配置数据流 (.env, configs/*.json, runtime_env.json)
- 市场数据流 (Alpha Vantage, Tushare, Binance -> merged.jsonl)
- 持仓数据流 (position.jsonl - US/CN/Crypto)
- 日志数据流 (log.jsonl - US/CN/Crypto)

**适用场景**:
- 理解数据存储结构
- 追踪三大市场数据来源和去向
- 优化数据访问性能
- 了解加密货币数据特点

### 5. MCP工具交互图 (mcp_interaction.puml)
**用途**: 详细展示MCP工具的工作机制

**展示内容**:
- MCP工具初始化流程
- 价格查询工具示例
- 信息搜索工具示例
- 买入交易工具示例 (US股票)
- 卖出交易工具示例 (A股)
- 加密货币交易示例 (BTC-USDT)
- 数学计算工具示例

**适用场景**:
- 理解MCP协议如何工作
- 开发新的MCP工具
- 调试工具调用问题
- 了解三大市场交易规则差异

## 🔧 如何查看架构图

### 方式1: 在线查看 (推荐)

使用PlantUML在线编辑器:

1. 访问 [PlantUML Online Editor](http://www.plantuml.com/plantuml/uml/)
2. 复制对应的.puml文件内容
3. 粘贴到编辑器中
4. 自动生成图表

### 方式2: VS Code插件

1. 安装VS Code插件: [PlantUML](https://marketplace.visualstudio.com/items?itemName=jebbs.plantuml)
2. 打开.puml文件
3. 按 `Alt+D` 预览图表
4. 支持导出为PNG、SVG等格式

### 方式3: 本地命令行

```bash
# 安装PlantUML
# macOS
brew install plantuml

# Ubuntu/Debian
sudo apt-get install plantuml

# 生成PNG图片
plantuml system_architecture.puml

# 生成SVG图片
plantuml -tsvg system_architecture.puml

# 批量生成所有图
plantuml *.puml
```

### 方式4: IntelliJ IDEA / PyCharm

1. 安装插件: PlantUML integration
2. 右键.puml文件
3. 选择 "Diagram" -> "Show PlantUML Diagram"

## 📊 架构图导出

生成的图片文件可以保存在同目录下:

```bash
# 生成所有架构图为PNG
plantuml -tpng *.puml

# 生成所有架构图为SVG (矢量图，推荐用于文档)
plantuml -tsvg *.puml
```

## 🔄 架构图更新

当系统架构变化时，请及时更新对应的PlantUML文件:

1. 修改.puml源文件
2. 重新生成图片
3. 提交更新到版本控制

## 📚 相关资源

- [PlantUML官方文档](https://plantuml.com/zh/)
- [PlantUML语法速查](https://plantuml.com/zh/guide)
- [PlantUML类图语法](https://plantuml.com/zh/class-diagram)
- [PlantUML序列图语法](https://plantuml.com/zh/sequence-diagram)
- [PlantUML组件图语法](https://plantuml.com/zh/component-diagram)

## 💡 提示

- 使用SVG格式可以获得更好的缩放效果
- 序列图适合展示时序流程
- 类图适合展示代码结构
- 组件图适合展示系统架构
- 可以使用`!include`来复用公共定义

## 📝 维护建议

1. **保持同步**: 代码变更后及时更新架构图
2. **简洁明了**: 避免在一个图中放入过多细节
3. **分层展示**: 用多个图从不同角度展示系统
4. **添加注释**: 在关键位置添加note说明
5. **版本控制**: 将.puml文件纳入git管理

---

**生成时间**: 2025-11-09
**维护者**: AI-Trader Team
