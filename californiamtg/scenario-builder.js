/* ============================================================
   California Mortgage — Scenario Builder & Concierge Intake
   Powered by West Coast Capital Mortgage Inc.

   Config-driven, branching, multi-step questionnaire. Vanilla JS,
   no dependencies, no build step. Mounts into #scenarioBuilder.

   Flow:  Goal  ->  scenario-specific questions  ->  general questions
          ->  contact  ->  submit  ->  thank-you / routing
   ============================================================ */
(function () {
  "use strict";

  var mount = document.getElementById("scenarioBuilder");
  if (!mount) return;

  /* ----------------------------------------------------------
     1. QUESTION LIBRARY
     Step kinds:
       choice  -> single-select option cards (auto-advances)
       form    -> grouped inputs (text/number/tel/email/select/radio/textarea)
       note    -> educational panel (no input)
       contact -> final contact form
     ---------------------------------------------------------- */

  // -- Step 1: the entry question that drives all branching --
  var GOAL = {
    id: "goal", kind: "choice",
    title: "What would you like guidance with?",
    sub: "Pick the closest match — you can add detail in the next steps.",
    options: [
      { v: "buying",           label: "Buying a home" },
      { v: "refinancing",      label: "Refinancing" },
      { v: "lowering-payment", label: "Lowering my monthly payment" },
      { v: "rates",            label: "Understanding rates" },
      { v: "cashout",          label: "Cash-out refinance" },
      { v: "investment",       label: "Investment property / DSCR" },
      { v: "self-employed",    label: "Self-employed mortgage options" },
      { v: "realtor",          label: "Realtor / client scenario" },
      { v: "denied",           label: "I was denied by a bank" },
      { v: "not-sure",         label: "Not sure yet" }
    ]
  };

  // -- Reusable building blocks --
  var YESNO = [{ v: "Yes", label: "Yes" }, { v: "No", label: "No" }, { v: "Not sure", label: "Not sure" }];
  var CREDIT = {
    id: "creditRange", kind: "choice", title: "Estimated credit range",
    options: ["Excellent", "Good", "Fair", "Needs work", "Not sure"].map(s => ({ v: s, label: s }))
  };
  var PROPERTY_TYPE = {
    id: "propertyType", kind: "choice", title: "Property type",
    options: ["Single-family", "Condo", "Townhome", "2-4 units", "Investment property"].map(s => ({ v: s, label: s }))
  };
  var OCCUPANCY = {
    id: "occupancy", kind: "choice", title: "Occupancy",
    options: ["Primary residence", "Second home", "Investment"].map(s => ({ v: s, label: s }))
  };
  var BUY_OR_REFI = {
    id: "buyOrRefi", kind: "choice", title: "Are you buying or refinancing?",
    options: [{ v: "Buying", label: "Buying" }, { v: "Refinancing", label: "Refinancing" }]
  };
  var INCOME_TYPE = {
    id: "incomeType", kind: "choice", title: "Income type",
    options: ["W2", "Self-employed", "1099", "Business owner", "Mixed income", "Not sure"].map(s => ({ v: s, label: s }))
  };

  // -- Scenario question sets --
  var PURCHASE = [
    { id: "purchaseNumbers", kind: "form", title: "Your purchase, by the numbers", sub: "Estimates are fine.",
      fields: [
        { name: "purchasePrice", label: "Estimated purchase price", type: "number", prefix: "$", placeholder: "e.g. 850,000" },
        { name: "downPayment",   label: "Estimated down payment",   type: "number", prefix: "$", placeholder: "e.g. 170,000" }
      ] },
    PROPERTY_TYPE,
    OCCUPANCY,
    { id: "purchasePrefs", kind: "form", title: "A few quick yes / no questions",
      fields: [
        { name: "hasRealtor",      label: "Are you already working with a Realtor?", type: "radio", options: ["Yes", "No"] },
        { name: "needPreapproval", label: "Do you need a pre-approval letter?",      type: "radio", options: ["Yes", "No"] },
        { name: "comparingPayment",label: "Are you comparing monthly payment options?", type: "radio", options: ["Yes", "No"] }
      ] },
    { id: "loanInterest", kind: "choice", title: "Are you interested in a particular program?",
      options: ["Jumbo", "FHA / VA", "Conventional", "Not sure"].map(s => ({ v: s, label: s })) },
    INCOME_TYPE,
    CREDIT
  ];

  var REFI = [
    { id: "refiNumbers", kind: "form", title: "Your current loan", sub: "Share what you know — estimates are fine.",
      fields: [
        { name: "homeValue",      label: "Current estimated home value", type: "number", prefix: "$", placeholder: "e.g. 900,000" },
        { name: "loanBalance",    label: "Current loan balance",         type: "number", prefix: "$", placeholder: "e.g. 540,000" },
        { name: "currentRate",    label: "Current interest rate (if known)", type: "number", suffix: "%", placeholder: "e.g. 6.75", required: false },
        { name: "currentPayment", label: "Current monthly payment (if known)", type: "number", prefix: "$", placeholder: "e.g. 3,400", required: false }
      ] },
    { id: "refiGoal", kind: "choice", title: "Main refinance goal",
      options: ["Lower monthly payment", "Cash-out", "Remove mortgage insurance", "Pay off debt",
                "Switch loan type", "Shorten loan term", "Not sure"].map(s => ({ v: s, label: s })) },
    { id: "keepDuration", kind: "choice", title: "How long do you plan to keep the property?",
      options: ["Under 2 years", "2-5 years", "5-10 years", "10+ years", "Not sure"].map(s => ({ v: s, label: s })) },
    { id: "occupancy", kind: "choice", title: "Is the property primary, second home, or investment?",
      options: ["Primary residence", "Second home", "Investment"].map(s => ({ v: s, label: s })) }
  ];

  var LOWER = [
    { id: "lowerNumbers", kind: "form", title: "Your current payment", sub: "Estimates are fine.",
      fields: [
        { name: "currentPayment", label: "Current monthly payment",        type: "number", prefix: "$", placeholder: "e.g. 3,400" },
        { name: "currentRate",    label: "Current interest rate (if known)",type: "number", suffix: "%", placeholder: "e.g. 7.1", required: false },
        { name: "loanBalance",    label: "Current loan balance",           type: "number", prefix: "$", placeholder: "e.g. 540,000" },
        { name: "homeValue",      label: "Estimated property value",       type: "number", prefix: "$", placeholder: "e.g. 900,000" }
      ] },
    { id: "openToPoints", kind: "choice", title: "Are you open to paying points if it lowers the rate?", options: YESNO },
    { id: "reduceReason", kind: "choice", title: "Why are you trying to reduce the payment?",
      options: ["High rate", "High debt", "Insurance / tax increase", "Income change", "ARM adjustment", "Other"].map(s => ({ v: s, label: s })) },
    { id: "considerRefi", kind: "choice", title: "Would you consider refinancing if the numbers make sense?",
      options: [{ v: "Yes", label: "Yes" }, { v: "No", label: "No" }, { v: "Maybe", label: "Maybe" }] }
  ];

  var RATES = [
    BUY_OR_REFI,
    { id: "rateNumbers", kind: "form", title: "A few numbers to frame the rate", sub: "Estimates are fine.",
      fields: [
        { name: "priceOrValue", label: "Estimated purchase price or property value", type: "number", prefix: "$", placeholder: "e.g. 850,000" },
        { name: "loanAmount",   label: "Estimated loan amount",                       type: "number", prefix: "$", placeholder: "e.g. 680,000" },
        { name: "downOrEquity", label: "Down payment or equity estimate",             type: "number", prefix: "$", placeholder: "e.g. 170,000" }
      ] },
    CREDIT,
    PROPERTY_TYPE,
    OCCUPANCY,
    { id: "ratePriority", kind: "choice", title: "What matters most to you?",
      options: ["Lowest rate", "Lowest monthly payment", "Lowest closing costs", "No points", "Comparing options", "Not sure"].map(s => ({ v: s, label: s })) },
    { id: "rateNote", kind: "note", title: "A quick, helpful note",
      body: "Sometimes the lowest rate is not always the best option. Points, closing costs, loan term, monthly payment, and how long you plan to keep the property all matter. A licensed mortgage professional can help you compare the full picture." }
  ];

  var INVESTOR = [
    BUY_OR_REFI,
    { id: "invNumbers", kind: "form", title: "The investment property", sub: "Estimates are fine.",
      fields: [
        { name: "priceOrValue", label: "Property value or purchase price", type: "number", prefix: "$", placeholder: "e.g. 650,000" },
        { name: "rentalIncome", label: "Estimated rental income (monthly)", type: "number", prefix: "$", placeholder: "e.g. 3,800" }
      ] },
    PROPERTY_TYPE,
    { id: "ownership", kind: "choice", title: "Is it owned personally or in an LLC?",
      options: ["Owned personally", "Held in an LLC", "Not sure"].map(s => ({ v: s, label: s })) },
    { id: "qualifyRental", kind: "choice", title: "Do you want to qualify based on rental income?", options: YESNO },
    { id: "propsOwned", kind: "choice", title: "How many investment properties do you own?",
      options: ["0", "1-2", "3-5", "6-10", "10+"].map(s => ({ v: s, label: s })) },
    { id: "rentalType", kind: "choice", title: "Is this long-term, short-term, or mixed?",
      options: ["Long-term rental", "Short-term rental", "Mixed"].map(s => ({ v: s, label: s })) }
  ];

  var SELFEMP = [
    { id: "seType", kind: "choice", title: "How is your income structured?",
      options: ["Business owner", "1099", "Contractor", "Mixed income"].map(s => ({ v: s, label: s })) },
    { id: "seLength", kind: "choice", title: "How long have you been self-employed?",
      options: ["Under 1 year", "1-2 years", "2-5 years", "5+ years"].map(s => ({ v: s, label: s })) },
    { id: "taxShowIncome", kind: "choice", title: "Do your tax returns show enough income?", options: YESNO },
    { id: "bankStatements", kind: "choice", title: "Do you have business or personal bank statements?",
      options: ["Business", "Personal", "Both", "Neither"].map(s => ({ v: s, label: s })) },
    { id: "seProgram", kind: "choice", title: "Are you looking for a particular option?",
      options: ["Bank statement", "P&L", "Non-QM", "Not sure"].map(s => ({ v: s, label: s })) },
    BUY_OR_REFI,
    { id: "seNumbers", kind: "form", title: "Estimated loan amount or property value",
      fields: [
        { name: "loanOrValue", label: "Estimated loan amount or property value", type: "number", prefix: "$", placeholder: "e.g. 750,000" }
      ] }
  ];

  var REALTOR = [
    { id: "representing", kind: "choice", title: "Are you representing the buyer or seller?",
      options: ["Buyer", "Seller", "Both"].map(s => ({ v: s, label: s })) },
    { id: "realtorUrgent", kind: "choice", title: "Is this urgent?", options: [{ v: "Yes", label: "Yes" }, { v: "No", label: "No" }] },
    { id: "realtorIssue", kind: "choice", title: "What is the issue?",
      options: ["Buyer denied", "Need second opinion", "Need fast pre-approval", "Jumbo file",
                "Self-employed buyer", "Investor / DSCR", "Condo issue", "Credit issue", "Other"].map(s => ({ v: s, label: s })) },
    { id: "realtorNumbers", kind: "form", title: "The deal",
      fields: [
        { name: "purchasePrice", label: "Estimated purchase price", type: "number", prefix: "$", placeholder: "e.g. 1,200,000" },
        { name: "closingTimeline", label: "Offer deadline or closing timeline", type: "text", placeholder: "e.g. close by Aug 15", required: false }
      ] },
    { id: "clientPermission", kind: "choice", title: "Client contact permission",
      options: [{ v: "Yes, contact client directly", label: "Yes, contact client directly" },
                { v: "Contact me first", label: "Contact me first" }] }
  ];

  var DENIED = [
    { id: "denyReason", kind: "choice", title: "What was the reason?",
      options: ["Income", "Credit", "Debt-to-income", "Self-employed income", "Property issue",
                "Condo issue", "Down payment", "Reserves", "Not sure"].map(s => ({ v: s, label: s })) },
    { id: "denialLetter", kind: "choice", title: "Do you have a denial letter?", options: [{ v: "Yes", label: "Yes" }, { v: "No", label: "No" }] },
    BUY_OR_REFI,
    { id: "deniedUrgency", kind: "choice", title: "How urgent is the situation?",
      options: ["Today / urgent", "This week", "This month", "Just researching"].map(s => ({ v: s, label: s })) },
    { id: "secondOpinion", kind: "choice", title: "Would you like a second opinion?", options: [{ v: "Yes", label: "Yes" }, { v: "No", label: "No" }] }
  ];

  var SCENARIO = {
    buying: PURCHASE,
    refinancing: REFI,
    cashout: REFI,            // cash-out reuses the refinance set (categorized separately)
    "lowering-payment": LOWER,
    rates: RATES,
    investment: INVESTOR,
    "self-employed": SELFEMP,
    realtor: REALTOR,
    denied: DENIED,
    "not-sure": []
  };

  // -- General questions asked of everyone --
  var GENERAL = [
    { id: "userType", kind: "choice", title: "What best describes you?",
      options: ["Home Buyer", "Homeowner", "Self-Employed Borrower", "Real Estate Investor", "Realtor / Agent", "Not Sure"].map(s => ({ v: s, label: s })) },
    { id: "propertyState", kind: "choice", title: "Where is the property?",
      options: ["California", "Florida", "Other state", "I have not chosen a property yet"].map(s => ({ v: s, label: s })) },
    { id: "timeline", kind: "choice", title: "How soon do you need help?",
      options: ["Today / urgent", "This week", "This month", "Just researching"].map(s => ({ v: s, label: s })) },
    { id: "nextStep", kind: "choice", title: "Preferred next step",
      options: ["AI scenario review", "Talk to a licensed mortgage professional", "Get pre-approved", "Learn loan options first"].map(s => ({ v: s, label: s })) }
  ];

  // -- Final contact step --
  var CONTACT = {
    id: "contact", kind: "contact", title: "Where should we send your scenario?",
    sub: "A licensed mortgage professional can review it and reach out.",
    fields: [
      { name: "fullName", label: "Full name", type: "text", required: true, placeholder: "First and last name" },
      { name: "phone",    label: "Phone",     type: "tel",  required: true, placeholder: "(310) 555-0199" },
      { name: "email",    label: "Email",     type: "email",required: true, placeholder: "you@example.com" },
      { name: "contactMethod", label: "Preferred contact method", type: "radio", options: ["Call", "Text", "Email"], required: true },
      { name: "bestTime", label: "Best time to contact", type: "select", options: ["Morning", "Afternoon", "Evening", "Anytime"] },
      { name: "message",  label: "Tell us anything else about your scenario", type: "textarea", required: false, placeholder: "Optional — share anything that helps." }
    ]
  };

  /* ----------------------------------------------------------
     2. STATE + FLOW
     ---------------------------------------------------------- */
  var answers = {};
  var index = 0;

  function buildFlow() {
    var flow = [GOAL];
    var goal = answers.goal;
    if (goal && SCENARIO[goal]) flow = flow.concat(SCENARIO[goal]);
    flow = flow.concat(GENERAL);
    flow.push(CONTACT);
    return flow;
  }

  /* ----------------------------------------------------------
     3. RENDERING
     ---------------------------------------------------------- */
  function el(tag, cls, html) {
    var n = document.createElement(tag);
    if (cls) n.className = cls;
    if (html != null) n.innerHTML = html;
    return n;
  }

  function render() {
    var flow = buildFlow();
    if (index >= flow.length) { return renderThankYou(); }
    var step = flow[index];
    var total = flow.length;

    mount.innerHTML = "";
    mount.classList.remove("is-thankyou");

    // Progress
    var pct = Math.round(((index) / total) * 100);
    var prog = el("div", "builder-progress");
    prog.innerHTML =
      '<div class="builder-progress-meta"><span>Step ' + (index + 1) + ' of ' + total + '</span>' +
      '<span>' + Math.max(pct, 2) + '% complete</span></div>' +
      '<div class="builder-bar"><span style="width:' + Math.max(pct, 2) + '%"></span></div>';
    mount.appendChild(prog);

    // Step body (animated in)
    var body = el("div", "builder-step");
    var head = el("div", "step-head");
    head.appendChild(el("h3", "step-title", step.title));
    if (step.sub) head.appendChild(el("p", "step-sub", step.sub));
    body.appendChild(head);

    if (step.kind === "choice") body.appendChild(renderChoice(step));
    else if (step.kind === "note") body.appendChild(renderNote(step));
    else body.appendChild(renderForm(step)); // form + contact

    mount.appendChild(body);

    // Nav
    var nav = el("div", "builder-nav");
    if (index > 0) {
      var back = el("button", "btn btn-ghost", "&larr; Back");
      back.type = "button";
      back.addEventListener("click", function () { index--; render(); scrollIntoView(); });
      nav.appendChild(back);
    } else {
      nav.appendChild(el("span", "", "")); // spacer
    }

    if (step.kind === "choice") {
      var hint = el("span", "builder-hint", "Select an option to continue");
      nav.appendChild(hint);
    } else {
      var next = el("button", "btn btn-gold", step.kind === "contact" ? "Submit Scenario" : "Continue &rarr;");
      next.type = "button";
      next.addEventListener("click", function () {
        if (collectForm(step)) {
          if (step.kind === "contact") return submit();
          index++; render(); scrollIntoView();
        }
      });
      nav.appendChild(next);
    }
    mount.appendChild(nav);

    requestAnimationFrame(function () { body.classList.add("in"); });
  }

  function renderChoice(step) {
    var wrap = el("div", "options" + (step.options.length > 6 ? " options-compact" : ""));
    step.options.forEach(function (opt) {
      var b = el("button", "option", '<span class="option-label">' + opt.label + '</span><span class="option-check" aria-hidden="true">&#10003;</span>');
      b.type = "button";
      if (answers[step.id] === opt.v) b.classList.add("selected");
      b.addEventListener("click", function () {
        answers[step.id] = opt.v;
        // visual select, then advance
        wrap.querySelectorAll(".option").forEach(function (o) { o.classList.remove("selected"); });
        b.classList.add("selected");
        window.setTimeout(function () { index++; render(); scrollIntoView(); }, 240);
      });
      wrap.appendChild(b);
    });
    return wrap;
  }

  function renderNote(step) {
    var wrap = el("div", "builder-note");
    wrap.appendChild(el("p", "", step.body));
    return wrap;
  }

  function renderForm(step) {
    var grid = el("div", "field-grid" + (step.kind === "contact" ? " field-grid-contact" : ""));
    step.fields.forEach(function (f) {
      var field = el("div", "field" + (f.type === "textarea" || f.type === "radio" ? " field-full" : ""));
      var id = step.id + "_" + f.name;
      var labelHtml = f.label + (f.required ? ' <span class="req">*</span>' : "");
      field.appendChild(el("label", "field-label", labelHtml)).setAttribute("for", id);

      var val = answers[f.name] != null ? answers[f.name] : "";

      if (f.type === "radio") {
        var rg = el("div", "radio-row");
        f.options.forEach(function (o) {
          var rid = id + "_" + o;
          var pill = el("label", "radio-pill" + (val === o ? " checked" : ""));
          pill.innerHTML = '<input type="radio" name="' + id + '" value="' + o + '"' + (val === o ? " checked" : "") + '><span>' + o + '</span>';
          pill.querySelector("input").addEventListener("change", function () {
            rg.querySelectorAll(".radio-pill").forEach(function (p) { p.classList.remove("checked"); });
            pill.classList.add("checked");
          });
          rg.appendChild(pill);
        });
        field.appendChild(rg);
      } else if (f.type === "select") {
        var sel = el("select", "field-input");
        sel.id = id; sel.name = f.name;
        sel.appendChild(el("option", "", "Select...")).value = "";
        f.options.forEach(function (o) {
          var op = el("option", "", o); op.value = o;
          if (val === o) op.selected = true;
          sel.appendChild(op);
        });
        field.appendChild(sel);
      } else if (f.type === "textarea") {
        var ta = el("textarea", "field-input");
        ta.id = id; ta.name = f.name; ta.rows = 3;
        if (f.placeholder) ta.placeholder = f.placeholder;
        ta.value = val;
        field.appendChild(ta);
      } else {
        var inWrap = el("div", "input-wrap" + (f.prefix ? " has-prefix" : "") + (f.suffix ? " has-suffix" : ""));
        if (f.prefix) inWrap.appendChild(el("span", "affix prefix", f.prefix));
        var inp = el("input", "field-input");
        inp.id = id; inp.name = f.name; inp.type = (f.type === "number" ? "text" : f.type);
        if (f.type === "number") inp.inputMode = "decimal";
        if (f.placeholder) inp.placeholder = f.placeholder;
        inp.value = val;
        inWrap.appendChild(inp);
        if (f.suffix) inWrap.appendChild(el("span", "affix suffix", f.suffix));
        field.appendChild(inWrap);
      }
      field.appendChild(el("p", "field-error", ""));
      grid.appendChild(field);
    });
    return grid;
  }

  // Reads inputs of the current step into `answers`; validates required fields.
  function collectForm(step) {
    if (step.kind === "note") return true;
    var ok = true;
    step.fields.forEach(function (f) {
      var id = step.id + "_" + f.name;
      var value, anchor;
      if (f.type === "radio") {
        var checked = mount.querySelector('input[name="' + id + '"]:checked');
        value = checked ? checked.value : "";
        anchor = mount.querySelector('input[name="' + id + '"]');
      } else {
        var node = mount.querySelector('[id="' + id + '"]');
        value = node ? node.value.trim() : "";
        anchor = node;
      }
      var errEl = anchor ? anchor.closest(".field").querySelector(".field-error") : null;

      // A field is required only when explicitly marked required:true.
      var fieldErr = "";
      if (f.required === true && !value) fieldErr = "This field is required.";
      else if (value && f.type === "email" && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value)) fieldErr = "Enter a valid email.";
      else if (value && f.type === "tel" && value.replace(/\D/g, "").length < 10) fieldErr = "Enter a valid phone number.";

      if (errEl) errEl.textContent = fieldErr;
      if (fieldErr) ok = false;
      if (value) answers[f.name] = value; else delete answers[f.name];
    });
    return ok;
  }

  function scrollIntoView() {
    var sec = document.getElementById("builder");
    if (sec && window.scrollY > sec.offsetTop + 40) {
      sec.scrollIntoView({ behavior: "smooth", block: "start" });
    }
  }

  /* ----------------------------------------------------------
     4. LEAD CATEGORY LOGIC + STRUCTURED LEAD OBJECT
     ---------------------------------------------------------- */
  function computeLeadCategories(a) {
    var c = [];
    function add(x) { if (c.indexOf(x) === -1) c.push(x); }
    switch (a.goal) {
      case "buying": add("Purchase Lead"); break;
      case "refinancing": add("Refinance Lead"); break;
      case "lowering-payment": add("Lower Payment Lead"); break;
      case "rates": add("Rate Comparison Lead"); break;
      case "cashout": add("Cash-Out Lead"); break;
      case "investment": add("Investor / DSCR Lead"); break;
      case "self-employed": add("Self-Employed Lead"); break;
      case "realtor": add("Realtor Scenario Lead"); break;
      case "denied": add("Bank Denial / Second Opinion Lead"); break;
    }
    // cross-cutting signals
    if (a.refiGoal === "Cash-out") add("Cash-Out Lead");
    if (a.userType === "Self-Employed Borrower" || ["Self-employed", "Business owner", "1099"].indexOf(a.incomeType) !== -1) add("Self-Employed Lead");
    if (a.userType === "Real Estate Investor") add("Investor / DSCR Lead");
    if (a.realtorIssue === "Buyer denied") add("Bank Denial / Second Opinion Lead");
    if ([a.timeline, a.deniedUrgency].indexOf("Today / urgent") !== -1 || a.realtorUrgent === "Yes") add("Urgent Lead");
    return c;
  }

  function getUTM() {
    var p = new URLSearchParams(window.location.search);
    return {
      utm_source: p.get("utm_source") || "",
      utm_medium: p.get("utm_medium") || "",
      utm_campaign: p.get("utm_campaign") || "",
      utm_term: p.get("utm_term") || "",
      utm_content: p.get("utm_content") || "",
      gclid: p.get("gclid") || "",
      referrer: document.referrer || "",
      landingPage: window.location.href
    };
  }

  function estimatedValue(a) {
    return a.purchasePrice || a.homeValue || a.priceOrValue || a.loanOrValue || a.loanAmount || "";
  }

  function buildLead() {
    var a = answers;
    return {
      leadCategories: computeLeadCategories(a),
      userType: a.userType || "",
      scenarioType: a.goal || "",
      timeline: a.timeline || a.deniedUrgency || "",
      propertyState: a.propertyState || "",
      estimatedValue: estimatedValue(a),
      preferredNextStep: a.nextStep || "",
      contact: {
        fullName: a.fullName || "",
        phone: a.phone || "",
        email: a.email || "",
        contactMethod: a.contactMethod || "",
        bestTime: a.bestTime || "",
        message: a.message || ""
      },
      answers: Object.assign({}, a),
      source: getUTM(),
      submittedAt: new Date().toISOString()
    };
  }

  /* ----------------------------------------------------------
     5. SUBMIT HANDLER (placeholder — connect integrations here)
     ---------------------------------------------------------- */
  function submit() {
    var lead = buildLead();

    /* =========================================================
       TODO: connect lead submission endpoint here.

       This is where the structured `lead` object should be sent.
       Wire up one or more of the following destinations:

         - CRM (e.g. HubSpot / Salesforce / GoHighLevel)
         - Email notification (transactional email / SMTP / SendGrid)
         - Zapier webhook   (https://hooks.zapier.com/...)
         - Make webhook     (https://hook.make.com/...)
         - Google Sheet     (Apps Script Web App endpoint)
         - Mortgage LOS     (Encompass / Arive / LendingPad, etc.)
         - WCCI.online AI payload (forward scenario for AI review)

       Example (uncomment + set ENDPOINT):
       // var ENDPOINT = "https://hook.example.com/california-mortgage-lead";
       // return fetch(ENDPOINT, {
       //   method: "POST",
       //   headers: { "Content-Type": "application/json" },
       //   body: JSON.stringify(lead)
       // }).then(function(){ renderThankYou(lead); })
       //   .catch(function(){ renderThankYou(lead); }); // still thank the user
       ========================================================= */

    // Placeholder: log + persist locally so nothing is lost before integration.
    try {
      console.log("[California Mortgage] Lead captured (placeholder):", lead);
      window.localStorage.setItem("cm_last_lead", JSON.stringify(lead));
    } catch (e) { /* storage may be unavailable */ }

    renderThankYou(lead);
  }

  /* ----------------------------------------------------------
     6. THANK-YOU + SMART ROUTING
     ---------------------------------------------------------- */
  function renderThankYou(lead) {
    lead = lead || buildLead();
    var next = lead.preferredNextStep;

    var primary = { label: "Continue to AI Scenario Review", href: "https://wcci.online" };
    if (next === "Talk to a licensed mortgage professional") primary = { label: "Talk to a Licensed Mortgage Professional", href: "/contact.html" };
    else if (next === "Get pre-approved") primary = { label: "Continue to Secure Pre-Approval", href: "/apply" };
    else if (next === "Learn loan options first") primary = { label: "Explore Loan Options", href: "/education/which-program-fits.html" };

    var cats = lead.leadCategories.length ? lead.leadCategories.join(" &middot; ") : "Scenario received";

    mount.classList.add("is-thankyou");
    mount.innerHTML =
      '<div class="thankyou">' +
        '<div class="ty-mark" aria-hidden="true">&#10003;</div>' +
        '<h3>Thank you' + (lead.contact.fullName ? ", " + escapeHtml(lead.contact.fullName.split(" ")[0]) : "") + '.</h3>' +
        '<p class="ty-lead">Your scenario has been received and can be reviewed by West Coast Capital Mortgage Inc.</p>' +
        '<p class="ty-cats"><span>Scenario tags:</span> ' + cats + '</p>' +
        '<div class="ty-actions">' +
          '<a class="btn btn-gold btn-lg" href="' + primary.href + '">' + primary.label + '</a>' +
        '</div>' +
        '<div class="ty-alt">' +
          '<span>Or choose another path:</span>' +
          '<a href="https://wcci.online">AI Scenario Review</a>' +
          '<a href="/contact.html">Talk to a Professional</a>' +
          '<a href="/apply">Secure Pre-Approval</a>' +
        '</div>' +
        '<p class="ty-compliance">This is not a loan approval, loan commitment, or rate quote. ' +
          'Final loan options are subject to review by a licensed mortgage professional.</p>' +
      '</div>';
    scrollIntoView();
  }

  function escapeHtml(s) {
    return String(s).replace(/[&<>"']/g, function (m) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[m];
    });
  }

  /* ----------------------------------------------------------
     7. PUBLIC ENTRY: start / restart (used by hero + nav CTAs)
     ---------------------------------------------------------- */
  window.CMScenario = {
    start: function (goal) {
      if (goal && SCENARIO.hasOwnProperty(goal)) { answers = { goal: goal }; index = 1; }
      else { answers = {}; index = 0; }
      render();
    }
  };

  // Initial render — honor ?goal=<scenario> deep links (e.g. from /scenarios.html)
  var qpGoal = new URLSearchParams(window.location.search).get("goal");
  if (qpGoal && SCENARIO.hasOwnProperty(qpGoal)) { window.CMScenario.start(qpGoal); }
  else { render(); }
})();
