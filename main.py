from tools.general_tools import get_config_value, write_config_value
import asyncio
import json
import os
from datetime import datetime, timedelta
from pathlib import Path
from pathlib import Path as _Path
from dotenv import load_dotenv

load_dotenv()

# 导入工具和提示

# Agent类映射表 - 仅支持A股Agent
AGENT_REGISTRY = {
    "BaseAgentAStock": {
        "module": "agent.base_agent_astock.base_agent_astock",
        "class": "BaseAgentAStock"
    }
}


def get_agent_class(agent_type):
    """
    根据agent类型名称动态导入并返回对应的类

    Args:
        agent_type: Agent类型名称（例如："BaseAgent"）

    Returns:
        Agent类

    Raises:
        ValueError: 如果agent类型不支持
        ImportError: 如果无法导入agent模块
    """
    if agent_type not in AGENT_REGISTRY:
        supported_types = ", ".join(AGENT_REGISTRY.keys())
        raise ValueError(
            f"❌ Unsupported agent type: {agent_type}\n" f"   Supported types: {supported_types}")

    agent_info = AGENT_REGISTRY[agent_type]
    module_path = agent_info["module"]
    class_name = agent_info["class"]

    try:
        # 动态导入模块
        import importlib

        module = importlib.import_module(module_path)
        agent_class = getattr(module, class_name)
        print(
            f"✅ Successfully loaded Agent class: {agent_type} (from {module_path})")
        return agent_class
    except ImportError as e:
        raise ImportError(
            f"❌ Unable to import agent module {module_path}: {e}")
    except AttributeError as e:
        raise AttributeError(
            f"❌ Class {class_name} not found in module {module_path}: {e}")


def load_config(config_path=None):
    """
    从configs目录加载配置文件

    Args:
        config_path: 配置文件路径，如果为None则使用默认配置

    Returns:
        dict: 配置字典
    """
    if config_path is None:
        # 默认A股配置文件路径
        config_path = Path(__file__).parent / "configs" / "astock_config.json"
    else:
        config_path = Path(config_path)

    if not config_path.exists():
        print(f"❌ Configuration file does not exist: {config_path}")
        exit(1)

    try:
        with open(config_path, "r", encoding="utf-8") as f:
            config = json.load(f)
        print(f"✅ Successfully loaded configuration file: {config_path}")
        return config
    except json.JSONDecodeError as e:
        print(f"❌ Configuration file JSON format error: {e}")
        exit(1)
    except Exception as e:
        print(f"❌ Failed to load configuration file: {e}")
        exit(1)


