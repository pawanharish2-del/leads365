/**
 * LEADS365.IN — Shared Global JavaScript
 * Product by Chonexa Technologies
 */

document.addEventListener('DOMContentLoaded', () => {
  // 1. Sticky Header Scroll Effect
  const siteHeader = document.getElementById('site-header');
  if (siteHeader) {
    window.addEventListener('scroll', () => {
      if (window.scrollY > 20) {
        siteHeader.classList.add('scrolled');
      } else {
        siteHeader.classList.remove('scrolled');
      }
    });
  }

  // 2. Active Nav Link Highlighter
  highlightActiveNavLink();

  // 3. Pre-fill Plan in Contact Form if passed via URL param
  handleUrlPlanParam();
});

/* --------------------------------------------------------------------------
   ACTIVE NAV LINK HIGHLIGHTER
   -------------------------------------------------------------------------- */
function highlightActiveNavLink() {
  const currentPath = window.location.pathname.split('/').pop() || 'index.html';
  const navLinks = document.querySelectorAll('.nav-link, .mobile-nav-link');

  navLinks.forEach((link) => {
    const href = link.getAttribute('href');
    if (!href) return;

    // Direct match or root home match
    if (
      href === currentPath ||
      (currentPath === '' && href === 'index.html') ||
      (currentPath === 'index.html' && href === 'index.html')
    ) {
      link.classList.add('active');
    } else {
      link.classList.remove('active');
    }
  });
}

/* --------------------------------------------------------------------------
   MOBILE MENU TOGGLE
   -------------------------------------------------------------------------- */
function toggleMobileMenu() {
  const drawer = document.getElementById('mobile-drawer');
  const iconOpen = document.getElementById('menu-icon-open');
  const iconClose = document.getElementById('menu-icon-close');

  if (!drawer) return;

  const isOpen = drawer.classList.contains('open');
  if (isOpen) {
    drawer.classList.remove('open');
    if (iconOpen) iconOpen.style.display = 'block';
    if (iconClose) iconClose.style.display = 'none';
  } else {
    drawer.classList.add('open');
    if (iconOpen) iconOpen.style.display = 'none';
    if (iconClose) iconClose.style.display = 'block';
  }
}

/* --------------------------------------------------------------------------
   FAQ ACCORDION TOGGLER
   -------------------------------------------------------------------------- */
function toggleFaq(itemIndex) {
  const faqItem = document.getElementById(`faq-item-${itemIndex}`);
  if (!faqItem) return;

  const isActive = faqItem.classList.contains('active');

  // Optional: close other accordions
  const allFaqs = document.querySelectorAll('.faq-item');
  allFaqs.forEach((item) => item.classList.remove('active'));

  if (!isActive) {
    faqItem.classList.add('active');
  }
}

/* --------------------------------------------------------------------------
   LIVE CRM STREAM SIMULATION (FOR HOME PAGE)
   -------------------------------------------------------------------------- */
const simulatedLeads = [
  {
    code: 'FB',
    badgeClass: 'badge-fb',
    name: 'Sandeep Khandelwal',
    source: 'Facebook Ad',
    desc: 'Commercial Plot Inquiry • Assigned to Aman S.'
  },
  {
    code: 'IM',
    badgeClass: 'badge-im',
    name: 'Vikas Sharma',
    source: 'IndiaMART Portal',
    desc: 'Solar Inverter 5kW Quote • Assigned to Priya M.'
  },
  {
    code: 'WA',
    badgeClass: 'badge-wa',
    name: 'Meera Joshi',
    source: 'WhatsApp Inbound',
    desc: '10-User CRM Demo Request • Assigned to Rohit K.'
  },
  {
    code: 'GG',
    badgeClass: 'badge-gg',
    name: 'Dr. Arjun Rathore',
    source: 'Google Search Ads',
    desc: 'Hospital Clinic Inquiry • Assigned to Aman S.'
  },
  {
    code: 'JD',
    badgeClass: 'badge-jd',
    name: 'Royal Builders Jaipur',
    source: 'Justdial Leads',
    desc: 'Luxury Villa Buyer • Assigned to Priya M.'
  }
];

let leadSimIndex = 0;

function simulateIncomingLead() {
  const list = document.getElementById('live-lead-stream');
  const counter = document.getElementById('live-counter-inquiries');
  if (!list || !counter) return;

  const lead = simulatedLeads[leadSimIndex % simulatedLeads.length];
  leadSimIndex++;

  // Increment counter
  const currentCount = parseInt(counter.textContent.replace(/[^0-9]/g, ''), 10) || 148;
  counter.textContent = currentCount + 1;

  // Create new stream element
  const item = document.createElement('div');
  item.className = 'stream-item';
  item.style.borderColor = 'var(--leads-violet)';
  item.innerHTML = `
    <div class="stream-item-left">
      <div class="stream-source-badge ${lead.badgeClass}">${lead.code}</div>
      <div>
        <div class="stream-item-name">${lead.name}</div>
        <div class="stream-item-sub">${lead.desc} (Just now)</div>
      </div>
    </div>
    <span class="stream-tag-btn" style="background: var(--status-success-bg); color: var(--status-success);">New Inbound</span>
  `;

  list.prepend(item);

  // Keep max 3 items in preview
  if (list.children.length > 3) {
    list.removeChild(list.lastElementChild);
  }
}

/* --------------------------------------------------------------------------
   PRICING PLAN PRE-FILL HELPER
   -------------------------------------------------------------------------- */
function selectPricingPlan(planName) {
  window.location.href = `contact.html?plan=${encodeURIComponent(planName)}`;
}

function handleUrlPlanParam() {
  const params = new URLSearchParams(window.location.search);
  const plan = params.get('plan');
  if (!plan) return;

  const messageField = document.getElementById('form-message');
  if (messageField) {
    messageField.value = `Hello Leads365 Team, I would like to schedule a live demo for the "${plan}". Please contact me.`;
  }
}

