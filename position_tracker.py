# position_tracker.py
from collections import defaultdict

# 內部儲存各策略倉位
_position_map = defaultdict(float)


def update_position(strategy_name, action, qty):
    """
    根據執行結果更新指定策略的部位
    """
    qty = float(qty)
    if action.upper() == "LONG":
        _position_map[strategy_name] += qty
    elif action.upper() == "SHORT":
        _position_map[strategy_name] -= qty
    elif action.upper() == "EXIT":
        _position_map[strategy_name] = 0


def get_position(strategy_name):
    return _position_map[strategy_name]


def get_all_positions():
    """
    回傳所有策略倉位資訊（dict）
    """
    return dict(_position_map)


def get_long_short_ratio():
    """
    計算目前所有策略中多單 vs 空單 數量比例
    """
    long_total = sum(v for v in _position_map.values() if v > 0)
    short_total = abs(sum(v for v in _position_map.values() if v < 0))
    total = long_total + short_total
    if total == 0:
        return {"long_pct": 0, "short_pct": 0}
    return {
        "long_pct": round(long_total / total * 100, 2),
        "short_pct": round(short_total / total * 100, 2)
    }
