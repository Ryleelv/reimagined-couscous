#!/usr/bin/env python3
"""Generate three landscape-A3 SVG study boards for the 963 cultural-VR exercise."""
from pathlib import Path

OUT = Path("output/lingjing-a3")
W, H = 4961, 3508  # A3 landscape, 300 dpi

NAVY, INK, TEAL, MINT, RED, GOLD, PAPER, LINE, GREY = (
    "#102B36", "#17232A", "#087E7B", "#8BD5C8", "#D65245", "#D9A441", "#F6F3EC", "#BFC9C5", "#6E7C80"
)

def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

def text(x, y, value, size=40, color=INK, weight=400, anchor="start", cls=""):
    return f'<text x="{x}" y="{y}" class="{cls}" text-anchor="{anchor}" font-size="{size}" font-weight="{weight}" fill="{color}">{esc(value)}</text>'

def multiline(x, y, lines, size=34, gap=48, color=INK, weight=400):
    return "".join(text(x, y+i*gap, line, size, color, weight) for i,line in enumerate(lines))

def box(x,y,w,h,title,body,accent=TEAL):
    lines = body if isinstance(body,list) else [body]
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="28" fill="#fff" stroke="{LINE}" stroke-width="5"/>'
            f'<rect x="{x}" y="{y}" width="14" height="{h}" rx="7" fill="{accent}"/>'
            + text(x+48,y+65,title,42,INK,700) + multiline(x+48,y+125,lines,30,44,GREY))

def tag(x,y,label,fill=TEAL):
    width=max(150,len(label)*38+58)
    return f'<rect x="{x}" y="{y-40}" width="{width}" height="58" rx="29" fill="{fill}"/>'+text(x+29,y,label,27,"#fff",700)

def arrow(x1,y1,x2,y2,color=TEAL):
    return f'<path d="M{x1},{y1} L{x2},{y2}" stroke="{color}" stroke-width="10" fill="none" marker-end="url(#arrow)"/>'

def headset(cx,cy,scale=1, exploded=False):
    # An original, simplified headset illustration—not a copy of the reference product.
    s=scale; x=cx-630*s; y=cy-250*s
    parts=[]
    parts.append(f'<path d="M{x+180*s},{y+270*s} Q{x+330*s},{y+5*s} {x+930*s},{y+30*s} Q{x+1210*s},{y+65*s} {x+1230*s},{y+330*s} L{x+1130*s},{y+420*s} Q{x+700*s},{y+210*s} {x+240*s},{y+420*s}Z" fill="#E7ECE9" stroke="{INK}" stroke-width="{16*s}"/>')
    parts.append(f'<path d="M{x+255*s},{y+390*s} Q{x+690*s},{y+190*s} {x+1135*s},{y+390*s} L{x+1070*s},{y+620*s} Q{x+700*s},{y+740*s} {x+320*s},{y+620*s}Z" fill="#152B33" stroke="{INK}" stroke-width="{16*s}"/>')
    parts.append(f'<path d="M{x+320*s},{y+585*s} Q{x+460*s},{y+430*s} {x+595*s},{y+580*s} Q{x+710*s},{y+460*s} {x+820*s},{y+580*s} Q{x+950*s},{y+430*s} {x+1070*s},{y+575*s}" fill="none" stroke="#5AB6B0" stroke-width="{18*s}"/>')
    parts.append(f'<path d="M{x+220*s},{y+285*s} Q{x+80*s},{y+135*s} {x+190*s},{y-20*s} Q{x+620*s},{y-330*s} {x+1150*s},{y-75*s} Q{x+1320*s},{y+45*s} {x+1180*s},{y+270*s}" fill="none" stroke="#D8DED9" stroke-width="{95*s}" stroke-linecap="round"/>')
    parts.append(f'<path d="M{x+250*s},{y+260*s} Q{x+95*s},{y+90*s} {x+210*s},{y-25*s} Q{x+650*s},{y-260*s} {x+1140*s},{y-65*s} Q{x+1280*s},{y+30*s} {x+1170*s},{y+250*s}" fill="none" stroke="{INK}" stroke-width="{15*s}"/>')
    parts.append(f'<rect x="{x+455*s}" y="{y-310*s}" width="{430*s}" height="{85*s}" rx="{42*s}" fill="#A7B4B3" stroke="{INK}" stroke-width="{12*s}"/>')
    parts.append(f'<circle cx="{x+470*s}" cy="{y+425*s}" r="{30*s}" fill="{RED}"/><circle cx="{x+930*s}" cy="{y+425*s}" r="{30*s}" fill="{RED}"/>')
    parts.append(f'<path d="M{x+405*s},{y+340*s} Q{x+690*s},{y+220*s} {x+1010*s},{y+340*s}" fill="none" stroke="#fff" stroke-opacity=".32" stroke-width="{22*s}"/>')
    return "".join(parts)

