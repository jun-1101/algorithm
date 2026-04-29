import sys
import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import cv2
from skimage import io, color

# ════════════════════════════════════════════════════════════
#  1. 核心演算法：拆解 X 與 Y 掃描的 Chamfer Distance
# ════════════════════════════════════════════════════════════

def chamfer_x_scan(feature: np.ndarray) -> np.ndarray:
    """僅進行 X 方向（橫向）的 Two-pass 掃描"""
    rows, cols = feature.shape
    dist = np.where(feature == 1, 0.0, 1e6)
    # Forward: Left to Right
    for r in range(rows):
        for c in range(1, cols):
            dist[r, c] = min(dist[r, c], dist[r, c-1] + 1)
    # Backward: Right to Left
    for r in range(rows):
        for c in range(cols - 2, -1, -1):
            dist[r, c] = min(dist[r, c], dist[r, c+1] + 1)
    return dist

def chamfer_y_scan(feature: np.ndarray) -> np.ndarray:
    """僅進行 Y 方向（縱向）的 Two-pass 掃描"""
    rows, cols = feature.shape
    dist = np.where(feature == 1, 0.0, 1e6)
    # Forward: Top to Bottom
    for c in range(cols):
        for r in range(1, rows):
            dist[r, c] = min(dist[r, c], dist[r-1, c] + 1)
    # Backward: Bottom to Top
    for c in range(cols):
        for r in range(rows - 2, -1, -1):
            dist[r, c] = min(dist[r, c], dist[r+1, c] + 1)
    return dist

def chamfer_2d_full(feature: np.ndarray) -> np.ndarray:
    """標準 2D Chamfer (L1)，結合 XY 掃描"""
    rows, cols = feature.shape
    dist = np.where(feature == 1, 0.0, 1e6)
    # Forward pass
    for r in range(rows):
        for c in range(cols):
            if r > 0: dist[r, c] = min(dist[r, c], dist[r-1, c] + 1)
            if c > 0: dist[r, c] = min(dist[r, c], dist[r, c-1] + 1)
    # Backward pass
    for r in range(rows - 1, -1, -1):
        for c in range(cols - 1, -1, -1):
            if r < rows - 1: dist[r, c] = min(dist[r, c], dist[r+1, c] + 1)
            if c < cols - 1: dist[r, c] = min(dist[r, c], dist[r, c+1] + 1)
    return dist

# ════════════════════════════════════════════════════════════
#  2. 視覺化模擬功能
# ════════════════════════════════════════════════════════════

def style_q1_cycle(dist_map: np.ndarray, cycle: int = 20):
    """模擬照片 1：週期性黑白條紋效果"""
    cycled = dist_map % cycle
    res = np.where(cycled < (cycle / 2), 0, 255)
    return res.astype(np.uint8)

def style_q2_glowing(dist_map: np.ndarray):
    """模擬照片 2：暗底發光距離場效果"""
    # 強化邊緣發光感
    glow = np.sqrt(dist_map)
    glow = np.clip(glow, 0, glow.max() * 0.4)
    return glow

# ════════════════════════════════════════════════════════════
#  3. 主執行流程
# ════════════════════════════════════════════════════════════

def run_assignments(img_path: str):
    # 影像讀取與預處理
    img_raw = io.imread(img_path)
    if img_raw.ndim == 3:
        gray = (color.rgb2gray(img_raw) * 255).astype(np.uint8)
    else:
        gray = img_raw.astype(np.uint8)
    
    # 邊緣偵測
    edges = (cv2.Canny(gray, 50, 150) > 0).astype(np.uint8)

    # --- 第一題：X 掃描 vs Y 掃描 (週期視覺化) ---
    dist_x = chamfer_x_scan(edges)
    dist_y = chamfer_y_scan(edges)
    vis_x  = style_q1_cycle(dist_x, cycle=20)
    vis_y  = style_q1_cycle(dist_y, cycle=20)

    # --- 第二題：完整 2D Chamfer (發光視覺化) ---
    dist_full = chamfer_2d_full(edges)
    vis_glow  = style_q2_glowing(dist_full)

    # 繪圖
    plt.rcParams['axes.facecolor'] = 'black'
    fig = plt.figure(figsize=(16, 10), facecolor='#0a0a0a')
    gs = gridspec.GridSpec(2, 2, hspace=0.3, wspace=0.1)

    # 第一題展示 (橫向與縱向掃描結果)
    ax1 = fig.add_subplot(gs[0, 0])
    ax1.set_title("Q1: X-Direction Scan (Horizontal Cycle)", color='white')
    ax1.imshow(vis_x, cmap='gray'); ax1.axis('off')

    ax2 = fig.add_subplot(gs[0, 1])
    ax2.set_title("Q1: Y-Direction Scan (Vertical Cycle)", color='white')
    ax2.imshow(vis_y, cmap='bone'); ax2.axis('off')

    # 第二題展示 (發光效果)
    ax3 = fig.add_subplot(gs[1, :])
    ax3.set_title("Q2: Glowing Distance Field (Assignment 2 Style)", color='cyan', fontsize=14)
    ax3.imshow(vis_glow, cmap='magma')
    ax3.axis('off')

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    # 請確保 demo1.png 存在或替換為正確路徑
    test_img = "fox.jpg"
    if os.path.exists(test_img):
        run_assignments(test_img)
    else:
        # 自動產生測試圖
        dummy = np.zeros((300, 300), dtype=np.uint8)
        cv2.putText(dummy, "CV", (50, 180), cv2.FONT_HERSHEY_SIMPLEX, 4, 255, 6)
        cv2.imwrite(test_img, dummy)
        run_assignments(test_img)