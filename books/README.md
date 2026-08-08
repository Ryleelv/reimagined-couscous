# 337 工业设计工程书目蒸馏

本目录按 cangjie-skill 的 RIA-TV++ 思路整理 337 工业设计工程复习书目：先做整书理解，再抽取可调用的方法论单元，最后形成可背诵、可迁移、可用于答题的 skill 化知识库。

## 当前状态

- 《交互设计精髓》：已完成 337 复习版草稿，但尚未接入原书文本，因此未标记为正式 cangjie verified。
- 其他书目：已建立待整理管线，等待目标院校大纲、原书文本或讲义。
- 材料需求：见 [SOURCE_REQUEST.md](./SOURCE_REQUEST.md)。

## 当前采用的书目口径

由于“337 工业设计工程”因学校不同而书目不同，本仓库先以常见且与用户明确提到的《交互设计精髓》相关的广东工业大学口径作为第一批整理对象，并保留可替换清单：

1. 柳冠中：《设计方法论》
2. 尹定邦、邵宏：《设计学概论》
3. 王受之：《世界现代设计史》
4. Alan Cooper 等：《About Face / 交互设计精髓》

> 注：公开页面中也存在不同年份或不同机构的 337 书目差异；如果目标院校不是广东工业大学，应以目标院校当年招生目录和考试大纲为准。

## 整理方式

每本书建立一个目录：

```text
books/<book-slug>/
├── PIPELINE_STATE.md
├── BOOK_OVERVIEW.md
├── verified.md
├── INDEX.md
├── GLOSSARY.md
├── DIGEST.md
├── candidates/
├── rejected/
└── <skill-slug>/
    ├── SKILL.md
    ├── test-prompts.json
    └── test-results.md
```

## 使用建议

- 考前第一轮：读 `BOOK_OVERVIEW.md` 建立框架。
- 考前第二轮：背 `INDEX.md` 和 `GLOSSARY.md`。
- 考前第三轮：用每个 skill 的 `test-prompts.json` 练习名词解释、简答、论述和案例题。
- 冲刺阶段：只读 `DIGEST.md`，把方法论迁移到智能硬件、服务设计、公共终端、医疗健康、校园产品等案例中。
