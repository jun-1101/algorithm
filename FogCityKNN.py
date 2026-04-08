import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.widgets import Slider, RadioButtons, Button
from collections import Counter


np.random.seed(42)

# ══════════════════════════════════════════════════════════
# 城市資料
# ══════════════════════════════════════════════════════════

def generate_city():
    residents = []
    for _ in range(35):
        x = np.random.uniform(0.5, 3.5)
        y = np.random.uniform(7.0, 9.5)
        label = np.random.choice(['A', 'B', 'C'], p=[0.70, 0.15, 0.15])
        residents.append({'x': x, 'y': y, 'label': label, 'zone': 'North'})
    for _ in range(35):
        x = np.random.uniform(0.5, 3.5)
        y = np.random.uniform(4.0, 6.5)
        label = np.random.choice(['A', 'B', 'C'], p=[0.10, 0.75, 0.15])
        residents.append({'x': x, 'y': y, 'label': label, 'zone': 'Middle'})
    for _ in range(30):
        x = np.random.uniform(0.8, 3.2)
        y = np.random.uniform(1.0, 3.2)
        label = np.random.choice(['C', 'A'], p=[0.93, 0.07])
        residents.append({'x': x, 'y': y, 'label': label, 'zone': 'South'})
    return residents

residents = generate_city()
YOU = {'x': 2.0, 'y': 3.3}
SAFE = ['A', 'B']
color_map = {'A': '#4fc3f7', 'B': '#81c784', 'C': '#ef5350'}

# ══════════════════════════════════════════════════════════
# KNN 函式
# ══════════════════════════════════════════════════════════

def dist(a, b):
    return np.sqrt((a['x']-b['x'])**2 + (a['y']-b['y'])**2)

def knn_baseline(query, data, k):
    ranked = sorted(data, key=lambda r: dist(query, r))
    neighbors = ranked[:k]
    votes = Counter(r['label'] for r in neighbors)
    vote = votes.most_common(1)[0][0]
    return vote, neighbors, votes

def knn_weighted(query, data, k):
    ranked = sorted(data, key=lambda r: dist(query, r))
    neighbors = ranked[:k]
    weights = {}
    for r in neighbors:
        d = dist(query, r)
        w = 1.0 / (d + 1e-5)
        weights[r['label']] = weights.get(r['label'], 0) + w
    vote = max(weights, key=weights.get)
    return vote, neighbors, weights

def knn_trust(query, data, k):
    ranked = sorted(data, key=lambda r: dist(query, r))
    neighbors = ranked[:k]
    trust_w = {}
    for r in neighbors:
        d = dist(query, r)
        trust = 0.2 if r['zone'] == 'South' else 1.0
        w = trust / (d + 1e-5)
        trust_w[r['label']] = trust_w.get(r['label'], 0) + w
    vote = max(trust_w, key=trust_w.get)
    return vote, neighbors, trust_w

def knn_adaptive(query, data, k):
    ranked = sorted(data, key=lambda r: dist(query, r))
    near5 = ranked[:5]
    zones = [r['zone'] for r in near5]
    actual_k = 2 if zones.count('South') >= 4 else k
    neighbors = ranked[:actual_k]
    votes = Counter(r['label'] for r in neighbors)
    vote = votes.most_common(1)[0][0]
    return vote, neighbors, votes, actual_k

def knn_reject(query, data, k):
    ranked = sorted(data, key=lambda r: dist(query, r))
    neighbors = ranked[:k]
    votes = Counter(r['label'] for r in neighbors)
    top_label, top_count = votes.most_common(1)[0]
    ratio = top_count / k
    if ratio < 0.70:
        return 'ABSTAIN', neighbors, votes
    return top_label, neighbors, votes

# ══════════════════════════════════════════════════════════
# 互動圖形
# ══════════════════════════════════════════════════════════

