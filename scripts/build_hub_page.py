import os
import re
import json
from build_city_pages import CITIES_DATA, GTM_HEAD_SNIPPET, GTM_BODY_SNIPPET

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

    # Generate ItemList Schema for all 60 cities
    item_list_elements = []
    for idx, c in enumerate(CITIES_DATA, 1):
        item_list_elements.append({
            "@type": "ListItem",
            "position": idx,
            "name": f"Lead Management Software in {c['name']}",
            "url": f"https://leads365.in/lead-management-software/{c['slug']}"
        })

    # Generate Quick 1-Tap Pills HTML
    pills_html = []
    for c in CITIES_DATA:
        region_group = "rajasthan" if c['state'] == "Rajasthan" else (
            "north" if c['state'] in ["Delhi", "Uttar Pradesh", "Haryana", "Punjab", "Chandigarh", "Uttarakhand"] else (
                "west" if c['state'] in ["Maharashtra", "Gujarat", "Madhya Pradesh"] else (
                    "south" if c['state'] in ["Karnataka", "Telangana", "Tamil Nadu", "Kerala", "Andhra Pradesh"] else "east-central"
                )
            )
        )
        pill = f'''<a href="/lead-management-software/{c['slug']}" class="hub-pill" data-name="{c['name'].lower()}" data-state="{c['state'].lower()}" data-region="{region_group}">
          <svg width="12" height="12" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M5.05 4.05a7 7 0 119.9 9.9L10 18.9l-4.95-4.95a7 7 0 010-9.9zM10 11a2 2 0 100-4 2 2 0 000 4z" clip-rule="evenodd"/></svg>
          <span>{c['name']}</span>
        </a>'''
        pills_html.append(pill)
    all_pills_string = "\n".join(pills_html)

    # Generate City Cards HTML
    city_cards_html = []
    for c in CITIES_DATA:
        ind_tags = "".join([f'<span class="hub-tag">{ind[0]}</span>' for ind in c['industries'][:2]])
        badge = '<span class="hub-badge-hq">Engineering HQ</span>' if c.get('is_hq') else f'<span class="hub-badge-state">{c["state"]}</span>'
        
        region_group = "rajasthan" if c['state'] == "Rajasthan" else (
            "north" if c['state'] in ["Delhi", "Uttar Pradesh", "Haryana", "Punjab", "Chandigarh", "Uttarakhand"] else (
                "west" if c['state'] in ["Maharashtra", "Gujarat", "Madhya Pradesh"] else (
                    "south" if c['state'] in ["Karnataka", "Telangana", "Tamil Nadu", "Kerala", "Andhra Pradesh"] else "east-central"
                )
            )
        )

        card = f'''
        <article class="hub-card" data-name="{c['name'].lower()}" data-state="{c['state'].lower()}" data-region="{region_group}" data-industries="{c['commercial_zones'].lower()}">
          <div class="hub-card-top">
            <div>
              <h3 class="hub-card-title"><a href="/lead-management-software/{c['slug']}">{c['name']}</a></h3>
              <p class="hub-card-location">
                <svg width="12" height="12" fill="var(--leads-cyan)" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M5.05 4.05a7 7 0 119.9 9.9L10 18.9l-4.95-4.95a7 7 0 010-9.9zM10 11a2 2 0 100-4 2 2 0 000 4z" clip-rule="evenodd"/></svg>
                <span>{c['commercial_zones'].split(',')[0].strip()} &bull; {c['state']}</span>
              </p>
            </div>
            {badge}
          </div>
          <p class="hub-card-desc">
            Optimized for {c['industries'][0][0]} and {c['industries'][1][0]}. Captures multi-portal leads in under 3 seconds with SIM call recording and automated WhatsApp quotation decks.
          </p>
          <div class="hub-card-tags">
            {ind_tags}
          </div>
          <div class="hub-card-footer">
            <a href="/lead-management-software/{c['slug']}" class="hub-card-link">
              <span>Explore {c['name']} Sales CRM</span>
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
{GTM_HEAD_SNIPPET}
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Lead Management Software Across India | 60+ Cities & Regional Hubs | Leads365</title>
  <meta name="description" content="Discover Leads365 Lead Management Software across 60+ commercial cities and industrial corridors in India. Capture multi-channel inquiries, automate WhatsApp follow-ups, and accelerate field sales pipelines with zero lead leakage." />
  <meta name="keywords" content="lead management software india, sales crm cities, crm software jaipur delhi mumbai bengaluru, localized lead management software, b2b sales crm india, real estate crm india, manufacturing crm" />
  <meta name="author" content="Chonexa Technologies" />
  <link rel="canonical" href="https://leads365.in/lead-management-software" />
  <meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1" />

  <!-- Open Graph -->
  <meta property="og:title" content="Lead Management Software Across India | 60+ Cities & Regional Hubs | Leads365" />
  <meta property="og:description" content="Empowering sales teams across 60+ Indian commercial hubs with instant lead distribution, WhatsApp Business API workflows, and tamper-proof telecalling analytics." />
  <meta property="og:type" content="website" />
  <meta property="og:url" content="https://leads365.in/lead-management-software" />
  <meta property="og:image" content="https://leads365.in/assets/images/LEADS365_Logo.png" />
  <meta property="og:site_name" content="Leads365" />
  <meta property="og:locale" content="en_IN" />

  <!-- Twitter Card -->
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:title" content="Lead Management Software Across India | 60+ Cities | Leads365" />
  <meta name="twitter:description" content="High-velocity lead management and sales CRM built for Indian SMBs and enterprises across 60+ cities." />
  <meta name="twitter:image" content="https://leads365.in/assets/images/LEADS365_Logo.png" />

  <!-- Google Fonts: Lora (Editorial Serif) & Plus Jakarta Sans (Modern Sans-Serif) -->
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Lora:ital,wght@0,500;0,600;0,700;1,400;1,600&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet" />

  <!-- Favicon -->
  <link rel="icon" type="image/png" href="/assets/images/favicon.png" />
  <link rel="apple-touch-icon" href="/assets/images/apple-touch-icon.png" />

  <!-- Core Shared Stylesheet -->
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
          "telephone": "+91-77919-10007",
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
    /* --------------------------------------------------------------------------
       MASTER DIRECTORY HERO & SEARCH ENHANCEMENTS
       -------------------------------------------------------------------------- */
    .hub-hero-banner {{
      padding: clamp(3.5rem, 5vw, 5rem) 0 3rem;
      background: radial-gradient(circle at 85% 15%, rgba(0, 229, 255, 0.08) 0%, transparent 45%),
                  radial-gradient(circle at 10% 85%, rgba(139, 32, 238, 0.06) 0%, transparent 45%),
                  var(--bg-surface);
      border-bottom: 1px solid var(--border-light);
      position: relative;
    }}
    .hub-hero-headline {{
      font-family: var(--font-serif);
      font-size: clamp(2.2rem, 4.2vw, 3.25rem);
      font-weight: 700;
      line-height: 1.18;
      color: var(--text-dark);
      margin-bottom: 1.25rem;
      letter-spacing: -0.02em;
    }}
    .hub-hero-subhead {{
      font-size: clamp(1.05rem, 1.8vw, 1.2rem);
      line-height: 1.7;
      color: var(--text-muted);
      max-width: 860px;
      margin-bottom: 2rem;
    }}

    /* Search & Filter Bar */
    .hub-search-box {{
      background: var(--bg-card);
      border: 1px solid var(--border-medium);
      border-radius: var(--radius-md);
      padding: 1.5rem;
      box-shadow: 0 12px 32px -8px rgba(11, 25, 76, 0.08);
      margin-top: 1.5rem;
    }}
    .hub-search-input-group {{
      position: relative;
      margin-bottom: 1.25rem;
    }}
    .hub-search-input-group svg {{
      position: absolute;
      left: 1.25rem;
      top: 50%;
      transform: translateY(-50%);
      color: var(--text-light);
      pointer-events: none;
    }}
    .hub-search-field {{
      width: 100%;
      padding: 1rem 1.25rem 1rem 3.4rem;
      font-size: 1.05rem;
      border: 2px solid var(--border-medium);
      border-radius: var(--radius-sm);
      outline: none;
      font-family: var(--font-sans);
      transition: all 0.25s ease;
      background: #FFFFFF;
      color: var(--text-dark);
    }}
    .hub-search-field:focus {{
      border-color: var(--leads-cyan);
      box-shadow: 0 0 0 4px rgba(0, 184, 217, 0.15);
    }}
    .hub-filter-tabs {{
      display: flex;
      flex-wrap: wrap;
      gap: 0.5rem;
      align-items: center;
    }}
    .hub-filter-tab {{
      padding: 0.55rem 1.15rem;
      border-radius: 999px;
      border: 1px solid var(--border-medium);
      background: var(--bg-surface);
      color: var(--text-body);
      font-size: 0.88rem;
      font-weight: 600;
      cursor: pointer;
      transition: all 0.2s ease;
      display: inline-flex;
      align-items: center;
      gap: 0.4rem;
    }}
    .hub-filter-tab:hover, .hub-filter-tab.active {{
      background: var(--leads-navy);
      color: #FFFFFF;
      border-color: var(--leads-navy);
      box-shadow: 0 4px 12px rgba(11, 25, 76, 0.15);
    }}
    .hub-filter-tab .badge-count {{
      font-size: 0.72rem;
      padding: 0.15rem 0.45rem;
      border-radius: 999px;
      background: rgba(255, 255, 255, 0.2);
    }}
    .hub-filter-tab:not(.active) .badge-count {{
      background: var(--border-medium);
      color: var(--text-dark);
    }}

    /* 1-Tap Quick Pill Cloud */
    .hub-pills-cloud-section {{
      background: #090E24;
      padding: 2.5rem 0;
      border-top: 1px solid rgba(255, 255, 255, 0.08);
      border-bottom: 1px solid rgba(255, 255, 255, 0.08);
    }}
    .hub-pills-title {{
      font-size: 0.85rem;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.08em;
      color: var(--leads-cyan);
      margin-bottom: 1rem;
      display: flex;
      align-items: center;
      gap: 0.5rem;
    }}
    .hub-pills-wrap {{
      display: flex;
      flex-wrap: wrap;
      gap: 0.5rem;
    }}
    .hub-pill {{
      background: rgba(255, 255, 255, 0.04);
      border: 1px solid rgba(255, 255, 255, 0.12);
      border-radius: var(--radius-sm);
      padding: 0.45rem 0.85rem;
      display: inline-flex;
      align-items: center;
      gap: 0.45rem;
      color: rgba(255, 255, 255, 0.88);
      font-size: 0.82rem;
      font-weight: 600;
      text-decoration: none;
      transition: all 0.2s ease;
    }}
    .hub-pill svg {{
      color: var(--leads-cyan);
    }}
    .hub-pill:hover {{
      background: rgba(0, 184, 217, 0.12);
      border-color: var(--leads-cyan);
      color: #FFFFFF;
      transform: translateY(-2px);
    }}

    /* City Cards Grid */
    .hub-directory-section {{
      padding: clamp(3.5rem, 5vw, 5rem) 0;
      background: #FFFFFF;
    }}
    .hub-grid-top-row {{
      display: flex;
      justify-content: space-between;
      align-items: flex-end;
      margin-bottom: 2.25rem;
      flex-wrap: wrap;
      gap: 1rem;
    }}
    .hub-grid-title {{
      font-family: var(--font-serif);
      font-size: 1.85rem;
      font-weight: 700;
      color: var(--text-dark);
      margin: 0;
    }}
    .hub-cards-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(330px, 1fr));
      gap: 1.75rem;
    }}
    .hub-card {{
      background: var(--bg-card);
      border: 1px solid var(--border-medium);
      border-radius: var(--radius-md);
      padding: 1.65rem;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      transition: transform 0.25s ease, box-shadow 0.25s ease, border-color 0.25s ease;
      position: relative;
    }}
    .hub-card:hover {{
      transform: translateY(-4px);
      box-shadow: 0 16px 32px -8px rgba(11, 25, 76, 0.1);
      border-color: var(--leads-cyan);
    }}
    .hub-card-top {{
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
      margin-bottom: 0.85rem;
      gap: 0.75rem;
    }}
    .hub-card-title {{
      font-family: var(--font-sans);
      font-size: 1.35rem;
      font-weight: 800;
      margin: 0 0 0.35rem;
      line-height: 1.25;
    }}
    .hub-card-title a {{
      color: var(--text-dark);
      text-decoration: none;
      transition: color 0.2s;
    }}
    .hub-card-title a:hover {{
      color: var(--leads-cyan-dark);
    }}
    .hub-card-location {{
      font-size: 0.84rem;
      color: var(--text-muted);
      margin: 0;
      display: flex;
      align-items: center;
      gap: 0.35rem;
    }}
    .hub-badge-hq {{
      background: #ECFDF5;
      color: #059669;
      font-size: 0.72rem;
      font-weight: 800;
      padding: 0.25rem 0.6rem;
      border-radius: 999px;
      white-space: nowrap;
      border: 1px solid #A7F3D0;
      text-transform: uppercase;
      letter-spacing: 0.04em;
    }}
    .hub-badge-state {{
      background: var(--bg-surface);
      color: var(--text-body);
      font-size: 0.74rem;
      font-weight: 700;
      padding: 0.25rem 0.6rem;
      border-radius: 999px;
      white-space: nowrap;
      border: 1px solid var(--border-medium);
    }}
    .hub-card-desc {{
      font-size: 0.92rem;
      color: var(--text-muted);
      line-height: 1.6;
      margin-bottom: 1.25rem;
    }}
    .hub-card-tags {{
      display: flex;
      flex-wrap: wrap;
      gap: 0.4rem;
      margin-bottom: 1.5rem;
    }}
    .hub-tag {{
      font-size: 0.76rem;
      background: var(--bg-surface);
      border: 1px solid var(--border-light);
      color: var(--text-body);
      padding: 0.25rem 0.6rem;
      border-radius: 6px;
      font-weight: 600;
    }}
    .hub-card-footer {{
      border-top: 1px solid var(--border-light);
      padding-top: 1rem;
    }}
    .hub-card-link {{
      display: inline-flex;
      align-items: center;
      gap: 0.45rem;
      color: var(--leads-violet);
      font-weight: 700;
      font-size: 0.92rem;
      text-decoration: none;
      transition: gap 0.2s, color 0.2s;
    }}
    .hub-card-link:hover {{
      gap: 0.75rem;
      color: var(--leads-indigo);
    }}

    /* Editorial Guide Styling */
    .hub-editorial-section {{
      padding: clamp(4rem, 6vw, 6rem) 0;
      background: var(--bg-surface);
      border-top: 1px solid var(--border-light);
    }}
    .editorial-container {{
      max-width: 920px;
      margin: 0 auto;
    }}
    .editorial-container h2 {{
      font-family: var(--font-serif);
      font-size: clamp(1.85rem, 3vw, 2.35rem);
      font-weight: 700;
      color: var(--text-dark);
      margin-top: 3rem;
      margin-bottom: 1.25rem;
      line-height: 1.28;
    }}
    .editorial-container h3 {{
      font-family: var(--font-sans);
      font-size: 1.35rem;
      font-weight: 700;
      color: var(--text-dark);
      margin-top: 2rem;
      margin-bottom: 0.75rem;
    }}
    .editorial-container p {{
      font-size: 1.05rem;
      line-height: 1.8;
      color: var(--text-body);
      margin-bottom: 1.35rem;
    }}
    .editorial-container ul {{
      margin-bottom: 1.75rem;
      padding-left: 1.5rem;
    }}
    .editorial-container li {{
      font-size: 1.02rem;
      line-height: 1.75;
      color: var(--text-body);
      margin-bottom: 0.6rem;
    }}
    .editorial-callout-box {{
      background: #FFFFFF;
      border-left: 4px solid var(--leads-cyan);
      padding: 1.65rem;
      border-radius: 0 var(--radius-sm) var(--radius-sm) 0;
      box-shadow: 0 4px 16px rgba(11, 25, 76, 0.04);
      margin: 2.25rem 0;
    }}

    /* Comparison Table */
    .comparison-table-scroll {{
      overflow-x: auto;
      margin: 2.25rem 0;
      background: #FFFFFF;
      border-radius: var(--radius-md);
      border: 1px solid var(--border-medium);
      box-shadow: 0 6px 20px rgba(11, 25, 76, 0.04);
    }}
    .comparison-table {{
      width: 100%;
      border-collapse: collapse;
      text-align: left;
      font-size: 0.95rem;
    }}
    .comparison-table th {{
      background: var(--leads-navy);
      color: #FFFFFF;
      padding: 1.15rem 1.35rem;
      font-weight: 700;
      font-size: 0.95rem;
    }}
    .comparison-table td {{
      padding: 1.15rem 1.35rem;
      border-bottom: 1px solid var(--border-light);
      color: var(--text-body);
    }}
    .comparison-table tr:last-child td {{
      border-bottom: none;
    }}
    .comparison-table tr:hover td {{
      background: var(--bg-surface);
    }}

    /* Accordion FAQ */
    .hub-faq-wrap {{
      max-width: 860px;
      margin: 0 auto;
    }}
    .hub-faq-card {{
      border: 1px solid var(--border-medium);
      border-radius: var(--radius-sm);
      margin-bottom: 1rem;
      background: #FFFFFF;
      overflow: hidden;
      transition: all 0.2s ease;
    }}
    .hub-faq-card.active {{
      border-color: var(--leads-cyan);
      box-shadow: 0 6px 18px rgba(0, 184, 217, 0.08);
    }}
    .hub-faq-header-btn {{
      width: 100%;
      padding: 1.35rem 1.5rem;
      background: #FFFFFF;
      border: none;
      display: flex;
      justify-content: space-between;
      align-items: center;
      cursor: pointer;
      font-family: var(--font-sans);
      font-size: 1.05rem;
      font-weight: 700;
      color: var(--text-dark);
      text-align: left;
    }}
    .hub-faq-content {{
      display: none;
      padding: 0 1.5rem 1.5rem;
      color: var(--text-muted);
      font-size: 0.98rem;
      line-height: 1.7;
    }}
    .hub-faq-card.active .hub-faq-content {{
      display: block;
    }}
    .hub-faq-card.active svg {{
      transform: rotate(180deg);
    }}
  </style>
</head>

<body>
{GTM_BODY_SNIPPET}
  <!-- =====================================================================
       1. TOP ANNOUNCEMENT BAR
       ===================================================================== -->
  <div class="top-bar">
    <div class="container top-bar-inner">
      <div class="top-bar-contact">
        <a href="tel:+917791910007" class="top-bar-link">
          <svg width="15" height="15" fill="none" stroke="var(--leads-cyan)" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z"/></svg>
          <span>Call / WhatsApp: <strong>+91 77919 10007</strong></span>
        </a>
        <span>|</span>
        <a href="mailto:info@leads365.in" class="top-bar-link">
          <svg width="15" height="15" fill="none" stroke="var(--leads-cyan)" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"/></svg>
          <span>info@leads365.in</span>
        </a>
      </div>
      <div class="top-bar-location">
        <svg width="15" height="15" fill="none" stroke="var(--leads-cyan)" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"/><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"/></svg>
        <span>Bhamashah Techno Hub Sansthan Path, Jhalana Gram, Malviya Nagar, Jaipur, Rajasthan 302017</span>
      </div>
    </div>
  </div>

  <!-- =====================================================================
       2. STICKY NAVBAR HEADER
       ===================================================================== -->
  <header id="site-header" class="site-header">
    <div class="container navbar">
      <a href="/" class="brand-logo-wrap" aria-label="Leads365 Home">
        <img src="/assets/images/LEADS365_Logo.png" alt="Leads365 Logo" class="brand-logo-img" />
      </a>

      <!-- Desktop Navigation Links -->
      <nav class="nav-links" aria-label="Main Navigation">
        <a href="/" class="nav-link">Home</a>
        <a href="/features" class="nav-link">Features & Industries</a>
        <a href="/pricing" class="nav-link">Pricing & FAQs</a>
        <a href="/about" class="nav-link">About Us</a>
        <a href="/lead-management-software" class="nav-link active">Locations</a>
        <a href="/contact" class="nav-link">Contact</a>
      </nav>

      <!-- Action Buttons -->
      <div class="nav-actions">
        <button onclick="openLoginModal()" class="btn btn-secondary btn-sm">Login</button>
        <a href="/contact" class="btn btn-primary btn-sm">
          <span>Book Free Demo</span>
          <svg width="15" height="15" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M13 7l5 5m0 0l-5 5m5-5H6"/></svg>
        </a>
      </div>

      <!-- Mobile Hamburger Button -->
      <button onclick="toggleMobileMenu()" class="mobile-menu-btn" aria-label="Toggle Mobile Menu">
        <svg id="menu-icon-open" width="28" height="28" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.2" d="M4 6h16M4 12h16M4 18h16"/></svg>
        <svg id="menu-icon-close" width="28" height="28" fill="none" stroke="currentColor" viewBox="0 0 24 24" style="display: none;"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.2" d="M6 18L18 6M6 6l12 12"/></svg>
      </button>
    </div>

    <!-- Mobile Drawer -->
    <div id="mobile-drawer" class="mobile-nav-drawer">
      <div class="mobile-nav-list">
        <a href="/" class="mobile-nav-link" onclick="toggleMobileMenu()">Home</a>
        <a href="/features" class="mobile-nav-link" onclick="toggleMobileMenu()">Features & Industries</a>
        <a href="/pricing" class="mobile-nav-link" onclick="toggleMobileMenu()">Pricing & FAQs</a>
        <a href="/about" class="mobile-nav-link" onclick="toggleMobileMenu()">About Us</a>
        <a href="/lead-management-software" class="mobile-nav-link active" onclick="toggleMobileMenu()">Locations (60+ Cities)</a>
        <a href="/contact" class="mobile-nav-link" onclick="toggleMobileMenu()">Contact Us</a>
      </div>
      <div class="mobile-nav-actions">
        <button onclick="openLoginModal(); toggleMobileMenu();" class="btn btn-secondary w-full">Login to CRM</button>
        <a href="/contact" onclick="toggleMobileMenu()" class="btn btn-primary w-full">Book a Free Demo</a>
      </div>
    </div>
  </header>

  <!-- =====================================================================
       3. BREADCRUMB BAR
       ===================================================================== -->
  <div class="breadcrumb-nav reveal-up" style="margin: 1.25rem 0 0;">
    <div class="container">
      <a href="/">Home</a>
      <span>/</span>
      <span style="color: var(--leads-cyan); font-weight: 600;">Lead Management Software Across India</span>
    </div>
  </div>

  <!-- =====================================================================
       4. HERO BANNER & SEARCH BAR
       ===================================================================== -->
  <section class="hub-hero-banner">
    <div class="container">
      <div class="badge-eyebrow" style="margin-bottom: 1.25rem;">
        <span class="badge-dot"></span>
        <span>PAN-INDIA SALES ACCELERATION NETWORK &bull; 60+ CITIES</span>
      </div>

      <h1 class="hub-hero-headline">
        Lead Management Software Across India: <span class="text-gradient-365">60+ Commercial Hubs</span>
      </h1>

      <p class="hub-hero-subhead">
        Stop losing high-value customer inquiries to spreadsheet chaos, delayed telecaller responses, and missing WhatsApp follow-ups. Leads365 delivers zero-lead-leakage sales automation built specifically for high-velocity Indian business environments—from Jaipur's manufacturing zones and Delhi NCR's corporate towers to Bengaluru's tech parks and Mumbai's financial epicenters.
      </p>

      <!-- Live Search & Category Filtering Bar -->
      <div class="hub-search-box">
        <div class="hub-search-input-group">
          <svg width="22" height="22" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/></svg>
          <input type="text" id="citySearchInput" class="hub-search-field" placeholder="Search by city name, state, or industry (e.g., Jaipur, Real Estate, Pune, Furniture, Textiles)..." aria-label="Search city or industry" />
        </div>
        <div class="hub-filter-tabs">
          <button class="hub-filter-tab active" data-filter="all">All Locations <span class="badge-count">60</span></button>
          <button class="hub-filter-tab" data-filter="rajasthan">Rajasthan <span class="badge-count">20</span></button>
          <button class="hub-filter-tab" data-filter="north">Delhi NCR & North <span class="badge-count">13</span></button>
          <button class="hub-filter-tab" data-filter="west">West & Central <span class="badge-count">13</span></button>
          <button class="hub-filter-tab" data-filter="south">South India <span class="badge-count">11</span></button>
          <button class="hub-filter-tab" data-filter="east-central">East & North-East <span class="badge-count">3</span></button>
        </div>
      </div>
    </div>
  </section>

  <!-- =====================================================================
       5. 1-TAP QUICK CITY PILLS CLOUD (MATCHING HOMEPAGE DESIGN)
       ===================================================================== -->
  <section class="hub-pills-cloud-section">
    <div class="container">
      <div class="hub-pills-title">
        <svg width="14" height="14" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M5.05 4.05a7 7 0 119.9 9.9L10 18.9l-4.95-4.95a7 7 0 010-9.9zM10 11a2 2 0 100-4 2 2 0 000 4z" clip-rule="evenodd"/></svg>
        <span>1-Tap Direct City Access (All 60 Commercial Centers)</span>
      </div>
      <div class="hub-pills-wrap" id="pillsContainer">
        {all_pills_string}
      </div>
    </div>
  </section>

  <!-- =====================================================================
       6. DEDICATED CITY CRM CARDS GRID
       ===================================================================== -->
  <section class="hub-directory-section">
    <div class="container">
      <div class="hub-grid-top-row">
        <div>
          <h2 class="hub-grid-title">Explore Dedicated Local City Portals</h2>
          <p style="color: var(--text-muted); font-size: 0.96rem; margin: 0.4rem 0 0;">
            Select your city to review tailored industry playbooks, local commercial pain point analyses, and rapid 48-hour onboarding roadmaps.
          </p>
        </div>
        <div id="cityResultCount" style="font-weight: 700; color: var(--leads-cyan-dark); font-size: 0.98rem; background: var(--bg-surface); padding: 0.4rem 0.9rem; border-radius: 999px; border: 1px solid var(--border-medium);">
          Showing 60 locations
        </div>
      </div>

      <div class="hub-cards-grid" id="citiesGridContainer">
        {cards_string}
      </div>
    </div>
  </section>

  <!-- =====================================================================
       7. IN-DEPTH EDITORIAL & COMPARISON GUIDE (1600+ WORDS)
       ===================================================================== -->
  <section class="hub-editorial-section">
    <div class="container">
      <div class="editorial-container">
        <h2>The State of Lead Management & Sales Operations Across India</h2>
        <p>
          India’s commercial landscape is undergoing the fastest digital commerce transformation in its history. From tier-1 metropolises like Delhi NCR, Mumbai, and Bengaluru to dynamic tier-2 and tier-3 industrial manufacturing hubs like Jaipur, Jodhpur, Surat, Ludhiana, and Coimbatore, enterprises are allocating unprecedented capital toward digital advertising. Businesses generate customer inquiries simultaneously through Meta Ads (Facebook & Instagram Lead Forms), Google Search, IndiaMART B2B catalogs, TradeIndia, Justdial, Magicbricks, 99acres, and organic search portals.
        </p>
        <p>
          Yet, despite spending hundreds of thousands of rupees every month on inbound marketing campaigns, sales directors across India consistently report a startling operational paradox: <strong>lead conversion rates remain stagnant between 2% and 4%</strong>. The root cause is almost never lead quality—it is lead leakage, sluggish telecalling response times, unstructured WhatsApp chats on personal employee smartphones, and lack of real-time management visibility.
        </p>

        <div class="editorial-callout-box">
          <h4 style="margin: 0 0 0.5rem; color: var(--text-dark); font-size: 1.15rem; font-family: var(--font-sans);">The 15-Minute Rule of Indian Inbound Sales</h4>
          <p style="margin: 0; font-size: 0.96rem; color: var(--text-muted); line-height: 1.65;">
            According to national B2B and real estate conversion benchmarks across India, inquiries contacted within <strong>5 to 15 minutes</strong> of form submission demonstrate a <strong>391% higher qualification rate</strong> than leads dialed after 2 hours. Inquiries left unaddressed overnight convert at less than 0.5% because prospective buyers have already engaged with faster competitors.
          </p>
        </div>

        <h2>Why Generic Global Enterprise CRMs Fail Inside Indian Sales Teams</h2>
        <p>
          Over the past decade, Indian enterprises invested heavily in enterprise CRM platforms developed primarily for North American and Western European B2B environments—most notably Salesforce, HubSpot, and Zoho. While these platforms excel at managing complex multi-month enterprise contract renewals through corporate email exchanges, they frequently fail when deployed in fast-paced, high-volume Indian sales operations.
        </p>

        <div class="comparison-table-scroll">
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
                <td>Add-on marketplace plugins requiring extra recurring fees with complex technical setup.</td>
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
                <td><strong>Pricing & Plans</strong></td>
                <td>Billed in expensive foreign USD with rigid seat tiers and mandatory consultation fees.</td>
                <td><strong>Transparent, team-tailored pricing</strong> with zero hidden per-connector charges or forced consulting.</td>
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

  <!-- =====================================================================
       8. MASTER FAQ ACCORDION SECTION
       ===================================================================== -->
  <section class="section-padding bg-white">
    <div class="container">
      <div class="hub-faq-wrap">
        <div style="text-align: center; margin-bottom: 2.75rem;">
          <span class="badge-eyebrow">Enterprise FAQs</span>
          <h2 style="font-family: var(--font-serif); font-size: clamp(2rem, 3.2vw, 2.5rem); font-weight: 700; color: var(--text-dark); margin: 0.5rem 0 0;">
            Frequently Asked Questions
          </h2>
          <p style="color: var(--text-muted); font-size: 1.05rem; margin-top: 0.5rem;">
            Everything you need to know about deploying Leads365 across distributed Indian sales operations.
          </p>
        </div>

        <div class="hub-faq-card active">
          <button class="hub-faq-header-btn" onclick="toggleFaq(this)">
            <span>What makes Leads365 the best Lead Management Software for Indian businesses?</span>
            <svg width="20" height="20" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/></svg>
          </button>
          <div class="hub-faq-content">
            Unlike foreign enterprise CRMs designed for email-first workflows, Leads365 is purpose-built for India's high-speed sales dynamics. It features instant multi-channel lead capture (IndiaMART, TradeIndia, 99acres, Meta Ads), official WhatsApp Business API automation, click-to-dial call masking, Android SIM tracking, and zero-training simplicity—backed by transparent, flexible pricing tailored for Indian teams.
          </div>
        </div>

        <div class="hub-faq-card">
          <button class="hub-faq-header-btn" onclick="toggleFaq(this)">
            <span>Can Leads365 capture leads simultaneously from Meta Ads, Google Ads, and B2B portals?</span>
            <svg width="20" height="20" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/></svg>
          </button>
          <div class="hub-faq-content">
            Yes. Leads365 connects directly with Meta Ads (Instant Forms), Google Search Webhooks, IndiaMART Push APIs, TradeIndia, Justdial, Magicbricks, 99acres, Housing.com, and custom website forms. All inquiries are ingested into your unified visual Kanban pipeline in under 30 seconds.
          </div>
        </div>

        <div class="hub-faq-card">
          <button class="hub-faq-header-btn" onclick="toggleFaq(this)">
            <span>How does the WhatsApp Business API integration work?</span>
            <svg width="20" height="20" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/></svg>
          </button>
          <div class="hub-faq-content">
            Leads365 integrates with Meta's official WhatsApp Business Cloud API. When an inquiry is captured, the CRM immediately triggers an automated, branded greeting message with product catalogs, brochures, or booking links. All incoming and outgoing WhatsApp messages are mirrored in the client record for full manager visibility.
          </div>
        </div>

        <div class="hub-faq-card">
          <button class="hub-faq-header-btn" onclick="toggleFaq(this)">
            <span>Can departing sales executives download or steal our company's customer data?</span>
            <svg width="20" height="20" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/></svg>
          </button>
          <div class="hub-faq-content">
            No. Leads365 implements strict enterprise role-based security. Sales executives cannot export contact lists or customer databases. Furthermore, our optional call-masking technology conceals prospective customer phone numbers during telecaller outreach, ensuring proprietary company leads remain protected.
          </div>
        </div>

        <div class="hub-faq-card">
          <button class="hub-faq-header-btn" onclick="toggleFaq(this)">
            <span>How does Leads365 support field sales representatives visiting clients in person?</span>
            <svg width="20" height="20" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/></svg>
          </button>
          <div class="hub-faq-content">
            Our lightweight mobile app allows field sales representatives to check in at client locations with GPS timestamp verification, record meeting notes via voice-to-text, generate on-the-spot price estimates, and update deal pipeline stages even when working in low-connectivity industrial belts.
          </div>
        </div>

        <div class="hub-faq-card">
          <button class="hub-faq-header-btn" onclick="toggleFaq(this)">
            <span>How long does historical customer data migration and staff training take?</span>
            <svg width="20" height="20" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/></svg>
          </button>
          <div class="hub-faq-content">
            Full data migration from Excel, CSV, Google Sheets, Zoho, or older CRM systems is completed within 48 hours. Because Leads365 is designed with an intuitive, clutter-free user interface, sales executives and telecallers master the platform after a single 45-minute live onboarding session.
          </div>
        </div>
      </div>
    </div>
  </section>

  <!-- =====================================================================
       9. BOTTOM CTA BANNER (MATCHING HOMEPAGE & CITY PAGES)
       ===================================================================== -->
  <section class="section-padding-sm bg-light">
    <div class="container">
      <div class="card cta-banner-card reveal-zoom">
        <span class="badge-eyebrow badge-white" style="margin-bottom: 1rem;">Drive Scalable All-India Revenue</span>
        <h2>Ready to Accelerate Your Inside Sales Team in Any Indian City?</h2>
        <p>
          Join forward-thinking businesses across Jaipur, Delhi NCR, Mumbai, Bengaluru, and 60+ commercial centers that rely on Leads365 to eliminate lead leakage, cut response times to under 60 seconds, and boost deal closure rates.
        </p>
        <div style="display: flex; justify-content: center; gap: 1rem; flex-wrap: wrap;">
          <a href="/contact" class="btn btn-primary btn-lg">Schedule a Free Demo</a>
          <a href="tel:+917791910007" class="btn btn-outline-white btn-lg">Call Sales: +91 77919 10007</a>
        </div>
      </div>
    </div>
  </section>

  <!-- =====================================================================
       10. GLOBAL SITE FOOTER (100% BRAND CONSISTENT)
       ===================================================================== -->
  <footer class="site-footer">
    <div class="container">
      <div class="footer-grid">
        
        <!-- Col 1: Brand -->
        <div class="footer-brand-col">
          <a href="/" class="footer-logo-wrap" aria-label="Leads365 Home">
            <img src="/assets/images/LEADS365_Logo.png" alt="Leads365 Logo" class="footer-logo-img" />
          </a>
          <p class="footer-about-text">
            <strong>Leads365 (leads365.in)</strong> is an all-in-one Cloud Lead Management and Sales CRM software built by <strong>Chonexa Technologies</strong> to help modern businesses capture inquiries, eliminate lead leakage, and close deals effortlessly.
          </p>
        </div>

        <!-- Col 2: Quick Links -->
        <div>
          <h3 class="footer-col-heading">Quick Links</h3>
          <div class="footer-links-list">
            <a href="/" class="footer-link">Home</a>
            <a href="/features" class="footer-link">CRM Features</a>
            <a href="/features#industries" class="footer-link">Industry Verticals</a>
            <a href="/pricing" class="footer-link">Pricing Plans</a>
            <a href="/about" class="footer-link">About Us</a>
            <a href="/lead-management-software" class="footer-link">Locations (60+ Cities)</a>
            <a href="/contact" class="footer-link">Contact & Demo</a>
          </div>
        </div>

        <!-- Col 3: Resources & Legal -->
        <div>
          <h3 class="footer-col-heading">Legal & Resources</h3>
          <div class="footer-links-list">
            <a href="/pricing#faq" class="footer-link">Frequently Asked Questions</a>
            <a href="/privacy-policy" class="footer-link">Privacy Policy</a>
            <a href="/privacy-policy#terms" class="footer-link">Terms & Conditions</a>
            <a href="/privacy-policy#security" class="footer-link">Data Security Guarantee</a>
            <a href="/sitemap.xml" class="footer-link">XML Sitemap</a>
            <a href="/contact" class="footer-link">Book Free Demo</a>
          </div>
        </div>

        <!-- Col 4: Corporate Contact Details -->
        <div>
          <h3 class="footer-col-heading">Headquarters & Support</h3>
          <div class="footer-contact-list">
            <div class="footer-contact-item">
              <span>📍</span>
              <span>Bhamashah Techno Hub Sansthan Path, Jhalana Gram, Malviya Nagar, Jaipur, Rajasthan 302017, India</span>
            </div>
            <div class="footer-contact-item">
              <span>📞</span>
              <a href="tel:+917791910007">+91 77919 10007</a>
            </div>
            <div class="footer-contact-item">
              <span>✉️</span>
              <a href="mailto:info@leads365.in">info@leads365.in</a>
            </div>
            <div class="footer-contact-item">
              <span>🌐</span>
              <a href="https://leads365.in">leads365.in</a>
            </div>
          </div>
        </div>

      </div>

      <div class="footer-bottom">
        <p>
          &copy; 2026 Leads365 — Bhamashah Techno Hub Sansthan Path, Jhalana Gram, Malviya Nagar, Jaipur, Rajasthan 302017. All rights reserved. Leads365 is a product of <strong>Chonexa Technologies</strong> | Designed and developed by <strong>Amazing IT</strong>
        </p>
      </div>
    </div>
  </footer>

  <!-- Floating Quick WhatsApp Button -->
  <a href="https://wa.me/917791910007?text=Hi%20Leads365%20Team,%20I%20would%20like%20to%20schedule%20a%20CRM%20demo%20for%20our%20sales%20team." target="_blank" rel="noopener" class="floating-whatsapp-btn" aria-label="Chat on WhatsApp with CRM Team">
    <div class="whatsapp-btn-pulse"></div>
    <span class="whatsapp-icon-wrap">
      <svg width="32" height="32" viewBox="0 0 24 24" fill="none">
        <path fill="#FFFFFF" d="M17.472 14.382c-.301-.15-1.781-.879-2.056-.98-.276-.1-.476-.15-.677.15-.2.301-.777.98-.952 1.18-.176.2-.351.226-.652.076-.301-.15-1.272-.469-2.423-1.496-.896-.799-1.501-1.787-1.677-2.088-.175-.301-.019-.464.132-.614.136-.135.301-.351.452-.527.15-.175.2-.301.301-.501.1-.2.05-.376-.025-.526-.075-.15-.677-1.631-.928-2.234-.244-.587-.493-.507-.677-.517-.175-.009-.376-.01-.577-.01-.201 0-.527.075-.802.376-.276.301-1.054 1.03-1.054 2.512s1.079 2.913 1.23 3.114c.15.201 2.124 3.243 5.145 4.549.719.311 1.28.497 1.718.636.722.23 1.379.197 1.898.12.578-.087 1.781-.728 2.032-1.431.25-.703.25-1.305.175-1.431-.075-.125-.276-.201-.577-.351z"/>
        <path fill="#FFFFFF" fill-rule="evenodd" clip-rule="evenodd" d="M12 2C6.477 2 2 6.477 2 12c0 1.89.525 3.66 1.438 5.168L2.054 22l4.98-1.306A9.957 9.957 0 0 0 12 22c5.523 0 10-4.477 10-10S17.523 2 12 2zm0 18.2a8.16 8.16 0 0 1-4.218-1.168l-.303-.18-2.957.776.789-2.883-.197-.314A8.167 8.167 0 0 1 3.8 12c0-4.529 3.671-8.2 8.2-8.2 4.529 0 8.2 3.671 8.2 8.2 0 4.529-3.671 8.2-8.2 8.2z"/>
      </svg>
    </span>
  </a>

  <!-- Login Modal -->
  <div id="login-modal" class="modal-overlay">
    <div class="modal-box">
      <button onclick="closeLoginModal()" class="modal-close-btn" aria-label="Close Modal">✕</button>
      <div class="brand-title" style="margin-bottom: 0.25rem;">
        <span class="logo-navy">LEADS</span><span class="text-gradient-365">365</span>
      </div>
      <p style="font-size: 0.78rem; font-weight: 700; text-transform: uppercase; color: var(--text-muted); margin-bottom: 1.5rem;">
        Workspace Portal Login
      </p>

      <form onsubmit="handleLoginSubmit(event)">
        <div class="form-group">
          <label class="form-label">Registered Mobile or Email</label>
          <input type="text" required placeholder="e.g. +91 77919 10007 or info@leads365.in" class="form-control" />
        </div>
        <div class="form-group">
          <label class="form-label">Password</label>
          <input type="password" required placeholder="••••••••" class="form-control" />
        </div>
        <button type="submit" class="btn btn-primary w-full" style="margin-top: 0.5rem;">Sign In to Dashboard</button>
        <div id="login-modal-feedback" class="toast-banner toast-info" style="margin-top: 1rem;"></div>
      </form>
    </div>
  </div>

  <!-- Shared Global JS -->
  <script src="/assets/js/main.js?v=2.4"></script>

  <!-- Interactive Search & Filtering JS -->
  <script>
    function toggleFaq(btn) {{
      const item = btn.parentElement;
      item.classList.toggle('active');
    }}

    document.addEventListener('DOMContentLoaded', function() {{
      const searchInput = document.getElementById('citySearchInput');
      const filterTabs = document.querySelectorAll('.hub-filter-tab');
      const cards = document.querySelectorAll('.hub-card');
      const pills = document.querySelectorAll('.hub-pill');
      const countEl = document.getElementById('cityResultCount');

      let currentFilter = 'all';

      function filterAll() {{
        const query = searchInput.value.toLowerCase().trim();
        let visibleCount = 0;

        cards.forEach(card => {{
          const name = card.getAttribute('data-name') || '';
          const state = card.getAttribute('data-state') || '';
          const region = card.getAttribute('data-region') || '';
          const industries = card.getAttribute('data-industries') || '';

          const matchesSearch = !query || name.includes(query) || state.includes(query) || industries.includes(query);
          const matchesFilter = currentFilter === 'all' || region === currentFilter;

          if (matchesSearch && matchesFilter) {{
            card.style.display = 'flex';
            visibleCount++;
          }} else {{
            card.style.display = 'none';
          }}
        }});

        pills.forEach(pill => {{
          const name = pill.getAttribute('data-name') || '';
          const state = pill.getAttribute('data-state') || '';
          const region = pill.getAttribute('data-region') || '';

          const matchesSearch = !query || name.includes(query) || state.includes(query);
          const matchesFilter = currentFilter === 'all' || region === currentFilter;

          if (matchesSearch && matchesFilter) {{
            pill.style.display = 'inline-flex';
          }} else {{
            pill.style.display = 'none';
          }}
        }});

        countEl.textContent = `Showing ${{visibleCount}} locations`;
      }}

      if (searchInput) {{
        searchInput.addEventListener('input', filterAll);
      }}

      filterTabs.forEach(tab => {{
        tab.addEventListener('click', function() {{
          filterTabs.forEach(t => t.classList.remove('active'));
          this.classList.add('active');
          currentFilter = this.getAttribute('data-filter');
          filterAll();
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
