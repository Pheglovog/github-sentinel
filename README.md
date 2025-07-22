# GitHub Sentinel 🔍

<div align="center">

![Python Version](https://img.shields.io/badge/python-3.10+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Status](https://img.shields.io/badge/status-active-brightgreen.svg)
![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)

**🤖 Never miss a GitHub update again!**

*An intelligent AI Agent that monitors your GitHub repositories and delivers comprehensive reports to keep you informed of all the action.*

[Quick Start](#-quick-start) • [Features](#-features) • [Installation](#-installation) • [Documentation](#-documentation) • [Contributing](#-contributing)

</div>

---

## 🎯 What is GitHub Sentinel?

**GitHub Sentinel** is a powerful, open-source AI Agent designed for developers, project managers, and open-source enthusiasts who need to stay updated on multiple GitHub repositories without the manual overhead.

### 💡 The Problem
- Manually checking dozens of repositories for updates is time-consuming
- Missing important releases, critical issues, or team contributions
- Lack of consolidated reporting across multiple projects
- No automated way to track repository health and activity trends

### ✨ The Solution
GitHub Sentinel automatically monitors your subscribed repositories and delivers intelligent, formatted reports through your preferred channels - whether that's email, Slack, or custom webhooks.

## 🎬 Quick Demo

```bash
# 1. Subscribe to a repository
github-sentinel subscribe -u 1 -r microsoft/vscode -f weekly

# 2. Analyze recent activity
github-sentinel analyze -r microsoft/vscode -d 7

# 3. Get instant insights
# ✅ 45 commits, 12 PRs, 8 issues, 1 release
# 📊 Full report with contributor stats and trending topics
```

## 🚀 Key Features

### 🔄 **Smart Repository Monitoring**
- **Real-time tracking** of commits, pull requests, issues, and releases
- **Configurable frequencies**: daily, weekly, or monthly updates
- **Intelligent filtering** by event types, contributors, or labels

### 📊 **Comprehensive Reporting**
- **Multiple formats**: Markdown, HTML, JSON for different use cases
- **Rich insights**: Contributor stats, activity trends, and summary analytics
- **Beautiful templates** with emoji-rich, readable formatting

### 🔔 **Multi-Channel Notifications**
- **📧 Email**: SMTP integration with HTML reports
- **💬 Slack**: Rich message formatting with threading
- **🎮 Discord**: Embed-rich notifications for gaming communities  
- **🔗 Webhooks**: Custom integrations with your tools

### 🏗️ **Enterprise-Ready Architecture**
- **Layered design** with clean separation of concerns
- **Repository pattern** for database operations
- **Async operations** for high performance
- **Type-safe** with Pydantic models and comprehensive validation

## 🚀 Quick Start

Get GitHub Sentinel running in under 2 minutes:

### 1️⃣ **Clone & Install**
```bash
git clone https://github.com/your-username/github-sentinel.git
cd github-sentinel

# Using uv (recommended)
uv sync && source .venv/bin/activate

# Or using pip
pip install -e .
```

### 2️⃣ **Get GitHub Token**
1. Go to [GitHub Settings > Personal Access Tokens](https://github.com/settings/tokens)
2. Create a new token with `repo` and `user` permissions
3. Copy the token

### 3️⃣ **Initialize**
```bash
export GITHUB_TOKEN="your_token_here"
github-sentinel init -u your_username -e your_email@example.com -t $GITHUB_TOKEN
```

### 4️⃣ **Start Monitoring**
```bash
# Subscribe to your favorite repositories
github-sentinel subscribe -u 1 -r microsoft/vscode -f daily
github-sentinel subscribe -u 1 -r facebook/react -f weekly

# Get instant analysis
github-sentinel analyze -r microsoft/vscode -d 7
```

🎉 **That's it!** You're now monitoring GitHub repositories like a pro.

## 📦 Installation Options

### 🔧 **Requirements**
- **Python 3.10+** (3.11+ recommended)
- **Git** for version control
- **GitHub Personal Access Token**

### ⚡ **Using uv** (Recommended)
```bash
# Install uv if you haven't already
curl -LsSf https://astral.sh/uv/install.sh | sh

# Clone and setup
git clone https://github.com/your-username/github-sentinel.git
cd github-sentinel
uv sync
```

### 🐍 **Using pip**
```bash
git clone https://github.com/your-username/github-sentinel.git
cd github-sentinel

python -m venv venv
source venv/bin/activate  # Linux/macOS
pip install -e .
```

### 🐳 **Using Docker** (Coming Soon)
```bash
docker run -e GITHUB_TOKEN=your_token github-sentinel:latest
```

## ⚙️ Configuration

### 📄 **Environment Setup**

Create a `.env` file in your project root:

```bash
# Essential Configuration
GITHUB_TOKEN=ghp_your_github_token_here
DATABASE_URL=sqlite:///github_sentinel.db

# Email Notifications (Optional)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your_email@gmail.com  
SMTP_PASSWORD=your_app_password
SMTP_USE_TLS=true

# Slack Integration (Optional)
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/YOUR/SLACK/WEBHOOK

# Discord Integration (Optional)  
DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/YOUR/DISCORD/WEBHOOK

# Advanced Settings
LOG_LEVEL=INFO
LOG_FILE=logs/github_sentinel.log
SCHEDULER_ENABLED=true
```

### 🔑 **GitHub Token Setup**

Your GitHub token needs these permissions:
- `repo` - Access repository information
- `user` - Access user information  
- `notifications` - Read notifications (optional)

**Security Tip**: Use fine-grained tokens when possible and limit scope to specific repositories.

## 💻 Usage Examples

### 🏃 **Common Workflows**

#### Monitor Your Favorite Projects
```bash
# Subscribe to popular repositories  
github-sentinel subscribe -u 1 -r microsoft/vscode -f daily -ch email
github-sentinel subscribe -u 1 -r facebook/react -f weekly -ch slack  
github-sentinel subscribe -u 1 -r python/cpython -f monthly -ch webhook

# Check what you're monitoring
github-sentinel list-subscriptions -u 1
```

#### Get Instant Repository Insights  
```bash
# Analyze any repository's recent activity
github-sentinel analyze -r microsoft/vscode -d 7
github-sentinel analyze -r tensorflow/tensorflow -d 30

# Check system status
github-sentinel status
```

#### Automate Your Workflow
```bash
# Process all daily subscriptions
github-sentinel process -f daily

# Set up in cron job for automation
0 9 * * * /path/to/github-sentinel process -f daily
```

### 📋 **Complete Command Reference**

| Command | Description | Example |
|---------|-------------|---------|
| `init` | Set up your user profile | `github-sentinel init -u john -e john@example.com -t token` |
| `subscribe` | Monitor a repository | `github-sentinel subscribe -u 1 -r owner/repo -f weekly` |
| `list-subscriptions` | View your subscriptions | `github-sentinel list-subscriptions -u 1` |
| `unsubscribe` | Stop monitoring | `github-sentinel unsubscribe -s 1` |
| `analyze` | Get repository insights | `github-sentinel analyze -r owner/repo -d 7` |
| `process` | Generate scheduled reports | `github-sentinel process -f daily` |
| `status` | System health check | `github-sentinel status` |

### 🎛️ **Advanced Options**

```bash
# Custom notification channels
github-sentinel subscribe -u 1 -r owner/repo -ch email -ch slack -ch discord

# Specific monitoring frequency  
github-sentinel subscribe -u 1 -r owner/repo -f weekly  # daily|weekly|monthly

# Extended analysis periods
github-sentinel analyze -r owner/repo -d 90  # Last 90 days
```

## 🏗️ Architecture

GitHub Sentinel follows a clean, layered architecture:

```
📦 github-sentinel/
├── 🧠 src/github_sentinel/
│   ├── 🏛️  core/           # Business models & config  
│   ├── 🔧 services/        # GitHub API, notifications, reports
│   ├── 🗄️  database/       # Data access & ORM models
│   ├── 💻 cli/            # Command-line interface
│   └── 🛠️  utils/          # Logging & helper functions
├── 🧪 tests/              # Unit & integration tests
├── 📋 pyproject.toml      # Project configuration
└── 📖 docs/              # Documentation
```

**Why This Architecture?**
- 🔄 **Separation of Concerns**: Each layer has a single responsibility
- 🧪 **Testability**: Easy to mock and test individual components
- 📈 **Scalability**: Add new features without affecting existing code
- 🔌 **Extensibility**: Plugin-friendly design for custom integrations

## 🛠️ Development

### **Local Development Setup**

```bash  
# Clone the repository
git clone https://github.com/your-username/github-sentinel.git
cd github-sentinel

# Install development dependencies
uv sync --dev

# Run tests
uv run pytest

# Code formatting & linting
uv run black src/ tests/
uv run flake8 src/ tests/
uv run mypy src/

# Run demo script
uv run python demo.py
```

### **Project Structure**
The codebase follows clean architecture principles with clear separation between layers. See [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) for detailed architecture documentation.

---

## 🤝 Contributing

We love contributions! GitHub Sentinel is built by developers, for developers.

### **How to Contribute**

1. 🍴 **Fork** the repository  
2. 🌿 **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. ✨ **Add** your feature with tests
4. 🧪 **Test** thoroughly (`uv run pytest`)  
5. 📝 **Commit** with clear messages (`git commit -m 'Add: amazing feature'`)
6. 🚀 **Push** to your branch (`git push origin feature/amazing-feature`)
7. 🎯 **Open** a Pull Request

### **Contribution Ideas**
- 🔔 Implement new notification channels
- 📊 Add data visualization features  
- 🌐 Build a web interface
- 📝 Improve documentation
- 🐛 Fix bugs and improve performance
- 🧪 Add more comprehensive tests

### **Code Standards**
- Follow existing code style (Black formatting)
- Add type hints for new functions
- Write tests for new features
- Update documentation as needed

---

## 🚧 Roadmap

### 🎯 **Upcoming Features**
- [ ] 🌐 **Web Dashboard** - Beautiful UI for managing subscriptions
- [ ] 🤖 **AI-Powered Insights** - Smart summaries and trend analysis
- [ ] 📊 **Data Visualization** - Charts and graphs for repository metrics
- [ ] 🔔 **More Integrations** - Teams, Discord, Telegram support
- [ ] 🐳 **Docker Support** - Containerized deployment options
- [ ] 📱 **Mobile Notifications** - Push notifications to mobile devices

### 🔮 **Future Vision**
- **Enterprise Features**: Multi-tenant support, advanced permissions
- **AI Analytics**: Predictive insights, anomaly detection, health scoring
- **Integrations**: GitLab, Bitbucket, and custom Git hosting support
- **Community**: Plugin ecosystem, shared report templates

---

## 📜 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

---

## 🙋‍♂️ Support & Community

### **Get Help**
- 📖 **Documentation**: Check our [docs](docs/) and [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)
- 🐛 **Bug Reports**: [Create an issue](https://github.com/your-username/github-sentinel/issues/new/choose)
- 💡 **Feature Requests**: [Suggest new features](https://github.com/your-username/github-sentinel/issues/new/choose)  
- 💬 **Discussions**: [GitHub Discussions](https://github.com/your-username/github-sentinel/discussions)

### **Connect With Us**
- ⭐ **Star** this repo if you find it helpful!
- 🐦 **Follow** us for updates [@github_sentinel](https://twitter.com/github_sentinel)
- 📧 **Email**: sentinel@example.com

---

## 🎉 Acknowledgments

- **GitHub API** for providing excellent repository data access
- **Python Community** for amazing libraries (Pydantic, SQLAlchemy, Click)
- **Contributors** who help make this project better
- **Users** who provide valuable feedback and feature requests

---

<div align="center">

### ⭐ **Star this repository if GitHub Sentinel helps you!** ⭐

**Made with ❤️ by developers, for developers**

[⬆ Back to Top](#github-sentinel-)

</div>

