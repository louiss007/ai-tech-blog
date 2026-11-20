#!/usr/bin/env python3
"""Generate the eight WeChat diagrams as SVG source files.

Usage:
    python3 make_diagrams.py
    python3 render_diagrams.py
"""

from __future__ import annotations

import html
from pathlib import Path

BASE = Path(__file__).resolve().parent
IMG_DIR = BASE / "images"
FONT = "'PingFang SC','Hiragino Sans GB','Microsoft YaHei',sans-serif"

INK = "#0f172a"
MUTED = "#64748b"
BODY = "#334155"
LINE = "#94a3b8"

BLUE = ("#2563eb", "#eff6ff", "#bfdbfe", "#1e3a8a")
TEAL = ("#0f766e", "#f0fdfa", "#99f6e4", "#115e59")
ORANGE = ("#d97706", "#fffbeb", "#fcd34d", "#92400e")
PURPLE = ("#7c3aed", "#f5f3ff", "#c4b5fd", "#5b21b6")
RED = ("#dc2626", "#fef2f2", "#fca5a5", "#991b1b")
GRAY = ("#64748b", "#f8fafc", "#e2e8f0", "#334155")


def esc(text: str) -> str:
    return html.escape(text, quote=False)


def text(
    x: int | float,
    y: int | float,
    value: str,
    size: int = 16,
    color: str = BODY,
    weight: int = 400,
    anchor: str = "start",
) -> str:
    return (
        f'<text x="{x}" y="{y}" font-size="{size}" fill="{color}" '
        f'font-weight="{weight}" text-anchor="{anchor}">{esc(value)}</text>'
    )


def rect(
    x: int | float,
    y: int | float,
    w: int | float,
    h: int | float,
    fill: str,
    stroke: str,
    rx: int = 12,
) -> str:
    return (
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" '
        f'fill="{fill}" stroke="{stroke}"/>'
    )


def arrow(
    x1: int | float,
    y1: int | float,
    x2: int | float,
    y2: int | float,
    color: str = LINE,
    dashed: bool = False,
    marker: str = "arrow",
) -> str:
    dash = ' stroke-dasharray="5 4"' if dashed else ""
    return (
        f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" '
        f'stroke="{color}" stroke-width="2"{dash} '
        f'marker-end="url(#{marker})"/>'
    )


def polyline(
    points: str,
    color: str = LINE,
    dashed: bool = False,
    marker: str = "arrow",
) -> str:
    dash = ' stroke-dasharray="5 4"' if dashed else ""
    return (
        f'<polyline points="{points}" fill="none" stroke="{color}" '
        f'stroke-width="2"{dash} marker-end="url(#{marker})"/>'
    )


def header(width: int, height: int, title: str, subtitle: str) -> str:
    markers = ""
    for name, color in (
        ("arrow", LINE),
        ("arrow-blue", BLUE[0]),
        ("arrow-teal", TEAL[0]),
        ("arrow-orange", ORANGE[0]),
        ("arrow-purple", PURPLE[0]),
        ("arrow-red", RED[0]),
    ):
        markers += (
            f'<marker id="{name}" viewBox="0 0 10 10" refX="8" refY="5" '
            f'markerWidth="6" markerHeight="6" orient="auto-start-reverse">'
            f'<path d="M0,0 L10,5 L0,10 z" fill="{color}"/></marker>'
        )
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="750" height="{height}" viewBox="0 0 750 {height}">
  <rect width="750" height="{height}" fill="#ffffff"/>
  <defs>{markers}</defs>
  <g font-family="{FONT}">
    {text(375, 46, title, 28, INK, 700, "middle")}
    {text(375, 76, subtitle, 15, MUTED, 400, "middle")}
"""


def footer(note: str, y: int) -> str:
    return f"""    {text(375, y, note, 14, MUTED, 400, "middle")}
  </g>
