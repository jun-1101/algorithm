import java.awt.*;
import java.awt.image.BufferedImage;
import java.io.File;
import java.io.IOException;
import javax.imageio.ImageIO;
import java.util.ArrayDeque;
import java.util.Queue;

public class bfs_multithreshold {

    // ══════════════════════════════════════════════════════════════════════════
    // Step 1: 建立 histogram h(i)
    // ══════════════════════════════════════════════════════════════════════════

    /** 將彩色影像轉為灰階 2D 陣列 */
    static int[][] toGrayscale(BufferedImage img) {
        int W = img.getWidth(), H = img.getHeight();
        int[][] gray = new int[H][W];
        for (int y = 0; y < H; y++)
            for (int x = 0; x < W; x++) {
                Color c = new Color(img.getRGB(x, y));
                gray[y][x] = (int)(0.299 * c.getRed()
                                 + 0.587 * c.getGreen()
                                 + 0.114 * c.getBlue());
            }
        return gray;
    }

    /**
     * h(i) = 灰階值 i 的像素數量，i ∈ [0, 255]
     * 回傳 double[] 長度 256（原始計數，尚未正規化）
     */
    static double[] buildHistogram(int[][] gray) {
        int H = gray.length, W = gray[0].length;
        double[] h = new double[256];
        for (int[] row : gray)
            for (int v : row)
                h[v]++;
        return h;
    }

    // ══════════════════════════════════════════════════════════════════════════
    // Step 2: 建立 cumulative sum P(i) 與前綴快取
    // ══════════════════════════════════════════════════════════════════════════

    /**
     * P(i) = h(i) / N   (PDF 第18頁定義)
     * 同時建立三條前綴陣列，讓每個區間統計量可 O(1) 查詢：
     *
     *   cumP[j]   = Σ P(i),    i=0..j-1
     *   cumIP[j]  = Σ i·P(i), i=0..j-1
     *   cumI2P[j] = Σ i²·P(i),i=0..j-1
     *
     * 查詢區間 [a, b]：
     *   q     = cumP[b+1]   - cumP[a]
     *   Σ iP  = cumIP[b+1]  - cumIP[a]
     *   Σ i²P = cumI2P[b+1] - cumI2P[a]
     */
    static double[][] buildPrefixTables(double[] h, int N) {
        double[] cumP   = new double[257];
        double[] cumIP  = new double[257];
        double[] cumI2P = new double[257];
        for (int i = 0; i < 256; i++) {
            double p = h[i] / N;            // P(i) = h(i) / N
            cumP[i+1]   = cumP[i]   + p;
            cumIP[i+1]  = cumIP[i]  + i * p;
            cumI2P[i+1] = cumI2P[i] + (double)i * i * p;
        }
        return new double[][]{ cumP, cumIP, cumI2P };
    }

    // ══════════════════════════════════════════════════════════════════════════
    // Step 4: 每個區間用 cumulative sum 算統計量  O(1)
    // ══════════════════════════════════════════════════════════════════════════

    /**
     * 依 PDF 公式計算區間 [a, b] 的三個統計量，全部 O(1)：
     *
     *   q    = Σ P(i),           i=a..b    (PDF: q_o 或 q_b)
     *   u    = Σ i·P(i) / q               (PDF: u_o 或 u_b)
     *   σ²   = Σ [i-u]² P(i)             (PDF: σ²_o 或 σ²_b)
     *        = Σ i²P(i)/q - u²            (展開化簡)
     *
     * @return double[3] = { q, u, sigma2 }
     */
    static double[] regionStats(int a, int b,
                                double[] cumP, double[] cumIP, double[] cumI2P) {
        double q     = cumP[b+1]   - cumP[a];
        double sumIP  = cumIP[b+1]  - cumIP[a];
        double sumI2P = cumI2P[b+1] - cumI2P[a];

        if (q < 1e-15) return new double[]{ 0, 0, 0 };

        // PDF 公式: u_o(t) = Σ i·P(i) / q_o(t)
        double u = sumIP / q;

        // PDF 公式: σ²_o(t) = Σ [i-u_o]² P(i)  →  展開 = E[i²] - u²
        double sigma2 = sumI2P - u * u * q; // PDF: σ²=Σ[i-u]²P(i)=sumI2P-u²·q
        if (sigma2 < 0) sigma2 = 0;         // 防止浮點誤差

        return new double[]{ q, u, sigma2 };
    }

