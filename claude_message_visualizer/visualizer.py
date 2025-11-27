"""
Message Visualizer for Claude API Responses

Provides beautiful HTML visualizations of Message objects from the Anthropic API.
Works in VS Code notebooks and Jupyter notebooks.

Usage:
    from message_visualizer import visualize_message

    response = client.messages.create(...)
    visualize_message(response)
"""

from anthropic.types import Message
from IPython.display import HTML, display
import json


def visualize_message(message):
    """
    Visualizes a Claude API Message object with color-coded blocks and icons.

    Args:
        message: A Message object from the Anthropic API
    """
    html = _build_html(message)
    display(HTML(html))


def _build_html(message):
    """Builds the complete HTML visualization with classic typographic style."""

    # Header - elegant, minimal black and white
    header_html = f"""
    <div style="font-family: 'Georgia', 'Times New Roman', serif;
                margin: 32px 0;
                border: 1px solid #000;
                background: #fff;">
        <div style="background: #fff;
                    color: #000;
                    padding: 24px 32px;
                    border-bottom: 3px solid #000;">
            <h3 style="margin: 0 0 16px 0;
                       font-size: 18px;
                       font-weight: 700;
                       letter-spacing: 0.05em;
                       text-transform: uppercase;">
                Claude API Response
            </h3>
            <div style="display: grid;
                       grid-template-columns: repeat(2, 1fr);
                       gap: 12px;
                       font-size: 13px;
                       color: #333;
                       font-family: 'Menlo', 'Monaco', 'Courier New', monospace;">
                <div><strong>ID:</strong> {message.id}</div>
                <div><strong>Model:</strong> {message.model}</div>
                <div><strong>Stop:</strong> {message.stop_reason}</div>
                <div><strong>Role:</strong> {message.role}</div>
            </div>
        </div>
    """

    # Usage statistics - minimal, typographic style
    if message.usage:
        usage = message.usage
        header_html += f"""
        <div style="background: #fff;
                    padding: 16px 32px;
                    border-bottom: 1px solid #ddd;
                    font-size: 13px;
                    font-family: 'Menlo', 'Monaco', 'Courier New', monospace;
                    color: #666;
                    line-height: 1.8;">
            <strong style="color: #000;">Usage:</strong>
            <span style="margin-left: 20px; white-space: nowrap;">Input: <strong style="color: #000;">{usage.input_tokens}</strong> tokens</span>
            <span style="margin-left: 20px; white-space: nowrap;">Output: <strong style="color: #000;">{usage.output_tokens}</strong> tokens</span>
        </div>
        """

    # Content blocks - clean white background
    content_html = '<div style="background: #fff; padding: 0;">'

    for idx, block in enumerate(message.content):
        content_html += _render_block(block, idx, message)

    content_html += '</div></div>'

    return header_html + content_html


def _get_block_tooltip_text(block_type):
    """Returns educational tooltip text for each block type."""
    tooltips = {
        'text': 'The main text content in Claude\'s response. This is where Claude writes its answers, explanations, and conversational replies.',
        'tool_use': 'Claude is requesting your application to execute a tool or function. Your code must run the tool and return the result in the next API call.',
        'tool_result': 'The result returned from executing a tool that Claude requested. This data is provided by your application after running the tool.',
        'server_tool_use': 'Server tools are built and maintained by Anthropic, execute on Anthropic\'s infrastructure, and return results in the same API call. Unlike regular tools, no client-side execution is required.',
        'web_search_tool_result': 'Results from a web search performed by Anthropic\'s servers. Contains search results that Claude can reference and cite in its response.',
        'image': 'Image content included in the message. Can be provided as base64-encoded data or a URL reference.',
        'thinking': 'Extended thinking content showing Claude\'s internal reasoning process. This helps you understand how Claude approached the problem.',
        'document': 'Document content attached to the message, such as PDFs or other file types provided as base64-encoded data.',
    }
    return tooltips.get(block_type, None)


