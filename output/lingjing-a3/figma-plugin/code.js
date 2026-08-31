figma.showUI(__html__, { width: 420, height: 430, themeColors: true });

figma.ui.onmessage = (message) => {
  if (message.type === "cancel") {
    figma.closePlugin();
    return;
  }

  if (message.type !== "import-boards") return;

  const boards = message.boards;
  if (!Array.isArray(boards) || boards.length !== 3) {
    figma.notify("请选择三张岭境 SVG 画板。", { error: true });
    return;
  }

  try {
    const imported = boards.map((board, index) => {
      const node = figma.createNodeFromSvg(board.svg);
      node.name = board.name.replace(/\.svg$/i, "");

      // Figma uses CSS pixels. 1587.4 × 1122.5 preserves the A3 420:297 ratio.
      node.resize(1587.4, 1122.5);
      node.x = index * 1767.4;
      node.y = 0;
      figma.currentPage.appendChild(node);
      return node;
    });

    figma.currentPage.selection = imported;
    figma.viewport.scrollAndZoomIntoView(imported);
    figma.notify("已将三张 A3 画板导入当前 Figma 页面。", { timeout: 3500 });
    figma.closePlugin();
  } catch (error) {
    figma.notify(`导入失败：${error.message}`, { error: true, timeout: 5000 });
  }
};
