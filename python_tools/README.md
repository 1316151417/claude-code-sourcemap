# Claude Code Tools - Python 移植版

将 Claude Code 的 FileReadTool、FileEditTool、FileWriteTool、GlobTool、GrepTool 移植为 Python 代码，可直接集成到 Python Agent 框架。

## 功能设计

### 工具列表

| 工具 | 类名 | 功能 |
|------|------|------|
| Read | `FileReadTool` | 读取文件，支持 offset/limit、图片( base64)、PDF、Notebook |
| Edit | `FileEditTool` | 编辑文件，old_string → new_string，支持 replace_all |
| Write | `FileWriteTool` | 写入文件，全量覆盖，自动检测 create/update |
| Glob | `GlobTool` | 文件名模式匹配，支持 `**` 递归，排除 VCS 目录 |
| Grep | `GrepTool` | 正则搜索，基于 ripgrep，支持 3 种输出模式 |

### 架构设计

```
python_tools/
├── base.py              # Tool 基类 (ABC)
├── types.py             # Pydantic 输入/输出类型定义
├── registry.py          # 工具注册表
├── utils/
│   ├── path.py          # expand_path, normalize_path
│   ├── file_ops.py      # read_file_range, write_text, atomic_write
│   ├── git_diff.py      # generate_patch, find_actual_string
│   └── subprocess.py    # run_ripgrep (ripgrep 封装)
└── tools/
    ├── read.py          # FileReadTool
    ├── edit.py          # FileEditTool
    ├── write.py         # FileWriteTool
    ├── glob.py          # GlobTool
    └── grep.py          # GrepTool
```

### 核心接口

```python
from python_tools.base import Tool

class Tool(ABC, Generic[InputT, OutputT]):
    name: str
    description: str = ""

    @abstractmethod
    async def call(self, input_data: InputT) -> ToolResult[OutputT]:
        pass
```

## 安装环境

### 依赖

- Python 3.10+
- Pydantic >= 2.0
- ripgrep (用于 GrepTool)

### 安装步骤

```bash
# 克隆仓库
git clone https://github.com/1316151417/claude-code-sourcemap.git
cd claude-code-sourcemap

# 安装依赖
pip install pydantic pytest

# 安装 ripgrep (macOS)
brew install ripgrep

# 安装 ripgrep (Linux)
apt install ripgrep
```

## 如何运行

### 运行测试

```bash
# 进入项目目录
cd claude-code-sourcemap

# 运行所有测试
PYTHONPATH=. pytest tests/ -v

# 运行特定测试文件
PYTHONPATH=. pytest tests/test_read.py -v

# 查看测试覆盖率
PYTHONPATH=. pytest tests/ --cov=python_tools
```

### 基本使用

```python
from python_tools import FileReadTool, FileEditTool, FileWriteTool, GlobTool, GrepTool
from python_tools.types import ReadInput, EditInput, WriteInput, GlobInput, GrepInput
from python_tools.registry import get_registry

# 方式一：直接使用工具
read_tool = FileReadTool()
result = read_tool.call(ReadInput(file_path="/path/to/file.txt", offset=1, limit=50))
print(result.data.content)

# 方式二：通过注册表使用
registry = get_registry()
print("已注册工具:", registry.list_tools())  # ['Read', 'Edit', 'Write', 'Glob', 'Grep']

edit_tool = registry.get("Edit")
result = edit_tool.call(EditInput(
    file_path="/path/to/file.txt",
    old_string="foo",
    new_string="bar",
    replace_all=True
))
```

### 示例：完整文件操作流程

```python
from python_tools import FileWriteTool, FileReadTool, FileEditTool
from python_tools.types import WriteInput, ReadInput, EditInput

# 1. 写入文件
write_tool = FileWriteTool()
write_result = write_tool.call(WriteInput(
    file_path="/tmp/example.txt",
    content="Hello World"
))
print(f"创建: {write_result.data.type}")  # create

# 2. 读取文件
read_tool = FileReadTool()
read_result = read_tool.call(ReadInput(file_path="/tmp/example.txt"))
print(f"内容: {read_result.data.content}")  # Hello World

# 3. 编辑文件
edit_tool = FileEditTool()
edit_result = edit_tool.call(EditInput(
    file_path="/tmp/example.txt",
    old_string="World",
    new_string="Python"
))
print(f"修改: {edit_result.data.user_modified}")  # True

# 4. 再次读取验证
read_result = read_tool.call(ReadInput(file_path="/tmp/example.txt"))
print(f"内容: {read_result.data.content}")  # Hello Python
```

### 示例：搜索文件

```python
from python_tools import GlobTool, GrepTool
from python_tools.types import GlobInput, GrepInput

# 1. 查找所有 .py 文件
glob_tool = GlobTool()
glob_result = glob_tool.call(GlobInput(pattern="**/*.py", path="/path/to/project"))
print(f"找到 {glob_result.data.num_files} 个 Python 文件")

# 2. 在文件中搜索关键词
grep_tool = GrepTool()
grep_result = grep_tool.call(GrepInput(
    pattern="def.*test",
    path="/path/to/project",
    output_mode="content",
    case_insensitive=True
))
print(f"找到 {grep_result.data.num_matches} 处匹配")
```

## 输出模式 (GrepTool)

| 模式 | 说明 | 返回字段 |
|------|------|----------|
| `files_with_matches` | 返回包含匹配的文件列表 | `filenames`, `num_files` |
| `content` | 返回匹配行及行号 | `content`, `num_lines` |
| `count` | 返回每个文件的匹配次数 | `filenames`, `num_matches` |

## 注意事项

- 所有路径处理使用 `expand_path()`，支持 `~` 展开和相对路径转绝对路径
- FileEditTool 会自动处理引号规范化（弯引号 ↔ 直引号）
- GlobTool 默认排除 VCS 目录：`.git`, `.svn`, `.hg`, `node_modules`, `__pycache__`
- GrepTool 依赖系统安装 ripgrep

## 许可证

基于 Claude Code 源码，遵循 Anthropic 相关协议。
