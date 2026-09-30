# Leads365 (leads365.in) — Cloud Lead Management & Sales CRM

Official website for **Leads365** ([www.leads365.in](https://leads365.in)), an all-in-one Cloud Lead Management and Sales CRM software built by **Chonexa Technologies** (Jaipur, India). Designed specifically for Indian tele-calling and high-velocity sales teams across Real Estate, Education, Loans/Finance, Travel, and B2B sectors.

---

## 🌟 Key Features & Architecture

- **Multi-Page Architecture**: Clean, modular structure separating Home, About, Features & Industries, Pricing & FAQs, Contact/Demo, and Privacy Policy into dedicated pages.
- **Unified Global CSS (`assets/css/style.css`)**: Pure custom CSS design system using `:root` variables, brand color palette (`#001C71` Deep Navy, `#9B26FF` Electric Violet, `#5900D9` Indigo, `#00C8EA` Target Cyan), and 100% responsive flex/grid layouts (Zero inline `<style>` tags).
- **Interactive JavaScript Engine (`assets/js/main.js`)**:
  - Live inbound lead simulator with sound/visual feedback
  - AI call waveform player with dynamic transcript preview
  - FAQ accordion toggles
  - Mobile drawer navigation
  - Demo booking validation and plan selection handlers
  - Workspace portal login modal

---

## 📁 Project Structure

```text
leads365/
├── index.html              # Home Page with Hero Live Preview & AI Engine Suite
├── about.html              # About Us, Mission, Vision, and Chonexa Story
├── features.html           # Detailed CRM Features, AI Automation & Industry Verticals
├── pricing.html            # Pricing Tiers (Starter, Growth, Enterprise) & FAQs
├── contact.html            # Contact Information & Interactive Live Demo Request Form
├── privacy-policy.html     # Privacy Policy, Terms & Data Security Protocol
├── .gitignore              # Git ignore rules
├── README.md               # Project documentation
└── assets/
    ├── css/
    │   └── style.css       # Global design system and responsive styles
    ├── js/
    │   └── main.js         # Shared client-side interactivity and simulations
    └── images/
        ├── LEADS365_Logo.png # Official brand logo asset
        └── favicon.png     # Web browser favicon
```

---

## 🚀 Getting Started

### Local Development
To run this website locally, open any of the `.html` files in your browser or run a lightweight local server:

```bash
# Using Python
python -m http.server 8000

# Using Node.js npx serve
npx serve .
```
Then visit `http://localhost:8000` in your web browser.

---

## 🏢 Corporate Credits

- **Product Name**: Leads365 ([www.leads365.in](https://leads365.in))
- **Parent Company**: **Chonexa Technologies**
- **Headquarters**: Malviya Nagar, Jaipur, Rajasthan 302017, India
- **Contact**: [+91 77919 10007](tel:+917791910007) | [info@leads365.in](mailto:info@leads365.in)
- **Design & Development**: **Amazing IT**