    /**
     * Within-group variance: sigma2_w = sum of sigma2_region(r)
     */
    static double withinGroupVariance(int[] boundaries,
                                      double[] cumP, double[] cumIP, double[] cumI2P) {
        double total = 0;
        int n = boundaries.length;
        for (int r = 0; r < n - 1; r++) {
            int a = boundaries[r];
            int b = (r < n - 2) ? boundaries[r+1] - 1 : 255;
            double[] stats = regionStats(a, b, cumP, cumIP, cumI2P);
            total += stats[2];
        }
        return total;
    }

    /**
     * Between-group variance: sigma2_b = sum q_r*(u_r - u_total)^2
     * Otsu's true objective -- maximise this to best separate sky vs penguin head.
     * Since sigma2_total = sigma2_w + sigma2_b is constant,
     * maximising sigma2_b == minimising sigma2_w mathematically,
     * but sigma2_b gives cleaner numerical contrast when regions overlap in brightness.
     */
    static double betweenGroupVariance(int[] boundaries,
                                       double[] cumP, double[] cumIP, double[] cumI2P) {
        double uTotal = cumIP[256]; // global weighted mean
        double total  = 0;
        int n = boundaries.length;
        for (int r = 0; r < n - 1; r++) {
            int a = boundaries[r];
            int b = (r < n - 2) ? boundaries[r+1] - 1 : 255;
            double[] stats = regionStats(a, b, cumP, cumIP, cumI2P);
            double q = stats[0];
            double u = stats[1];
            total += q * (u - uTotal) * (u - uTotal);
        }
        return total;
    }

    // ══════════════════════════════════════════════════════════════════════════
    // Step 3 & 5: BFS 廣度優先搜尋最佳 threshold 組合
    // ══════════════════════════════════════════════════════════════════════════

    /**
     * BFS 搜尋最佳 k 個 threshold，使 σ²_w 最小。
     *
     * BFS 狀態: int[] { t1, t2, ..., t_depth, nextStart }
     *   - 前 depth 個元素 = 已選的 threshold
     *   - 最後一個元素    = 下一個可選的起始灰階值
     *
     * 到達深度 k 時為葉節點，計算 σ²_w 並更新最佳解 (Step 5)。
     *
     * 時間複雜度: O( C(L, k) )  每個葉節點 O(1) 評估（靠前綴快取）
     *
     * @param k        threshold 數量
     * @param minGap   相鄰 threshold 最小間距
     * @return int[] 最佳 threshold 陣列，長度 k
     */
    static int[] bfsFindThresholds(double[] cumP, double[] cumIP, double[] cumI2P,
                                   int k, int minGap) {
        double bestVar = -1.0;          // maximise between-group variance
        int[] bestThresholds = new int[k];
        long nodesVisited = 0;

        // BFS queue：每個狀態 = int 陣列，長度 k+1
        // 前 depth 個 = 已選 threshold，index k = nextStart
        Queue<int[]> queue = new ArrayDeque<>();
        // 初始狀態：depth=0，nextStart=1
        queue.add(new int[]{ 1 });   // 只存 nextStart，depth=0

        // 使用通用的 BFS：狀態存 [t1, t2, ..., t_depth, nextStart]
        // 深度 = 陣列長度 - 1
        while (!queue.isEmpty()) {
            int[] state = queue.poll();
            nodesVisited++;
            int depth = state.length - 1;       // 已選 threshold 數
            int start = state[depth];           // 下一個可選起始值

            if (depth == k) {
                // 葉節點：建立 boundaries 並計算 σ²_w
                int[] boundaries = new int[k + 2];
                boundaries[0] = 0;
                for (int i = 0; i < k; i++) boundaries[i+1] = state[i];
                boundaries[k+1] = 256;          // 上界哨兵

                // Step 5: maximise sigma2_b (between-group variance = Otsu objective)
                double var = betweenGroupVariance(boundaries, cumP, cumIP, cumI2P);
                if (var > bestVar) {
                    bestVar = var;
                    for (int i = 0; i < k; i++) bestThresholds[i] = state[i];
                }
                continue;
            }

            // 展開下一層
            int remaining = k - depth;
            int maxT = 255 - (remaining - 1) * minGap - minGap;
            for (int t = start; t <= maxT; t++) {
                // 新狀態 = 舊狀態前 depth 個 + t + (t+minGap)
                int[] next = new int[depth + 2];
                for (int i = 0; i < depth; i++) next[i] = state[i];
                next[depth]   = t;
                next[depth+1] = t + minGap;     // nextStart
                queue.add(next);
            }
        }

        System.out.printf("  [BFS] 訪問節點數: %,d%n", nodesVisited);
        System.out.printf("  [BFS] 最大 σ²_b : %.8f%n", bestVar);
        return bestThresholds;
    }

