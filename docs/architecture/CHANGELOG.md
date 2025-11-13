# 架构图更新日志

## 2025-11-13 - 简化为仅支持A股市场

### 更新内容

根据项目需求，将所有架构图简化为仅支持A股市场，移除了美股和加密货币相关内容。

#### 1. 系统架构图 (system_architecture.puml)
- ✅ 移除 `BaseAgent` (美股Agent)
- ✅ 移除 `BaseAgentCrypto` (加密货币Agent)
- ✅ 移除 `BaseAgent_Hour` (美股小时级Agent)
- ✅ 仅保留 `BaseAgentAStock` (A股交易Agent)
- ✅ 移除美股数据 (`merged.jsonl`, `agent_data/`)
- ✅ 移除加密货币数据 (`crypto/merged.jsonl`, `agent_data_crypto/`)
- ✅ 移除 Alpha Vantage 和 Binance API
- ✅ 仅保留 Tushare API、A_stock/merged.jsonl、agent_data_astock/
- ✅ 标题更新为 "AI-Trader系统架构图"

#### 2. 核心类图 (class_diagram.puml)
- ✅ 移除 `BaseAgent` 和 `BaseAgentCrypto` 类定义
- ✅ 扩展 `BaseAgentAStock` 类，显示完整属性和方法
  - 核心属性：signature, basemodel, market="cn", stock_symbols, initial_cash=100000.0
  - 核心方法：initialize(), run_trading_session(), run_date_range()
  - A股特性：上证50股票池, T+1结算, 100股手数验证
- ✅ 更新 `AgentRegistry` 仅包含 "BaseAgentAStock"
- ✅ 将 `AgentPrompt` 更名为 `AgentPromptAStock`
- ✅ 标题更新为 "AI-Trader核心类图"

#### 3. 数据流图 (data_flow.puml)
- ✅ 完全重写为 "AI-Trader数据流图 - A股市场"
- ✅ 配置数据流
  - .env (包含 TUSHARE_TOKEN)
  - configs/astock_config.json (A股专用配置)
  - runtime_env.json (MARKET="cn")
- ✅ A股市场数据流
  - Tushare API → sse_50_weight.csv → daily_prices_sse_50.csv → merged.jsonl
  - index_daily_sse_50.json (上证50指数数据)
- ✅ A股持仓数据流
  - agent_data_astock/{signature}/position/position.jsonl
  - 追加写入模式，文件锁保证原子性
  - 100股手数验证，T+1结算
- ✅ A股日志数据流
  - agent_data_astock/{signature}/log/{date}/log.jsonl
  - 包含中文市场分析和推理过程

#### 4. MCP工具交互图 (mcp_interaction.puml)
- ✅ 完全重写为 "MCP工具交互图 - A股市场"
- ✅ 添加详细的A股交易示例
  - A股价格查询：600519.SH (贵州茅台) 2025-10-15
  - A股信息搜索：中文查询示例 "贵州茅台最新财报"
  - A股买入失败：600519.SH 200股，现金不足示例
  - A股买入成功：600036.SH 100股，完整交易流程
  - A股卖出：600036.SH 100股，完整卖出流程
- ✅ 展示A股特殊处理
  - 市场类型检测 (.SH/.SZ 后缀)
  - 100股手数验证
  - 人民币计价
  - T+1结算规则
  - 文件锁保证并发安全

#### 5. 交易流程图 (trading_flow.puml)
- ✅ 完全重写为 "AI-Trader A股交易流程序列图"
- ✅ 将所有参与者更新为A股专用
  - configs/astock_config.json
  - BaseAgentAStock (A股交易Agent)
  - MCP工具链 (A股专用)
  - A股数据存储 (agent_data_astock/)
  - Tushare (A股数据源)
- ✅ 初始化阶段
  - 自动设置 market="cn"
  - 初始资金 ¥100,000
  - 上证50股票池
  - A股工具服务端口 (8000-8003)
- ✅ 数据准备阶段
  - 检查A股持仓文件
  - 读取 A_stock/merged.jsonl
  - 验证A股交易日
- ✅ A股交易执行阶段
  - 使用 AgentPromptAStock
  - .SH/.SZ 股票代码格式
  - 100股手数验证
  - T+1结算规则
  - 人民币计价
  - 文件锁保证原子性
  - 中文推理过程

#### 6. 文档更新
- ✅ README.md 和 INDEX.md 保持通用说明
- ✅ CHANGELOG.md 记录简化过程

### 支持的市场

系统现在仅支持A股市场：

| 市场 | Agent类 | 货币 | 初始资金 | 交易规则 | 特点 |
|-----|---------|------|---------|---------|------|
| **A股** | BaseAgentAStock | CNY (¥) | ¥100,000 | T+1，100股为单位 | 上证50成分股 |

### 数据结构

A股市场数据完全独立：

```
data/
└── A_stock/
    ├── sse_50_weight.csv           # 上证50成分股列表
    ├── daily_prices_sse_50.csv     # 日线价格数据
    ├── merged.jsonl                # 统一JSONL格式
    └── index_daily_sse_50.json     # 上证50指数数据

agent_data_astock/
└── {signature}/
    ├── position/
    │   └── position.jsonl          # A股持仓记录
    └── log/
        └── {date}/
            └── log.jsonl           # A股交易日志
```

### 配置示例

#### A股配置 (configs/astock_config.json)
```json
{
  "agent_type": "BaseAgentAStock",
  "market": "cn",
  "date_range": {
    "init_date": "2025-01-01",
    "end_date": "2025-12-31"
  },
  "agent_config": {
    "initial_cash": 100000.0
  },
  "models": [
    {
      "basemodel": "gpt-4",
      "signature": "astock_gpt4"
    }
  ]
}
```

### 主要代码对应

在 `main.py` 中：

1. **AGENT_REGISTRY** 仅包含：
```python
AGENT_REGISTRY = {
    "BaseAgentAStock": {
        "module": "agent.base_agent_astock.base_agent_astock",
        "class": "BaseAgentAStock"
    }
}
```

2. **市场自动检测**：
```python
# 从agent_type自动检测市场
if agent_type == "BaseAgentAStock":
    market = "cn"
```

3. **货币符号显示**：
```python
if agent.market == "cn":
    currency_symbol = "¥"
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

### 简化优势

1. **专注A股市场**：去除冗余的美股和加密货币逻辑
2. **清晰的架构**：所有图表专注于A股特性
3. **易于维护**：减少市场类型判断，降低复杂度
4. **中文友好**：A股专用提示词和中文分析

---

**更新人**: Claude Code
**更新日期**: 2025-11-13
**影响范围**: 所有架构图、部分文档

---

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