def doc(title, subtitle):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="420mm" height="297mm" viewBox="0 0 {W} {H}">
<defs><marker id="arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="10" markerHeight="10" orient="auto-start-reverse"><path d="M 0 0 L 10 5 L 0 10 z" fill="{TEAL}"/></marker>
<pattern id="grid" width="64" height="64" patternUnits="userSpaceOnUse"><path d="M64 0H0V64" fill="none" stroke="#D9DFDC" stroke-width="2"/></pattern>
<style>text{{font-family:'Noto Sans CJK SC','Microsoft YaHei','PingFang SC',sans-serif;letter-spacing:1px}} .small{{letter-spacing:0}}</style></defs>
<rect width="{W}" height="{H}" fill="{PAPER}"/><rect x="95" y="90" width="4771" height="3328" rx="42" fill="url(#grid)" opacity=".37"/>
<rect x="95" y="90" width="4771" height="3328" rx="42" fill="none" stroke="{INK}" stroke-width="8"/>
{tag(180,225,'广工 963 · 文旅产品系统设计',NAVY)}{text(180,375,title,96,INK,800)}{text(185,442,subtitle,35,GREY,400)}
<line x1="180" y1="500" x2="4780" y2="500" stroke="{INK}" stroke-width="8"/>
<text x="180" y="3330" font-size="25" fill="{GREY}">LINGJING · 广东古镇沉浸式导览系统 ｜ A3 横版学习示意 ｜ 姓名：__________  准考证号：__________</text></svg>'''

def replace(svg, insert): return svg.replace('</svg>', insert+'\n</svg>')

def analysis():
    s=doc('01 / 设计分析', '从“看遗址”到“进入古镇的一天”｜题意、用户、系统与商业闭环')
    c=[]
    c += [box(180,590,1030,350,'命题关键词',['广东古镇遗址展览馆','VR/AR 眼镜创新｜展览活动｜商业可行性','外观结构｜UI 流程｜情景使用｜工作原理'],RED)]
    c += [box(180,990,1030,570,'用户与痛点',['年轻游客：内容碎片化，缺少分享动力','亲子家庭：展板难懂，互动不足','展馆运营：客流分散，设备卫生与复购压力','关键洞察：传统封闭 VR 不能安全地“边走边看”'],TEAL)]
    c += [box(180,1610,1030,550,'设计目标',['开放导览：看得见真实展厅与同行者','沉浸复原：在遗址节点进入历史场景','共享运营：快速消毒、模块维护、内容可更新','文化转译：建筑、声景、人物故事形成任务线'],GOLD)]
    c += [f'<circle cx="1780" cy="1030" r="270" fill="#E0F1EC" stroke="{TEAL}" stroke-width="12"/>',text(1780,970,'核心策略',52,INK,800,'middle'),text(1780,1040,'双态切换',72,TEAL,800,'middle'),text(1780,1100,'开放导览 × 沉浸复原',30,GREY,500,'middle')]
    for x,y,t,b in [(1450,1510,'① 到馆领用','票务绑定 / 选择路线'),(2000,1510,'② 识别遗址','空间定位 / AR 导航'),(2550,1510,'③ 历史复原','翻下遮光镜片 / 进入场景'),(3100,1510,'④ 完成任务','获得数字印章 / 生成纪念')]:
        c += [f'<circle cx="{x}" cy="{y}" r="155" fill="#fff" stroke="{TEAL}" stroke-width="10"/>',text(x,y-10,t,33,INK,800,'middle'),text(x,y+46,b,25,GREY,400,'middle')]
    c += [arrow(1610,1510,1820,1510),arrow(2160,1510,2370,1510),arrow(2710,1510,2920,1510)]
    c += [box(1370,1890,1330,680,'体验闭环：用户动作 → 产品反馈',['01 凝视 / 手势框选展品 → 弹出构件信息','02 翻转镜片 → 古镇建筑与生活场景 1:1 复原','03 耳挂定向声场 → 听见粤语市集、非遗工艺声','04 完成任务 → 数字纪念卡 + 文创兑换券'],TEAL)]
    c += [box(2780,1890,1980,680,'商业闭环：一次设备，多次内容运营',['B 端：展馆采购 + 内容年度订阅 + 设备维护服务','C 端：门票联动 / 限时租赁 / 夜游专题 / 研学套装','传播：AI 生成“我的古镇漫游卡” → 社交分享 → 再访','数据：热点展项、路线停留、设备状态 → 后台优化','可复制：硬件平台不变，替换不同古镇的数字内容包'],RED)]
    c += [text(4100,970,'评分抓手',36,INK,800), text(4100,1030,'产品 40%',45,TEAL,800),text(4100,1100,'系统 40%',45,RED,800),text(4100,1170,'原理 10% · 完成度 10%',32,GREY,600)]
    return replace(s,"".join(c))

def sketch():
    s=doc('02 / 设计草图推演', '从形态探索到最终方案：每一笔都对应一个明确的使用问题')
    c=[]
    c += [text(190,620,'A. 形态方向',42,INK,800), text(190,675,'“轻薄、开放、可共享”的展馆眼镜',30,GREY)]
    # four thumbnail concept frames
    for i,(x,name,desc,accent) in enumerate([(190,'01 折叠护目','交通收纳',GREY),(950,'02 环抱头带','重量平衡',GOLD),(1710,'03 翻转镜片','开放 / 沉浸',TEAL),(2470,'04 耳挂模块','定向声场',RED)]):
        c += [f'<rect x="{x}" y="730" width="650" height="650" rx="30" fill="#fff" stroke="{LINE}" stroke-width="5"/>',tag(x+30,800,name,accent),f'<path d="M{x+100} 1100 Q{x+300} 860 {x+540} 1010 L{x+570} 1210 Q{x+330} 1320 {x+120} 1200Z" fill="none" stroke="{INK}" stroke-width="15"/>',f'<path d="M{x+130} 1025 Q{x+300} 870 {x+540} 1010" fill="none" stroke="{accent}" stroke-width="45" stroke-linecap="round"/>',text(x+45,1325,desc,30,GREY,600)]
    c += [text(3400,620,'B. 核心创新草图',42,INK,800), text(3400,675,'“双态翻转镜片”使展馆行走更安全',30,GREY)]
    c += [f'<rect x="3370" y="730" width="1380" height="650" rx="30" fill="#EAF5F1" stroke="{TEAL}" stroke-width="7"/>']
    c += [headset(3640,1030,.55),arrow(3850,1030,4420,1030,RED),f'<path d="M4300 980 q160 -180 320 0 l-25 260 q-150 70 -290 -5z" fill="#152B33" stroke="{INK}" stroke-width="10"/>',text(3610,1305,'开放导览',32,TEAL,800),text(4300,1305,'沉浸复原',32,RED,800)]
    c += [f'<rect x="180" y="1500" width="2350" height="1550" rx="34" fill="#fff" stroke="{INK}" stroke-width="6"/>',text(230,1585,'C. 选定方案：岭境 LingJing',55,INK,800),text(230,1640,'轻量化混合现实文化眼镜 · 展馆共享使用',31,GREY)]
    c += [headset(1250,2200,1.18),tag(270,2880,'01 半透镜片',TEAL),tag(890,3000,'02 磁吸卫生面罩',RED),tag(1540,2830,'03 定向声场耳挂',GOLD)]
    c += [f'<rect x="2630" y="1500" width="2120" height="1550" rx="34" fill="#fff" stroke="{INK}" stroke-width="6"/>',text(2680,1585,'D. 草图必须说清楚的 4 件事',55,INK,800)]
    for i,(title,detail,color) in enumerate([('佩戴','后置软垫平衡重量',TEAL),('翻转','遮光镜片进入历史复原',RED),('卫生','一客一换亲肤面罩',GOLD),('维护','磁吸模块便于消毒与检修',NAVY)]):
        yy=1715+i*285
        c += [f'<circle cx="2740" cy="{yy}" r="48" fill="{color}"/>',text(2820,yy-10,title,44,INK,800),text(2820,yy+42,detail,31,GREY)]
    c += [text(180,3200,'草图表现提示：外轮廓最重 → 结构线次之 → 辅助线最轻；青绿强调“文化科技”，朱砂红只标注关键交互。',34,INK,600)]
    return replace(s,"".join(c))

def main():
    s=doc('03 / 主体物与体验系统', '“岭境”双态文化眼镜｜外观、结构、UI、情景与工作原理一页讲清')
    c=[]
    c += [f'<rect x="180" y="590" width="2700" height="2210" rx="38" fill="#fff" stroke="{INK}" stroke-width="7"/>',tag(230,675,'主效果图｜45°佩戴视角',NAVY),headset(1450,1530,1.65)]
    c += [arrow(1450,1300,1290,960,TEAL),text(1060,900,'翻转式遮光镜片',35,INK,800),text(1060,946,'开放导览 ↔ 沉浸复原',27,GREY)]
    c += [arrow(1990,1620,2300,1520,RED),text(2300,1455,'磁吸卫生面罩',35,INK,800),text(2300,1501,'可替换 / 可消毒',27,GREY)]
    c += [arrow(900,1060,750,770,GOLD),text(470,720,'环抱式头带',35,INK,800),text(470,766,'软垫配重 · 适配头围',27,GREY)]
    c += [f'<rect x="2980" y="590" width="1780" height="800" rx="34" fill="#fff" stroke="{INK}" stroke-width="7"/>',text(3030,675,'三视图与 CMF',48,INK,800)]
    # simple 3views
    for x,lab in [(3110,'正视图'),(3650,'侧视图'),(4200,'后视图')]:
        c += [f'<rect x="{x}" y="760" width="400" height="350" rx="85" fill="#E7ECE9" stroke="{INK}" stroke-width="10"/>',f'<rect x="{x+50}" y="850" width="300" height="150" rx="60" fill="#152B33"/>',text(x+200,1190,lab,30,INK,700,'middle')]
    c += [text(3040,1300,'CMF：岭南青绿 / 暖白 / 石墨灰 / 朱砂红',29,GREY,600)]
    c += [f'<rect x="2980" y="1460" width="1780" height="1340" rx="34" fill="#fff" stroke="{INK}" stroke-width="7"/>',text(3030,1545,'交互、情景与原理',48,INK,800)]
    # UI flow
    for i,(label,sub) in enumerate([('01 绑定','票务 / 路线'),('02 识别','凝视展品'),('03 复原','翻下镜片'),('04 奖励','数字印章')]):
        x=3040+i*415
        c += [f'<rect x="{x}" y="1630" width="330" height="330" rx="35" fill="#EAF5F1" stroke="{TEAL}" stroke-width="6"/>',text(x+165,1740,label,28,INK,800,'middle'),text(x+165,1800,sub,23,GREY,500,'middle'),f'<circle cx="{x+165}" cy="1890" r="32" fill="{TEAL}"/>']
        if i<3:c += [arrow(x+345,1795,x+395,1795)]
    c += [f'<path d="M3070 2190 H4620" stroke="{LINE}" stroke-width="5"/>',text(3040,2280,'工作原理',34,INK,800)]
    c += [text(3060,2350,'遗址 / 展品',27,GREY,700),arrow(3260,2340,3400,2340),text(3420,2350,'空间识别',27,GREY,700),arrow(3580,2340,3720,2340),text(3740,2350,'内容引擎',27,GREY,700),arrow(3900,2340,4040,2340),text(4060,2350,'镜片 + 声场',27,GREY,700)]
    c += [box(3040,2470,1620,240,'商业价值',['设备租赁 · 夜游专题 · 研学包 · 文创兑换 · 内容订阅'],RED)]
    c += [f'<rect x="180" y="2880" width="4580" height="300" rx="34" fill="{NAVY}"/>',text(250,2985,'核心价值',42,"#fff",800),text(250,3055,'让遗址“可看见”、历史“可进入”、文化“可带走”；硬件平台可复用，内容可随不同广东古镇持续更新。',34,"#DCEBE7",500)]
    return replace(s,"".join(c))

def main_write():
    OUT.mkdir(parents=True, exist_ok=True)
    boards=[('01-design-analysis.svg',analysis()),('02-design-sketches.svg',sketch()),('03-product-system.svg',main())]
    for name,data in boards: (OUT/name).write_text(data,encoding='utf-8')
    (OUT/'README.md').write_text('''# 岭境 A3 学习示意图\n\n三张文件均为 **A3 横版（420 × 297 mm）SVG**，按 300 dpi 的 4961 × 3508 画布制作，可直接在浏览器、Illustrator、Inkscape 或 Affinity Designer 中打开、打印或导出 PDF/PNG。\n\n- `01-design-analysis.svg`：题目分析、用户痛点、体验与商业闭环。\n- `02-design-sketches.svg`：形态推演、关键创新与草图表达要点。\n- `03-product-system.svg`：主体产品、三视图、UI、场景与工作原理。\n- `index.html`：三页缩略预览和逐页打开入口。\n\n## 推荐阅读顺序\n\n1. 第 1 页先回答“为什么设计”：用户、痛点、设计目标与商业闭环。\n2. 第 2 页回答“方案如何形成”：四条形态路线、核心创新与最终取舍。\n3. 第 3 页回答“产品如何工作”：主体造型、结构、UI、原理和市场价值。\n\n设计对象为原创概念“岭境 LingJing”双态文化眼镜；参考图仅用于理解轻量化混合现实眼镜的产品类别，不复刻其外观。\n''',encoding='utf-8')
    (OUT/'index.html').write_text('''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>岭境 A3 学习示意图</title><style>body{margin:0;background:#102b36;color:#fff;font-family:system-ui,"Microsoft YaHei",sans-serif}header{padding:32px max(4vw,24px)}h1{margin:0 0 8px}.grid{display:grid;gap:28px;padding:0 max(4vw,24px) 50px}.card{background:#fff;border-radius:14px;overflow:hidden;box-shadow:0 15px 50px #0006}.card h2{color:#102b36;margin:0;padding:18px 24px}.card a{display:block}.card img{display:block;width:100%;height:auto;border-top:1px solid #dfe6e3}</style></head><body><header><h1>岭境 LingJing｜广工 963 A3 示意图</h1><div>点击任意画板可单独打开原尺寸 SVG。</div></header><main class="grid"><section class="card"><h2>01｜设计分析</h2><a href="01-design-analysis.svg"><img src="01-design-analysis.svg" alt="设计分析 A3"></a></section><section class="card"><h2>02｜设计草图</h2><a href="02-design-sketches.svg"><img src="02-design-sketches.svg" alt="设计草图 A3"></a></section><section class="card"><h2>03｜主体物与体验系统</h2><a href="03-product-system.svg"><img src="03-product-system.svg" alt="主体物 A3"></a></section></main></body></html>''',encoding='utf-8')

if __name__ == '__main__': main_write()
