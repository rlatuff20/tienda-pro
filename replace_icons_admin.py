import re

with open('admin.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Add Boxicons CDN if not present
if "boxicons.min.css" not in content:
    content = content.replace('<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">',
                              '<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">\n  <link href="https://unpkg.com/boxicons@2.1.4/css/boxicons.min.css" rel="stylesheet">')

replacements = {
    '👁️': "<i class='bx bx-show'></i>",
    '🙈': "<i class='bx bx-hide'></i>",
    '📦': "<i class='bx bx-package'></i>",
    '➕': "<i class='bx bx-plus'></i>",
    '📋': "<i class='bx bx-list-ul'></i>",
    '🚪': "<i class='bx bx-log-out'></i>",
    '⚠️': "<i class='bx bx-error-circle'></i>",
    '🔴': "<i class='bx bx-x-circle'></i>",
    '🏷️': "<i class='bx bx-purchase-tag-alt'></i>",
    '🔍': "<i class='bx bx-search'></i>",
    '📁': "<i class='bx bx-folder'></i>",
    '🚀': "<i class='bx bx-rocket'></i>",
    '✏️': "<i class='bx bx-pencil'></i>",
    '💾': "<i class='bx bx-save'></i>",
    '✅': "<i class='bx bx-check-circle'></i>",
    '❌': "<i class='bx bx-x'></i>",
    'ℹ️': "<i class='bx bx-info-circle'></i>",
    '🗑️': "<i class='bx bx-trash'></i>"
}

for emoji, boxicon in replacements.items():
    content = content.replace(emoji, boxicon)

with open('admin.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Icons replaced in admin.")
