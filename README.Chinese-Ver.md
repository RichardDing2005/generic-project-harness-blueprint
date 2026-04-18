# 通用项目 Harness 蓝图

这是一套干净、可直接发布的蓝图，适用于需要稳定控制内核、显式工作流阶段、结构化记忆以及可控遗忘机制的长周期项目。

本仓库采用**以内核为中心的 harness 模型**：

- `AGENTS.md` 定义始终生效的运行时协议
- `PIPELINE.md` 定义项目工作流及各阶段语义
- `state/` 存储当前执行指针
- `memory/` 存储有价值的历史证据
- `garbage/` 存储已退役的噪声和被替代的产物
- `config/` 存储阶段默认配置与运行阈值

该蓝图同时支持：

- 从空白项目开始的**全新启动**
- 针对已经包含代码、输出结果和部分历史记录项目的**改造接入**

## 设计目标

1. 让控制逻辑保持集中且显式。
2. 支持可重启的多轮迭代工作。
3. 通过稳定锚点，使工作流阶段可被机器定位。
4. 通过快照与退役机制防止上下文膨胀。
5. 在不保留全部原始噪声的前提下，保留有价值的失败经验。
6. 保持仓库足够整洁，可直接对外公开发布。

## 仓库结构

```text
generic-project-harness-blueprint/
├── README.md
├── LICENSE
├── AGENTS.md
├── PIPELINE.md
├── CONTRIBUTIONS.md
├── docs/
│   ├── ARCHITECTURE.md
│   ├── EXECUTION_PROTOCOL.md
│   ├── MEMORY_POLICY.md
│   ├── GARBAGE_POLICY.md
│   ├── ADOPTION_GUIDE.md
│   └── OPTIMIZATION_NOTES.md
├── state/
│   ├── README.md
│   ├── CURRENT_STATE.json
│   └── CURRENT_STATE.example.json
├── memory/
│   ├── README.md
│   ├── index.json
│   ├── index.example.json
│   ├── active/
│   │   ├── events/
│   │   │   └── MEM-EXAMPLE-0001.example.md
│   │   └── snapshots/
│   │       └── SNAPSHOT-primary_iteration-0001.example.md
│   └── templates/
│       ├── memory_event.template.md
│       └── memory_snapshot.template.md
├── garbage/
│   ├── README.md
│   ├── index.json
│   ├── index.example.json
│   └── records/
│       └── GARBAGE-EXAMPLE-0001.example.md
├── schemas/
│   ├── current_state.schema.json
│   ├── memory_index.schema.json
│   ├── memory_event.schema.json
│   ├── memory_snapshot.schema.json
│   └── garbage_index.schema.json
├── config/
│   ├── stage_defaults.json
│   └── stage_defaults.example.json
├── scripts/
│   ├── extract_pipeline_anchors.py
│   ├── validate_state.py
│   ├── garbage_collect.py
│   └── init_project.py
└── examples/
    └── generic_project/
        ├── CURRENT_STATE.example.json
        ├── pipeline_anchor_map.example.json
        ├── memory_event.example.md
        └── garbage_record.example.md
```

## 快速开始

### 全新启动

1. 阅读 `AGENTS.md`。
2. 如有需要，初始化运行时文件：

```bash
python scripts/init_project.py --project-name <your_project_name>
```

3. 打开 `state/CURRENT_STATE.json`。
4. 根据 `PIPELINE.md` 解析 state 中记录的锚点。
5. 读取 `required_config_refs` 中列出的配置文件。
6. 如果存在快照，则与 state 中指定的 event refs 一并加载。
7. 检查所需产物。
8. 按照当前激活阶段及其子流程规则执行。
9. 回写 state、memory，以及可选的 garbage 记录。

### 改造接入

1. 将本蓝图文件加入现有仓库。
2. 运行 `scripts/init_project.py`。
3. 重写 `PIPELINE.md`，使阶段规则与真实项目一致。
4. 将有价值的历史知识整理并提升到 `memory/`。
5. 仅在相关经验教训已被保留后，再将过时的原始材料退役到 `garbage/`。

## 为什么没有强制性的外层循环 skill

如果一条控制规则满足以下条件：

- 始终生效，
- 具有项目特异性，
- 并且在每次运行中都必须执行，

那么它应当写入 `AGENTS.md`，而不是放入按需懒加载的 skill 中。

后续仍然可以为高负载、可复用、且不属于核心控制逻辑的操作，额外添加可选 skill。