fig = plt.figure(figsize=(14, 9), facecolor='#0d1117')
fig.suptitle('Fog City KNN Simulator — The Silent Choice',
             color='white', fontsize=14, fontweight='bold', y=0.98)

# 主地圖區域
ax_map = fig.add_axes([0.05, 0.25, 0.50, 0.68])
ax_map.set_facecolor('#0d1117')

# 投票長條圖
ax_bar = fig.add_axes([0.60, 0.55, 0.37, 0.38])
ax_bar.set_facecolor('#0d1117')

# 資訊文字區
ax_info = fig.add_axes([0.60, 0.25, 0.37, 0.27])
ax_info.set_facecolor('#111827')
ax_info.axis('off')

# 滑桿：K 值
ax_slider = fig.add_axes([0.10, 0.13, 0.45, 0.035],
                          facecolor='#1a1a2e')
slider_k = Slider(ax_slider, 'K值', 1, 20,
                  valinit=1, valstep=1,
                  color='#4fc3f7')
slider_k.label.set_color('white')
slider_k.valtext.set_color('#ffd700')

# 策略選擇按鈕
ax_radio = fig.add_axes([0.60, 0.05, 0.37, 0.18],
                         facecolor='#0d1117')
radio = RadioButtons(
    ax_radio,
    ('Baseline（標準多數決）',
     'Weighted（距離加權）',
     'Trust-aware（可信度建模）',
     'Adaptive K（自適應K）',
     'Reject/Abstain（拒絕不穩定）'),
    activecolor='#4fc3f7'
)
for label in radio.labels:
    label.set_color('white')
    label.set_fontsize(9)

# 重置按鈕
ax_btn = fig.add_axes([0.10, 0.05, 0.10, 0.05])
btn_reset = Button(ax_btn, 'Reset K=1',
                   color='#1a1a2e', hovercolor='#2a2a4e')
btn_reset.label.set_color('white')

# ── 說明文字 ──
fig.text(0.10, 0.195,
         '← 拖動滑桿調整 K 值（1–20），觀察你的決策如何改變',
         color='#aaaaaa', fontsize=9)

# ══════════════════════════════════════════════════════════
# 繪製函式
# ══════════════════════════════════════════════════════════