    // ══════════════════════════════════════════════════════════════════════════
    // Step 6: 根據 threshold 做影像分割
    // ══════════════════════════════════════════════════════════════════════════

    /**
     * Multi-level 灰階分割，支援任意 k 個 threshold (k+1 個區間)。
     * 各區間依均勻間隔指派灰階輸出值 0, 255/(k), 2*255/(k), ..., 255。
     *
     * @param bestT 排序好的 threshold 陣列，長度 k
     */
    static BufferedImage segment(int[][] gray, int[] bestT) {
        int k = bestT.length;
        int H = gray.length, W = gray[0].length;
        BufferedImage out = new BufferedImage(W, H, BufferedImage.TYPE_INT_RGB);
        // 輸出灰階值：k+1 個區間均勻分配
        int[] levels = new int[k + 1];
        for (int r = 0; r <= k; r++)
            levels[r] = (int)Math.round(r * 255.0 / k);
        for (int y = 0; y < H; y++)
            for (int x = 0; x < W; x++) {
                int v = gray[y][x];
                int region = k;  // 預設最後一區
                for (int r = 0; r < k; r++) {
                    if (v < bestT[r]) { region = r; break; }
                }
                int lv = levels[region];
                out.setRGB(x, y, new Color(lv, lv, lv).getRGB());
            }
        return out;
    }

    /**
     * 彩色 overlay，支援任意 k 個 threshold (k+1 個區間)。
     *
     * 4 個區間配色 (k=3)：
     *   region 0 (最暗) → 藍  (30,  80, 180) — 企鵝暗部細節
     *   region 1        → 綠  (80, 180,  60) — 企鵝主體中間調
     *   region 2        → 橘  (220, 140,  0) — 企鵝亮部 / 過渡
     *   region 3 (最亮) → 紅橘 (220, 60,  40) — 背景（最亮）
     *
     * 相較於原本 k=2 三色版，多一層橘色讓原本「亮企鵝 ≈ 亮背景」的像素
     * 被獨立成 region 2，最右大企鵝因此不再與紅橘背景 (region 3) 混同。
     *
     * @param bestT 排序好的 threshold 陣列，長度 k
     */
    static BufferedImage colourOverlay(int[][] gray, int[] bestT) {
        int k = bestT.length;
        int H = gray.length, W = gray[0].length;
        BufferedImage out = new BufferedImage(W, H, BufferedImage.TYPE_INT_RGB);

        // 預定義最多 6 區顏色；若 k > 5 則循環
        Color[] palette = {
            new Color( 30,  80, 180),  // 0: 深藍
            new Color( 80, 180,  60),  // 1: 綠
            new Color(220, 140,   0),  // 2: 橘黃 ← 新增，分離亮企鵝與亮背景
            new Color(220,  60,  40),  // 3: 紅橘 (亮背景)
            new Color(160,   0, 200),  // 4: 紫
            new Color(  0, 200, 200),  // 5: 青
        };

        for (int y = 0; y < H; y++)
            for (int x = 0; x < W; x++) {
                int v = gray[y][x];
                int region = k;
                for (int r = 0; r < k; r++) {
                    if (v < bestT[r]) { region = r; break; }
                }
                out.setRGB(x, y, palette[region % palette.length].getRGB());
            }
        return out;
    }

    /** 灰階 int[][] → BufferedImage */
    static BufferedImage grayToImage(int[][] gray) {
        int H = gray.length, W = gray[0].length;
        BufferedImage out = new BufferedImage(W, H, BufferedImage.TYPE_INT_RGB);
        for (int y = 0; y < H; y++)
            for (int x = 0; x < W; x++) {
                int v = gray[y][x];
                out.setRGB(x, y, new Color(v, v, v).getRGB());
            }
        return out;
    }

    // ══════════════════════════════════════════════════════════════════════════
    // Histogram chart (含 σ²_w 曲線與 threshold 標記)
    // ══════════════════════════════════════════════════════════════════════════