async def main(config_path=None):
    """使用BaseAgentAStock类运行A股交易实验

    Args:
        config_path: 配置文件路径，如果为None则使用默认A股配置
    """
    # 加载配置文件
    config = load_config(config_path)

    # 获取Agent类型（仅支持BaseAgentAStock）
    agent_type = config.get("agent_type", "BaseAgentAStock")
    try:
        AgentClass = get_agent_class(agent_type)
    except (ValueError, ImportError, AttributeError) as e:
        print(str(e))
        exit(1)

    # A股市场（固定）
    market = "cn"
    print(f"🌍 市场类型: A股市场（中国）")

    # 从配置文件获取日期范围
    INIT_DATE = config["date_range"]["init_date"]
    END_DATE = config["date_range"]["end_date"]

    # 环境变量可以覆盖配置文件中的日期
    if os.getenv("INIT_DATE"):
        INIT_DATE = os.getenv("INIT_DATE")
        print(
            f"⚠️  Using environment variable to override INIT_DATE: {INIT_DATE}")
    if os.getenv("END_DATE"):
        END_DATE = os.getenv("END_DATE")
        print(
            f"⚠️  Using environment variable to override END_DATE: {END_DATE}")

    # 验证日期范围
    # 支持 YYYY-MM-DD 和 YYYY-MM-DD HH:MM:SS 两种格式
    if ' ' in INIT_DATE:
        INIT_DATE_obj = datetime.strptime(INIT_DATE, "%Y-%m-%d %H:%M:%S")
    else:
        INIT_DATE_obj = datetime.strptime(INIT_DATE, "%Y-%m-%d")

    if ' ' in END_DATE:
        END_DATE_obj = datetime.strptime(END_DATE, "%Y-%m-%d %H:%M:%S")
    else:
        END_DATE_obj = datetime.strptime(END_DATE, "%Y-%m-%d")

    if INIT_DATE_obj > END_DATE_obj:
        print("❌ INIT_DATE is greater than END_DATE")
        exit(1)

    # 从配置文件获取模型列表（仅选择已启用的模型）
    enabled_models = [model for model in config["models"]
                      if model.get("enabled", True)]

    # 获取agent配置
    agent_config = config.get("agent_config", {})
    log_config = config.get("log_config", {})
    max_steps = agent_config.get("max_steps", 10)
    max_retries = agent_config.get("max_retries", 3)
    base_delay = agent_config.get("base_delay", 0.5)
    initial_cash = agent_config.get("initial_cash", 10000.0)

    # 显示已启用的模型信息
    model_names = [m.get("name", m.get("signature")) for m in enabled_models]

    print("🚀 启动A股交易实验")
    print(f"🤖 Agent类型: {agent_type}")
    print(f"📅 日期范围: {INIT_DATE} 至 {END_DATE}")
    print(f"🤖 模型列表: {model_names}")
    print(
        f"⚙️  Agent配置: max_steps={max_steps}, max_retries={max_retries}, base_delay={base_delay}, initial_cash={initial_cash}"
    )

    for model_config in enabled_models:
        # 直接从配置文件读取basemodel和signature
        model_name = model_config.get("name", "unknown")
        basemodel = model_config.get("basemodel")
        signature = model_config.get("signature")
        openai_base_url = model_config.get("openai_base_url", None)
        openai_api_key = model_config.get("openai_api_key", None)

        # 验证必需字段
        if not basemodel:
            print(f"❌ Model {model_name} missing basemodel field")
            continue
        if not signature:
            print(f"❌ Model {model_name} missing signature field")
            continue

        print("=" * 60)
        print(f"🤖 Processing model: {model_name}")
        print(f"📝 Signature: {signature}")
        print(f"🔧 BaseModel: {basemodel}")

        # 初始化运行时配置
        # 使用.env中RUNTIME_ENV_PATH的共享配置文件

        project_root = _Path(__file__).resolve().parent

        # 获取日志路径配置
        log_path = log_config.get("log_path", "./data/agent_data")

        # 检查持仓文件以确定是否为全新开始
        position_file = project_root / log_path / \
            signature / "position" / "position.jsonl"

        # 如果持仓文件不存在，重置配置从INIT_DATE开始
        if not position_file.exists():
            # 清除共享配置文件以便全新开始
            from tools.general_tools import _resolve_runtime_env_path
            runtime_env_path = _resolve_runtime_env_path()
            if os.path.exists(runtime_env_path):
                os.remove(runtime_env_path)
                print(
                    f"🔄 Position file not found, cleared config for fresh start from {INIT_DATE}")

        # 将配置值写入共享配置文件（来自.env的RUNTIME_ENV_PATH）
        write_config_value("SIGNATURE", signature)
        write_config_value("IF_TRADE", False)
        write_config_value("MARKET", market)
        write_config_value("LOG_PATH", log_path)

        print(
            f"✅ 运行时配置已初始化: SIGNATURE={signature}, MARKET={market}")

        # BaseAgentAStock使用自己的默认上证50股票池
        stock_symbols = None

        try:
            # 创建BaseAgentAStock实例
            agent = AgentClass(
                signature=signature,
                basemodel=basemodel,
                stock_symbols=stock_symbols,
                log_path=log_path,
                max_steps=max_steps,
                max_retries=max_retries,
                base_delay=base_delay,
                initial_cash=initial_cash,
                init_date=INIT_DATE,
                openai_base_url=openai_base_url,
                openai_api_key=openai_api_key
            )

            print(f"✅ {agent_type} instance created successfully: {agent}")

            # 初始化MCP连接和AI模型
            await agent.initialize()
            print("✅ Initialization successful")
            # 运行日期范围内的所有交易日
            await agent.run_date_range(INIT_DATE, END_DATE)

            # 显示最终A股持仓摘要
            summary = agent.get_position_summary()

            # A股使用人民币符号
            currency_symbol = "¥"

            print(f"📊 最终持仓摘要:")
            print(f"   - 最新日期: {summary.get('latest_date')}")
            print(f"   - 总记录数: {summary.get('total_records')}")
            print(
                f"   - 现金余额: {currency_symbol}{summary.get('positions', {}).get('CASH', 0):,.2f}")

        except Exception as e:
            print(
                f"❌ Error processing model {model_name} ({signature}): {str(e)}")
            print(f"📋 Error details: {e}")
            # 可以选择继续处理下一个模型，或退出
            # continue  # 继续处理下一个模型
            exit()  # 或退出程序

        print("=" * 60)
        print(f"✅ Model {model_name} ({signature}) processing completed")
        print("=" * 60)

    print("🎉 All models processing completed!")


if __name__ == "__main__":
    import sys

    # 支持通过命令行参数指定配置文件
    # 用法: python main.py [config_path]
    # 示例: python main.py configs/my_config.json
    config_path = sys.argv[1] if len(sys.argv) > 1 else None

    if config_path:
        print(f"📄 使用指定的配置文件: {config_path}")
    else:
        print(f"📄 使用默认A股配置文件: configs/astock_config.json")

    asyncio.run(main(config_path))