def draw(k, strategy):
    # 取得結果
    actual_k = k
    if strategy == 'Baseline（標準多數決）':
        vote, neighbors, votes = knn_baseline(YOU, residents, k)
        method_note = f'Standard majority vote  K={k}'
    elif strategy == 'Weighted（距離加權）':
        vote, neighbors, votes = knn_weighted(YOU, residents, k)
        method_note = f'Weight = 1/distance  K={k}'
    elif strategy == 'Trust-aware（可信度建模）':
        vote, neighbors, votes = knn_trust(YOU, residents, k)
        method_note = f'South zone trust=0.2  K={k}'
    elif strategy == 'Adaptive K（自適應K）':
        vote, neighbors, votes, actual_k = knn_adaptive(YOU, residents, k)
        method_note = f'Auto-adjusted K: {k}→{actual_k}'
    else:
        vote, neighbors, votes = knn_reject(YOU, residents, k)
        method_note = f'Abstain if ratio<70%  K={k}'

    safe = vote in SAFE
    nbr_ids = set(id(r) for r in neighbors)

    # ── 清除並重繪地圖 ──
    ax_map.cla()
    ax_map.set_facecolor('#0d1117')

    # 偏差區背景
    bias_bg = mpatches.FancyBboxPatch(
        (0.3, 0.8), 3.4, 2.6,
        boxstyle="round,pad=0.15",
        linewidth=2, edgecolor='#ef5350',
        facecolor='#ef535018', zorder=1)
    ax_map.add_patch(bias_bg)
    ax_map.text(2.0, 1.0, 'BIAS ZONE (South)',
                color='#ef5350', ha='center', fontsize=8,
                fontweight='bold', alpha=0.75, zorder=2)

    # 區域標示
    ax_map.text(3.8, 8.5, 'NORTH\nZone', color='#888',
                fontsize=8, ha='right', va='top', alpha=0.7)
    ax_map.text(3.8, 6.2, 'MIDDLE\nZone', color='#888',
                fontsize=8, ha='right', va='top', alpha=0.7)

    # 所有居民
    for r in residents:
        alpha = 0.35 if id(r) not in nbr_ids else 0.9
        size  = 45   if id(r) not in nbr_ids else 130
        edge  = 'none' if id(r) not in nbr_ids else 'yellow'
        ew    = 0 if id(r) not in nbr_ids else 2
        ax_map.scatter(r['x'], r['y'],
                       c=color_map[r['label']],
                       s=size, alpha=alpha,
                       edgecolors=edge, linewidths=ew,
                       zorder=3)
        # 連線到被選中的鄰居
        if id(r) in nbr_ids:
            ax_map.plot([YOU['x'], r['x']],
                        [YOU['y'], r['y']],
                        '--', color='yellow',
                        alpha=0.4, linewidth=1, zorder=4)

    # 你
    you_color = '#81c784' if safe else ('#ef5350' if vote != 'ABSTAIN' else '#ffd700')
    ax_map.scatter(YOU['x'], YOU['y'],
                   c='white', s=280, marker='*',
                   edgecolors=you_color, linewidths=3, zorder=6)
    ax_map.text(YOU['x']+0.15, YOU['y']+0.22,
                'YOU', color='white', fontsize=10, fontweight='bold')

    # 結果標示（地圖上方）
    if vote == 'ABSTAIN':
        result_str = '⚠ ABSTAIN — 暫停跟隨'
        r_color = '#ffd700'
    elif safe:
        result_str = f'Exit {vote}  ✓ SAFE'
        r_color = '#81c784'
    else:
        result_str = f'Exit {vote}  ✗ DANGER'
        r_color = '#ef5350'

    ax_map.text(2.0, 10.1, result_str,
                ha='center', color=r_color,
                fontsize=13, fontweight='bold', zorder=7)

    # 出口標示
    for y_pos, label, color in [(9.2, 'EXIT A', '#4fc3f7'),
                                 (5.6, 'EXIT B', '#81c784'),
                                 (1.8, 'EXIT C', '#ef5350')]:
        ax_map.text(-0.2, y_pos, label, color=color,
                    fontsize=9, fontweight='bold', va='center')

    ax_map.set_xlim(-0.5, 4.3)
    ax_map.set_ylim(0.4, 10.5)
    ax_map.set_title(f'City Map  |  K = {actual_k}  |  Strategy: {strategy.split("（")[0]}',
                     color='white', fontsize=10, pad=6)
    ax_map.tick_params(colors='#555')
    for sp in ax_map.spines.values():
        sp.set_color('#333')

    # ── 投票長條圖 ──
    ax_bar.cla()
    ax_bar.set_facecolor('#0d1117')

    if isinstance(votes, dict):
        all_labels = ['A', 'B', 'C']
        counts = [votes.get(l, 0) for l in all_labels]
        total = sum(counts)
        # 轉成比例
        vals = [c / total if total > 0 else 0 for c in counts]
    else:
        all_labels = ['A', 'B', 'C']
        counts = [votes.get(l, 0) for l in all_labels]
        total = sum(counts)
        vals = [c / total if total > 0 else 0 for c in counts]

    bars = ax_bar.bar(
        ['Exit A\n(Safe)', 'Exit B\n(Safe)', 'Exit C\n(Danger)'],
        vals,
        color=['#4fc3f7', '#81c784', '#ef5350'],
        alpha=0.8, zorder=3, width=0.5
    )

    # 標示獲選的出口
    for i, (bar, lbl) in enumerate(zip(bars, all_labels)):
        if lbl == vote:
            bar.set_edgecolor('yellow')
            bar.set_linewidth(3)
        pct = f'{vals[i]*100:.0f}%'
        ax_bar.text(bar.get_x() + bar.get_width()/2,
                    bar.get_height() + 0.02,
                    pct, ha='center', color='white',
                    fontsize=11, fontweight='bold')

    ax_bar.set_ylim(0, 1.15)
    ax_bar.set_ylabel('Vote share', color='#aaa', fontsize=9)
    ax_bar.tick_params(colors='#888', labelsize=9)
    for sp in ax_bar.spines.values():
        sp.set_color('#333')
    ax_bar.set_facecolor('#0d1117')
    ax_bar.grid(axis='y', color='#333', linewidth=0.5, zorder=0)
    ax_bar.set_title(f'Neighbor Votes  ({len(neighbors)} neighbors)',
                     color='white', fontsize=10, pad=6)
    ax_bar.axhline(0.5, color='#555', linestyle='--',
                   linewidth=1, alpha=0.6)
    ax_bar.text(2.4, 0.52, '50%', color='#555', fontsize=8)

    # ── 資訊文字 ──
    ax_info.cla()
    ax_info.set_facecolor('#111827')
    ax_info.axis('off')

    south_n = sum(1 for r in neighbors if r['zone'] == 'South')
    north_n = sum(1 for r in neighbors if r['zone'] == 'North')
    mid_n   = sum(1 for r in neighbors if r['zone'] == 'Middle')

    info_lines = [
        (f'Strategy: {strategy.split("（")[0]}', '#ffd700', 10, 'bold'),
        (f'{method_note}', '#aaaaaa', 9,  'normal'),
        ('', 'white', 8, 'normal'),
        (f'Neighbors from:', 'white', 9, 'normal'),
        (f'  North  {north_n} people', '#888', 9, 'normal'),
        (f'  Middle {mid_n} people', '#888', 9, 'normal'),
        (f'  South  {south_n} people  ← BIAS ZONE', '#ef5350' if south_n > 0 else '#888', 9, 'normal'),
        ('', 'white', 8, 'normal'),
        (result_str, r_color, 11, 'bold'),
    ]

    y = 0.95
    for text, color, size, weight in info_lines:
        ax_info.text(0.05, y, text,
                     transform=ax_info.transAxes,
                     color=color, fontsize=size,
                     fontweight=weight, va='top')
        y -= 0.13

    fig.canvas.draw_idle()

