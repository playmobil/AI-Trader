#!/usr/bin/env python3
"""分析A股交易持仓和收益"""
import json
from pathlib import Path

def analyze_position(signature="deepseek-chat-v3.1"):
    position_file = Path(f"data/agent_data_astock/{signature}/position/position.jsonl")

    if not position_file.exists():
        print(f"❌ 持仓文件不存在: {position_file}")
        return

    # 读取所有记录
    records = []
    with open(position_file, 'r') as f:
        for line in f:
            records.append(json.loads(line))

    if not records:
        print("❌ 没有交易记录")
        return

    # 获取初始和最终记录
    initial = records[0]
    final = records[-1]

    initial_cash = initial['positions']['CASH']
    final_cash = final['positions']['CASH']

    print("=" * 60)
    print(f"📊 A股交易分析报告 - {signature}")
    print("=" * 60)
    print(f"\n📅 交易周期: {initial['date']} → {final['date']}")
    print(f"📝 总交易记录数: {len(records)}")

    print(f"\n💰 资金情况:")
    print(f"   初始资金: ¥{initial_cash:,.2f}")
    print(f"   当前现金: ¥{final_cash:,.2f}")

    # 统计当前持仓
    current_holdings = {k: v for k, v in final['positions'].items()
                       if k != 'CASH' and v > 0}

    print(f"\n📈 当前持仓 ({len(current_holdings)} 只股票):")
    if current_holdings:
        for symbol, amount in sorted(current_holdings.items(), key=lambda x: x[1], reverse=True):
            print(f"   {symbol}: {amount} 股")
    else:
        print("   （全部清仓）")

    # 统计交易次数
    buy_count = sum(1 for r in records if r.get('this_action', {}).get('action') == 'buy')
    sell_count = sum(1 for r in records if r.get('this_action', {}).get('action') == 'sell')
    hold_count = sum(1 for r in records if r.get('this_action', {}).get('action') == 'no_trade')

    print(f"\n📊 交易统计:")
    print(f"   买入次数: {buy_count}")
    print(f"   卖出次数: {sell_count}")
    print(f"   持仓不动: {hold_count}")

    # 计算现金变化
    cash_change = final_cash - initial_cash
    cash_return = (cash_change / initial_cash) * 100

    print(f"\n💵 现金收益:")
    print(f"   现金变化: ¥{cash_change:,.2f}")
    print(f"   现金收益率: {cash_return:+.2f}%")

    print("\n" + "=" * 60)

    # 显示最近5次交易
    print("\n📋 最近5次交易:")
    for record in records[-5:]:
        action = record['this_action']
        date = record['date']
        if action['action'] == 'buy':
            print(f"   {date}: 买入 {action['symbol']} {action['amount']} 股")
        elif action['action'] == 'sell':
            print(f"   {date}: 卖出 {action['symbol']} {action['amount']} 股")
        else:
            print(f"   {date}: 持仓不动")

if __name__ == "__main__":
    analyze_position()
