/**
 * LEADS365.IN — Shared Global JavaScript
 * Product by Chonexa Technologies
 * Handles Responsive Navigation, Scroll Reveals, Animated Counters, Modals, FAQs, Live Stream & AI Demo
 */

document.addEventListener('DOMContentLoaded', () => {
  // 1. Sticky Header Scroll Effect
  const siteHeader = document.getElementById('site-header');
  if (siteHeader) {
    const handleScroll = () => {
      if (window.scrollY > 20) {
        siteHeader.classList.add('scrolled');
      } else {
        siteHeader.classList.remove('scrolled');
      }
    };
    window.addEventListener('scroll', handleScroll, { passive: true });
    handleScroll();
  }

  // 2. Active Nav Link Highlighter (Supports clean URLs & .html fallback)
  highlightActiveNavLink();

  // 3. Scroll Reveal Animation Engine (IntersectionObserver)
  initScrollAnimations();

  // 4. Animated Number Counters on Scroll
  initAnimatedCounters();

  // 5. Pre-fill Plan in Contact Form if passed via URL param
  handleUrlPlanParam();
});

/* --------------------------------------------------------------------------
   ACTIVE NAV LINK HIGHLIGHTER (CLEAN URL COMPATIBLE)
   -------------------------------------------------------------------------- */
function highlightActiveNavLink() {
  const pathname = window.location.pathname;
  let currentFile = pathname.split('/').pop().replace('.html', '') || 'index';
  if (currentFile === '' || currentFile === 'index') {
    currentFile = 'index';
  }

  const navLinks = document.querySelectorAll('.nav-link, .mobile-nav-link');

  navLinks.forEach((link) => {
    const href = link.getAttribute('href');
    if (!href) return;

    let cleanHref = href.split('?')[0].split('#')[0].replace(/^\.\//, '').replace('.html', '');
    if (cleanHref === '' || cleanHref === '.' || cleanHref === 'index') {
      cleanHref = 'index';
    }

    if (cleanHref === currentFile) {
      link.classList.add('active');
    } else {
      link.classList.remove('active');
    }
  });
}

/* --------------------------------------------------------------------------
   SCROLL REVEAL ANIMATIONS (INTERSECTION OBSERVER)
   -------------------------------------------------------------------------- */
function initScrollAnimations() {
  const revealElements = document.querySelectorAll('.reveal, .reveal-up, .reveal-down, .reveal-left, .reveal-right, .reveal-zoom');
  if (!revealElements.length) return;

  const revealEl = (el) => {
    el.classList.add('active', 'is-revealed');
  };

  if ('IntersectionObserver' in window) {
    const revealObserver = new IntersectionObserver((entries, observer) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          revealEl(entry.target);
          observer.unobserve(entry.target);
        }
      });
    }, {
      root: null,
      threshold: 0.05,
      rootMargin: '0px 0px 50px 0px'
    });

    revealElements.forEach((el) => {
      // If already in viewport on load, reveal immediately
      const rect = el.getBoundingClientRect();
      if (rect.top < window.innerHeight && rect.bottom > 0) {
        revealEl(el);
      } else {
        revealObserver.observe(el);
      }
    });

    // Safety fallback: reveal all after 1.5s in case of headless or weird scroll containers
    setTimeout(() => {
      revealElements.forEach(revealEl);
    }, 1500);
  } else {
    // Fallback for browsers without IntersectionObserver
    revealElements.forEach(revealEl);
  }
}

/* --------------------------------------------------------------------------
   ANIMATED NUMBER COUNTERS ON SCROLL
   -------------------------------------------------------------------------- */
