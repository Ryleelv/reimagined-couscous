# 导入 Figma

由于当前运行环境没有连接到你的 Figma 账号，不能替你直接写入某个云端 Figma 文件。本地插件可以把三张 SVG 一次性导入你当前打开的 Figma 页面。

## 安装插件（只需一次）

1. 打开 Figma 桌面版。
2. 依次选择 **Plugins → Development → Import plugin from manifest…**。
3. 选择本目录中的 `manifest.json`。

## 导入三张画板

1. 在 Figma 中打开目标文件和页面。
2. 运行 **Plugins → Development → 岭境 A3 画板导入器**。
3. 一次选择上一级目录中的三张 SVG：
   - `01-design-analysis.svg`
   - `02-design-sketches.svg`
   - `03-product-system.svg`
4. 点击 **导入 Figma**。

插件会保持 A3 的 420:297 比例，将三张画板按“设计分析 → 设计草图 → 主体物与体验系统”的顺序横向排列并选中。
