/* WCCI AI Mortgage Assistant — front-end for the West Coast Capital Mortgage site.
   Talks to the existing /.netlify/functions/chat proxy (Anthropic) when deployed,
   and falls back to a fully offline Short Scenario Intake + smart document
   checklist so it works locally and without API keys.
   Preliminary educational guidance only — not a loan approval or commitment. */
(function () {
  "use strict";
  var root = document.getElementById("wcci-tool");
  if (!root) return;

  var CHAT_ENDPOINT = "/.netlify/functions/chat";
  var LEAD_ENDPOINT = "/.netlify/functions/partial-lead";
  var MODEL = "claude-sonnet-4-6";

  var SYSTEM = [
    "You are the WCCI AI Mortgage Assistant for West Coast Capital Mortgage Inc. (NMLS #2817729).",
    "You provide PRELIMINARY, EDUCATIONAL mortgage guidance only. You are warm, concise, and professional.",
    "You help borrowers organize goals, review their scenario, identify POSSIBLE loan paths, and prepare a document checklist before they speak with a licensed mortgage professional (MLO).",
    "Ask short questions ONE at a time to learn: loan purpose, state, occupancy, property type, estimated price/value, desired loan amount, down payment/equity, income type, credit range, timeline, and biggest concern. Then ask for name, phone, and email so an MLO can follow up.",
    "You DO NOT approve or deny loans, issue a Loan Estimate, quote or lock rates, pull credit, or commit to lend. If asked for a rate or approval, explain that only a licensed MLO can provide those after full review.",
    "Keep answers brief (2-4 sentences). Avoid crypto, investment-pitch, or tokenization language. This is mortgage lending only.",
    "When you have gathered the borrower's contact info and core scenario, end your message with a single line beginning exactly with 'SCENARIO_COMPLETE:' followed by a compact JSON object with keys: name, phone, email, loanPurpose, state, occupancy, propertyType, purchasePrice, loanAmount, downPayment, incomeType, creditScore, timeline, concern. Do not mention this line to the user."
  ].join(" ");

  /* ---------- Tabs ---------- */
  var tabs = root.querySelectorAll(".wcci-tab");
  var panels = { chat: document.getElementById("wcci-panel-chat"), intake: document.getElementById("wcci-panel-intake") };
  tabs.forEach(function (t) {
    t.addEventListener("click", function () {
      tabs.forEach(function (x) { x.classList.remove("active"); x.setAttribute("aria-selected", "false"); });
      t.classList.add("active"); t.setAttribute("aria-selected", "true");
      var k = t.getAttribute("data-tab");
      panels.chat.classList.toggle("hide", k !== "chat");
      panels.intake.classList.toggle("hide", k !== "intake");
    });
  });
  function showIntake() { tabs.forEach(function (t) { t.click && (t.getAttribute("data-tab") === "intake") && t.click(); }); }

  /* ---------- Chat ---------- */
  var chat = document.getElementById("wcci-chat");
  var form = document.getElementById("wcci-chat-form");
  var input = document.getElementById("wcci-chat-text");
  var history = [];   // {role, content}
  var busy = false;

  function bubble(text, who) {
    var d = document.createElement("div");
    d.className = "wcci-msg " + who;
    d.textContent = text;
    chat.appendChild(d);
    chat.scrollTop = chat.scrollHeight;
    return d;
  }

  bubble("Hi! I'm the WCCI AI Mortgage Assistant. Tell me what you'd like to do — buy a home, refinance, or finance an investment — and I'll help organize your scenario before a licensed mortgage professional reviews it.", "bot");

  function fallback() {
    bubble("The live AI assistant runs on the deployed site (it needs a server connection). You can use the “Short Scenario Intake” tab right now to get your preliminary review and document checklist.", "note");
    showIntake();
  }

  function send(text) {
    if (busy || !text.trim()) return;
    busy = true;
    bubble(text, "user");
    history.push({ role: "user", content: text });
    input.value = "";
    var typing = bubble("…", "bot");
    fetch(CHAT_ENDPOINT, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ model: MODEL, max_tokens: 700, system: SYSTEM, messages: history })
    }).then(function (r) { return r.json(); }).then(function (data) {
      typing.remove();
      if (!data || data.error || !data.content) { fallback(); busy = false; return; }
      var full = (data.content || []).map(function (b) { return b.text || ""; }).join("");
      var display = full, complete = false;
      if (full.indexOf("SCENARIO_COMPLETE:") !== -1) {
        display = full.split("SCENARIO_COMPLETE:")[0].trim();
        complete = true;
      }
      if (display) { bubble(display, "bot"); history.push({ role: "assistant", content: display }); }
      if (complete) bubble("Your preliminary review is ready. A licensed mortgage professional from West Coast Capital Mortgage will follow up. This is not a loan approval or commitment to lend.", "note");
      busy = false;
    }).catch(function () { typing.remove(); fallback(); busy = false; });
  }
  form.addEventListener("submit", function (e) { e.preventDefault(); send(input.value); });

  /* ---------- Offline intake + document checklist (ported from chat.js) ---------- */
  function buildChecklist(s) {
    var income = (s.incomeType || "").toLowerCase();
    var purpose = (s.loanPurpose || "").toLowerCase();
    var concern = (s.concern || "").toLowerCase();
    var occupancy = (s.occupancy || "").toLowerCase();
    var buckets = [];
    var needsBankStmt = concern.indexOf("bank statement") > -1 || concern.indexOf("tax returns too low") > -1;
    var isInvestor = purpose.indexOf("investment") > -1 || occupancy.indexOf("investment") > -1 || income.indexOf("investor") > -1 || concern.indexOf("dscr") > -1;
    var isSelfEmp = income.indexOf("self-employed") > -1 || income.indexOf("1099") > -1 || income.indexOf("business owner") > -1 || income.indexOf("commission") > -1;
    var isW2 = income.indexOf("w-2") > -1 || income.indexOf("w2") > -1;
    var isRefi = purpose.indexOf("refinance") > -1 || purpose.indexOf("cash-out") > -1;
    if (needsBankStmt) buckets.push({ label: "Bank statement / non-QM", items: ["12 or 24 months personal or business bank statements", "Business verification (license, CPA letter, or website)", "Government-issued ID", "Asset statements (savings, retirement, reserves)"] });
    else if (isInvestor) buckets.push({ label: "DSCR / investor", items: ["Lease agreement or market rent estimate", "Property expenses (insurance, taxes, HOA estimate)", "Entity documents if applicable (LLC, trust)", "Asset statements", "Government-issued ID"] });
    else if (isSelfEmp) buckets.push({ label: "Self-employed / business owner", items: ["Last 2 years personal tax returns", "Business tax returns if applicable", "Year-to-date profit and loss statement", "Business bank statements", "Government-issued ID", "Asset statements"] });
    else if (isW2) buckets.push({ label: "W-2 borrower", items: ["Recent paystubs (last 30 days)", "Last 2 years W-2s", "Government-issued ID", "Recent bank statements", "Purchase contract if available"] });
    else buckets.push({ label: "Standard starting list", items: ["Government-issued ID", "Recent paystubs or income documentation", "Last 2 years tax returns", "Recent bank and asset statements"] });
    if (isRefi) buckets.push({ label: "Refinance", items: ["Current mortgage statement", "Homeowners insurance declaration page", "Property tax bill", "Payoff statement if available", "HELOC or second mortgage statement if applicable"] });
    var seen = {}, items = [];
    buckets.forEach(function (b) { b.items.forEach(function (it) { var k = it.toLowerCase(); if (!seen[k]) { seen[k] = 1; items.push(it); } }); });
    return { primaryLabel: buckets.map(function (b) { return b.label; }).join(" + "), items: items };
  }

  function esc(x) { return (x || "").replace(/[&<>]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;" }[c]; }); }

  var ifm = document.getElementById("wcci-intake-form");
  var out = document.getElementById("wcci-result");
  if (ifm) ifm.addEventListener("submit", function (e) {
    e.preventDefault();
    var f = function (id) { var el = document.getElementById(id); return el ? el.value : ""; };
    var s = {
      name: f("name"), phone: f("phone"), email: f("email"), loanPurpose: f("loanPurpose"),
      state: f("state"), occupancy: f("occupancy"), propertyType: f("propertyType"),
      purchasePrice: f("purchasePrice"), loanAmount: f("loanAmount"), downPayment: f("downPayment"),
      incomeType: f("incomeType"), creditScore: f("creditScore"), timeline: f("timeline"), concern: f("concern")
    };
    var cl = buildChecklist(s);
    var rows = [
      ["Loan purpose", s.loanPurpose], ["State", s.state], ["Occupancy", s.occupancy], ["Property type", s.propertyType],
      ["Estimated price / value", s.purchasePrice ? "$" + s.purchasePrice : ""], ["Desired loan amount", s.loanAmount ? "$" + s.loanAmount : ""],
      ["Down payment / equity", s.downPayment ? "$" + s.downPayment : ""], ["Income type", s.incomeType],
      ["Credit range", s.creditScore], ["Timeline", s.timeline], ["Biggest concern", s.concern]
    ].filter(function (r) { return r[1]; }).map(function (r) { return "<b>" + esc(r[0]) + "</b><span>" + esc(r[1]) + "</span>"; }).join("");
    var li = cl.items.map(function (i) { return "<li>" + esc(i) + "</li>"; }).join("");
    out.innerHTML =
      '<h3>Your preliminary scenario summary</h3><div class="sum">' + rows + '</div>' +
      '<h3>Smart document checklist <span class="muted" style="font-weight:400;font-size:.85rem">(' + esc(cl.primaryLabel) + ')</span></h3>' +
      '<ul>' + li + '</ul>' +
      '<div class="btn-row" style="margin-top:22px"><a class="btn btn-blue" href="https://2817729.my1003app.com/2775380/register" target="_blank" rel="noopener noreferrer">Continue to Full Application</a><a class="btn btn-outline" href="loan-officer.html">Talk to a Loan Officer</a></div>' +
      '<p class="apply-note">You will be redirected to our secure mortgage application portal.</p>' +
      '<p class="wcci-note"><span class="wcci-tag">Powered by WCCI.Online</span> WCCI.Online provides preliminary educational mortgage guidance only. It is not a loan approval, loan denial, Loan Estimate, rate quote, rate lock, or commitment to lend. All mortgage options are subject to borrower qualification, property review, documentation, and underwriting approval by licensed mortgage professionals.</p>';
    out.classList.remove("hide");
    out.scrollIntoView({ behavior: "smooth", block: "start" });
    // Best-effort lead capture when deployed (silently ignored locally / without keys).
    if (s.email || s.phone) {
      var transcript = Object.keys(s).map(function (k) { return k + ": " + (s[k] || "-"); }).join("\n");
      try {
        fetch(LEAD_ENDPOINT, { method: "POST", headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ messages: [{ role: "user", content: "WCCI Short Scenario Intake\n" + transcript }], updateNumber: 1 }) }).catch(function () {});
      } catch (e) {}
    }
  });
})();
