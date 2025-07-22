# Contributing to GitHub Sentinel 🤝

Thank you for your interest in contributing to GitHub Sentinel! This document provides guidelines and information for contributors.

## 🚀 Quick Start for Contributors

### 1. Development Setup
```bash
# Fork and clone the repository
git clone https://github.com/your-username/github-sentinel.git
cd github-sentinel

# Install dependencies
uv sync --dev

# Set up pre-commit hooks (optional but recommended)
uv run pre-commit install
```

### 2. Environment Setup
```bash
# Copy environment template
cp .env.example .env

# Add your GitHub token
export GITHUB_TOKEN="your_github_token_here"

# Run tests to ensure everything works
uv run pytest
```

## 📋 How to Contribute

### 🐛 **Bug Reports**
1. Check existing [issues](https://github.com/your-username/github-sentinel/issues) first
2. Create a new issue with:
   - Clear, descriptive title
   - Steps to reproduce
   - Expected vs actual behavior
   - Environment details (OS, Python version, etc.)
   - Error messages/logs if applicable

### 💡 **Feature Requests**
1. Check if the feature is already requested
2. Create a new issue with:
   - Clear description of the feature
   - Use cases and benefits
   - Possible implementation approach
   - Willingness to implement it yourself

### 🔧 **Code Contributions**

#### **Branch Naming**
- `feature/feature-name` - New features
- `fix/bug-description` - Bug fixes
- `docs/improvement-area` - Documentation updates
- `refactor/component-name` - Code refactoring

#### **Development Workflow**
```bash
# 1. Create and switch to your feature branch
git checkout -b feature/amazing-feature

# 2. Make your changes
# ... code, test, iterate ...

# 3. Run the full test suite
uv run pytest
uv run black src/ tests/
uv run flake8 src/ tests/
uv run mypy src/

# 4. Commit your changes
git add .
git commit -m "Add: amazing feature description

- Detailed change 1
- Detailed change 2
- Fixes #issue_number"

# 5. Push and create PR
git push origin feature/amazing-feature
```

## 🧪 Testing Guidelines

### **Running Tests**
```bash
# Run all tests
uv run pytest

# Run tests with coverage
uv run pytest --cov=github_sentinel

# Run specific test file
uv run pytest tests/test_github_service.py

# Run tests matching pattern
uv run pytest -k "test_subscription"
```

### **Writing Tests**
- Write tests for all new functionality
- Use descriptive test names
- Follow the existing test structure
- Mock external services (GitHub API, SMTP, etc.)
- Test both success and error scenarios

### **Test Structure**
```python
def test_feature_should_do_something_when_condition():
    """Test description explaining what is being tested."""
    # Arrange
    setup_test_data()
    
    # Act
    result = function_under_test()
    
    # Assert
    assert result == expected_value
```

## 📝 Code Standards

### **Python Code Style**
- Use [Black](https://black.readthedocs.io/) for code formatting
- Follow [PEP 8](https://pep8.org/) conventions
- Use type hints for function parameters and return values
- Write docstrings for classes and functions

### **Code Quality**
```bash
# Auto-format code
uv run black src/ tests/

# Check code style
uv run flake8 src/ tests/

# Type checking
uv run mypy src/

# Import sorting
uv run isort src/ tests/
```

### **Commit Message Format**
```
Type: Short description (50 chars or less)

Longer explanation if needed. Wrap at 72 characters.

- List specific changes
- Use bullet points for multiple changes
- Reference issues: Fixes #123, Closes #456

Co-authored-by: Name <email@example.com>
```

**Commit Types:**
- `Add:` New features
- `Fix:` Bug fixes
- `Update:` Improvements to existing features
- `Remove:` Removing code/features
- `Refactor:` Code restructuring without behavior change
- `Docs:` Documentation changes
- `Test:` Adding or updating tests

## 🏗️ Architecture Guidelines

### **Code Organization**
```
src/github_sentinel/
├── core/           # Core business models and configuration
├── services/       # Business logic and external integrations
├── database/       # Data access layer
├── cli/           # Command-line interface
└── utils/         # Shared utilities
```

### **Design Principles**
1. **Single Responsibility**: Each class/function has one clear purpose
2. **Dependency Injection**: Pass dependencies explicitly
3. **Type Safety**: Use type hints and Pydantic models
4. **Error Handling**: Use custom exceptions and proper logging
5. **Async First**: Use async/await for I/O operations

### **Adding New Features**

#### **New Service Class**
```python
# services/new_service.py
from ..core.config import Config
from ..core.exceptions import CustomException
from ..utils.logger import get_logger

logger = get_logger(__name__)

class NewService:
    def __init__(self, config: Config):
        self.config = config
    
    async def do_something(self, param: str) -> str:
        """Do something useful."""
        try:
            # Implementation
            result = await some_async_operation()
            logger.info(f"Successfully did something: {result}")
            return result
        except Exception as e:
            logger.error(f"Failed to do something: {e}")
            raise CustomException(f"Operation failed: {str(e)}")
```

#### **New CLI Command**
```python
# cli/commands.py
@main.command()
@click.option('--param', '-p', help='Parameter description')
@click.pass_context
def new_command(ctx, param):
    """Description of what this command does."""
    try:
        config, db_manager, services = setup_application(ctx.obj['config_file'])
        
        # Implementation
        result = await service.do_something(param)
        click.echo(f"Success: {result}")
        
    except Exception as e:
        click.echo(f"Error: {str(e)}")
        sys.exit(1)
```

## 📚 Documentation

### **Code Documentation**
- Use docstrings for all public classes and methods
- Include parameter and return type information
- Provide usage examples for complex functions

### **README Updates**
- Update README.md if you add new features
- Add new CLI commands to the usage section
- Update installation instructions if needed

## 🤔 Need Help?

### **Getting Support**
- 💬 **Discussions**: Use [GitHub Discussions](https://github.com/your-username/github-sentinel/discussions) for questions
- 🐛 **Issues**: Create an issue for bugs or feature requests
- 📧 **Email**: Contact maintainers at sentinel@example.com
- 📖 **Documentation**: Check [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) for architecture details

### **Good First Issues**
Look for issues labeled:
- `good first issue` - Perfect for new contributors
- `help wanted` - We'd love community help on these
- `documentation` - Help improve our docs
- `bug` - Fix reported issues

## 🎉 Recognition

### **Contributors**
All contributors will be:
- Added to the contributors list
- Mentioned in release notes for their contributions
- Given credit in the acknowledgments section

### **Contribution Ideas**
- 🔔 **Notification Channels**: Add support for new platforms
- 📊 **Data Visualization**: Create charts and dashboards  
- 🌐 **Web Interface**: Build a web UI for the CLI tool
- 🤖 **AI Features**: Implement smart insights and summaries
- 📱 **Mobile App**: Create mobile notifications
- 🐳 **DevOps**: Docker, Kubernetes, CI/CD improvements

---

**Thank you for contributing to GitHub Sentinel!** 🙏

Every contribution, no matter how small, makes this project better for everyone. 