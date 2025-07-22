#!/usr/bin/env python3
"""
GitHub Sentinel Demo Script

这个脚本演示了GitHub Sentinel的架构和基本功能。
"""

import sys
from pathlib import Path

# Add src directory to Python path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

from github_sentinel.core.config import Config
from github_sentinel.core.models import User, NotificationChannel
from github_sentinel.utils.helpers import validate_github_repo_name, parse_github_url


def demo_architecture():
    """演示项目架构"""
    print("🏗️  GitHub Sentinel 项目架构演示")
    print("=" * 50)
    
    print("\n📁 项目结构:")
    print("""
    src/github_sentinel/
    ├── core/                    # 核心模块
    │   ├── models.py           # 数据模型 (Repository, Subscription, Report等)
    │   ├── config.py           # 配置管理
    │   └── exceptions.py       # 异常定义
    ├── services/               # 业务逻辑层
    │   ├── github_service.py   # GitHub API 服务
    │   ├── subscription_service.py  # 订阅管理
    │   ├── notification_service.py  # 通知服务
    │   ├── report_service.py   # 报告生成
    │   └── scheduler_service.py     # 任务调度
    ├── database/               # 数据访问层
    │   ├── connection.py       # 数据库连接和ORM模型
    │   └── repositories.py     # 数据仓库模式实现
    ├── cli/                    # 命令行界面
    │   └── commands.py         # CLI 命令实现
    └── utils/                  # 工具函数
        ├── logger.py          # 日志工具
        └── helpers.py         # 辅助函数
    """)


def demo_config():
    """演示配置管理"""
    print("\n⚙️  配置管理演示")
    print("=" * 30)
    
    try:
        config = Config()
        print(f"✓ 应用名称: {config.app_name}")
        print(f"✓ 版本: {config.version}")
        print(f"✓ 环境: {config.environment}")
        print(f"✓ 数据库URL: {config.get_database_url()}")
        print(f"✓ GitHub API URL: {config.github.base_url}")
        
        missing = config.validate_required_settings()
        if missing:
            print(f"⚠️  缺少配置: {', '.join(missing)}")
        else:
            print("✓ 所有必要配置都已设置")
            
    except Exception as e:
        print(f"❌ 配置加载失败: {e}")


def demo_models():
    """演示数据模型"""
    print("\n📊 数据模型演示")
    print("=" * 30)
    
    # 创建用户模型
    user = User(
        username="demo_user",
        email="demo@example.com", 
        github_token="demo_token",
        notification_preferences={
            NotificationChannel.EMAIL: True,
            NotificationChannel.SLACK: False
        }
    )
    
    print(f"✓ 用户模型: {user.username} ({user.email})")
    print(f"✓ 通知偏好: {user.notification_preferences}")
    
    # 演示枚举类型
    print(f"✓ 支持的通知渠道: {[ch.value for ch in NotificationChannel]}")


def demo_helpers():
    """演示辅助函数"""
    print("\n🔧 辅助函数演示")
    print("=" * 30)
    
    # 测试GitHub URL解析
    test_urls = [
        "https://github.com/microsoft/vscode",
        "git@github.com:facebook/react.git",
        "microsoft/typescript"
    ]
    
    for url in test_urls:
        parsed = parse_github_url(url)
        valid = validate_github_repo_name(parsed) if parsed else False
        print(f"✓ {url} -> {parsed} (有效: {valid})")


def demo_cli_commands():
    """演示CLI命令"""
    print("\n💻 CLI 命令演示")
    print("=" * 30)
    
    print("可用的命令:")
    print("  • python main.py --help                    # 显示帮助")
    print("  • python main.py status                    # 检查状态")
    print("  • python main.py init -u user -e email -t token  # 初始化用户")
    print("  • python main.py subscribe -u 1 -r owner/repo    # 订阅仓库")
    print("  • python main.py analyze -r owner/repo -d 7      # 分析活动")
    print("  • python main.py process -f daily              # 处理订阅")


def main():
    """主演示函数"""
    print("🚀 GitHub Sentinel - 项目演示")
    print("=" * 60)
    
    try:
        demo_architecture()
        demo_config()
        demo_models() 
        demo_helpers()
        demo_cli_commands()
        
        print("\n" + "=" * 60)
        print("🎉 演示完成！")
        print("\n📝 下一步:")
        print("1. 设置 GITHUB_TOKEN 环境变量")
        print("2. 运行: python main.py init -u your_name -e your_email -t your_token")
        print("3. 运行: python main.py subscribe -u 1 -r microsoft/vscode")
        print("4. 运行: python main.py analyze -r microsoft/vscode")
        print("\n🔗 项目特点:")
        print("• 🏗️  清晰的分层架构 (Core → Services → Database → CLI)")
        print("• 📦 模块化设计，易于扩展")
        print("• 🛠️  完整的配置管理")
        print("• 🎯 基于Pydantic的数据验证")
        print("• 📊 Repository模式的数据访问")
        print("• 🔧 完整的CLI界面")
        print("• 📝 异步支持和错误处理")
        
    except Exception as e:
        print(f"❌ 演示过程中出错: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main() 