import re
import requests
import os
from typing import Dict, List

def markdown_to_html(text: str) -> str:
    """Convert markdown formatting to HTML."""
    if not text:
        return text
    
    # Convert **bold** to <strong>bold</strong>
    text = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', text)
    
    # Convert *italic* to <em>italic</em>
    text = re.sub(r'\*(.*?)\*', r'<em>\1</em>', text)
    
    # Convert line breaks to <br>
    text = text.replace('\n', '<br>')
    
    # Convert bullet points
    text = re.sub(r'^• ', '&bull; ', text, flags=re.MULTILINE)
    
    return text

def get_slack_user_info(user_id: str) -> Dict[str, str]:
    """Get user information from Slack API."""
    try:
        bot_token = os.getenv("SLACK_BOT_TOKEN")
        if not bot_token:
            return {"name": f"User {user_id[-4:]}", "real_name": f"User {user_id[-4:]}"}
        
        # For now, return a formatted user ID
        # In a real implementation, you'd call the Slack API
        return {
            "name": f"User {user_id[-4:]}",
            "real_name": f"User {user_id[-4:]}",
            "display_name": f"User {user_id[-4:]}"
        }
    except:
        return {"name": f"User {user_id[-4:]}", "real_name": f"User {user_id[-4:]}"}

def format_user_mention(user_id: str) -> str:
    """Format user mention for display."""
    user_info = get_slack_user_info(user_id)
    return f"@{user_info['display_name']}"

def clean_message_text(text: str) -> str:
    """Clean and format message text for display."""
    if not text:
        return text
    
    # Replace user mentions with formatted names
    text = re.sub(r'<@([A-Z0-9]+)>', lambda m: format_user_mention(m.group(1)), text)
    
    # Clean up other Slack formatting
    text = re.sub(r'<!(channel|here|everyone)>', r'@\1', text)
    
    return text

def highlight_keywords(text: str) -> str:
    """Highlight important keywords in the text."""
    if not text:
        return text
    
    # Problem keywords
    problem_keywords = ['problem', 'issue', 'error', 'bug', 'stuck', 'help', 'broken', 'failed', 'trouble']
    for keyword in problem_keywords:
        text = re.sub(f'\\b({keyword})\\b', r'<span class="text-danger fw-bold">\1</span>', text, flags=re.IGNORECASE)
    
    # Question keywords
    question_keywords = ['how', 'what', 'where', 'when', 'why', 'can', 'could', 'would', 'should']
    for keyword in question_keywords:
        text = re.sub(f'\\b({keyword})\\b', r'<span class="text-info fw-bold">\1</span>', text, flags=re.IGNORECASE)
    
    # Highlight question marks
    text = text.replace('?', '<span class="text-info fw-bold">?</span>')
    
    return text