    /**
     * 繪製 histogram 圖表，以多色區分區間，
     * 並在每個 threshold 位置畫垂直線。
     *
     * @param bestT 排序好的 threshold 陣列，長度 k
     */
    static BufferedImage drawHistogram(double[] h, int N, int[] bestT,
                                       double[] cumP, double[] cumIP, double[] cumI2P) {
        int t1 = bestT[0], t2 = bestT[bestT.length - 1];
        int CW = 960, CH = 440;
        int PAD = 65, CW2 = CW - 2*PAD, CH2 = CH - 2*PAD;
        BufferedImage img = new BufferedImage(CW, CH, BufferedImage.TYPE_INT_RGB);
        Graphics2D g = img.createGraphics();
        g.setRenderingHint(RenderingHints.KEY_ANTIALIASING,
                           RenderingHints.VALUE_ANTIALIAS_ON);
        g.setColor(new Color(245, 245, 245));
        g.fillRect(0, 0, CW, CH);

        // ── histogram bars ───────────────────────────────────────────────────
        double maxP = 0;
        for (double v : h) if (v / N > maxP) maxP = v / N;

        // 與 colourOverlay 同調色板
        Color[] barPalette = {
            new Color( 30,  80, 180, 160),
            new Color( 80, 180,  60, 160),
            new Color(220, 140,   0, 160),
            new Color(220,  60,  40, 160),
            new Color(160,   0, 200, 160),
            new Color(  0, 200, 200, 160),
        };
        for (int i = 0; i < 256; i++) {
            double p = h[i] / N;
            int barH = (int)(p / maxP * CH2);
            int bx   = PAD + (int)(i / 255.0 * CW2);
            int bw   = Math.max(1, CW2 / 256);
            // 判斷 region
            int region = bestT.length;
            for (int r = 0; r < bestT.length; r++) {
                if (i < bestT[r]) { region = r; break; }
            }
            g.setColor(barPalette[region % barPalette.length]);
            g.fillRect(bx, PAD + CH2 - barH, bw, barH);
        }

        // ── σ²_w curve ───────────────────────────────────────────────────────
        // 單 threshold 掃描：σ²_w(t) = σ²_o(t) + σ²_b(t)
        double[] sigmaW = new double[256];
        double maxSigma = 0;
        for (int t = 1; t < 255; t++) {
            double[] so = regionStats(0,   t,   cumP, cumIP, cumI2P);
            double[] sb = regionStats(t+1, 255, cumP, cumIP, cumI2P);
            sigmaW[t] = so[2] + sb[2];
            if (sigmaW[t] > maxSigma) maxSigma = sigmaW[t];
        }
        g.setColor(new Color(100, 0, 100, 200));
        g.setStroke(new BasicStroke(1.8f, BasicStroke.CAP_ROUND, BasicStroke.JOIN_ROUND));
        for (int i = 1; i < 254; i++) {
            int x1c = PAD + (int)(i / 255.0 * CW2);
            int x2c = PAD + (int)((i+1) / 255.0 * CW2);
            int y1c = PAD + CH2 - (int)(sigmaW[i]   / maxSigma * CH2);
            int y2c = PAD + CH2 - (int)(sigmaW[i+1] / maxSigma * CH2);
            g.drawLine(x1c, y1c, x2c, y2c);
        }

        // ── threshold lines ──────────────────────────────────────────────────
        Color[] lineColors = { Color.RED, new Color(180,0,180), new Color(0,120,0),
                               new Color(0,0,180) };
        g.setStroke(new BasicStroke(2.5f));
        for (int r = 0; r < bestT.length; r++) {
            int lx = PAD + (int)(bestT[r] / 255.0 * CW2);
            g.setColor(lineColors[r % lineColors.length]);
            g.drawLine(lx, PAD, lx, PAD + CH2);
        }

        // ── axes & labels ────────────────────────────────────────────────────
        g.setColor(Color.BLACK);
        g.setStroke(new BasicStroke(1.5f));
        g.drawRect(PAD, PAD, CW2, CH2);

        g.setFont(new Font("SansSerif", Font.BOLD, 14));
        g.drawString("Histogram  +  σ²_w curve  (PDF Region Threshold using Moments)", PAD, PAD - 12);

        g.setFont(new Font("SansSerif", Font.PLAIN, 12));
        g.drawString("0",   PAD - 5,       PAD + CH2 + 16);
        g.drawString("255", PAD + CW2 - 15, PAD + CH2 + 16);
        g.drawString("Intensity", PAD + CW2/2 - 25, PAD + CH2 + 32);

        g.setFont(new Font("SansSerif", Font.BOLD, 12));
        for (int r = 0; r < bestT.length; r++) {
            int lx = PAD + (int)(bestT[r] / 255.0 * CW2);
            g.setColor(lineColors[r % lineColors.length]);
            g.drawString("T" + (r+1) + "=" + bestT[r], lx + 4, PAD + 20 + r * 16);
        }

        // ── legend ───────────────────────────────────────────────────────────
        int legendX = CW - 230, legendY = PAD + 10;
        g.setFont(new Font("SansSerif", Font.PLAIN, 11));
        Color[] barPaletteL = {
            new Color( 30,  80, 180), new Color( 80, 180,  60),
            new Color(220, 140,   0), new Color(220,  60,  40),
        };
        // Build region labels
        int k2 = bestT.length;
        String[] ll = new String[k2 + 2];
        ll[0] = "Region 0  (< T1)";
        for (int r = 1; r < k2; r++)
            ll[r] = "Region " + r + "  [T" + r + ",T" + (r+1) + ")";
        ll[k2] = "Region " + k2 + "  (≥ T" + k2 + ")";
        ll[k2 + 1] = "σ²_w curve";
        Color[] lc2 = new Color[k2 + 2];
        for (int r = 0; r <= k2; r++) lc2[r] = barPaletteL[r % barPaletteL.length];
        lc2[k2 + 1] = new Color(100, 0, 100);

        for (int i = 0; i < ll.length; i++) {
            g.setColor(lc2[i]);
            g.fillRect(legendX, legendY + i*18, 12, 12);
            g.setColor(Color.BLACK);
            g.drawString(ll[i], legendX + 16, legendY + i*18 + 11);
        }

        g.dispose();
        return img;
    }

