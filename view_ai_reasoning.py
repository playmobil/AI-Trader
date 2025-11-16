#!/usr/bin/env python3
"""查看AI的推理和决策过程"""
import json
import sys
from pathlib import Path

def view_ai_reasoning(date="2025-11-11", signature="deepseek-chat-v3.1"):
    log_file = Path(f"data/agent_data_astock/{signature}/log/{date}/log.jsonl")

    if not log_file.exists():
        print(f"❌ 日志文件不存在: {log_file}")
        return

    print(f"📊 查看AI在 {date} 的交易决策过程")
    print("=" * 80)

    step_num = 0
    with open(log_file, 'r') as f:
        for line in f:
            record = json.loads(line)
            messages = record.get('new_messages', [])

            for msg in messages:
                role = msg.get('role')
                content = msg.get('content', '')

                if role == 'assistant':
                    step_num += 1
                    print(f"\n🤖 【第{step_num}步 - AI思考】")

                    # 显示文本内容
                    if isinstance(content, str) and content.strip():
                        # 只显示前800字符
                        print(content[:800])
                        if len(content) > 800:
                            print("...[内容过长，已截断]...")

                    # 显示工具调用
                    if 'tool_calls' in msg:
                        print("\n🔧 【工具调用】")
                        for tc in msg['tool_calls']:
                            func = tc.get('function', {})
                            func_name = func.get('name', '')
                            try:
                                args = json.loads(func.get('arguments', '{}'))
                                print(f"  • {func_name}({', '.join(f'{k}={v}' for k, v in args.items())})")
                            except:
                                print(f"  • {func_name}(...)")

                    print("-" * 80)

                elif role == 'tool' and step_num > 0:
                    tool_name = msg.get('name', '未知工具')
                    print(f"\n📥 【工具返回 - {tool_name}】")
                    # 工具返回的内容通常较长，只显示概要
                    if isinstance(content, str):
                        if len(content) < 200:
                            print(content)
                        else:
                            print(content[:200] + "...[结果已截断]...")

    print("\n" + "=" * 80)
    print(f"✅ 共 {step_num} 步推理完成")

if __name__ == "__main__":
    date = sys.argv[1] if len(sys.argv) > 1 else "2025-11-11"
    view_ai_reasoning(date)