# ══════════════════════════════════════════════════════════
# 事件綁定
# ══════════════════════════════════════════════════════════

current_strategy = ['Baseline（標準多數決）']

def update(val):
    k = int(slider_k.val)
    draw(k, current_strategy[0])

def strategy_changed(label):
    current_strategy[0] = label
    k = int(slider_k.val)
    draw(k, current_strategy[0])

def reset(event):
    slider_k.set_val(1)

def on_click(event):
    """點擊地圖移動你的位置"""
    if event.inaxes == ax_map:
        YOU['x'] = event.xdata
        YOU['y'] = event.ydata
        k = int(slider_k.val)
        draw(k, current_strategy[0])

slider_k.on_changed(update)
radio.on_clicked(strategy_changed)
btn_reset.on_clicked(reset)
fig.canvas.mpl_connect('button_press_event', on_click)

# 圖例
legend_elements = [
    mpatches.Patch(color='#4fc3f7', label='Exit A (Safe)'),
    mpatches.Patch(color='#81c784', label='Exit B (Safe)'),
    mpatches.Patch(color='#ef5350', label='Exit C (Danger/Bias)'),
    plt.Line2D([0],[0], marker='o', color='w',
               markerfacecolor='yellow', markersize=9,
               markeredgecolor='yellow', label='Selected neighbor'),
]
fig.legend(handles=legend_elements,
           loc='lower left', ncol=2,
           framealpha=0.15, labelcolor='white',
           facecolor='#0d1117', fontsize=8,
           bbox_to_anchor=(0.05, 0.0))

# 初始畫面
draw(1, 'Baseline（標準多數決）')

plt.show()
