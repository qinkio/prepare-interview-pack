# prepare-interview-pack

一个面向真实求职场景、兼容 Codex 与 WorkBuddy 的面试准备 Skill。它会结合岗位 JD、个人简历、项目资产、面试时间和面试轮次，生成有证据、可直接开口练习的完整面试作战手册。

它不只做 JD 摘要，而是从招聘方第一印象开始，识别岗位真正想验证的问题，再用候选人的真实项目证据生成自我介绍、项目故事、高概率问答、风险回答和临场复习计划。

## 核心能力

- 模拟 HR 与业务主管的简历快速扫描，提炼第一印象和三个关键验证风险。
- 拆解岗位使命、业务结果、硬性要求、隐性约束和五项核心能力。
- 使用 STARS 模型分析母公司、业务单元和岗位所处阶段。
- 将候选人经历区分为强匹配、可迁移和真实缺口。
- 对简历中的每个命名项目建立覆盖清单，逐项标记 P0、P1、P2 或 Excluded，防止相关项目因指标不完整而被静默遗漏。
- 根据岗位直接性、个人所有权和结果可信度选择主项目与备用项目。
- 生成 60 秒、90 秒自我介绍和可直接口述的项目故事。
- 生成至少 10～12 道高概率面试问题及完整回答。
- 针对 HR、业务主管、跨部门面试和终面调整问题重点。
- 根据剩余时间自动切换 Sprint、Standard 或 Deep 模式。
- 生成“临场作战卡＋完整手册”的双层文档。
- 在面试不足 24 小时、用户主动要求或完整手册过长时，生成独立的“面试前 30 分钟速背卡”。
- 严格区分个人贡献、团队结果、事实、推断和待确认信息。
- 隔离口述稿、记忆提示和分析附录，避免把“简历记录”“资料显示”等编辑语言写进口述答案。
- 支持 Markdown 输出，并能按宿主现有连接器发布到 Notion、腾讯文档等服务。
- 提供自动检查脚本，防止遗漏关键章节、重复大章节和口述语言泄漏。
- 自动探测宿主能力；缺少联网、发布连接器或 Python 时提供安全降级路径。

## 适合的场景

- 已经拿到一个具体岗位 JD，需要系统准备面试。
- 希望结合自己的简历和项目资料预测面试重点。
- 面试临近，需要明确先背什么、后看什么。
- 工作经历与岗位相邻，但存在行业、管理、预算或业务所有权缺口。
- 希望把多次面试准备统一成可复用流程。

不适合单独用于简历重写、求职信、Offer 评估、职位搜索或面试后感谢信。

## 安装到 Codex

```bash
git clone https://github.com/qinkio/prepare-interview-pack.git
mkdir -p ~/.codex/skills
cp -R prepare-interview-pack/prepare-interview-pack ~/.codex/skills/
```

安装完成后，重新打开 Codex 或开始一个新任务，即可使用 `$prepare-interview-pack`。

## 安装到 WorkBuddy

WorkBuddy 支持上传本地技能包。最简单的方式是直接下载仓库中预先构建的技能包：

