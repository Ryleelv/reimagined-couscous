# test-results — 人物模型

- 当前状态：结构校验通过，未做独立 agent 盲测。
- 原因：缺少原文文本，不能判断 R/A1/B 是否符合书内证据。
- 测试集：`test-prompts.json` 已按 darwin 兼容对象格式提供 should_trigger、should_not_trigger、edge_case。
- 后续：补齐原文并重做三重验证后，再执行盲测并记录通过率。
