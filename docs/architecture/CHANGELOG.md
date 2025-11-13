# 架构图更新日志

## 2025-11-12 - 添加加密货币市场支持

### 更新内容

#### 1. 系统架构图 (system_architecture.puml)
- ✅ 添加 `BaseAgentCrypto` 到Agent层
- ✅ 添加加密货币数据库到数据层
  - `crypto/merged.jsonl` - 主流加密货币价格数据
  - `agent_data_crypto/` - 加密货币交易记录
- ✅ 添加外部服务 `Binance API`
- ✅ 更新所有关系连接，包含BaseAgentCrypto
- ✅ 更新注释说明，强调三大市场支持

#### 2. 核心类图 (class_diagram.puml)
- ✅ 添加 `BaseAgentCrypto` 类
  - 继承自 `BaseAgent`
  - market = "crypto"
  - crypto_symbols: List[str]
  - initial_cash: float = 10000.0 (USDT)
  - 无stock_symbols参数
- ✅ 更新 `AgentRegistry` 包含 "BaseAgentCrypto"
- ✅ 添加继承关系: `BaseAgent <|-- BaseAgentCrypto`
- ✅ 添加依赖关系: `MainModule ..> BaseAgentCrypto : creates`
- ✅ 添加注释说明加密货币Agent特性

#### 3. 数据流图 (data_flow.puml)
- ✅ 添加 `Binance API` 外部服务
- ✅ 添加 `crypto/merged.jsonl` 市场数据
- ✅ 添加 `agent_data_crypto/` 持仓数据
- ✅ 添加 `agent_data_crypto/log/` 日志数据
- ✅ 更新数据流向，包含加密货币数据路径
- ✅ 添加加密货币数据特点说明
  - 7×24小时连续数据
  - USDT交易对
  - 分钟级/小时级数据
  - 实时更新
- ✅ 添加加密货币持仓特点说明
  - CASH用USDT计价
  - 支持小数精度
  - 无手数限制
  - 7×24小时可交易

#### 4. MCP工具交互图 (mcp_interaction.puml)
- ✅ 更新交易工具核心逻辑注释，包含Crypto市场
- ✅ 添加加密货币交易示例
  - 买入 BTC-USDT 0.01 个
  - 展示市场类型检测 (-USDT后缀)
  - 展示小数精度支持
  - 展示USDT计价
  - 展示无手数限制
- ✅ 添加加密货币特殊处理注释

#### 5. 文档更新
- ✅ 更新 `README.md`
  - 系统架构图说明
  - 类图说明
  - 数据流图说明
  - MCP工具交互图说明
- ✅ 更新 `INDEX.md`
  - 关键要点
  - 主要类列表
  - 数据类型说明
  - 工具示例
  - 快速导航表格

### 支持的市场

系统现在完整支持三大市场：

| 市场 | Agent类 | 货币 | 初始资金 | 交易规则 | 特点 |
|-----|---------|------|---------|---------|------|
| **US股票** | BaseAgent | USD ($) | $10,000 | T+0，无手数限制 | NASDAQ 100成分股 |
| **A股** | BaseAgentAStock | CNY (¥) | ¥100,000 | T+1，100股为单位 | 上证50成分股 |
| **加密货币** | BaseAgentCrypto | USDT | 10,000 USDT | 7×24小时，无限制 | 主流加密货币 |

### 数据隔离

三大市场数据完全隔离：

```
data/
├── merged.jsonl                    # US股票数据
├── A_stock/merged.jsonl            # A股数据
├── crypto/merged.jsonl             # 加密货币数据
├── agent_data/                     # US交易记录
├── agent_data_astock/              # A股交易记录
└── agent_data_crypto/              # 加密货币交易记录
```

### 配置示例

#### US股票配置
```json
{
  "agent_type": "BaseAgent",
  "market": "us",
  "agent_config": {
    "initial_cash": 10000.0
  }
}
```

#### A股配置
```json
{
  "agent_type": "BaseAgentAStock",
  "agent_config": {
    "initial_cash": 100000.0
  }
}
```

#### 加密货币配置
```json
{
  "agent_type": "BaseAgentCrypto",
  "agent_config": {
    "initial_cash": 10000.0
  }
}
```

### 主要代码变更

在 `main.py` 中：

1. **AGENT_REGISTRY** 添加：
```python
"BaseAgentCrypto": {
    "module": "agent.base_agent_crypto.base_agent_crypto",
    "class": "BaseAgentCrypto"
}
```

2. **市场检测**：
```python
if agent_type == "BaseAgentCrypto":
    market = "crypto"
```

3. **Agent创建**：
```python
if agent_type == "BaseAgentCrypto":
    agent = AgentClass(
        signature=signature,
        basemodel=basemodel,
        # 注意：不传stock_symbols
        log_path=log_path,
        ...
    )
```

4. **货币符号显示**：
```python
if agent.market == "crypto":
    currency_symbol = "USDT"
elif agent.market == "cn":
    currency_symbol = "¥"
else:
    currency_symbol = "$"
```

### 架构图生成

更新后的架构图可以通过以下方式生成：

```bash
cd docs/architecture

# 生成SVG格式（推荐）
bash generate_diagrams.sh svg

# 生成PNG格式
bash generate_diagrams.sh png

# 同时生成两种格式
bash generate_diagrams.sh both
```

### 下一步计划

- [ ] 添加更多加密货币交易对支持
- [ ] 添加分钟级交易支持
- [ ] 添加加密货币特定指标分析
- [ ] 完善加密货币回测功能

---

**更新人**: Claude Code
**更新日期**: 2025-11-12
**影响范围**: 架构图、文档、部分代码注释
