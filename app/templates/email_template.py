"""
Email HTML template for contact form submissions.
"""
from datetime import datetime


def get_html_template(name: str, sender_email: str, message_body: str) -> str:
    """Generate professional HTML email template."""
    timestamp = datetime.now().strftime('%B %d, %Y at %H:%M:%S UTC')
    
    return f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 600px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }}
        .email-container {{
            background-color: #ffffff;
            border-radius: 8px;
            padding: 30px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .header {{
            border-bottom: 3px solid #8b5cf6;
            padding-bottom: 20px;
            margin-bottom: 30px;
        }}
        .header h1 {{
            margin: 0;
            color: #8b5cf6;
            font-size: 24px;
        }}
        .header p {{
            margin: 5px 0 0 0;
            color: #666;
            font-size: 14px;
        }}
        .info-section {{
            background-color: #f9fafb;
            border-left: 4px solid #8b5cf6;
            padding: 15px 20px;
            margin: 20px 0;
            border-radius: 4px;
        }}
        .info-row {{
            margin: 10px 0;
        }}
        .label {{
            font-weight: 600;
            color: #555;
            display: inline-block;
            min-width: 100px;
        }}
        .value {{
            color: #333;
        }}
        .message-section {{
            margin: 30px 0;
            padding: 20px;
            background-color: #fafafa;
            border-radius: 6px;
            border: 1px solid #e5e7eb;
        }}
        .message-label {{
            font-weight: 600;
            color: #555;
            margin-bottom: 10px;
            font-size: 14px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}
        .message-content {{
            color: #333;
            white-space: pre-wrap;
            font-size: 15px;
            line-height: 1.7;
        }}
        .footer {{
            margin-top: 30px;
            padding-top: 20px;
            border-top: 1px solid #e5e7eb;
            color: #666;
            font-size: 13px;
            text-align: center;
        }}
        .reply-button {{
            display: inline-block;
            margin: 20px 0;
            padding: 12px 24px;
            background-color: #8b5cf6;
            color: white;
            text-decoration: none;
            border-radius: 6px;
            font-weight: 600;
        }}
        .timestamp {{
            color: #999;
            font-size: 12px;
        }}
    </style>
</head>
<body>
    <div class="email-container">
        <div class="header">
            <h1>📬 Hi , I am Maliha Mehnaz. I will get back to you.</h1>
            <p class="timestamp">Received on {timestamp}</p>
        </div>
        
        <div class="info-section">
            <div class="info-row">
                <span class="label">👤 Name:</span>
                <span class="value">{name}</span>
            </div>
            <div class="info-row">
                <span class="label">📧 Email:</span>
                <span class="value"><a href="mailto:{sender_email}" style="color: #8b5cf6; text-decoration: none;">{sender_email}</a></span>
            </div>
        </div>
        
        <div class="message-section">
            <div class="message-label">💬 Message</div>
            <div class="message-content">{message_body}</div>
        </div>
        
        <div style="text-align: center;">
            <a href="mailto:{sender_email}" class="reply-button">Reply to {name}</a>
        </div>
        
        <div class="footer">
            <p>This message was sent via your portfolio contact form</p>
            <p>You can reply directly to this email to respond to the sender.</p>
        </div>
    </div>
</body>
</html>
"""


def get_text_template(name: str, sender_email: str, message_body: str) -> str:
    """Generate plain text email template."""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')
    
    return f"""New Portfolio Contact Form Submission

Name: {name}
Email: {sender_email}
Received: {timestamp}

Message:
{message_body}

---
This message was sent via your portfolio contact form.
Reply directly to this email to respond to {sender_email}."""