</svg>
"""


def diagram_1() -> str:
    w, h = 750, 430
    parts = [header(w, h, "从“像不像”到“对不对”", "后训练的奖励信号，越来越接近可执行的事实判断")]
    cards = [
        ("SFT", "示范答案", "token 级似然", "只学正例", GRAY),
        ("RLHF", "人类偏好", "训练奖励模型", "代理可被优化", ORANGE),
        ("RLAIF", "AI 反馈", "训练奖励模型", "继承裁判偏差", PURPLE),
        ("RLVR", "可验证判据", "程序 / 测试 / 符号", "验证器可被攻击", BLUE),
    ]
    x0, width, gap = 32, 154, 14
    for i, (name, signal, detail, risk, color) in enumerate(cards):
        x = x0 + i * (width + gap)
        y = 108
        parts.append(rect(x, y, width, 206, color[1], color[2], 14))
        parts.append(rect(x, y, width, 7, color[0], color[0], 4))
        parts.append(text(x + width / 2, y + 44, name, 24, color[3], 700, "middle"))
        parts.append(text(x + width / 2, y + 80, signal, 16, BODY, 600, "middle"))
        parts.append(text(x + width / 2, y + 110, detail, 14, MUTED, 400, "middle"))
        parts.append(f'<line x1="{x + 20}" y1="{y + 132}" x2="{x + width - 20}" y2="{y + 132}" stroke="{color[2]}" stroke-width="1"/>')
        parts.append(text(x + width / 2, y + 160, "风险", 12, MUTED, 400, "middle"))
        parts.append(text(x + width / 2, y + 184, risk, 14, color[0], 600, "middle"))
        if i < 3:
            parts.append(arrow(x + width + 2, y + 103, x + width + gap - 2, y + 103, color[0]))
    parts.append(f'<line x1="55" y1="352" x2="695" y2="352" stroke="{LINE}" stroke-width="2"/>')
    parts.append(arrow(680, 352, 705, 352))
    parts.append(text(55, 380, "更主观", 14, MUTED, 400, "start"))
    parts.append(text(695, 380, "更客观", 14, MUTED, 400, "end"))
    parts.append(footer("越往右，奖励越接近任务本身；也越依赖验证器的质量。", 408))
    return "".join(parts)


def diagram_2() -> str:
    w, h = 750, 410
    parts = [header(w, h, "RLVR 的最小闭环", "模型负责提出候选，验证器负责判断候选")]
    boxes = [
        ("问题", "prompt", BLUE),
        ("采样", "N 个回答", BLUE),
        ("Verifier", "规则 / 测试", TEAL),
        ("奖励", "0 / 1 / 分级", ORANGE),
        ("更新", "策略梯度", PURPLE),
    ]
    x0, width, gap = 29, 116, 28
    y, height = 118, 78
    for i, (title, desc, color) in enumerate(boxes):
        x = x0 + i * (width + gap)
        parts.append(rect(x, y, width, height, color[1], color[2], 12))
        parts.append(text(x + width / 2, y + 34, title, 20, color[3], 700, "middle"))
        parts.append(text(x + width / 2, y + 59, desc, 14, MUTED, 400, "middle"))
        if i < 4:
            parts.append(arrow(x + width + 2, y + height / 2, x + width + gap - 2, y + height / 2, color[0]))
    parts.append(polyline(f"663,196 663,300 231,300 231,202", PURPLE[0], True, "arrow-purple"))
    parts.append(text(447, 326, "下一轮采样", 14, PURPLE[0], 600, "middle"))
    pills = [("多探索", BLUE), ("可靠筛选", TEAL), ("KL 约束", ORANGE)]
    for i, (label, color) in enumerate(pills):
        x = 218 + i * 108
        parts.append(rect(x, 342, 96, 32, color[1], color[2], 16))
        parts.append(text(x + 48, 364, label, 14, color[3], 600, "middle"))
    parts.append(footer("多采样提高命中率，验证器提供对比信号，KL 防止策略漂移。", 402))
    return "".join(parts)


def diagram_3() -> str:
    w, h = 750, 570
    parts = [header(w, h, "RLVR 的七步训练流程", "从数据到 checkpoint，每一步都要可追踪")]
    rows = [
        ("1", "数据准备", "题目、答案、测试、规则", BLUE),
        ("2", "Rollout", "同一问题采样 N 次，记录 logprob", BLUE),
        ("3", "Verifier", "格式、答案、执行、符号、模型辅助", TEAL),
        ("4", "Reward", "正确性 + 格式 + 过程 - 惩罚 - KL", TEAL),
        ("5", "RL 优化", "PPO / GRPO / REINFORCE", PURPLE),
        ("6", "评估", "pass@1、pass@k、安全回归", ORANGE),
        ("7", "Checkpoint", "版本、配置、数据、验证器", ORANGE),
    ]
    for i, (num, title, desc, color) in enumerate(rows):
        y = 104 + i * 60
        parts.append(rect(60, y, 630, 48, color[1], color[2], 10))
        parts.append(f'<circle cx="86" cy="{y + 24}" r="14" fill="{color[0]}"/>')
        parts.append(text(86, y + 29, num, 12, "#ffffff", 700, "middle"))
        parts.append(text(112, y + 30, title, 19, color[3], 700))
        parts.append(text(664, y + 30, desc, 14, BODY, 400, "end"))
        if i < len(rows) - 1:
            parts.append(arrow(86, y + 48, 86, y + 58, color[0]))
    parts.append(footer("数据、验证器和模型版本必须一起记录，否则奖励无法重放。", 544))
    return "".join(parts)


def diagram_4() -> str:
    w, h = 750, 470
    parts = [header(w, h, "Verifier 的四层漏斗", "便宜的先跑，昂贵的兜底")]
    layers = [
        (70, 610, 110, "格式与结构", "正则 / JSON Schema / 解析器", "快、便宜", BLUE),
        (120, 510, 188, "答案等价 / 执行", "数值比较 / 符号计算 / 单元测试", "中等成本", TEAL),
        (170, 410, 266, "符号 / 形式化", "CAS / SMT / 证明助手", "高置信", PURPLE),
        (220, 310, 344, "模型裁判 / 人工", "长尾、歧义、抽检", "最贵", ORANGE),
    ]
    for x, width, y, title, desc, note, color in layers:
        parts.append(rect(x, y, width, 62, color[1], color[2], 10))
        parts.append(rect(x, y, 7, 62, color[0], color[0], 4))
        parts.append(text(x + 24, y + 27, title, 19, color[3], 700))
        parts.append(text(x + 24, y + 50, desc, 14, BODY))
        parts.append(text(x + width - 16, y + 38, note, 13, color[0], 600, "end"))
    parts.append(text(28, 140, "成本", 14, MUTED, 400, "middle"))
    parts.append(arrow(28, 158, 28, 390, ORANGE[0], False, "arrow-orange"))
    parts.append(footer("越往下成本越高；形式化层置信度最高，模型裁判用于长尾。", 444))
    return "".join(parts)


def diagram_5() -> str:
    w, h = 750, 560
    parts = [header(w, h, "不同任务，验证方式不同", "规则、执行、语义三层，按任务组合")]
    cols = [30, 160, 340, 520]
    widths = [130, 180, 180, 200]
    headers = ["任务", "规则与结构", "执行与测试", "语义与终态"]
    for x, width, label in zip(cols, widths, headers):
        parts.append(rect(x, 102, width, 44, BLUE[1], BLUE[2], 0))
        parts.append(text(x + width / 2, 130, label, 16, BLUE[3], 700, "middle"))
    rows = [
        ("数学", "答案归一化", "代入 / 数值", "符号等价", BLUE),
        ("代码", "签名 / 语法", "单元测试", "静态 / 安全", TEAL),
        ("JSON", "Schema", "下游 dry-run", "业务规则", TEAL),
        ("SQL", "语法 / 权限", "只读执行", "结果集比较", PURPLE),
        ("工具调用", "参数 Schema", "环境执行", "终态检查", ORANGE),
        ("Agent", "轨迹规则", "环境执行", "终态 + 安全", ORANGE),
    ]
    for i, (task, c1, c2, c3, color) in enumerate(rows):
        y = 146 + i * 58
        if i % 2 == 0:
            parts.append(rect(30, y, 690, 58, "#fafafa", "#fafafa", 0))
        parts.append(rect(30, y, 6, 58, color[0], color[0], 0))
        parts.append(text(48, y + 35, task, 16, color[3], 700))
        parts.append(text(175, y + 35, c1, 15, BODY))
        parts.append(text(355, y + 35, c2, 15, BODY))
        parts.append(text(535, y + 35, c3, 15, BODY))
    parts.append(footer("能规则化的先规则化；能执行的就执行；模型裁判只处理长尾。", 540))
    return "".join(parts)


def diagram_6() -> str:
    w, h = 750, 500
    parts = [header(w, h, "RLVR 的系统架构", "主链路 + 两个旁路：实验追踪与安全沙箱")]
    top = [
        (30, "数据管理", "题目 / 测试 / 切分", BLUE),
        (210, "Rollout", "采样 / logprob", BLUE),
        (390, "验证服务", "规则 / 执行 / 符号", TEAL),
        (570, "奖励计算", "聚合 / 惩罚 / KL", TEAL),
    ]
    bottom = [
        (570, "RL 训练", "PPO / GRPO", PURPLE),
        (390, "Checkpoint", "权重 / 配置", PURPLE),
        (210, "评估", "pass@k / 安全", ORANGE),
        (30, "部署候选", "灰度 / 回滚", ORANGE),
    ]
    for x, title, desc, color in top:
        parts.append(rect(x, 110, 150, 64, color[1], color[2], 10))
        parts.append(text(x + 75, 138, title, 19, color[3], 700, "middle"))
        parts.append(text(x + 75, 160, desc, 13, MUTED, 400, "middle"))
    for x in (180, 360, 540):
        parts.append(arrow(x, 142, x + 24, 142, BLUE[0]))
    for x, title, desc, color in bottom:
        parts.append(rect(x, 270, 150, 64, color[1], color[2], 10))
        parts.append(text(x + 75, 298, title, 19, color[3], 700, "middle"))
        parts.append(text(x + 75, 320, desc, 13, MUTED, 400, "middle"))
    parts.append(arrow(645, 174, 645, 264, TEAL[0]))
    for x in (570, 390, 210):
        parts.append(arrow(x, 302, x - 24, 302, PURPLE[0]))
    parts.append(rect(30, 382, 330, 46, GRAY[1], GRAY[2], 10))
    parts.append(text(195, 410, "Experiment Tracker：配置 / 指标 / 血缘", 15, GRAY[3], 600, "middle"))
    parts.append(rect(380, 382, 340, 46, ORANGE[1], ORANGE[2], 10))
    parts.append(text(550, 410, "Safety Sandbox：隔离 / 限权 / 审计", 15, ORANGE[3], 600, "middle"))
    parts.append(footer("验证器与沙箱是两套独立的安全边界，不能互相替代。", 470))
    return "".join(parts)


def diagram_7() -> str:
    w, h = 750, 480
    parts = [header(w, h, "评估要看四层", "训练奖励上升，不等于模型真的变强")]
    cards = [
        (30, 108, "任务效果", ["pass@1 / pass@k", "执行通过率", "精确匹配"], BLUE),
        (390, 108, "推理能力", ["过程一致性", "分布外泛化", "难题准确率"], TEAL),
        (30, 258, "训练稳定性", ["KL / 熵 / 长度", "梯度范数", "零方差组比例"], PURPLE),
        (390, 258, "安全与效率", ["沙箱违规", "危险工具调用", "每个正确样本成本"], ORANGE),
    ]
    for x, y, title, bullets, color in cards:
        parts.append(rect(x, y, 330, 130, color[1], color[2], 14))
        parts.append(rect(x, y, 7, 130, color[0], color[0], 4))
        parts.append(text(x + 24, y + 34, title, 21, color[3], 700))
        for j, item in enumerate(bullets):
            parts.append(f'<circle cx="{x + 30}" cy="{y + 62 + j * 24}" r="4" fill="{color[0]}"/>')
            parts.append(text(x + 44, y + 68 + j * 24, item, 15, BODY))
    parts.append(rect(30, 410, 690, 38, RED[1], RED[2], 10))
    parts.append(text(375, 435, "pass@1 上升但 pass@k 不升：可能只是锐化，不是扩展", 15, RED[3], 700, "middle"))
    parts.append(footer("指标要分任务、分难度、分版本看，并记录置信区间。", 474))
    return "".join(parts)


def diagram_8() -> str:
    w, h = 750, 400
    parts = [header(w, h, "RLVR 落地三阶段", "先建验证器，再跑小闭环，最后扩规模")]
    stages = [
        (30, 120, 210, 200, "阶段一 验证器", ["选可验证任务", "建审核集", "搭安全沙箱"], "产出：可信验证器", BLUE),
        (270, 100, 210, 220, "阶段二 小闭环", ["小模型试点", "采样与奖励", "评估与回滚"], "产出：可复现闭环", TEAL),
        (510, 80, 210, 240, "阶段三 规模化", ["多验证器", "红队测试", "成本与容量"], "产出：稳定收益", PURPLE),
    ]
    for x, y, width, height, title, bullets, note, color in stages:
        parts.append(rect(x, y, width, height, color[1], color[2], 14))
        parts.append(rect(x, y, width, 8, color[0], color[0], 4))
        parts.append(text(x + 20, y + 40, title, 19, color[3], 700))
        parts.append(text(x + 20, y + 66, note, 14, color[0], 600))
        for j, item in enumerate(bullets):
            parts.append(f'<circle cx="{x + 26}" cy="{y + 100 + j * 30}" r="4" fill="{color[0]}"/>')
            parts.append(text(x + 40, y + 106 + j * 30, item, 15, BODY))
    parts.append(arrow(240, 350, 266, 330, TEAL[0]))
    parts.append(arrow(480, 330, 506, 290, PURPLE[0]))
    parts.append(footer("不要跳过验证器直接上 RL；每一阶段都要能评估、能回滚。", 380))
    return "".join(parts)


def main() -> None:
    IMG_DIR.mkdir(exist_ok=True)
    diagrams = {
        "fig01-reward-spectrum.svg": diagram_1(),
        "fig02-rlvr-loop.svg": diagram_2(),
        "fig03-training-flow.svg": diagram_3(),
        "fig04-verifier-funnel.svg": diagram_4(),
        "fig05-task-matrix.svg": diagram_5(),
        "fig06-architecture.svg": diagram_6(),
        "fig07-eval-layers.svg": diagram_7(),
        "fig08-roadmap.svg": diagram_8(),
    }
    for name, svg in diagrams.items():
        (IMG_DIR / name).write_text(svg + "\n", encoding="utf-8")
        print(f"wrote images/{name}")


if __name__ == "__main__":
    main()
