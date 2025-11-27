# Claude Message Visualizer

Beautiful HTML visualizations for Claude API Message objects in Jupyter notebooks and IPython environments.

## Features

✨ **Rich Visualizations**
- Color-coded block types with icons
- Expandable details for complex content
- Clean, typographic styling

🔍 **Citation Support**
- Automatic citation numbering
- URL matching to search results
- Quoted text previews

🛠️ **Tool Use Debugging**
- Clear tool call visualization
- Input/output formatting
- Error highlighting

📚 **Educational Tooltips**
- Hover over block types for explanations
- Learn the API as you develop
- Perfect for learning Claude

🌐 **Web Search Results**
- Expandable search result cards
- Page age and URL display
- Encrypted content handling

## Installation

```bash
pip install claude-message-visualizer
```

## Quick Start

```python
from anthropic import Anthropic
from claude_message_visualizer import visualize_message

# Create client and get response
client = Anthropic()
response = client.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=1000,
    messages=[{"role": "user", "content": "Hello!"}]
)

# Visualize the response
visualize_message(response)
```

That's it! The visualization will display inline in your notebook.

## Usage Examples

### Basic Text Response

```python
response = client.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=1000,
    messages=[{"role": "user", "content": "Explain quantum computing"}]
)

visualize_message(response)
```

### Web Search with Citations

```python
response = client.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=1000,
    messages=[{"role": "user", "content": "What are the best exercises for leg muscle gain?"}],
    tools=[{"type": "web_search_20250305", "name": "web_search", "max_uses": 5}]
)

visualize_message(response)
```

The visualizer automatically:
- Numbers citations based on search results
- Shows quoted text from each citation
- Links citations to their source URLs

### Tool Use Debugging

```python
tools = [
    {
        "name": "get_weather",
        "description": "Get weather for a location",
        "input_schema": {
            "type": "object",
            "properties": {
                "location": {"type": "string"}
            }
        }
    }
]

response = client.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=1000,
    messages=[{"role": "user", "content": "What's the weather in SF?"}],
    tools=tools
)

visualize_message(response)
```

See tool calls with:
- Tool name and ID
- Formatted input parameters
- Clear visual separation

### Extended Thinking

```python
response = client.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=1000,
    messages=[{"role": "user", "content": "Solve this math problem: ..."}],
    thinking={
        "type": "enabled",
        "budget_tokens": 5000
    }
)

visualize_message(response)
```

Thinking blocks are collapsible with character counts, letting you inspect Claude's reasoning process.

## What Gets Visualized?

The visualizer handles all Claude API block types:

| Block Type | Description | Visual Treatment |
|------------|-------------|------------------|
| **Text** | Claude's text responses | Clean typography, citations |
| **Tool Use** | Tool call requests | Formatted JSON, tool name |
| **Tool Result** | Tool execution results | Expandable, error highlighting |
| **Server Tool Use** | Anthropic-hosted tools | Like tool_use, with server badge |
| **Web Search Results** | Search results from web_search | Expandable cards with metadata |
| **Citations** | Source references | Numbered, linked to search results |
| **Thinking** | Extended thinking content | Collapsible, italic styling |
| **Image** | Image content | Inline display |
| **Document** | Document content | Preview with metadata |

## Requirements

- Python 3.8+
- IPython 7.0+ (Jupyter notebooks, IPython terminal, VS Code notebooks)
- Anthropic Python SDK 0.40.0+

## API Reference

### `visualize_message(message)`

Visualizes a Claude API Message object.

**Parameters:**
- `message` (Message): A Message object returned from `client.messages.create()`

**Returns:**
- None (displays HTML inline)

**Example:**
```python
from claude_message_visualizer import visualize_message

response = client.messages.create(...)
visualize_message(response)
```

## Development

Want to modify the visualizer for your needs?

```bash
# Clone the repo
git clone https://github.com/frankiewarren/claude-message-visualizer.git
cd claude-message-visualizer

# Install in editable mode
pip install -e .

# Make changes to claude_message_visualizer/visualizer.py
# Changes take effect immediately in your notebooks
```

## Contributing

Contributions welcome! This project is designed to help the Claude developer community. Feel free to:

- Report bugs via [GitHub Issues](https://github.com/frankiewarren/claude-message-visualizer/issues)
- Suggest features
- Submit pull requests

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Acknowledgments

Built for developers working with the [Anthropic Claude API](https://www.anthropic.com/api). Special thanks to the Anthropic team for creating such a powerful API.

## Related Resources

- [Anthropic API Documentation](https://docs.anthropic.com/)
- [Anthropic Python SDK](https://github.com/anthropics/anthropic-sdk-python)
- [Claude API Cookbook](https://github.com/anthropics/anthropic-cookbook)

---

**Questions or feedback?** Open an issue on [GitHub](https://github.com/frankiewarren/claude-message-visualizer/issues)!
