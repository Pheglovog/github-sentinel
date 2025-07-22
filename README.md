# GitHub Sentinel 🔍

**GitHub Sentinel** 是一款开源工具类 AI Agent，专为开发者和项目管理人员设计，能够定期（每日/每周/每月）自动获取并汇总订阅的 GitHub 仓库最新动态。

## 🚀 主要功能

- **📋 订阅管理**: 轻松订阅和管理感兴趣的 GitHub 仓库
- **🔄 自动更新获取**: 定期获取仓库的最新提交、PR、Issues 和发布信息
- **📱 多渠道通知**: 支持邮件、Slack、Discord、Webhook 等通知方式
- **📊 智能报告生成**: 生成 Markdown、HTML、JSON 等格式的活动报告
- **⏰ 灵活的调度系统**: 支持每日、每周、每月的定时监控
- **🎯 精准过滤**: 可配置监控特定类型的活动（提交、PR、Issues、发布等）

## 📦 安装

### 环境要求

- Python 3.10+
- Git

### 使用 uv 安装（推荐）

```bash
# 克隆项目
git clone https://github.com/your-username/github-sentinel.git
cd github-sentinel

# 使用 uv 创建虚拟环境并安装依赖
uv sync

# 激活虚拟环境
source .venv/bin/activate  # Linux/macOS
# 或者直接使用 uv run
```

### 使用 pip 安装

```bash
# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/macOS
# venv\Scripts\activate  # Windows

# 安装依赖
pip install -e .
```

## ⚙️ 配置

### 1. 环境变量配置

创建 `.env` 文件：

```bash
# GitHub API 配置
GITHUB_TOKEN=your_github_personal_access_token

# 数据库配置
DATABASE_URL=sqlite:///github_sentinel.db

# 通知配置
SMTP_HOST=smtp.gmail.com
SMTP_USERNAME=your_email@gmail.com
SMTP_PASSWORD=your_app_password

# 日志配置
LOG_LEVEL=INFO
LOG_FILE=logs/github_sentinel.log
```

### 2. 获取 GitHub Token

1. 访问 [GitHub Settings > Developer settings > Personal access tokens](https://github.com/settings/tokens)
2. 点击 "Generate new token"
3. 选择必要的权限：
   - `repo` - 访问仓库信息
   - `user` - 访问用户信息
4. 复制生成的 token 到 `.env` 文件中

## 🔧 使用方法

### 初始化用户

```bash
github-sentinel init -u your_username -e your_email@example.com -t your_github_token
```

### 订阅仓库

```bash
# 订阅单个仓库
github-sentinel subscribe -u 1 -r owner/repo

# 指定通知频率和渠道
github-sentinel subscribe -u 1 -r microsoft/vscode -f weekly -ch email -ch slack
```

### 查看订阅

```bash
github-sentinel list-subscriptions -u 1
```

### 分析仓库活动

```bash
# 分析最近7天的活动
github-sentinel analyze -r microsoft/vscode

# 分析最近30天的活动
github-sentinel analyze -r microsoft/vscode -d 30
```

### 处理订阅并生成报告

```bash
# 处理每日订阅
github-sentinel process -f daily

# 处理每周订阅
github-sentinel process -f weekly
```

### 查看状态

```bash
github-sentinel status
```

### 取消订阅

```bash
github-sentinel unsubscribe -s subscription_id
```

## 📁 项目结构

```
github-sentinel/
├── src/github_sentinel/
│   ├── __init__.py
│   ├── core/                    # 核心模块
│   │   ├── models.py           # 数据模型
│   │   ├── config.py           # 配置管理
│   │   └── exceptions.py       # 异常定义
│   ├── services/               # 业务逻辑层
│   │   ├── github_service.py   # GitHub API 服务
│   │   ├── subscription_service.py  # 订阅管理
│   │   ├── notification_service.py  # 通知服务
│   │   ├── report_service.py   # 报告生成
│   │   └── scheduler_service.py     # 任务调度
│   ├── database/               # 数据访问层
│   │   ├── connection.py       # 数据库连接
│   │   └── repositories.py     # 数据仓库
│   ├── cli/                    # 命令行界面
│   │   └── commands.py         # CLI 命令
│   └── utils/                  # 工具函数
│       ├── logger.py          # 日志工具
│       └── helpers.py         # 辅助函数
├── tests/                      # 测试文件
├── pyproject.toml             # 项目配置
└── README.md                  # 项目说明
```

## 🛠️ 开发

### 安装开发依赖

```bash
uv add --dev pytest black flake8 mypy
```

### 运行测试

```bash
pytest
```

### 代码格式化

```bash
black src/
```

### 类型检查

```bash
mypy src/
```

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

1. Fork 项目
2. 创建功能分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'Add some amazing feature'`)
4. 推送分支 (`git push origin feature/amazing-feature`)
5. 创建 Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 🙋‍♂️ 支持

如有问题，请：

1. 查看 [Issues](https://github.com/your-username/github-sentinel/issues)
2. 创建新的 Issue
3. 联系维护者

## 🎯 路线图

- [ ] Web 界面支持
- [ ] 更多通知渠道（钉钉、企业微信等）
- [ ] AI 生成的智能报告摘要
- [ ] 仓库健康度评分
- [ ] 团队协作功能
- [ ] 报告模板自定义
- [ ] 数据可视化图表

---

**GitHub Sentinel** - 让仓库监控变得简单高效！ 🚀