/* --------------------------------------------------------------------------
   CONTACT & DEMO REQUEST FORM HANDLER
   -------------------------------------------------------------------------- */
function handleDemoFormSubmit(event) {
  event.preventDefault();

  const nameInput = document.getElementById('form-name');
  const businessInput = document.getElementById('form-business');
  const phoneInput = document.getElementById('form-phone');
  const emailInput = document.getElementById('form-email');
  const teamInput = document.getElementById('form-team');
  const industryInput = document.getElementById('form-industry');
  const messageInput = document.getElementById('form-message');
  const toast = document.getElementById('demo-toast');
  const submitBtn = event.target.querySelector('button[type="submit"]');

  if (!nameInput || !businessInput || !phoneInput) return;

  const name = nameInput.value.trim();
  const business = businessInput.value.trim();
  const phone = phoneInput.value.trim();
  const email = emailInput ? emailInput.value.trim() : '';
  const team = teamInput ? teamInput.value : '';
  const industry = industryInput ? industryInput.value : '';

  if (!name || !business || !phone) {
    alert('Please fill in all required fields marked with an asterisk (*).');
    return;
  }

  // Button loading state
  if (submitBtn) {
    submitBtn.disabled = true;
    submitBtn.innerHTML = `<span>Scheduling Your Demo...</span>`;
  }

  setTimeout(() => {
    if (submitBtn) {
      submitBtn.disabled = false;
      submitBtn.innerHTML = `<span>Book My Free Demo</span> <svg width="18" height="18" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M13 7l5 5m0 0l-5 5m5-5H6"/></svg>`;
    }

    if (toast) {
      toast.style.display = 'block';
      toast.className = 'toast-banner toast-success';
      toast.innerHTML = `
        <strong>✓ Thank you, ${name}!</strong><br>
        Your live demo request for <strong>${business}</strong> (${team || 'Sales Team'}) has been submitted. Our product specialist from Malviya Nagar, Jaipur will call/WhatsApp you on <strong>${phone}</strong> shortly.
      `;
      toast.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }

    event.target.reset();
  }, 700);
}

/* --------------------------------------------------------------------------
   LOGIN MODAL CONTROLLERS
   -------------------------------------------------------------------------- */
function openLoginModal() {
  const modal = document.getElementById('login-modal');
  if (modal) {
    modal.classList.add('open');
  }
}

function closeLoginModal() {
  const modal = document.getElementById('login-modal');
  const feedback = document.getElementById('login-modal-feedback');
  if (modal) {
    modal.classList.remove('open');
  }
  if (feedback) {
    feedback.style.display = 'none';
  }
}

function handleLoginSubmit(event) {
  event.preventDefault();
  const feedback = document.getElementById('login-modal-feedback');
  if (feedback) {
    feedback.style.display = 'block';
    feedback.innerHTML = `Connecting to Leads365 Cloud Portal... For new corporate provisioning or trial access, please book a demo or call <strong style="color: var(--leads-indigo);">+91 77919 10007</strong>.`;
  }
}

// Close modal on escape key
document.addEventListener('keydown', (e) => {
  if (e.key === 'Escape') {
    closeLoginModal();
  }
});

/* --------------------------------------------------------------------------
   INTERACTIVE AI CALL PLAYER DEMO (HOME PAGE)
   -------------------------------------------------------------------------- */
let isAiDemoPlaying = false;
let aiTimerInterval = null;
let aiSeconds = 14;

function toggleAiCallDemo() {
  const btn = document.getElementById('ai-play-btn');
  const waveform = document.getElementById('ai-waveform');
  const timerText = document.getElementById('ai-call-timer');
  const transcriptText = document.getElementById('ai-live-transcript');
  const summaryBlock = document.getElementById('ai-summary-bullets');

  if (!btn || !waveform) return;

  isAiDemoPlaying = !isAiDemoPlaying;

  if (isAiDemoPlaying) {
    waveform.classList.add('playing');
    btn.innerHTML = `<svg width="16" height="16" fill="currentColor" viewBox="0 0 24 24"><path d="M6 4h4v16H6V4zm8 0h4v16h-4V4z"/></svg> <span>Pause Analysis</span>`;
    btn.style.background = 'var(--gradient-cyan)';
    btn.style.color = 'var(--leads-navy-dark)';

    // Start timer increment
    aiTimerInterval = setInterval(() => {
      aiSeconds++;
      const mins = Math.floor(aiSeconds / 60);
      const secs = aiSeconds % 60;
      if (timerText) {
        timerText.textContent = `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')} / 03:42`;
      }
    }, 1000);

    if (transcriptText) {
      transcriptText.innerHTML = `
        <span class="speaker-tag speaker-agent">Agent (Priya):</span> "Namaste Rajesh Ji! Leads365 CRM ke 3BHK luxury villas regarding call kiya tha. Possession next month ready hai."<br>
        <span class="speaker-tag speaker-customer">Customer:</span> "Haan Priya ji, hum weekend par family ke sath site visit karna chahte hain. HDFC loan already approved hai."
      `;
    }

    if (summaryBlock) {
      summaryBlock.style.opacity = '1';
      summaryBlock.style.transform = 'translateY(0)';
    }

  } else {
    waveform.classList.remove('playing');
    btn.innerHTML = `<svg width="16" height="16" fill="currentColor" viewBox="0 0 24 24"><path d="M8 5v14l11-7z"/></svg> <span>Play Sample AI Analysis</span>`;
    btn.style.background = 'var(--gradient-btn)';
    btn.style.color = '#FFFFFF';
    clearInterval(aiTimerInterval);
  }
}