function initAnimatedCounters() {
  const counterElements = document.querySelectorAll('[data-counter], .animate-number');
  if (!counterElements.length) return;

  const runCounter = (el) => {
    const target = parseFloat(el.getAttribute('data-target') || el.textContent.replace(/[^0-9.]/g, ''));
    if (isNaN(target)) return;

    const prefix = el.getAttribute('data-prefix') || '';
    const suffix = el.getAttribute('data-suffix') || '';
    const duration = parseInt(el.getAttribute('data-duration') || '1600', 10);
    const hasDecimal = target % 1 !== 0;

    let startTime = null;

    const step = (timestamp) => {
      if (!startTime) startTime = timestamp;
      const progress = Math.min((timestamp - startTime) / duration, 1);
      // Easing: easeOutExpo
      const ease = progress === 1 ? 1 : 1 - Math.pow(2, -10 * progress);
      const current = target * ease;

      el.textContent = `${prefix}${hasDecimal ? current.toFixed(1) : Math.floor(current).toLocaleString('en-IN')}${suffix}`;

      if (progress < 1) {
        window.requestAnimationFrame(step);
      } else {
        el.textContent = `${prefix}${hasDecimal ? target.toFixed(1) : target.toLocaleString('en-IN')}${suffix}`;
      }
    };

    window.requestAnimationFrame(step);
  };

  if ('IntersectionObserver' in window) {
    const counterObserver = new IntersectionObserver((entries, observer) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          runCounter(entry.target);
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.2 });

    counterElements.forEach((el) => counterObserver.observe(el));
  } else {
    counterElements.forEach((el) => runCounter(el));
  }
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
    document.body.style.overflow = '';
  } else {
    drawer.classList.add('open');
    if (iconOpen) iconOpen.style.display = 'none';
    if (iconClose) iconClose.style.display = 'block';
    document.body.style.overflow = 'hidden';
  }
}

/* --------------------------------------------------------------------------
   FAQ ACCORDION TOGGLER
   -------------------------------------------------------------------------- */
