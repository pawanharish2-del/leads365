import os
import re

core_html_files = ['index.html', 'features.html', 'about.html', 'contact.html', 'pricing.html', 'privacy-policy.html']

for filename in core_html_files:
    if not os.path.exists(filename):
        continue
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()

    orig = content

    # 1. Replace any trailing-slash /lead-management-software/slug/ with clean URL /lead-management-software/slug
    content = re.sub(
        r'href=["\']/lead-management-software/([a-z0-9\-]+)/["\']',
        r'href="/lead-management-software/\1"',
        content
    )
    # Also if still contact?city=
    content = re.sub(
        r'href=["\']contact\?city=([a-z0-9\-]+)["\']',
        r'href="/lead-management-software/\1"',
        content
    )

    # 2. Replace /lead-management-software/ with /lead-management-software
    content = re.sub(
        r'href=["\']/lead-management-software/["\']',
        r'href="/lead-management-software"',
        content
    )

    # 3. In about.html and contact.html, replace href="./#locations" with href="/lead-management-software"
    content = content.replace('href="./#locations"', 'href="/lead-management-software"')
    content = content.replace('href="/#locations"', 'href="/lead-management-software"')

    # 4. In index.html and features.html, ensure clean hub link
    if 'Browse Full All-India 60+ Cities Directory' not in content and 'locations-desc' in content:
        hub_link = '<br /><a href="/lead-management-software" style="color: var(--leads-cyan-dark); font-weight: 700; text-decoration: underline; margin-top: 0.5rem; display: inline-block;">Browse Full All-India 60+ Cities Directory &rarr;</a>'
        content = content.replace(
            'Explore our solutions for Jaipur, Delhi, Mumbai, Bengaluru, Hyderabad, and 40+ cities and regions.',
            f'Explore our solutions for Jaipur, Delhi, Mumbai, Bengaluru, Hyderabad, and 40+ cities and regions. {hub_link}'
        )

    # 5. In main nav links: if "Locations" isn't in nav, add it right after About Us
    if 'href="/lead-management-software"' not in content:
        content = content.replace(
            '<li><a href="about" class="nav-link">About Us</a></li>',
            '<li><a href="about" class="nav-link">About Us</a></li>\n          <li><a href="/lead-management-software" class="nav-link">Locations</a></li>'
        )
        content = content.replace(
            '<li><a href="/about" class="nav-link">About Us</a></li>',
            '<li><a href="/about" class="nav-link">About Us</a></li>\n          <li><a href="/lead-management-software" class="nav-link">Locations</a></li>'
        )
        content = content.replace(
            '<a href="/about" class="nav-link">About Us</a>',
            '<a href="/about" class="nav-link">About Us</a>\n        <a href="/lead-management-software" class="nav-link">Locations</a>'
        )
        content = content.replace(
            '<a href="about" class="nav-link">About Us</a>',
            '<a href="about" class="nav-link">About Us</a>\n        <a href="/lead-management-software" class="nav-link">Locations</a>'
        )

    if content != orig:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated {filename}")
    else:
        print(f"No changes needed for {filename}")