def _render_block(block, index, message=None, depth=0):
    """Renders individual content blocks with classic typographic styling."""
    block_type = block.type

    # Get styling for block type
    color = _get_block_color(block_type)
    icon = _get_block_icon(block_type)

    # Get tooltip text for this block type
    tooltip_text = _get_block_tooltip_text(block_type)

    # Add tooltip to block type label if description exists
    if tooltip_text:
        label_start = f"""<strong style="color: {color};
                          font-size: 13px;
                          font-weight: 700;
                          letter-spacing: 0.15em;
                          text-transform: uppercase;
                          position: relative;
                          display: inline-block;">"""
        tooltip_content = f"""
                <span style="position: absolute;
                             bottom: calc(100% + 8px);
                             left: 0;
                             background: #323232;
                             color: #fff;
                             padding: 12px 16px;
                             border-radius: 4px;
                             font-size: 12px;
                             font-weight: 400;
                             line-height: 1.5;
                             white-space: normal;
                             width: 280px;
                             text-align: left;
                             box-shadow: 0 4px 12px rgba(0,0,0,0.15);
                             opacity: 0;
                             visibility: hidden;
                             transition: opacity 0.13s ease-in-out, visibility 0.13s ease-in-out;
                             pointer-events: none;
                             z-index: 1000;
                             text-transform: none;
                             letter-spacing: normal;
                             font-family: 'Helvetica Neue', Arial, sans-serif;">
                    {tooltip_text}
                    <span style="position: absolute;
                                 top: 100%;
                                 left: 16px;
                                 width: 0;
                                 height: 0;
                                 border-left: 6px solid transparent;
                                 border-right: 6px solid transparent;
                                 border-top: 6px solid #323232;"></span>
                </span>
        """
    else:
        label_start = f"<strong style=\"color: {color}; font-size: 13px; font-weight: 700; letter-spacing: 0.15em; text-transform: uppercase;\">"
        tooltip_content = ""

    label_end = "</strong>"

    html = f"""
    <div style="margin: 0;
                padding: 28px 36px;
                background: #fff;
                border-bottom: 1px solid #e5e5e5;">
        <div style="display: flex;
                   align-items: baseline;
                   margin-bottom: 20px;
                   font-family: 'Georgia', 'Times New Roman', serif;">
            <span style="font-size: 18px; margin-right: 10px; color: {color};">{icon}</span>
            {label_start}
                {block_type.replace('_', ' ')}
                {tooltip_content}
            {label_end}
            <span style="margin-left: auto;
                        color: #bbb;
                        font-size: 12px;
                        font-weight: 400;
                        font-family: 'Menlo', 'Monaco', monospace;">
                Block {index}
            </span>
        </div>
    """

    # Add hover style for tooltip if present
    if tooltip_text:
        html += """
        <style>
            strong[style*="position: relative"]:hover span[style*="opacity: 0"] {
                opacity: 1 !important;
                visibility: visible !important;
            }
        </style>
        """

    # Render based on block type
    if block_type == "text":
        html += _render_text_block(block, message)

    elif block_type == "tool_use":
        html += _render_tool_use_block(block)

    elif block_type == "tool_result":
        html += _render_tool_result_block(block)

    elif block_type == "server_tool_use":
        html += _render_server_tool_use_block(block)

    elif block_type == "web_search_tool_result":
        html += _render_web_search_result_block(block, depth)

    elif block_type == "image":
        html += _render_image_block(block)

    elif block_type == "thinking":
        html += _render_thinking_block(block)

    elif block_type == "document":
        html += _render_document_block(block)

    else:
        # Generic rendering for unknown types
        html += f'<pre style="background: rgba(0,0,0,0.05); padding: 10px; border-radius: 4px; overflow-x: auto; font-size: 12px;">{_safe_json(block)}</pre>'

    html += '</div>'
    return html


