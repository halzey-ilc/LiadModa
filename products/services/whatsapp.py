def generate_whatsapp_link(number: str, title: str) -> str:
    return f"https://wa.me/{number}?text=Здравствуйте! Меня интересует товар: {title}"
