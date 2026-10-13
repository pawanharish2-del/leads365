import os
from build_city_pages import CITIES_DATA

def update_sitemap():
    sitemap_path = os.path.join(os.path.dirname(__file__), '..', 'sitemap.xml')

    xml_lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"',
        '        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"',
        '        xsi:schemaLocation="http://www.sitemaps.org/schemas/sitemap/0.9',
        '        http://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd">',
        '',
        '  <!-- Core Pages -->',
        '  <url>',
        '    <loc>https://leads365.in/</loc>',
        '    <lastmod>2026-10-13</lastmod>',
        '    <changefreq>weekly</changefreq>',
        '    <priority>1.00</priority>',
        '  </url>',
        '  <url>',
        '    <loc>https://leads365.in/features</loc>',
        '    <lastmod>2026-10-13</lastmod>',
        '    <changefreq>weekly</changefreq>',
        '    <priority>0.90</priority>',
        '  </url>',
        '  <url>',
        '    <loc>https://leads365.in/pricing</loc>',
        '    <lastmod>2026-10-13</lastmod>',
        '    <changefreq>weekly</changefreq>',
        '    <priority>0.90</priority>',
        '  </url>',
        '  <url>',
        '    <loc>https://leads365.in/about</loc>',
        '    <lastmod>2026-10-13</lastmod>',
        '    <changefreq>monthly</changefreq>',
        '    <priority>0.80</priority>',
        '  </url>',
        '  <url>',
        '    <loc>https://leads365.in/contact</loc>',
        '    <lastmod>2026-10-13</lastmod>',
        '    <changefreq>monthly</changefreq>',
        '    <priority>0.85</priority>',
        '  </url>',
        '  <url>',
        '    <loc>https://leads365.in/privacy-policy</loc>',
        '    <lastmod>2026-10-13</lastmod>',
        '    <changefreq>yearly</changefreq>',
        '    <priority>0.50</priority>',
        '  </url>',
        '',
        '  <!-- Master Cities Directory Hub -->',
        '  <url>',
        '    <loc>https://leads365.in/lead-management-software</loc>',
        '    <lastmod>2026-10-13</lastmod>',
        '    <changefreq>weekly</changefreq>',
        '    <priority>0.90</priority>',
        '  </url>',
        '',
        '  <!-- 60 Dedicated Localized City Landing Pages -->'
    ]

    for c in CITIES_DATA:
        xml_lines.extend([
            '  <url>',
            f'    <loc>https://leads365.in/lead-management-software/{c["slug"]}</loc>',
            '    <lastmod>2026-10-13</lastmod>',
            '    <changefreq>monthly</changefreq>',
            '    <priority>0.80</priority>',
            '  </url>'
        ])

    xml_lines.extend([
        '',
        '</urlset>',
        ''
    ])

    with open(sitemap_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(xml_lines))

    print(f"Successfully generated sitemap.xml with {len(CITIES_DATA) + 7} URLs.")

if __name__ == '__main__':
    update_sitemap()