def _render_text_block(block, message=None):
    """Renders a text content block with classic typography."""
    text = block.text

    # Check if text is empty or just whitespace
    is_empty = not text or text.strip() == ""

    # Check for citations
    has_citations = hasattr(block, 'citations') and block.citations

    if has_citations:
        # Build a URL-to-index mapping from web search results in the message
        url_to_index = {}
        if message:
            for msg_block in message.content:
                if hasattr(msg_block, 'type') and msg_block.type == 'web_search_tool_result':
                    # Extract search results and map URLs to indices (1-indexed for display)
                    for idx, result in enumerate(msg_block.content):
                        if hasattr(result, 'url'):
                            url_to_index[result.url] = idx + 1

        # Render text with citation indicators - clean style
        citation_info = ""
        for idx, citation in enumerate(block.citations):
            if hasattr(citation, 'cited_text'):
                cited_text = citation.cited_text[:100] + "..." if len(citation.cited_text) > 100 else citation.cited_text

                # Get the actual result index by matching citation URL to search result URL
                citation_number = idx + 1  # Default to sequential numbering

                if hasattr(citation, 'url') and citation.url in url_to_index:
                    citation_number = url_to_index[citation.url]

                citation_info += f"""
                <div style="background: #f9f9f9;
                            padding: 12px 16px;
                            margin-top: 12px;
                            border-left: 3px solid #dc2626;
                            font-size: 13px;
                            line-height: 1.6;
                            font-family: 'Georgia', 'Times New Roman', serif;">
                    <strong style="color: #dc2626;">[{citation_number}]</strong>
                    <span style="color: #333; margin-left: 8px;">"{cited_text}"</span>
                </div>
                """

        html = f"""
        <div style="background: #fff;
                    padding: 0;
                    font-size: 15px;
                    line-height: 1.8;
                    font-family: 'Georgia', 'Times New Roman', serif;">
            <div style="white-space: pre-wrap; color: #000;">{text}</div>
            {citation_info}
        </div>
        """
    elif is_empty:
        # Show a subtle indicator for empty text blocks
        html = f"""
        <div style="background: #fafafa;
                    padding: 12px 16px;
                    font-size: 13px;
                    color: #999;
                    font-style: italic;
                    font-family: 'Georgia', 'Times New Roman', serif;
                    border: 1px dashed #e5e5e5;">
            Empty text block
        </div>
        """
    elif len(text) > 1000:
        # Truncate very long text with expand option
        html = f"""
        <details>
            <summary style="cursor: pointer;
                           color: #000;
                           margin-bottom: 16px;
                           font-weight: 600;
                           padding: 8px 0;
                           border-bottom: 1px solid #ddd;
                           font-family: 'Georgia', 'Times New Roman', serif;">
                Long content ({len(text)} characters) — Click to expand
            </summary>
            <div style="background: #fff;
                       padding: 16px 0;
                       white-space: pre-wrap;
                       font-size: 15px;
                       line-height: 1.8;
                       color: #000;
                       font-family: 'Georgia', 'Times New Roman', serif;">
{text}
            </div>
        </details>
        """
    else:
        html = f"""
        <div style="background: #fff;
                    padding: 0;
                    white-space: pre-wrap;
                    font-size: 15px;
                    line-height: 1.8;
                    color: #000;
                    font-family: 'Georgia', 'Times New Roman', serif;">
{text}
        </div>
        """

    return html