function toggleFaq(itemIndex) {
  const faqItem = document.getElementById(`faq-item-${itemIndex}`);
  if (!faqItem) return;

  const isActive = faqItem.classList.contains('active');

  // Close all other accordions
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
  item.className = 'stream-item reveal-zoom active';
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
  window.location.href = `contact?plan=${encodeURIComponent(planName)}`;
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
   INTERACTIVE REAL-TIME AI ENGINE SIMULATION (HOME PAGE)
   -------------------------------------------------------------------------- */
let isAiDemoPlaying = false;
let aiTimerInterval = null;
let aiTypewriterTimeout = null;
let aiCurrentStepIndex = 0;
let aiTotalElapsedSecs = 0;
let aiPlayheadProgress = 0;

const aiDemoScript = [
  {
    speaker: 'agent',
    speakerLabel: 'Agent (Priya M.):',
    tagClass: 'speaker-agent-tag',
    bubbleClass: 'speaker-agent',
    text: "Namaste Rajesh Ji! Leads365 CRM ke 3BHK luxury villas regarding follow-up call kiya tha. Next month possession ready hai.",
    talkAgent: 65,
    talkCust: 35,
    sentiment: 'Positive Intent (88%)',
    sentimentClass: 'sentiment-positive',
    leadScore: '🎯 Lead Score: 86/100 (Warm)',
    leadScoreClass: 'sentiment-positive',
    bulletId: 'ai-bullet-req',
    durationSecs: 3
  },
  {
    speaker: 'customer',
    speakerLabel: 'Customer (Rajesh Sharma):',
    tagClass: 'speaker-customer-tag',
    bubbleClass: 'speaker-customer',
    text: "Haan Priya ji, hum weekend par family ke sath site visit karna chahte hain. HDFC pre-approved loan ₹1.4 Cr ready hai.",
    talkAgent: 38,
    talkCust: 62,
    sentiment: '🔥 High Buying Intent (94%)',
    sentimentClass: 'sentiment-hot',
    leadScore: '🎯 Lead Score: 94/100 (Hot 🔥)',
    leadScoreClass: 'sentiment-hot',
    bulletId: 'ai-bullet-budget',
    durationSecs: 4
  },
  {
    speaker: 'agent',
    speakerLabel: 'Agent (Priya M.):',
    tagClass: 'speaker-agent-tag',
    bubbleClass: 'speaker-agent',
    text: "Perfect sir! Saturday 11:30 AM VIP slot lock kar diya hai aur floor plan WhatsApp par dispatch ho gaya hai.",
    talkAgent: 42,
    talkCust: 58,
    sentiment: '⚡ VIP Lead: Ready to Close (96%)',
    sentimentClass: 'sentiment-hot',
    leadScore: '🎯 Lead Score: 98/100 (Top Tier ⚡)',
    leadScoreClass: 'sentiment-hot',
    bulletId: 'ai-bullet-action',
    durationSecs: 3
  }
];

function toggleAiCallDemo() {
  const btn = document.getElementById('ai-play-btn');
  const waveform = document.getElementById('ai-waveform');
  if (!btn || !waveform) return;

  if (isAiDemoPlaying) {
    pauseAiCallDemo();
  } else {
    startAiCallDemo();
  }
}

function startAiCallDemo() {
  const btn = document.getElementById('ai-play-btn');
  const waveform = document.getElementById('ai-waveform');
  const liveBadge = document.getElementById('ai-live-badge');
  const transcriptBox = document.getElementById('ai-live-transcript');

  if (!btn || !waveform) return;

  isAiDemoPlaying = true;
  waveform.classList.add('playing');
  if (liveBadge) liveBadge.style.display = 'inline-flex';

  btn.innerHTML = `<svg width="16" height="16" fill="currentColor" viewBox="0 0 24 24"><path d="M6 4h4v16H6V4zm8 0h4v16h-4V4z"/></svg> <span>Pause Live Stream</span>`;
  btn.style.background = 'var(--gradient-cyan)';
  btn.style.color = 'var(--leads-navy-dark)';

  // If at start, clear transcript container
  if (aiCurrentStepIndex === 0 && transcriptBox) {
    transcriptBox.innerHTML = '';
    resetAiBullets();
  }

  // Start real-time elapsed timer
  clearInterval(aiTimerInterval);
  aiTimerInterval = setInterval(updateAiTimerAndPlayhead, 250);

  // Play dialogue steps sequentially
  streamNextAiDialogueStep();
}

function pauseAiCallDemo() {
  const btn = document.getElementById('ai-play-btn');
  const waveform = document.getElementById('ai-waveform');
  const liveBadge = document.getElementById('ai-live-badge');

  isAiDemoPlaying = false;
  if (waveform) waveform.classList.remove('playing');
  if (liveBadge) liveBadge.style.display = 'none';

  if (btn) {
    btn.innerHTML = `<svg width="16" height="16" fill="currentColor" viewBox="0 0 24 24"><path d="M8 5v14l11-7z"/></svg> <span>Resume Live Stream</span>`;
    btn.style.background = 'var(--gradient-btn)';
    btn.style.color = '#FFFFFF';
  }

  clearInterval(aiTimerInterval);
  clearTimeout(aiTypewriterTimeout);
}

function updateAiTimerAndPlayhead() {
  aiTotalElapsedSecs += 0.25;
  const totalDuration = 10.0;
  const playhead = document.getElementById('ai-waveform-playhead');
  const timerText = document.getElementById('ai-call-timer');

  const progressPct = Math.min((aiTotalElapsedSecs / totalDuration) * 100, 100);
  if (playhead) {
    playhead.style.left = progressPct + '%';
  }

  if (timerText) {
    const mins = Math.floor(aiTotalElapsedSecs / 60);
    const secs = Math.floor(aiTotalElapsedSecs % 60);
    timerText.textContent = `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')} / 00:10`;
  }
}

function streamNextAiDialogueStep() {
  if (!isAiDemoPlaying) return;

  if (aiCurrentStepIndex >= aiDemoScript.length) {
    // Demo sequence finished
    onAiDemoCompleted();
    return;
  }

  const step = aiDemoScript[aiCurrentStepIndex];
  const transcriptBox = document.getElementById('ai-live-transcript');
  if (!transcriptBox) return;

  // Update Talk Ratio Bar & Text
  const talkAgentBar = document.getElementById('ai-talk-ratio-agent');
  const talkCustBar = document.getElementById('ai-talk-ratio-cust');
  const talkAgentText = document.getElementById('ai-talk-agent-pct');
  const talkCustText = document.getElementById('ai-talk-cust-pct');

  if (talkAgentBar) talkAgentBar.style.width = step.talkAgent + '%';
  if (talkCustBar) talkCustBar.style.width = step.talkCust + '%';
  if (talkAgentText) talkAgentText.textContent = step.talkAgent + '%';
  if (talkCustText) talkCustText.textContent = step.talkCust + '%';

  // Update Sentiment Badge
  const sentimentBadge = document.getElementById('ai-sentiment-badge');
  const sentimentText = document.getElementById('ai-sentiment-text');
  if (sentimentBadge && sentimentText) {
    sentimentBadge.className = 'sentiment-badge ' + step.sentimentClass;
    sentimentText.textContent = 'Sentiment: ' + step.sentiment;
  }

  // Update Lead Score Badge
  const leadScoreBadge = document.getElementById('ai-lead-score-badge');
  if (leadScoreBadge) {
    leadScoreBadge.className = 'sentiment-badge ' + step.leadScoreClass;
    leadScoreBadge.innerHTML = `<span>${step.leadScore}</span>`;
  }

  // Highlight Right Card Bullet
  highlightAiBullet(step.bulletId);

  // Create active dialogue row
  const turnEl = document.createElement('div');
  turnEl.className = `transcript-turn ${step.bubbleClass} active-speaker`;
  turnEl.innerHTML = `<span class="speaker-tag ${step.tagClass}">${step.speakerLabel}</span> <span class="stream-text"></span><span class="transcript-cursor">▌</span>`;
  transcriptBox.appendChild(turnEl);
  transcriptBox.scrollTop = transcriptBox.scrollHeight;

  const textSpan = turnEl.querySelector('.stream-text');
  const cursorSpan = turnEl.querySelector('.transcript-cursor');
  let charIndex = 0;
  const fullText = step.text;
  const typeSpeed = Math.max(20, Math.floor((step.durationSecs * 1000) / fullText.length));

  function typeNextChar() {
    if (!isAiDemoPlaying) return;

    if (charIndex < fullText.length) {
      textSpan.textContent += fullText.charAt(charIndex);
      charIndex++;
      transcriptBox.scrollTop = transcriptBox.scrollHeight;
      aiTypewriterTimeout = setTimeout(typeNextChar, typeSpeed);
    } else {
      // Finished typing this turn
      turnEl.classList.remove('active-speaker');
      if (cursorSpan) cursorSpan.remove();
      aiCurrentStepIndex++;
      aiTypewriterTimeout = setTimeout(streamNextAiDialogueStep, 700);
    }
  }

  typeNextChar();
}

function highlightAiBullet(bulletId) {
  if (!bulletId) return;
  const bullet = document.getElementById(bulletId);
  if (bullet) {
    bullet.classList.add('is-highlighted');
  }
}

function resetAiBullets() {
  ['ai-bullet-req', 'ai-bullet-budget', 'ai-bullet-action'].forEach(id => {
    const el = document.getElementById(id);
    if (el) el.classList.remove('is-highlighted');
  });
}

function onAiDemoCompleted() {
  pauseAiCallDemo();
  const btn = document.getElementById('ai-play-btn');
  if (btn) {
    btn.innerHTML = `<svg width="16" height="16" fill="currentColor" viewBox="0 0 24 24"><path d="M12 5V1L7 6l5 5V7c3.31 0 6 2.69 6 6s-2.69 6-6 6-6-2.69-6-6H4c0 4.42 3.58 8 8 8s8-3.58 8-8-3.58-8-8-8z"/></svg> <span>Replay AI Live Demo</span>`;
    btn.style.background = 'var(--gradient-btn)';
    btn.style.color = '#FFFFFF';
  }
  // Reset index for replay
  aiCurrentStepIndex = 0;
  aiTotalElapsedSecs = 0;
}

// Auto-trigger when scrolled into view
document.addEventListener('DOMContentLoaded', () => {
  const aiSection = document.getElementById('ai-waveform');
  if (aiSection && 'IntersectionObserver' in window) {
    let hasAutoStarted = false;
    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting && !hasAutoStarted && !isAiDemoPlaying) {
          hasAutoStarted = true;
          setTimeout(() => {
            if (!isAiDemoPlaying) {
              startAiCallDemo();
            }
          }, 600);
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.35 });
    observer.observe(aiSection);
  }
});
