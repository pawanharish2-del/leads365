import os
import re

GTM_HEAD = """  <!-- Google Tag Manager -->
  <script>(function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':
  new Date().getTime(),event:'gtm.js'});var f=d.getElementsByTagName(s)[0],
  j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
  'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
  })(window,document,'script','dataLayer','GTM-WX3XJT56');</script>
  <!-- End Google Tag Manager -->
  <!-- Google tag (gtag.js) -->
  <script async src="https://www.googletagmanager.com/gtag/js?id=G-6HLFBEL8DG"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){dataLayer.push(arguments);}
    gtag('js', new Date());

    gtag('config', 'G-6HLFBEL8DG');
  </script>"""

GTM_BODY = """  <!-- Google Tag Manager (noscript) -->
  <noscript><iframe src="https://www.googletagmanager.com/ns.html?id=GTM-WX3XJT56"
  height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>
  <!-- End Google Tag Manager (noscript) -->"""

core_files = [
    'index.html',
    'features.html',
    'pricing.html',
    'about.html',
    'contact.html',
    'privacy-policy.html',
    '404.html'
]

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

for filename in core_files:
    file_path = os.path.join(base_dir, filename)
    if not os.path.exists(file_path):
        print(f"Skipping {filename} - not found")
        continue

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    if 'GTM-WX3XJT56' in content:
        print(f"{filename} already has GTM - skipping")
        continue

    # Insert after <head>
    head_pattern = re.compile(r'(<head[^>]*>)', re.IGNORECASE)
    if not head_pattern.search(content):
        print(f"Error: <head> not found in {filename}")
        continue
    content = head_pattern.sub(r'\1\n' + GTM_HEAD, content, count=1)

    # Insert after <body...>
    body_pattern = re.compile(r'(<body[^>]*>)', re.IGNORECASE)
    if not body_pattern.search(content):
        print(f"Error: <body> not found in {filename}")
        continue
    content = body_pattern.sub(r'\1\n' + GTM_BODY, content, count=1)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"Successfully injected GTM & gtag into {filename}")