def _render_tool_use_block(block):
    """Renders a tool_use content block."""
    html = f"""
    <div style="margin-bottom: 16px; font-family: 'Menlo', 'Monaco', monospace; font-size: 12px;">
        <span style="color: #666;">Tool:</span> <strong style="color: #000;">{block.name}</strong>
        <span style="margin-left: 24px; color: #666;">ID:</span> <span style="color: #999;">{block.id}</span>
    </div>
    <details open>
        <summary style="cursor: pointer;
                        color: #000;
                        margin-bottom: 12px;
                        font-size: 13px;
                        font-weight: 600;
                        font-family: 'Georgia', 'Times New Roman', serif;">
            Input
        </summary>
        <pre style="background: #fafafa;
                    padding: 18px;
                    border: 1px solid #e5e5e5;
                    border-radius: 2px;
                    overflow-x: auto;
                    font-size: 13px;
                    line-height: 1.7;
                    font-family: 'Menlo', 'Monaco', monospace;
                    color: #000;">{json.dumps(block.input, indent=2)}</pre>
    </details>
    """
    return html


def _render_tool_result_block(block):
    """Renders a tool_result content block."""
    is_error = hasattr(block, 'is_error') and block.is_error
    status_badge = ""

    if is_error:
        status_badge = '<span style="margin-left: 24px; padding: 2px 6px; background: #dc2626; color: #fff; font-weight: 700; font-size: 9px; letter-spacing: 0.05em; display: inline-block; vertical-align: middle;">ERROR</span>'

    html = f"""
    <div style="margin-bottom: 16px; font-family: 'Menlo', 'Monaco', monospace; font-size: 12px;">
        <span style="color: #666;">Tool Use ID:</span> <span style="color: #999;">{block.tool_use_id}</span>
        {status_badge}
    </div>
    <details open>
        <summary style="cursor: pointer;
                        color: #000;
                        margin-bottom: 12px;
                        font-size: 13px;
                        font-weight: 600;
                        font-family: 'Georgia', 'Times New Roman', serif;">
            Result
        </summary>
        <div style="background: #fafafa;
                    padding: 18px;
                    border: 1px solid #e5e5e5;
                    border-radius: 2px;
                    font-size: 13px;
                    line-height: 1.7;
                    font-family: 'Georgia', 'Times New Roman', serif;
                    color: #000;
                    white-space: pre-wrap;">
    """

    # Handle content - could be string or list
    if isinstance(block.content, str):
        html += block.content
    elif isinstance(block.content, list):
        # Content is a list of blocks - render each
        for content_block in block.content:
            if hasattr(content_block, 'type'):
                html += f'<div style="margin-bottom: 12px;"><strong>[{content_block.type}]</strong></div>'
            html += _safe_json(content_block)
    else:
        html += str(block.content)

    html += """
        </div>
    </details>
    """
    return html


def _render_server_tool_use_block(block):
    """Renders a server_tool_use content block (like web_search)."""
    html = f"""
    <div style="margin-bottom: 16px; font-family: 'Menlo', 'Monaco', monospace; font-size: 12px;">
        <span style="color: #666;">Tool:</span> <strong style="color: #000;">{block.name}</strong>
        <span style="margin-left: 24px; color: #666;">ID:</span> <span style="color: #999;">{block.id}</span>
    </div>
    <details open>
        <summary style="cursor: pointer;
                        color: #000;
                        margin-bottom: 12px;
                        font-size: 13px;
                        font-weight: 600;
                        font-family: 'Georgia', 'Times New Roman', serif;">
            Input
        </summary>
        <pre style="background: #fafafa;
                    padding: 18px;
                    border: 1px solid #e5e5e5;
                    border-radius: 2px;
                    overflow-x: auto;
                    font-size: 13px;
                    line-height: 1.7;
                    font-family: 'Menlo', 'Monaco', monospace;
                    color: #000;">{json.dumps(block.input, indent=2)}</pre>
    </details>
    """
    return html


