import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Add Boxicons CDN if not present
if "boxicons.min.css" not in content:
    content = content.replace('<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">',
                              '<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">\n    <link href="https://unpkg.com/boxicons@2.1.4/css/boxicons.min.css" rel="stylesheet">')

replacements = {
    '💳': "<i class='bx bx-credit-card'></i>",
    '📍': "<i class='bx bx-map'></i>",
    '☰': "<i class='bx bx-menu'></i>",
    '🛒': "<i class='bx bx-shopping-bag'></i>",
    '🚀': "<i class='bx bx-rocket'></i>",
    '✅': "<i class='bx bx-check-circle'></i>",
    '📦': "<i class='bx bx-package'></i>",
    '✕': "<i class='bx bx-x'></i>",
    '🔥': "<i class='bx bx-grid-alt'></i>",
    '🔌': "<i class='bx bx-plug'></i>",
    '⚡': "<i class='bx bx-bolt-circle'></i>",
    '🎧': "<i class='bx bx-headphone'></i>",
    '📱': "<i class='bx bx-mobile-alt'></i>",
    '📸': "<i class='bx bxl-instagram'></i>",
    '💬': "<i class='bx bxl-whatsapp'></i>",
    '🔍': "<i class='bx bx-search'></i>",
    '🛡️': "<i class='bx bx-shield-quarter'></i>",
    '🏷️': "<i class='bx bx-purchase-tag-alt'></i>",
    '🚚': "<i class='bx bx-truck'></i>",
    '🗑️': "<i class='bx bx-trash'></i>",
    '⚠️': "<i class='bx bx-error-circle'></i>"
}

for emoji, boxicon in replacements.items():
    content = content.replace(emoji, boxicon)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Icons replaced.")