[下载 prepare-interview-pack-workbuddy.zip](https://github.com/qinkio/prepare-interview-pack/raw/main/dist/prepare-interview-pack-workbuddy.zip)

然后在 WorkBuddy 中执行：

1. 打开左侧的“专家·技能·连接器”；
2. 选择“添加技能”→“上传技能”；
3. 上传 `prepare-interview-pack-workbuddy.zip`；
4. 启用技能，新建对话并用自然语言描述面试准备任务。

也可以安装为本地用户技能：

```bash
mkdir -p ~/.workbuddy/skills
cp -R prepare-interview-pack/prepare-interview-pack ~/.workbuddy/skills/
```

WorkBuddy 不需要使用 `$prepare-interview-pack`。直接输入“结合这份 JD 和简历，生成完整面试手册”即可触发。若没有联网、文档连接器或 Python 执行能力，Skill 会保留核心分析与答案库，并改用人工核验和 Markdown 交付。

### 重新构建 WorkBuddy 技能包

仓库维护者修改 Skill 后可运行：

```bash
python3 tools/build_workbuddy_package.py
```

生成的 ZIP 以 `SKILL.md` 为包根目录，不包含 Codex 专属的 `agents/openai.yaml`。

## 使用方法

准备以下信息：

1. 完整岗位 JD；
2. 当前简历；
3. 可选的项目资料或职业资产库；
4. 面试时间；
5. 面试轮次，例如 HR、业务主管、交叉面或终面；
6. 希望输出到 Markdown，还是发布到当前宿主已连接的文档服务。

示例：

```text
使用 $prepare-interview-pack，结合这份 JD、我的简历和项目资料，
为明天下午的业务主管一面生成完整面试手册，并标注先背什么、后看什么。
```

在 WorkBuddy 中可直接说：

```text
结合这份 JD、我的简历和项目资料，为明天下午的业务主管一面生成完整面试手册，
先做招聘方 10 秒扫描，再标注先背什么、后看什么；没有证据的内容不要编造。
```

也可以继续进行模拟面试：

```text
使用刚才的手册，从最高概率问题开始逐题问我。
根据相关性、清晰度、可信度、个人贡献边界和表达效果评分并修改答案。
```

## 输出结构

### 临场作战卡

放在文档最前面，包含：

- 面试快照与练习安排；
- 招聘方第一印象与三个验证风险；
- 一句话岗位定位和个人定位；
- 60 秒自我介绍；
- 主项目与备用项目记忆卡；
- 核心缺口回答；
- 五道 P0 问题；
- 三个反问；
- 最后事实卡。

### 完整面试手册

包含 JD 分析、STARS 公司地图、梦想候选人画像、能力与经历映射、完整项目故事、10～12 道高概率问题、文化匹配表达、领域知识和事实边界。

### 面试前 30 分钟速背卡

在面试临近或手册较长时额外生成，包含 30 分钟练习顺序、60 秒自我介绍、主项目与备用项目、三个核心缺口、五道 P0、三个反问和五条事实红线。速背卡是完整手册的配套入口，不会替代完整答案库。

发布到支持关联页面的文档服务时，速背卡会作为子页或关联页，并从完整手册顶部进入。

## 时间模式

| 模式 | 距离面试时间 | 重点 |
| --- | --- | --- |
| Sprint | 少于 24 小时 | 保留完整答案库，但优先生成可立即练习的作战卡 |
| Standard | 1～3 天或时间未知 | 完整手册、公司分析和面试追问 |
| Deep | 超过 3 天 | 深入公司研究、多轮面试策略和扩展案例 |

## 事实安全机制

Skill 会为重要信息标记状态：

- `Verified`：有材料支持，可以直接使用；
- `Candidate-confirmed`：候选人本人明确确认、且口径与使用边界完整的事实；在职业资产库标记为 `user-confirmed` 时可包括历史数字结果；
- `Derived-safe`：从事实谨慎提炼的方法、判断或未来行动；
- `Confirm`：需要候选人确认；
- `Conflict`：不同材料存在冲突；
- `Inference`：分析推断，不是候选人事实；
- `Do not use`：不应在面试中使用。

数字结果、历史所有权和过去业务成果必须有文档证据，或由候选人在口径、周期、群体、贡献边界和发布权限完整的前提下明确确认。团队结果不会自动被包装成个人成果，相邻经验也不会被包装成直接经验。

## 自动检查

生成 Markdown 手册后，可以运行：

```bash
python3 prepare-interview-pack/scripts/validate_pack.py 面试手册.md --mode sprint --resume-projects 简历项目清单.json
```

生成独立速背卡后，可以运行：

```bash
python3 prepare-interview-pack/scripts/validate_rapid_card.py 面试前30分钟速背卡.md
```

检查器会验证：

- 60 秒和 90 秒自我介绍；
- 公司 STARS 地图；
- 主项目与备用项目；
- 至少 10 道高概率问题；
- 三个面试官反问；
- 文化假设或文化表达；
- 最后事实卡和更新时间；
- P0 内容是否包含证据、追问和安全边界；
- 简历中的每个命名项目是否出现在覆盖清单，并有 P0、P1、P2 或 Excluded 处置；
- 口述稿是否泄漏简历来源或内部证据状态；
- 是否存在重复的大章节；
- 速背卡是否包含 30 分钟流程、两个项目、三个缺口、五道 P0、三个反问和事实红线。

## 目录结构

```text
prepare-interview-pack/
├── README.md
├── dist/
│   └── prepare-interview-pack-workbuddy.zip
├── tools/
│   └── build_workbuddy_package.py
└── prepare-interview-pack/
    ├── SKILL.md
    ├── agents/
    │   └── openai.yaml
    ├── references/
    │   ├── gold-quality-standard.md
    │   ├── output-template.md
    │   ├── quality-checklist.md
    │   ├── rapid-review-card.md
    │   ├── resume-screening-lens.md
    │   └── routing-and-scoring.md
    └── scripts/
        ├── validate_pack.py
        └── validate_rapid_card.py
```

## 隐私说明

仓库只包含 Skill 规则、参考文档和检查脚本，不包含作者的简历、职业资产、面试手册、Notion 页面、公司内部资料或本机路径。

使用时请自行判断上传到模型或第三方服务的资料是否包含个人隐私、商业秘密或受限制信息。

## 当前状态

当前版本已经使用不同类型的真实面试手册进行结构回归，重点解决以下问题：

- 临近面试时答案被过度删减；
- 公司地图和岗位背景被遗漏；
- 选择了表达完整但与岗位不够直接的项目；
- 风险警告过多，压过候选人的优势；
- 文档分析正确，但无法直接开口练习；
- 证据来源和内部状态词泄漏到候选人口述稿；
- 补充内容反复追加，导致章节重复和手册膨胀；
- 完整手册过长，面试前缺少独立的 30 分钟复习入口；
- 连接文档服务发布后缺少回读检查；
- 简历中与 JD 相关的项目因为指标未完全核验而被静默遗漏。

## 跨平台说明

- `SKILL.md`、`references/` 和 `scripts/` 是 Codex 与 WorkBuddy 共用的核心。
- `agents/openai.yaml` 只为 Codex 提供界面元数据，不会被放入 WorkBuddy 上传包。
- Skill 不依赖固定命令名、固定当前目录或某一种文档连接器。
- WorkBuddy 第三方 Skill 会在用户授权范围内读取文件或执行脚本；首次使用建议先用脱敏材料测试，并检查包内脚本。

欢迎根据自己的岗位和面试流程继续迭代。