def _render_web_search_result_block(block, depth):
    """Renders a web_search_tool_result content block with nested results."""
    html = f"""
    <div style="margin-bottom: 16px;">
        <strong style="color: #000;
                       font-size: 13px;
                       font-weight: 600;
                       font-family: 'Georgia', 'Times New Roman', serif;">
            Search Results
        </strong>
        <span style="color: #999;
                     font-size: 12px;
                     margin-left: 12px;
                     font-family: 'Menlo', 'Monaco', monospace;">
            {len(block.content)} results
        </span>
    </div>
    """

    # Render individual search results
    for idx, result in enumerate(block.content):
        if hasattr(result, 'type') and result.type == 'web_search_result':
            html += _render_individual_search_result(result, idx)

    return html


def _render_individual_search_result(result, index):
    """Renders an individual web search result."""
    html = f"""
    <details style="margin-top: 12px;
                    border: 1px solid #ddd;
                    border-radius: 2px;
                    background: #fafafa;">
        <summary style="cursor: pointer;
                        padding: 12px 16px;
                        font-family: 'Georgia', 'Times New Roman', serif;
                        font-size: 14px;
                        line-height: 1.6;">
            <strong style="color: #000; font-weight: 600;">Result {index + 1}</strong>
            <span style="color: #333; margin-left: 8px;">{result.title}</span>
        </summary>
        <div style="padding: 16px;
                    background: #fff;
                    border-top: 1px solid #e5e5e5;
                    font-size: 13px;
                    line-height: 1.8;
                    font-family: 'Georgia', 'Times New Roman', serif;">
            <div style="margin-bottom: 12px;">
                <span style="color: #666; font-size: 12px; text-transform: uppercase; letter-spacing: 0.05em;">URL</span><br>
                <a href="{result.url}" target="_blank" style="color: #000; text-decoration: underline; word-break: break-all;">
                    {result.url}
                </a>
            </div>
            <div style="margin-bottom: 12px;">
                <span style="color: #666; font-size: 12px; text-transform: uppercase; letter-spacing: 0.05em;">Page Age</span><br>
                <span style="color: #000;">{result.page_age}</span>
            </div>
            <div>
                <span style="color: #666; font-size: 12px; text-transform: uppercase; letter-spacing: 0.05em;">Content</span><br>
                <span style="color: #999; font-size: 12px; font-family: 'Menlo', 'Monaco', monospace;">
                    Encrypted · {len(result.encrypted_content)} characters
                </span>
            </div>
        </div>
    </details>
    """
    return html


def _render_image_block(block):
    """Renders an image content block."""
    source = block.source
    source_type = source.get('type') if isinstance(source, dict) else source.type

    html = f"""
    <div style="margin-bottom: 16px; font-family: 'Menlo', 'Monaco', monospace; font-size: 12px;">
        <span style="color: #666;">Source Type:</span> <strong style="color: #000;">{source_type}</strong>
    """

    if source_type == "base64":
        media_type = source.get('media_type') if isinstance(source, dict) else source.media_type
        data = source.get('data') if isinstance(source, dict) else source.data
        data_size = len(data) if data else 0

        html += f"""
        <span style="margin-left: 24px; color: #666;">Media Type:</span> <strong style="color: #000;">{media_type}</strong>
        <span style="margin-left: 24px; color: #666;">Size:</span> <span style="color: #999;">{data_size} bytes</span>
    </div>
    <div style="margin-top: 12px;">
        <img src="data:{media_type};base64,{data}"
             style="max-width: 100%; height: auto; border: 1px solid #ddd; border-radius: 2px;"
             alt="Content image" />
    </div>
        """
    elif source_type == "url":
        url = source.get('url') if isinstance(source, dict) else source.url
        html += f"""
        <span style="margin-left: 24px; color: #666;">URL:</span> <a href="{url}" target="_blank" style="color: #000; text-decoration: underline;">{url}</a>
    </div>
    <div style="margin-top: 12px;">
        <img src="{url}"
             style="max-width: 100%; height: auto; border: 1px solid #ddd; border-radius: 2px;"
             alt="Content image" />
    </div>
        """
    else:
        html += "</div>"

    return html


