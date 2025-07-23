# GitHub Sentinel 报告生成指南

本指南总结了如何使用GitHub Sentinel项目来监控GitHub仓库并生成分析报告的完整流程。

## 🚀 快速开始

### 1. 环境准备

```bash
# 进入项目目录
cd /path/to/agent-hub

# 激活虚拟环境
source .venv/bin/activate

# 加载环境变量 (包含GITHUB_TOKEN)
source ~/.zshrc

# 安装依赖
uv sync

# 创建必要目录
mkdir -p reports logs
```

### 2. 验证配置

```bash
# 检查项目状态和配置
python main.py status
```

预期输出应包含：
- ✓ GitHub API connection successful
- Token: ***OczX (显示token后4位)

## 📊 报告生成流程

### 第一步：初始化用户

```bash
# 创建用户账户
python main.py init -u github_user -e user@example.com -t $GITHUB_TOKEN
```

成功后会显示：
```
User 'github_user' created successfully!
User ID: 1
```

### 第二步：订阅仓库

```bash
# 订阅要监控的仓库
python main.py subscribe -u 1 -r langchain-ai/langchain

# 也可以订阅其他仓库，例如：
# python main.py subscribe -u 1 -r microsoft/vscode
# python main.py subscribe -u 1 -r facebook/react
```

成功后会显示：
```
Successfully subscribed to langchain-ai/langchain
Subscription ID: 1
Frequency: daily
Channels: email
```

### 第三步：生成分析报告

```bash
# 分析最近7天的活动
python main.py analyze -r langchain-ai/langchain -d 7

# 分析最近30天的活动
python main.py analyze -r langchain-ai/langchain -d 30

# 将报告输出到文件
python main.py analyze -r langchain-ai/langchain -d 30 > reports/langchain_30days.txt
```

### 第四步：批量处理订阅

```bash
# 处理所有日订阅
python main.py process -f daily

# 处理所有周订阅
python main.py process -f weekly

# 处理所有月订阅
python main.py process -f monthly
```

## 🛠️ 常用命令详解

### 用户管理
```bash
# 初始化用户
python main.py init -u <username> -e <email> -t <github_token>
```

### 订阅管理
```bash
# 订阅仓库
python main.py subscribe -u <user_id> -r <owner/repo>

# 列出用户的所有订阅
python main.py list-subscriptions -u <user_id>

# 取消订阅
python main.py unsubscribe -u <user_id> -r <owner/repo>
```

### 分析和报告
```bash
# 基本分析
python main.py analyze -r <owner/repo> -d <days>

# 示例：分析不同时间范围
python main.py analyze -r langchain-ai/langchain -d 1    # 昨天
python main.py analyze -r langchain-ai/langchain -d 7    # 最近一周  
python main.py analyze -r langchain-ai/langchain -d 30   # 最近一月
python main.py analyze -r langchain-ai/langchain -d 90   # 最近三月
```

### 系统状态
```bash
# 检查系统状态
python main.py status

# 查看帮助
python main.py --help
python main.py <command> --help
```

## 📋 实际生成报告示例

以下是我们成功生成langchain-ai/langchain仓库报告的完整命令序列：

```bash
# 1. 环境准备
source ~/.zshrc
mkdir -p reports logs

# 2. 检查配置
python main.py status

# 3. 初始化用户
python main.py init -u github_user -e user@example.com -t $GITHUB_TOKEN

# 4. 订阅仓库
python main.py subscribe -u 1 -r langchain-ai/langchain

# 5. 生成分析报告
python main.py analyze -r langchain-ai/langchain -d 7

# 6. 处理订阅
python main.py process -f daily
```

## 📈 报告输出样例

运行 `python main.py analyze -r langchain-ai/langchain -d 7` 会得到：

```
=== Repository: langchain-ai/langchain ===
Description: 🦜🔗 Build context-aware reasoning applications
Language: Jupyter Notebook
Stars: 112058
Forks: 18267
Open Issues: 265

=== Activity Summary (7 days) ===
Commits: 50
Pull Requests: 0
Issues: 25
Releases: 9

=== Recent Commits ===
• 0f39155f - docs: Specify environment variables for BedrockConverse...
• 6aeda24a - docs(chroma): update feature table...
...

=== Recent Issues ===
• #32195 - QdrantVectorStore cannot be used in a truly async form...
...

=== Recent Releases ===
• langchain-xai==0.2.5 - langchain-xai==0.2.5 (2025-07-22)
...
```

## 🎯 最佳实践

### 1. 定期监控
```bash
# 每日检查重要仓库
python main.py analyze -r langchain-ai/langchain -d 1
python main.py analyze -r microsoft/vscode -d 1
```

### 2. 保存报告
```bash
# 创建带时间戳的报告
python main.py analyze -r langchain-ai/langchain -d 7 > "reports/langchain_$(date +%Y%m%d).txt"
```

### 3. 批量分析
```bash
# 分析多个仓库的脚本示例
repos=("langchain-ai/langchain" "microsoft/vscode" "facebook/react")
for repo in "${repos[@]}"; do
    echo "Analyzing $repo..."
    python main.py analyze -r "$repo" -d 7 > "reports/${repo//\//_}_$(date +%Y%m%d).txt"
done
```

## 🔧 故障排除

### 常见问题

1. **"Missing required settings: GITHUB_TOKEN"**
   ```bash
   # 确保设置了GitHub Token
   echo $GITHUB_TOKEN
   source ~/.zshrc
   ```

2. **"can't compare offset-naive and offset-aware datetimes"**
   ```bash
   # 这个问题已在项目中修复，确保使用最新代码
   ```

3. **GitHub API限制**
   ```bash
   # 检查API限制状态
   curl -H "Authorization: token $GITHUB_TOKEN" https://api.github.com/rate_limit
   ```

### 日志查看
```bash
# 查看应用日志
tail -f logs/github_sentinel.log

# 查看详细错误
python main.py analyze -r owner/repo -d 7 --debug
```

## 📁 输出文件结构

```
reports/
├── langchain_activity_report.md    # 详细分析报告 (Markdown格式)
├── langchain_activity_report.txt   # 原始命令输出
└── <repo_name>_<date>.txt          # 自定义报告文件
```

---

**提示**: 确保在运行命令前已正确配置GitHub Personal Access Token，并具有足够的API请求配额。

*最后更新: 2025-07-23* 