    // ══════════════════════════════════════════════════════════════════════════
    // Step 7: 印出時間複雜度
    // ══════════════════════════════════════════════════════════════════════════

    static void printComplexity(int N, int L, int k, long elapsedMs) {
        // C(L, k) 計算
        long combLk = 1;
        for (int i = 0; i < k; i++) combLk = combLk * (L - i) / (i + 1);

        System.out.println();
        System.out.println("================================================================");
        System.out.println("  [Step 7] 時間複雜度分析");
        System.out.println("================================================================");
        System.out.printf("  N = %,d 像素   L = %d (灰階等級)   k = %d (threshold 數)%n",
                          N, L, k);
        System.out.println();
        System.out.println("  步驟                           複雜度          說明");
        System.out.println("  " + "-".repeat(62));
        System.out.printf("  Step1  buildHistogram()        O(N)            掃描所有像素%n");
        System.out.printf("  Step2  buildPrefixTables()     O(L)            建3條前綴陣列%n");
        System.out.printf("  Step3  BFS 展開                O(C(L,k))       所有有效組合%n");
        System.out.printf("  Step4  regionStats() 每次      O(1)            前綴快取加速%n");
        System.out.printf("  Step5  記錄最佳解              O(1)            BFS內即時更新%n");
        System.out.printf("  Step6  segment()               O(N)            掃描所有像素%n");
        System.out.println();
        System.out.printf("  整體複雜度: O(N + k·C(L,k))%n");
        System.out.printf("    C(%d,%d)    = %,d%n", L, k, combLk);
        System.out.printf("    k·C(L,k)  = %,d%n", k * combLk);
        System.out.println();
        System.out.printf("  若不用前綴快取 (naive，每次 regionStats = O(L)):%n");
        System.out.printf("    BFS 總計 O(k·L·C(L,k)) = O(L^(k+1)/k!)%n");
        System.out.printf("    k·L·C(L,k) = %,d   ← 慢 %d 倍%n",
                          (long)k * L * combLk, L);
        System.out.println();
        System.out.printf("  實際執行時間: %d ms%n", elapsedMs);
        System.out.println("================================================================");
    }

    // ══════════════════════════════════════════════════════════════════════════
    // Main
    // ══════════════════════════════════════════════════════════════════════════

