import re
import uuid
import os
import base64
from datetime import datetime


def generate_slug(text: str) -> str:
    """Generate URL-friendly slug from text."""
    text = text.lower().strip()
    text = re.sub(r'[àáạảãâầấậẩẫăằắặẳẵ]', 'a', text)
    text = re.sub(r'[èéẹẻẽêềếệểễ]', 'e', text)
    text = re.sub(r'[ìíịỉĩ]', 'i', text)
    text = re.sub(r'[òóọỏõôồốộổỗơờớợởỡ]', 'o', text)
    text = re.sub(r'[ùúụủũưừứựửữ]', 'u', text)
    text = re.sub(r'[ỳýỵỷỹ]', 'y', text)
    text = re.sub(r'[đ]', 'd', text)
    text = re.sub(r'[^a-z0-9\s-]', '', text)
    text = re.sub(r'[\s-]+', '-', text)
    text = text.strip('-')
    return text or str(uuid.uuid4())[:8]


def generate_order_code() -> str:
    """Generate unique order code."""
    now = datetime.now()
    return f"ORD-{now.strftime('%Y%m%d')}-{uuid.uuid4().hex[:6].upper()}"


def format_currency(amount: float) -> str:
    """Format number as Vietnamese currency."""
    return f"{amount:,.0f}₫"

