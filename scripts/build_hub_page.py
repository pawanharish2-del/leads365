import os
import re
import json
from build_city_pages import CITIES_DATA

def count_visible_words(html_text: str) -> int:
    text = re.sub(r'<script.*?</script>', ' ', html_text, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r'<style.*?</style>', ' ', html_text, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r'<!--.*?-->', ' ', text, flags=re.DOTALL)
    text = re.sub(r'<.*?>', ' ', text)
    words = re.findall(r'\b[A-Za-z0-9\'-]+\b', text)
    return len(words)

def build_hub_page():
    output_path = os.path.join(os.path.dirname(__file__), '..', 'lead-management-software', 'index.html')
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # Group cities
    rajasthan_cities = [c for c in CITIES_DATA if c['state'] == 'Rajasthan']
    other_cities = [c for c in CITIES_DATA if c['state'] != 'Rajasthan']

    # Generate ItemList Schema for all 60 cities
    item_list_elements = []
    for idx, c in enumerate(CITIES_DATA, 1):
        item_list_elements.append({
            "@type": "ListItem",
            "position": idx,
            "name": f"Lead Management Software in {c['name']}",
            "url": f"https://leads365.in/lead-management-software/{c['slug']}"
        })

    # Generate City Cards HTML
    city_cards_html = []
    for c in CITIES_DATA:
        ind_tags = "".join([f'<span class="city-card-tag">{ind[0]}</span>' for ind in c['industries'][:2]])
        badge = '<span class="city-card-badge-hq">Engineering HQ</span>' if c.get('is_hq') else f'<span class="city-card-badge-state">{c["state"]}</span>'
        
        region_group = "rajasthan" if c['state'] == "Rajasthan" else (
            "north" if c['state'] in ["Delhi", "Uttar Pradesh", "Haryana", "Punjab", "Chandigarh", "Uttarakhand"] else (
                "west" if c['state'] in ["Maharashtra", "Gujarat", "Madhya Pradesh"] else (
                    "south" if c['state'] in ["Karnataka", "Telangana", "Tamil Nadu", "Kerala", "Andhra Pradesh"] else "east-central"
                )
            )
        )

        card = f'''
        <article class="hub-city-card" data-name="{c['name'].lower()}" data-state="{c['state'].lower()}" data-region="{region_group}" data-industries="{c['commercial_zones'].lower()}">
          <div class="hub-city-card-header">
            <div>
              <h3 class="hub-city-card-title"><a href="/lead-management-software/{c['slug']}">{c['name']}</a></h3>
              <p class="hub-city-card-subtitle">{c['state']} &bull; {c['commercial_zones'].split(',')[0]}</p>
            </div>
            {badge}
          </div>
          <p class="hub-city-card-desc">
            Optimized for {c['industries'][0][0]} and {c['industries'][1][0]}. Zero lead leakage with automated WhatsApp and masked calling.
          </p>
          <div class="hub-city-card-tags">
            {ind_tags}
          </div>
          <div class="hub-city-card-footer">
            <a href="/lead-management-software/{c['slug']}" class="hub-city-card-link">
              <span>Explore {c['name']} CRM</span>
              <svg width="14" height="14" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M9 5l7 7-7 7"/></svg>
            </a>
          </div>
        </article>
        '''
        city_cards_html.append(card)

    cards_string = "\n".join(city_cards_html)

    # Master hub HTML
    hub_html = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Lead Management Software Across India | 60+ Cities & Regional Hubs | Leads365</title>
  <meta name="description" content="Discover Leads365 Lead Management Software across 60+ commercial cities and industrial corridors in India. Capture multi-channel inquiries, automate WhatsApp follow-ups, and accelerate field sales pipelines with zero lead leakage." />
  <meta name="keywords" content="lead management software india, sales crm cities, crm software jaipur delhi mumbai bengaluru, localized lead management software, b2b sales crm india, real estate crm india, manufacturing crm" />
  <link rel="canonical" href="https://leads365.in/lead-management-software" />
  <meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1" />

  <!-- Open Graph -->
  <meta property="og:title" content="Lead Management Software Across India | 60+ Cities & Regional Hubs | Leads365" />
  <meta property="og:description" content="Empowering sales teams across 60+ Indian commercial hubs with instant lead distribution, WhatsApp Business API workflows, and tamper-proof telecalling analytics." />
  <meta property="og:type" content="website" />
  <meta property="og:url" content="https://leads365.in/lead-management-software" />
  <meta property="og:image" content="https://leads365.in/assets/images/LEADS365_Logo.png" />
  <meta property="og:site_name" content="Leads365" />

  <!-- Twitter Card -->
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:title" content="Lead Management Software Across India | 60+ Cities | Leads365" />
  <meta name="twitter:description" content="High-velocity lead management and sales CRM built for Indian SMBs and enterprises across 60+ cities." />
  <meta name="twitter:image" content="https://leads365.in/assets/images/LEADS365_Logo.png" />

  <!-- Favicon -->
  <link rel="icon" type="image/png" href="/assets/images/favicon.png" />
  <link rel="apple-touch-icon" href="/assets/images/apple-touch-icon.png" />

  <!-- Fonts & Core Stylesheet -->
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Space+Grotesk:wght@500;600;700&display=swap" rel="stylesheet" />
  <link rel="stylesheet" href="/assets/css/style.css?v=2.3" />

  <!-- Structured Data JSON-LD -->
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@graph": [
      {{
        "@type": "Organization",
        "@id": "https://leads365.in/#organization",
        "name": "Leads365",
        "url": "https://leads365.in/",
        "logo": "https://leads365.in/assets/images/LEADS365_Logo.png",
        "description": "Enterprise-grade lead management software and sales acceleration CRM built by Chonexa Technologies.",
        "address": {{
          "@type": "PostalAddress",
          "streetAddress": "Bhamashah Techno Hub, Sansthan Path, Jhalana Gram, Malviya Nagar",
          "addressLocality": "Jaipur",
          "addressRegion": "Rajasthan",
          "postalCode": "302017",
          "addressCountry": "IN"
        }},
        "contactPoint": {{
          "@type": "ContactPoint",
          "telephone": "+91-9876543210",
          "contactType": "sales",
          "areaServed": "IN",
          "availableLanguage": ["English", "Hindi"]
        }}
      }},
      {{
        "@type": "CollectionPage",
        "@id": "https://leads365.in/lead-management-software#collection",
        "url": "https://leads365.in/lead-management-software",
        "name": "Lead Management Software Across India - 60+ City Directory",
        "description": "Complete directory of localized Lead Management Software and Sales CRM solutions tailored for businesses across 60+ Indian commercial hubs.",
        "isPartOf": {{
          "@id": "https://leads365.in/#website"
        }}
      }},
      {{
        "@type": "ItemList",
        "name": "Leads365 Indian Cities Directory",
        "itemListElement": {json.dumps(item_list_elements)}
      }},
      {{
        "@type": "BreadcrumbList",
        "itemListElement": [
          {{
            "@type": "ListItem",
            "position": 1,
            "name": "Home",
            "item": "https://leads365.in/"
          }},
          {{
            "@type": "ListItem",
            "position": 2,
            "name": "Locations",
            "item": "https://leads365.in/lead-management-software"
          }}
        ]
      }},
      {{
        "@type": "FAQPage",
        "mainEntity": [
          {{
            "@type": "Question",
            "name": "What is Leads365 Lead Management Software and which Indian cities are supported?",
            "acceptedAnswer": {{
              "@type": "Answer",
              "text": "Leads365 is a cloud-based Lead Management and Sales CRM platform designed specifically for high-velocity Indian sales operations. It powers businesses across 60+ cities including Jaipur, Delhi NCR, Mumbai, Bengaluru, Hyderabad, Chennai, Kolkata, Pune, Ahmedabad, and 20 major commercial districts in Rajasthan. Features include multi-portal lead sync (IndiaMART, 99acres, Meta Ads), official WhatsApp Business API integration, click-to-dial call masking, and GPS-verified field sales tracking."
            }}
          }},
          {{
            "@type": "Question",
            "name": "How does Leads365 prevent lead leakage for distributed sales teams across India?",
            "acceptedAnswer": {{
              "@type": "Answer",
              "text": "Leads365 ingests inquiries in real-time under 30 seconds via webhooks from all digital marketing channels and B2B portals. Inquiries are automatically assigned via smart round-robin logic to telecallers, and auto-triggered WhatsApp greeting messages with brochures are sent immediately. If an executive does not contact a lead within the configured SLA window (e.g., 15 minutes), the CRM escalates the lead to team managers."
            }}
          }},
          {{
            "@type": "Question",
            "name": "Why is Leads365 more suitable for Indian businesses than foreign enterprise CRMs like Salesforce or HubSpot?",
            "acceptedAnswer": {{
              "@type": "Answer",
              "text": "Global enterprise CRMs are complex, expensive in foreign currencies, lack direct connectors for Indian B2B portals like IndiaMART, TradeIndia, and Justdial, and offer zero native SIM-based telecaller tracking. Leads365 is purpose-built for India with out-of-the-box portal connectors, compliant WhatsApp Business automation, rupee-based transparent pricing, and intuitive Hindi/English telecaller usability requiring zero lengthy training."
            }}
          }},
          {{
            "@type": "Question",
            "name": "Can field sales teams use Leads365 on mobile devices in Tier 1 and Tier 2 cities?",
            "acceptedAnswer": {{
              "@type": "Answer",
              "text": "Yes, Leads365 includes a high-performance Android mobile application equipped with offline caching, GPS-tagged client visit check-ins, meeting voice note transcription, and instant quotation generation, ensuring complete visibility into field operations even in low-connectivity areas."
            }}
          }},
          {{
            "@type": "Question",
            "name": "How fast can an Indian enterprise migrate historical customer data to Leads365?",
            "acceptedAnswer": {{
              "@type": "Answer",
              "text": "Leads365 provides automated historical data migration templates for Excel, CSV, Google Sheets, Zoho, and older legacy systems. Complete data deduplication, contact enrichment, and pipeline stage mapping are executed within 48 hours accompanied by a dedicated implementation manager."
            }}
          }}
        ]
      }}
    ]
  }}
  </script>

  <style>
    /* Master Hub Custom Styles */
    .hub-hero {{
      padding: 5rem 0 3rem;
      background: radial-gradient(circle at top right, rgba(0, 201, 167, 0.08), transparent 45%),
                  radial-gradient(circle at bottom left, rgba(15, 76, 129, 0.05), transparent 45%),
                  var(--leads-surface-light, #f8fafc);
      border-bottom: 1px solid var(--leads-border, #e2e8f0);
    }}
    .hub-hero-badge {{
      display: inline-flex;
      align-items: center;
      gap: 0.5rem;
      padding: 0.4rem 0.9rem;
      border-radius: 999px;
      background: rgba(0, 201, 167, 0.12);
      color: var(--leads-cyan-dark, #008770);
      font-size: 0.82rem;
      font-weight: 700;
      letter-spacing: 0.05em;
      text-transform: uppercase;
      margin-bottom: 1.25rem;
    }}
    .hub-hero-title {{
      font-size: clamp(2.2rem, 4.5vw, 3.4rem);
      font-weight: 800;
      line-height: 1.15;
      color: var(--leads-slate-900, #0f172a);
      margin-bottom: 1.25rem;
      letter-spacing: -0.02em;
    }}
    .hub-hero-title span {{
      color: var(--leads-cyan-dark, #00a887);
    }}
    .hub-hero-desc {{
      font-size: 1.125rem;
      line-height: 1.65;
      color: var(--leads-slate-600, #475569);
      max-width: 860px;
      margin-bottom: 2rem;
    }}

    /* Search & Filter Toolbar */
    .hub-filter-bar {{
      background: #ffffff;
      border: 1px solid var(--leads-border, #e2e8f0);
      border-radius: 16px;
      padding: 1.5rem;
      box-shadow: 0 10px 25px -5px rgba(0,0,0,0.05);
      margin-top: 2rem;
    }}
    .hub-search-input-wrap {{
      position: relative;
      margin-bottom: 1.25rem;
    }}
    .hub-search-input-wrap svg {{
      position: absolute;
      left: 1.25rem;
      top: 50%;
      transform: translateY(-50%);
      color: #94a3b8;
    }}
    .hub-search-input {{
      width: 100%;
      padding: 1rem 1.25rem 1rem 3.2rem;
      font-size: 1.05rem;
      border: 2px solid #e2e8f0;
      border-radius: 12px;
      outline: none;
      transition: all 0.2s ease;
      font-family: inherit;
    }}
    .hub-search-input:focus {{
      border-color: var(--leads-cyan, #00c9a7);
      box-shadow: 0 0 0 4px rgba(0, 201, 167, 0.15);
    }}
    .hub-filter-buttons {{
      display: flex;
      flex-wrap: wrap;
      gap: 0.5rem;
    }}
    .hub-filter-btn {{
      padding: 0.5rem 1rem;
      border-radius: 999px;
      border: 1px solid #cbd5e1;
      background: #f8fafc;
      color: #475569;
      font-size: 0.875rem;
      font-weight: 600;
      cursor: pointer;
      transition: all 0.2s ease;
    }}
    .hub-filter-btn:hover, .hub-filter-btn.active {{
      background: var(--leads-slate-900, #0f172a);
      color: #ffffff;
      border-color: var(--leads-slate-900, #0f172a);
    }}

    /* Hub Cities Grid */
    .hub-grid-section {{
      padding: 4rem 0;
      background: #ffffff;
    }}
    .hub-grid-header {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 2rem;
      flex-wrap: wrap;
      gap: 1rem;
    }}
    .hub-grid-header h2 {{
      font-size: 1.75rem;
      font-weight: 700;
      color: #0f172a;
    }}
    .hub-cities-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
      gap: 1.5rem;
    }}
    .hub-city-card {{
      background: #ffffff;
      border: 1px solid #e2e8f0;
      border-radius: 14px;
      padding: 1.5rem;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      transition: transform 0.2s ease, box-shadow 0.2s ease, border-color 0.2s ease;
    }}
    .hub-city-card:hover {{
      transform: translateY(-4px);
      box-shadow: 0 12px 24px -6px rgba(0,0,0,0.08);
      border-color: #00c9a7;
    }}
    .hub-city-card-header {{
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
      margin-bottom: 0.75rem;
      gap: 0.5rem;
    }}
    .hub-city-card-title {{
      font-size: 1.25rem;
      font-weight: 700;
      margin: 0;
    }}
    .hub-city-card-title a {{
      color: #0f172a;
      text-decoration: none;
      transition: color 0.2s;
    }}
    .hub-city-card-title a:hover {{
      color: #00a887;
    }}
    .hub-city-card-subtitle {{
      font-size: 0.82rem;
      color: #64748b;
      margin-top: 0.25rem;
    }}
    .hub-city-card-badge-hq {{
      background: #ecfdf5;
      color: #059669;
      font-size: 0.72rem;
      font-weight: 700;
      padding: 0.25rem 0.5rem;
      border-radius: 6px;
      white-space: nowrap;
      border: 1px solid #a7f3d0;
    }}
    .hub-city-card-badge-state {{
      background: #f1f5f9;
      color: #475569;
      font-size: 0.72rem;
      font-weight: 600;
      padding: 0.25rem 0.5rem;
      border-radius: 6px;
      white-space: nowrap;
    }}
    .hub-city-card-desc {{
      font-size: 0.88rem;
      color: #475569;
      line-height: 1.5;
      margin-bottom: 1rem;
    }}
    .hub-city-card-tags {{
      display: flex;
      flex-wrap: wrap;
      gap: 0.4rem;
      margin-bottom: 1.25rem;
    }}
    .city-card-tag {{
      font-size: 0.75rem;
      background: #f8fafc;
      border: 1px solid #e2e8f0;
      color: #334155;
      padding: 0.2rem 0.55rem;
      border-radius: 6px;
      font-weight: 500;
    }}
    .hub-city-card-footer {{
      border-top: 1px solid #f1f5f9;
      padding-top: 0.9rem;
    }}
    .hub-city-card-link {{
      display: inline-flex;
      align-items: center;
      gap: 0.4rem;
      color: #008770;
      font-weight: 600;
      font-size: 0.88rem;
      text-decoration: none;
      transition: gap 0.2s;
    }}
    .hub-city-card-link:hover {{
      gap: 0.7rem;
      color: #005f4e;
    }}

    /* In-Depth Content Sections */
    .hub-editorial-section {{
      padding: 4.5rem 0;
      background: #f8fafc;
      border-top: 1px solid #e2e8f0;
    }}
    .editorial-content {{
      max-width: 900px;
      margin: 0 auto;
    }}
    .editorial-content h2 {{
      font-size: 2rem;
      font-weight: 800;
      color: #0f172a;
      margin-top: 2.5rem;
      margin-bottom: 1rem;
      line-height: 1.25;
    }}
    .editorial-content h3 {{
      font-size: 1.45rem;
      font-weight: 700;
      color: #1e293b;
      margin-top: 2rem;
      margin-bottom: 0.75rem;
    }}
    .editorial-content p {{
      font-size: 1.05rem;
      line-height: 1.75;
      color: #334155;
      margin-bottom: 1.25rem;
    }}
    .editorial-content ul {{
      margin-bottom: 1.5rem;
      padding-left: 1.5rem;
    }}
    .editorial-content li {{
      font-size: 1.02rem;
      line-height: 1.7;
      color: #334155;
      margin-bottom: 0.5rem;
    }}
    .editorial-callout {{
      background: #ffffff;
      border-left: 4px solid #00c9a7;
      padding: 1.5rem;
      border-radius: 0 12px 12px 0;
      box-shadow: 0 4px 12px rgba(0,0,0,0.03);
      margin: 2rem 0;
    }}
    .comparison-table-wrap {{
      overflow-x: auto;
      margin: 2rem 0;
      background: #ffffff;
      border-radius: 12px;
      border: 1px solid #e2e8f0;
      box-shadow: 0 4px 12px rgba(0,0,0,0.03);
    }}
    .comparison-table {{
      width: 100%;
      border-collapse: collapse;
      text-align: left;
      font-size: 0.95rem;
    }}
    .comparison-table th {{
      background: #0f172a;
      color: #ffffff;
      padding: 1rem 1.25rem;
      font-weight: 600;
    }}
    .comparison-table td {{
      padding: 1rem 1.25rem;
      border-bottom: 1px solid #f1f5f9;
      color: #334155;
    }}
    .comparison-table tr:last-child td {{
      border-bottom: none;
    }}
    .comparison-table tr:hover td {{
      background: #f8fafc;
    }}

    /* Hub FAQ Accordion */
    .hub-faq-section {{
      padding: 4.5rem 0;
      background: #ffffff;
      border-top: 1px solid #e2e8f0;
    }}
    .hub-faq-wrap {{
      max-width: 860px;
      margin: 0 auto;
    }}
    .hub-faq-item {{
      border: 1px solid #e2e8f0;
      border-radius: 12px;
      margin-bottom: 1rem;
      overflow: hidden;
      transition: all 0.2s ease;
    }}
    .hub-faq-item.active {{
      border-color: #00c9a7;
      box-shadow: 0 4px 12px rgba(0, 201, 167, 0.08);
    }}
    .hub-faq-btn {{
      width: 100%;
      padding: 1.25rem 1.5rem;
      background: #ffffff;
      border: none;
      display: flex;
      justify-content: space-between;
      align-items: center;
      cursor: pointer;
      font-size: 1.05rem;
      font-weight: 700;
      color: #0f172a;
      text-align: left;
    }}
    .hub-faq-body {{
      display: none;
      padding: 0 1.5rem 1.5rem;
      color: #475569;
      font-size: 0.98rem;
      line-height: 1.65;
    }}
    .hub-faq-item.active .hub-faq-body {{
      display: block;
    }}
    .hub-faq-item.active svg {{
      transform: rotate(180deg);
    }}

    /* Breadcrumbs */
    .hub-breadcrumbs {{
      padding: 1rem 0;
      background: #ffffff;
      border-bottom: 1px solid #f1f5f9;
      font-size: 0.85rem;
      color: #64748b;
    }}
    .hub-breadcrumbs a {{
      color: #008770;
      text-decoration: none;
    }}
    .hub-breadcrumbs span {{
      margin: 0 0.5rem;
    }}
  </style>
</head>

<body>
  <!-- Header / Navigation Bar -->
  <header class="site-header">
    <div class="container header-container">
      <a href="/" class="brand-logo" aria-label="Leads365 Home">
        <img src="/assets/images/LEADS365_Logo.png" alt="Leads365 Logo" class="brand-logo-img" />
      </a>
      <nav class="main-nav" aria-label="Main Navigation">
        <ul class="nav-links">
          <li><a href="/" class="nav-link">Home</a></li>
          <li><a href="/features" class="nav-link">Features</a></li>
          <li><a href="/pricing" class="nav-link">Pricing</a></li>
          <li><a href="/about" class="nav-link">About Us</a></li>
          <li><a href="/lead-management-software" class="nav-link active">Locations</a></li>
          <li><a href="/contact" class="nav-link">Contact</a></li>
        </ul>
      </nav>
      <div class="header-cta-wrap">
        <a href="/contact" class="btn btn-outline">Book 15-Min Demo</a>
        <a href="https://app.leads365.in/signup" class="btn btn-primary" target="_blank" rel="noopener">Start Free Trial</a>
      </div>
      <button class="mobile-menu-btn" aria-label="Toggle navigation menu">
        <span class="hamburger-line"></span>
        <span class="hamburger-line"></span>
        <span class="hamburger-line"></span>
      </button>
    </div>
  </header>

  <!-- Breadcrumbs -->
  <nav class="hub-breadcrumbs" aria-label="Breadcrumb">
    <div class="container">
      <a href="/">Home</a>
      <span>&rsaquo;</span>
      <span style="color: #0f172a; font-weight: 600;">Lead Management Software Across India</span>
    </div>
  </nav>

  <!-- Hero Section -->
  <section class="hub-hero">
    <div class="container">
      <div class="hub-hero-badge">
        <svg width="14" height="14" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M5.05 4.05a7 7 0 119.9 9.9L10 18.9l-4.95-4.95a7 7 0 010-9.9zM10 11a2 2 0 100-4 2 2 0 000 4z" clip-rule="evenodd"/></svg>
        60+ Cities & Regional Industrial Corridors
      </div>
      <h1 class="hub-hero-title">
        Lead Management Software Across India: <span>60+ Dedicated Commercial Hubs</span>
      </h1>
      <p class="hub-hero-desc">
        Stop losing high-value customer inquiries to spreadsheet chaos, delayed telecaller responses, and missing WhatsApp follow-ups. Leads365 delivers zero-lead-leakage sales automation built specifically for high-velocity Indian business environments—from Jaipur's manufacturing zones and Delhi NCR's corporate towers to Bengaluru's tech parks and Mumbai's financial epicenters.
      </p>

      <!-- Live Search & Filtering Interface -->
      <div class="hub-filter-bar">
        <div class="hub-search-input-wrap">
          <svg width="20" height="20" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/></svg>
          <input type="text" id="citySearchInput" class="hub-search-input" placeholder="Search by city name, state, or industry (e.g., Jaipur, Real Estate, Pune, Furniture, Pharma)..." aria-label="Search city or industry" />
        </div>
        <div class="hub-filter-buttons">
          <button class="hub-filter-btn active" data-filter="all">All Cities (60)</button>
          <button class="hub-filter-btn" data-filter="rajasthan">Rajasthan (20)</button>
          <button class="hub-filter-btn" data-filter="north">Delhi NCR & North (13)</button>
          <button class="hub-filter-btn" data-filter="west">West & Central (13)</button>
          <button class="hub-filter-btn" data-filter="south">South India (11)</button>
          <button class="hub-filter-btn" data-filter="east-central">East & North-East (3)</button>
        </div>
      </div>
    </div>
  </section>

  <!-- Interactive Cities Directory Grid -->
  <section class="hub-grid-section">
    <div class="container">
      <div class="hub-grid-header">
        <div>
          <h2>Browse Dedicated City CRM Portals</h2>
          <p style="color: #64748b; font-size: 0.95rem; margin-top: 0.25rem;">Select your local commercial zone to review tailored industry playbooks, local pain point breakdowns, and rapid onboarding roadmaps.</p>
        </div>
        <div id="cityResultCount" style="font-weight: 600; color: #008770; font-size: 0.95rem;">
          Showing 60 locations
        </div>
      </div>

      <div class="hub-cities-grid" id="citiesGridContainer">
        {cards_string}
      </div>
    </div>
  </section>

  <!-- In-Depth Educational Guide (1600+ Words Total) -->
  <section class="hub-editorial-section">
    <div class="container">
      <div class="editorial-content">
        <h2>The State of Lead Management & Sales Operations Across India</h2>
        <p>
          India’s commercial landscape is undergoing the fastest digital commerce transformation in its history. From tier-1 metropolises like Delhi NCR, Mumbai, and Bengaluru to dynamic tier-2 and tier-3 industrial manufacturing hubs like Jaipur, Jodhpur, Surat, Ludhiana, and Coimbatore, enterprises are allocating unprecedented capital toward digital advertising. Businesses generate customer inquiries simultaneously through Meta Ads (Facebook & Instagram Lead Forms), Google Search, IndiaMART B2B catalogs, TradeIndia, Justdial, Magicbricks, 99acres, and organic search portals.
        </p>
        <p>
          Yet, despite spending hundreds of thousands of rupees every month on inbound marketing campaigns, sales directors across India consistently report a startling operational paradox: <strong>lead conversion rates remain stagnant between 2% and 4%</strong>. The root cause is almost never lead quality—it is lead leakage, sluggish telecalling response times, unstructured WhatsApp chats on personal employee smartphones, and lack of real-time management visibility.
        </p>

        <div class="editorial-callout">
          <h4 style="margin: 0 0 0.5rem; color: #0f172a; font-size: 1.15rem;">The 15-Minute Rule of Indian Inbound Sales</h4>
          <p style="margin: 0; font-size: 0.95rem; color: #475569;">
            According to national B2B and real estate conversion benchmarks across India, inquiries contacted within <strong>5 to 15 minutes</strong> of form submission demonstrate a <strong>391% higher qualification rate</strong> than leads dialed after 2 hours. Inquiries left unaddressed overnight convert at less than 0.5% because prospective buyers have already engaged with faster competitors.
          </p>
        </div>

        <h2>Why Generic Global Enterprise CRMs Fail Inside Indian Sales Teams</h2>
        <p>
          Over the past decade, Indian enterprises invested heavily in enterprise CRM platforms developed primarily for North American and Western European B2B environments—most notably Salesforce, HubSpot, and Zoho. While these platforms excel at managing complex multi-month enterprise contract renewals through corporate email exchanges, they frequently fail when deployed in fast-paced, high-volume Indian sales operations.
        </p>

        <div class="comparison-table-wrap">
          <table class="comparison-table">
            <thead>
              <tr>
                <th>Operational Dimension</th>
                <th>Global Enterprise CRMs (Salesforce / HubSpot)</th>
                <th>Leads365 Indian Sales CRM</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td><strong>Lead Ingestion Latency</strong></td>
                <td>Requires expensive third-party Zapier/Make middleware; 10-30 minute delays common.</td>
                <td><strong>Sub-30-second native webhooks</strong> for IndiaMART, TradeIndia, 99acres, Meta, & Justdial.</td>
              </tr>
              <tr>
                <td><strong>WhatsApp Business API</strong></td>
                <td>Add-on marketplace plugins costing extra USD/month with complex technical setup.</td>
                <td><strong>Deep native WhatsApp automation</strong>: instant catalog sharing, PDF quotations, & chat logs.</td>
              </tr>
              <tr>
                <td><strong>Telecalling & Call Masking</strong></td>
                <td>Requires foreign VoIP services like Twilio with high minute tariffs and telecom friction.</td>
                <td><strong>Native Android SIM tracking & Cloud Telephony</strong>: masked calling, call recording, & analytics.</td>
              </tr>
              <tr>
                <td><strong>Field Sales Mobility</strong></td>
                <td>Heavy, data-intensive web apps unusable in patchy 4G industrial zones.</td>
                <td><strong>Lightweight mobile app</strong> with offline check-ins, geo-tagged visits, & instant billing sync.</td>
              </tr>
              <tr>
                <td><strong>Telecaller Adoption Curve</strong></td>
                <td>Steep learning curve with dozens of mandatory fields; telecallers abandon CRM for Excel.</td>
                <td><strong>Clean, zero-training interface</strong>; telecallers master visual disposition workflows in 15 minutes.</td>
              </tr>
              <tr>
                <td><strong>Pricing & Currency</strong></td>
                <td>Billed in foreign USD with fluctuating exchange rates, seat tiers, and mandatory consultation fees.</td>
                <td><strong>Transparent INR pricing</strong> with zero hidden per-connector charges or forced consulting.</td>
              </tr>
            </tbody>
          </table>
        </div>

        <h2>Regional Industrial Clusters: How Leads365 Delivers Localized CRM Workflows</h2>
        <p>
          A lead management platform cannot succeed with a generic, one-size-fits-all approach. Sales dynamics differ fundamentally between an export furniture manufacturer in Jodhpur's Boranada SEZ, a luxury real estate brokerage along Jaipur’s Ajmer Road, an electronics contract assembly firm in Noida, and a SaaS scale-up in Bengaluru’s Bellandur tech corridor. Leads365 provides pre-configured vertical blueprints tailored to India's regional economies:
        </p>

        <h3>1. Real Estate, Commercial Townships & Plot Developers</h3>
        <p>
          In rapid-expansion corridors across Jaipur, Delhi NCR (Gurugram, Noida, Faridabad), Mumbai Metropolitan Region (Thane, Navi Mumbai), Bengaluru, and Hyderabad, property developers handle massive lead surges during weekend campaigns. Leads365 captures inquiries simultaneously from 99acres, Magicbricks, Housing.com, and Meta Ads. Inquiries are instantly distributed to property advisors based on budget tier and project location. The CRM automatically dispatches digital brochures and floor plans via WhatsApp, schedules site visits with Google Calendar sync, and alerts executives when a prospective buyer arrives on location.
        </p>

        <h3>2. Manufacturing, Industrial Machinery & B2B Exporters</h3>
        <p>
          India’s industrial heartlands—including Sitapura and VKI in Jaipur, Boranada in Jodhpur, Sukher in Udaipur, Bhosari and Chakan in Pune, Vatva and Sanand in Ahmedabad, and Peenya in Bengaluru—depend on high-value B2B buyer inquiries. Leads365 connects directly with IndiaMART Buyer APIs, TradeIndia, and inbound RFQ mailboxes. It calculates custom GST pricing, generates professional PDF quotations directly inside WhatsApp, and tracks stage-by-stage sample dispatch milestones, ensuring multi-lakh-rupee orders are closed before competitors respond.
        </p>

        <h3>3. Professional Services, Healthcare Networks & Education Institutes</h3>
        <p>
          From NEET/JEE coaching academies in Kota, Sikar, and Jaipur to corporate diagnostic clinic networks like Medical365 in tier-1 metropolises, high-volume inquiry qualification requires absolute data privacy and rapid response. Leads365 enables counselor call recording, automated demo class reminders via SMS and WhatsApp, and lead scoring based on student or patient urgency. Role-based security guarantees that prospective client phone numbers and personal medical inquiries cannot be exported or leaked by departing staff.
        </p>

        <h3>4. Gems, Jewellery, Handicrafts & Modern Retail Networks</h3>
        <p>
          In luxury retail centers across Jaipur, Surat, Mumbai, and Kolkata, high-ticket retail inquiries require personalized relationship management. Leads365 allows retail staff to send high-resolution digital product lookbooks over verified WhatsApp Business accounts, track digital showroom appointment walk-ins, and schedule anniversary or festive seasonal repeat-purchase reminders with zero manual tracking.
        </p>

        <h2>Architectural Pillars of Leads365 Zero-Lead-Leakage System</h2>
        <p>
          To ensure reliable performance across 60+ cities and hundreds of thousands of concurrent daily inquiries, Leads365 is built upon a fault-tolerant cloud architecture hosted within Tier-4 Indian data centers:
        </p>
        <ul>
          <li><strong>Universal Inbound Webhook Ingestion Engine:</strong> Ingests structured and unstructured payloads from Meta Ads, Google Ads Webhooks, IndiaMART, Justdial, TradeIndia, and WordPress forms in under 300 milliseconds.</li>
          <li><strong>Intelligent Lead Distribution Matrix:</strong> Configurable round-robin, capability-weighted, geographic-proximity, or language-matched lead assignment ensures inquiries reach the right executive immediately.</li>
          <li><strong>Telecaller Performance & Disposition Analytics:</strong> Real-time telecalling dashboards track total dials, connected talk time, first-call resolution rate, and call recordings. Supervisors can identify bottleneck executives in minutes.</li>
          <li><strong>Official Meta WhatsApp Business Cloud API:</strong> Pre-approved HSM message templates, interactive button responses, automated catalog sharing, and centralized team inbox eliminate employee reliance on personal SIM cards.</li>
          <li><strong>Enterprise Data Shielding & Call Masking:</strong> Executive phone dials are bridged through secure virtual telecommunication nodes. Telecallers connect directly to prospects without exposing client numbers, completely preventing customer poaching.</li>
        </ul>

        <h2>Rapid 48-Hour Implementation & Data Migration Roadmap</h2>
        <p>
          Transitioning to a modern sales CRM should never disrupt daily business operations. While legacy enterprise platforms require three to six months of painful system configuration and expensive systems integrators, Leads365 adheres to an agile 48-hour onboarding methodology:
        </p>
        <ul>
          <li><strong>Hour 0 - 12 (Data Cleansing & Deduplication):</strong> Import historical customer databases from Excel, CSV, Google Sheets, or previous CRM exports. Our ingestion algorithms normalize phone numbers (+91), eliminate duplicates, and preserve call history tags.</li>
          <li><strong>Hour 12 - 24 (Connector Activation):</strong> Direct API integration with your Meta Ads accounts, Google Ads webhooks, IndiaMART seller tokens, and website forms. Real-time test leads verify sub-30-second pipeline delivery.</li>
          <li><strong>Hour 24 - 36 (Team Hierarchy & WhatsApp Configuration):</strong> Configure user roles, regional territory boundaries, automated WhatsApp templates, and manager notification webhooks.</li>
          <li><strong>Hour 36 - 48 (Live Team Onboarding & Go-Live):</strong> A 45-minute interactive onboarding session trains telecallers, sales reps, and managers. Your team commences real-time dialing with dedicated live WhatsApp support.</li>
        </ul>
      </div>
    </div>
  </section>

  <!-- Master FAQ Accordion Section -->
  <section class="hub-faq-section">
    <div class="container">
      <div class="hub-faq-wrap">
        <div style="text-align: center; margin-bottom: 2.5rem;">
          <h2 style="font-size: 2rem; font-weight: 800; color: #0f172a;">Frequently Asked Questions</h2>
          <p style="color: #64748b; font-size: 1rem; margin-top: 0.5rem;">Everything you need to know about deploying Leads365 across Indian sales teams.</p>
        </div>

        <div class="hub-faq-item active">
          <button class="hub-faq-btn" onclick="toggleFaq(this)">
            <span>What makes Leads365 the best Lead Management Software for Indian businesses?</span>
            <svg width="20" height="20" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/></svg>
          </button>
          <div class="hub-faq-body">
            Unlike foreign enterprise CRMs designed for email-first workflows, Leads365 is purpose-built for India's high-speed sales dynamics. It features instant multi-channel lead capture (IndiaMART, TradeIndia, 99acres, Meta Ads), official WhatsApp Business API automation, click-to-dial call masking, Android SIM tracking, and zero-training simplicity—backed by transparent INR pricing.
          </div>
        </div>

        <div class="hub-faq-item">
          <button class="hub-faq-btn" onclick="toggleFaq(this)">
            <span>Can Leads365 capture leads simultaneously from Meta Ads, Google Ads, and B2B portals?</span>
            <svg width="20" height="20" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/></svg>
          </button>
          <div class="hub-faq-body">
            Yes. Leads365 connects directly with Meta Ads (Instant Forms), Google Search Webhooks, IndiaMART Push APIs, TradeIndia, Justdial, Magicbricks, 99acres, Housing.com, and custom website forms. All inquiries are ingested into your unified visual Kanban pipeline in under 30 seconds.
          </div>
        </div>

        <div class="hub-faq-item">
          <button class="hub-faq-btn" onclick="toggleFaq(this)">
            <span>How does the WhatsApp Business API integration work?</span>
            <svg width="20" height="20" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/></svg>
          </button>
          <div class="hub-faq-body">
            Leads365 integrates with Meta's official WhatsApp Business Cloud API. When an inquiry is captured, the CRM immediately triggers an automated, branded greeting message with product catalogs, brochures, or booking links. All incoming and outgoing WhatsApp messages are mirrored in the client record for full manager visibility.
          </div>
        </div>

        <div class="hub-faq-item">
          <button class="hub-faq-btn" onclick="toggleFaq(this)">
            <span>Can departing sales executives download or steal our company's customer data?</span>
            <svg width="20" height="20" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/></svg>
          </button>
          <div class="hub-faq-body">
            No. Leads365 implements strict enterprise role-based security. Sales executives cannot export contact lists or customer databases. Furthermore, our optional call-masking technology conceals prospective customer phone numbers during telecaller outreach, ensuring proprietary company leads remain protected.
          </div>
        </div>

        <div class="hub-faq-item">
          <button class="hub-faq-btn" onclick="toggleFaq(this)">
            <span>How does Leads365 support field sales representatives visiting clients in person?</span>
            <svg width="20" height="20" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/></svg>
          </button>
          <div class="hub-faq-body">
            Our lightweight mobile app allows field sales representatives to check in at client locations with GPS timestamp verification, record meeting notes via voice-to-text, generate on-the-spot price estimates, and update deal pipeline stages even when working in low-connectivity industrial belts.
          </div>
        </div>

        <div class="hub-faq-item">
          <button class="hub-faq-btn" onclick="toggleFaq(this)">
            <span>How long does historical customer data migration and staff training take?</span>
            <svg width="20" height="20" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/></svg>
          </button>
          <div class="hub-faq-body">
            Full data migration from Excel, CSV, Google Sheets, Zoho, or older CRM systems is completed within 48 hours. Because Leads365 is designed with an intuitive, clutter-free user interface, sales executives and telecallers master the platform after a single 45-minute live onboarding session.
          </div>
        </div>
      </div>
    </div>
  </section>

  <!-- Bottom CTA Banner -->
  <section class="cta-section" style="background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%); color: #ffffff; padding: 5rem 0; text-align: center;">
    <div class="container">
      <div style="max-width: 760px; margin: 0 auto;">
        <h2 style="font-size: clamp(2rem, 3.5vw, 2.75rem); font-weight: 800; line-height: 1.2; margin-bottom: 1.25rem;">
          Accelerate Your Sales Team in Any Indian City Today
        </h2>
        <p style="font-size: 1.15rem; color: #94a3b8; line-height: 1.6; margin-bottom: 2.25rem;">
          Join forward-thinking businesses across Jaipur, Delhi NCR, Mumbai, Bengaluru, and 60+ commercial centers that rely on Leads365 to eliminate lead leakage, cut response times to under 60 seconds, and boost deal closure rates.
        </p>
        <div style="display: flex; gap: 1rem; justify-content: center; flex-wrap: wrap;">
          <a href="/contact" class="btn btn-primary" style="padding: 0.9rem 2rem; font-size: 1.05rem; background: #00c9a7; border-color: #00c9a7; color: #0f172a; font-weight: 700;">
            Schedule a 15-Minute Live Demo
          </a>
          <a href="https://app.leads365.in/signup" class="btn btn-outline" style="padding: 0.9rem 2rem; font-size: 1.05rem; border-color: rgba(255,255,255,0.3); color: #ffffff;" target="_blank" rel="noopener">
            Start 14-Day Free Trial
          </a>
        </div>
        <p style="font-size: 0.85rem; color: #64748b; margin-top: 1.25rem;">
          No credit card required &bull; 48-Hour Go-Live Guarantee &bull; Dedicated Implementation Specialist
        </p>
      </div>
    </div>
  </section>

  <!-- Global Footer -->
  <footer class="site-footer">
    <div class="container">
      <div class="footer-grid">
        <div class="footer-brand-col">
          <a href="/" class="footer-logo-wrap" aria-label="Leads365 Home">
            <img src="/assets/images/LEADS365_Logo.png" alt="Leads365 Logo" class="footer-logo-img" />
          </a>
          <p class="footer-about-text">
            <strong>Leads365 (leads365.in)</strong> is an all-in-one Cloud Lead Management and Sales CRM software built by <strong>Chonexa Technologies</strong> to help modern businesses capture inquiries, eliminate lead leakage, and close deals effortlessly.
          </p>
        </div>

        <div class="footer-links-col">
          <h4 class="footer-col-title">Core Modules</h4>
          <ul class="footer-links-list">
            <li><a href="/features#capture">Multi-Channel Lead Capture</a></li>
            <li><a href="/features#distribution">Smart Round-Robin Routing</a></li>
            <li><a href="/features#whatsapp">WhatsApp Business API</a></li>
            <li><a href="/features#pipeline">Visual Deal Pipelines</a></li>
            <li><a href="/features#telephony">Masked Calling & Dialing</a></li>
            <li><a href="/features#security">Data Shielding & Access</a></li>
          </ul>
        </div>

        <div class="footer-links-col">
          <h4 class="footer-col-title">Company & Resources</h4>
          <ul class="footer-links-list">
            <li><a href="/about">About Leads365</a></li>
            <li><a href="/pricing">Pricing Plans</a></li>
            <li><a href="/lead-management-software">Locations We Serve (60+ Cities)</a></li>
            <li><a href="/contact">Book Product Demo</a></li>
            <li><a href="/privacy-policy">Privacy & Security Policy</a></li>
            <li><a href="/terms-of-service">Terms of Service</a></li>
          </ul>
        </div>

        <div class="footer-contact-col">
          <h4 class="footer-col-title">Engineering Headquarters</h4>
          <p class="footer-contact-text">
            <strong>Chonexa Technologies Private Limited</strong><br />
            Bhamashah Techno Hub, Sansthan Path,<br />
            Jhalana Gram, Malviya Nagar,<br />
            Jaipur, Rajasthan 302017, India
          </p>
          <div class="footer-contact-links">
            <a href="mailto:support@leads365.in" class="footer-contact-link">support@leads365.in</a>
            <a href="tel:+919876543210" class="footer-contact-link">+91 98765 43210</a>
          </div>
        </div>
      </div>

      <div class="footer-bottom">
        <p>&copy; 2026 Leads365 (Chonexa Technologies Pvt. Ltd.). All rights reserved.</p>
        <div class="footer-bottom-links">
          <a href="/privacy-policy">Privacy Policy</a>
          <a href="/terms-of-service">Terms of Service</a>
          <a href="/sitemap.xml">XML Sitemap</a>
        </div>
      </div>
    </div>
  </footer>

  <!-- Search & Filter JavaScript -->
  <script>
    function toggleFaq(btn) {{
      const item = btn.parentElement;
      item.classList.toggle('active');
    }}

    document.addEventListener('DOMContentLoaded', function() {{
      const searchInput = document.getElementById('citySearchInput');
      const filterBtns = document.querySelectorAll('.hub-filter-btn');
      const cards = document.querySelectorAll('.hub-city-card');
      const countEl = document.getElementById('cityResultCount');

      let currentFilter = 'all';

      function filterCities() {{
        const query = searchInput.value.toLowerCase().trim();
        let visibleCount = 0;

        cards.forEach(card => {{
          const name = card.getAttribute('data-name');
          const state = card.getAttribute('data-state');
          const region = card.getAttribute('data-region');
          const industries = card.getAttribute('data-industries');

          const matchesSearch = !query || name.includes(query) || state.includes(query) || industries.includes(query);
          const matchesFilter = currentFilter === 'all' || region === currentFilter;

          if (matchesSearch && matchesFilter) {{
            card.style.display = 'flex';
            visibleCount++;
          }} else {{
            card.style.display = 'none';
          }}
        }});

        countEl.textContent = `Showing ${{visibleCount}} locations`;
      }}

      if (searchInput) {{
        searchInput.addEventListener('input', filterCities);
      }}

      filterBtns.forEach(btn => {{
        btn.addEventListener('click', function() {{
          filterBtns.forEach(b => b.classList.remove('active'));
          this.classList.add('active');
          currentFilter = this.getAttribute('data-filter');
          filterCities();
        }});
      }});
    }});
  </script>
</body>
</html>'''

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(hub_html)

    words = count_visible_words(hub_html)
    print(f"Generated lead-management-software/index.html with {words} visible words.")

if __name__ == '__main__':
    build_hub_page()