    public static void main(String[] args) throws IOException {
        String inputPath = args.length > 0 ? args[0] : "animal.jpg";
        String outDir    = args.length > 1 ? args[1] : ".";
        int    k         = args.length > 2 ? Integer.parseInt(args[2]) : 3;  // 預設 k=3 → 4 個區間
        int    minGap    = 1;  // 相鄰 threshold 最小間距（縮小至 1，讓 BFS 在亮度相近區間找到更好切點）

        System.out.println("=== Assignment 1 – BFS Multi-threshold Segmentation ===");
        System.out.println("Input : " + inputPath);
        System.out.println("k     : " + k + " thresholds → " + (k+1) + " regions");

        long t0 = System.currentTimeMillis();

        // ── 讀取影像 ────────────────────────────────────────────────────────
        BufferedImage original = ImageIO.read(new File(inputPath));
        if (original == null) {
            System.err.println("[ERROR] 無法讀取影像: " + inputPath);
            System.exit(1);
        }
        int W = original.getWidth(), H = original.getHeight();
        int N = W * H;
        System.out.printf("Image size: %d × %d = %,d pixels%n", W, H, N);

        // ── Step 1: Histogram ────────────────────────────────────────────────
        System.out.println("\n[Step 1] 建立 histogram h(i) ...");
        int[][] gray = toGrayscale(original);
        double[] h   = buildHistogram(gray);

        // ── Step 2: P(i) + 前綴快取 ─────────────────────────────────────────
        System.out.println("[Step 2] 建立 P(i) 與累積前綴快取 ...");
        double[][] prefix = buildPrefixTables(h, N);
        double[] cumP  = prefix[0];
        double[] cumIP = prefix[1];
        double[] cumI2P= prefix[2];

        // ── Step 3 & 4 & 5: BFS ─────────────────────────────────────────────
        System.out.printf("%n[Step 3~5] BFS 搜尋最佳 %d 個 threshold ...%n", k);
        int[] bestT = bfsFindThresholds(cumP, cumIP, cumI2P, k, minGap);

        // 印出各 threshold
        StringBuilder tStr = new StringBuilder();
        for (int i = 0; i < k; i++) {
            if (i > 0) tStr.append(", ");
            tStr.append("T").append(i+1).append("=").append(bestT[i]);
        }
        System.out.printf("  最佳 threshold: %s%n", tStr);

        // 印出各區間統計量（對應 PDF 公式的 q_o, u_o, σ²_o, q_b, u_b, σ²_b）
        System.out.println("\n  各區間統計量 (PDF 公式):");
        System.out.printf("  %-14s %-22s %14s %10s %12s%n",
                          "區間", "名稱", "q (機率質量)", "u (均值)", "σ² (變異數)");
        System.out.println("  " + "-".repeat(74));
        int[] boundaries = new int[k + 2];
        boundaries[0] = 0;
        for (int i = 0; i < k; i++) boundaries[i+1] = bestT[i];
        boundaries[k+1] = 256;
        String[] regionNames = new String[k+1];
        regionNames[0]   = "Region0/最暗";
        regionNames[k]   = "Region" + k + "/最亮(背景)";
        for (int i = 1; i < k; i++) regionNames[i] = "Region" + i + "/中間-" + i;

        double sigmaWTotal = 0;
        for (int r = 0; r < k + 1; r++) {
            int a = boundaries[r];
            int b = (r < k) ? boundaries[r+1] - 1 : 255;
            double[] stats = regionStats(a, b, cumP, cumIP, cumI2P);
            sigmaWTotal += stats[2];
            System.out.printf("  [%3d,%3d]     %-22s %14.6f %10.4f %12.6f%n",
                              a, b, regionNames[r], stats[0], stats[1], stats[2]);
        }
        System.out.printf("  %58s σ²_w = %.8f%n", "", sigmaWTotal);

        // ── Step 6: 影像分割 ─────────────────────────────────────────────────
        System.out.println("\n[Step 6] 根據 threshold 做影像分割 ...");
        new File(outDir).mkdirs();

        ImageIO.write(grayToImage(gray),
                      "PNG", new File(outDir + "/1_grayscale2.png"));
        ImageIO.write(drawHistogram(h, N, bestT, cumP, cumIP, cumI2P),
                      "PNG", new File(outDir + "/2_histogram2.png"));
        ImageIO.write(segment(gray, bestT),
                      "PNG", new File(outDir + "/3_segmented2.png"));
        ImageIO.write(colourOverlay(gray, bestT),
                      "PNG", new File(outDir + "/4_colour_overlay2.png"));

        System.out.println("  輸出至: " + outDir);
        System.out.println("    1_grayscale2.png      – 灰階影像");
        System.out.println("    2_histogram2.png      – histogram + σ²_w 曲線 + T1/T2 標記");
        System.out.println("    3_segmented2.png      – 3段分割 (0/128/255)");
        System.out.println("    4_colour_overlay2.png – 彩色 region map");

        // ── Step 7: 時間複雜度 ───────────────────────────────────────────────
        long elapsed = System.currentTimeMillis() - t0;
        printComplexity(N, 256, k, elapsed);

        System.out.println("Done.");
    }
}