def _render_thinking_block(block):
    """Renders a thinking content block (extended thinking)."""
    thinking = block.thinking

    html = f"""
    <details>
        <summary style="cursor: pointer;
                        color: #666;
                        margin-bottom: 12px;
                        font-size: 13px;
                        font-weight: 600;
                        font-family: 'Georgia', 'Times New Roman', serif;
                        font-style: italic;">
            Extended Thinking ({len(thinking)} characters) — Click to view
        </summary>
        <div style="background: #fafafa;
                    padding: 18px;
                    border: 1px solid #e5e5e5;
                    border-left: 3px solid #666;
                    border-radius: 2px;
                    white-space: pre-wrap;
                    font-size: 13px;
                    line-height: 1.7;
                    color: #333;
                    font-family: 'Georgia', 'Times New Roman', serif;
                    font-style: italic;">
{thinking}
        </div>
    </details>
    """
    return html


def _render_document_block(block):
    """Renders a document content block."""
    source = block.source
    source_type = source.get('type') if isinstance(source, dict) else source.type

    html = f"""
    <div style="margin-bottom: 16px; font-family: 'Menlo', 'Monaco', monospace; font-size: 12px;">
        <span style="color: #666;">Source Type:</span> <strong style="color: #000;">{source_type}</strong>
    """

    if source_type == "base64":
        media_type = source.get('media_type') if isinstance(source, dict) else source.media_type
        data = source.get('data') if isinstance(source, dict) else source.data
        data_size = len(data) if data else 0

        html += f"""
        <span style="margin-left: 24px; color: #666;">Media Type:</span> <strong style="color: #000;">{media_type}</strong>
        <span style="margin-left: 24px; color: #666;">Size:</span> <span style="color: #999;">{data_size} bytes</span>
    </div>
    <div style="background: #fafafa;
                padding: 18px;
                border: 1px solid #e5e5e5;
                border-radius: 2px;
                margin-top: 12px;
                text-align: center;
                color: #666;
                font-family: 'Georgia', 'Times New Roman', serif;">
        <strong>Document Preview Not Available</strong><br>
        <span style="font-size: 12px;">Base64-encoded document: {media_type}</span>
    </div>
        """
    else:
        html += "</div>"

    return html


def _get_block_icon(block_type):
    """Returns a minimal typographic symbol for each block type."""
    icons = {
        'text': '§',  # Section mark
        'tool_use': '⚙',  # Gear
        'tool_result': '✓',  # Check mark
        'server_tool_use': '◆',  # Diamond
        'web_search_tool_result': '◇',  # Hollow diamond
        'web_search_result': '·',  # Middle dot
        'image': '◉',  # Image/visual
        'thinking': '∴',  # Therefore (reasoning)
        'document': '▭',  # Document rectangle
    }
    return icons.get(block_type, '•')


def _get_block_color(block_type):
    """Returns a color for each block type - minimal black palette with rare red accent."""
    colors = {
        'text': '#000',  # Black for text
        'tool_use': '#000',  # Black for tool use
        'tool_result': '#000',  # Black for tool results
        'server_tool_use': '#000',  # Black for server tools
        'web_search_tool_result': '#000',  # Black for search results
        'web_search_result': '#666',  # Gray for individual results
        'image': '#000',  # Black for images
        'thinking': '#666',  # Gray for thinking (less prominent)
        'document': '#000',  # Black for documents
    }
    return colors.get(block_type, '#666')


def _safe_json(obj):
    """Safely converts an object to JSON string."""
    try:
        # Try to convert to dict first if it's a Pydantic model
        if hasattr(obj, 'model_dump'):
            return json.dumps(obj.model_dump(), indent=2)
        elif hasattr(obj, '__dict__'):
            return json.dumps(obj.__dict__, indent=2, default=str)
        else:
            return json.dumps(obj, indent=2, default=str)
    except Exception as e:
        return f"<Unable to serialize: {str(e)}>"
