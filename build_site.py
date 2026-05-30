#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""One-time generator for the West Coast Capital Mortgage Inc. corporate site.
Emits pure static HTML/CSS/JS into ./wccm-corporate (Netlify drag-and-drop ready).
Running this is a convenience only — the OUTPUT has no build step or dependencies."""

import os

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "wccm-corporate")
NMLS = "2817729"
OFFICE_PHONE = "310-654-1577"
OFFICE_TEL = "3106541577"
DIRECT_PHONE = "310-686-5053"
DIRECT_TEL = "3106865053"
EMAIL = "westccmortgage@gmail.com"
# Real external portals
APPLY_URL = "https://2817729.my1003app.com/2775380/register"      # full borrower 1003
AGENT_URL = "https://2817729.myagentloans.com/register"           # agent / partner portal
WCCI_URL = "https://wcci.online"                                  # external AI mortgage review tool
APPLY_NOTE_TEXT = "You will be redirected to our secure mortgage application portal."

def contact_block(office_label="Office / Loan Officer Questions"):
    return (f'<b>{office_label}:</b> <a href="tel:{OFFICE_TEL}">{OFFICE_PHONE}</a><br>'
            f'<b>Anatoliy Direct:</b> <a href="tel:{DIRECT_TEL}">{DIRECT_PHONE}</a><br>'
            f'<b>Email:</b> <a href="mailto:{EMAIL}">{EMAIL}</a>')

# ----------------------------------------------------------------------------
# Stylesheet
# ----------------------------------------------------------------------------
CSS = r"""/* West Coast Capital Mortgage Inc. — corporate mortgage lender stylesheet */
:root{
  --black:#1f1f1f;
  --charcoal:#111111;
  --white:#ffffff;
  --light:#f5f6f7;
  --gray:#666666;
  --border:#dddddd;
  --blue:#0073e6;
  --blue-dark:#005db8;
  --navy:#0c1c33;
  --max:1180px;
}
*,*::before,*::after{box-sizing:border-box}
html{-webkit-text-size-adjust:100%}
body{
  margin:0;
  font-family:'Inter',system-ui,-apple-system,'Segoe UI',Roboto,Arial,sans-serif;
  color:var(--black);
  background:var(--white);
  line-height:1.65;
  font-size:17px;
  letter-spacing:.01em;
  -webkit-font-smoothing:antialiased;
}
img{max-width:100%;display:block}
a{color:inherit;text-decoration:none}
h1,h2,h3,h4{margin:0 0 .5em;line-height:1.15;letter-spacing:-.015em;font-weight:800;color:var(--charcoal)}
h1{font-size:clamp(2.4rem,5vw,3.9rem)}
h2{font-size:clamp(1.9rem,3.4vw,2.9rem)}
h3{font-size:1.35rem;letter-spacing:-.01em}
h4{font-size:1.02rem}
p{margin:0 0 1.1em}
.lead{font-size:clamp(1.05rem,1.6vw,1.3rem);color:var(--gray);line-height:1.6;max-width:60ch}
.muted{color:var(--gray)}
.wrap{max-width:var(--max);margin:0 auto;padding:0 24px}
.eyebrow{display:inline-block;font-size:.74rem;font-weight:700;letter-spacing:.18em;text-transform:uppercase;color:var(--blue);margin-bottom:14px}
.center{text-align:center}
section{padding:88px 0}
.section-head{max-width:720px;margin-bottom:46px}
.section-head.center{margin-left:auto;margin-right:auto}

/* ---------- Buttons ---------- */
.btn{display:inline-flex;align-items:center;justify-content:center;gap:8px;
  font-weight:600;font-size:.86rem;letter-spacing:.06em;text-transform:uppercase;
  padding:14px 26px;border-radius:6px;border:2px solid transparent;cursor:pointer;
  transition:background .18s,color .18s,border-color .18s,transform .18s;white-space:nowrap}
.btn:hover{transform:translateY(-1px)}
.btn-blue{background:var(--blue);color:#fff;border-color:var(--blue)}
.btn-blue:hover{background:var(--blue-dark);border-color:var(--blue-dark)}
.btn-black{background:var(--charcoal);color:#fff;border-color:var(--charcoal)}
.btn-black:hover{background:#000}
.btn-outline{background:transparent;color:var(--charcoal);border-color:var(--charcoal)}
.btn-outline:hover{background:var(--charcoal);color:#fff}
.btn-outline-light{background:transparent;color:#fff;border-color:rgba(255,255,255,.6)}
.btn-outline-light:hover{background:#fff;color:var(--charcoal);border-color:#fff}
.btn-lg{padding:17px 34px;font-size:.92rem}
.btn-row{display:flex;gap:14px;flex-wrap:wrap}

/* ---------- Top utility bar ---------- */
.topbar{background:var(--charcoal);color:#cfd4da;font-size:.8rem}
.topbar-inner{display:flex;align-items:center;justify-content:space-between;height:40px}
.topbar a{color:#cfd4da;padding:4px 0;margin-right:22px;letter-spacing:.04em;font-weight:500}
.topbar a:hover{color:#fff}
.topbar-left,.topbar-right{display:flex;align-items:center}
.topbar-right a{margin-right:0;margin-left:22px}
.topbar .ico{font-size:.95rem}
.lang-switch{display:inline-flex;gap:2px;margin-left:18px;border:1px solid #3a4350;border-radius:6px;overflow:hidden;vertical-align:middle}
.lang-switch button{font:inherit;font-size:.72rem;font-weight:700;letter-spacing:.04em;padding:4px 9px;background:transparent;color:#cfd4da;border:0;cursor:pointer;line-height:1.2;transition:background .15s,color .15s}
.lang-switch button:hover{background:#222b38;color:#fff}
.lang-switch button.active{background:var(--blue);color:#fff}

/* ---------- Header / nav ---------- */
.site-header{position:sticky;top:0;z-index:50;background:#fff;border-bottom:1px solid var(--border)}
.header-inner{display:flex;align-items:center;gap:28px;height:84px}
.logo{display:flex;flex-direction:column;line-height:1.04;letter-spacing:.02em;font-weight:800;color:var(--navy)}
.logo .l1{font-size:1.04rem}
.logo .l2{font-size:.66rem;letter-spacing:.26em;color:var(--blue);font-weight:700;margin-top:3px}
.nav-collapse{display:flex;align-items:center;gap:28px;flex:1;justify-content:flex-end}
.mainnav{display:flex;align-items:center;gap:6px}
.mainnav a{padding:10px 13px;font-size:.95rem;font-weight:600;color:var(--black);border-radius:6px;letter-spacing:.03em}
.mainnav a:hover{color:var(--blue)}
.mainnav a.active{color:var(--blue)}
.header-cta{display:flex;align-items:center;gap:12px}
.header-cta .btn{padding:11px 20px;font-size:.78rem}
.hamburger{display:none;width:46px;height:46px;border:1px solid var(--border);border-radius:8px;background:#fff;cursor:pointer;align-items:center;justify-content:center;flex-direction:column;gap:5px}
.hamburger span{display:block;width:22px;height:2px;background:var(--charcoal);transition:.2s}
.hamburger[aria-expanded="true"] span:nth-child(1){transform:translateY(7px) rotate(45deg)}
.hamburger[aria-expanded="true"] span:nth-child(2){opacity:0}
.hamburger[aria-expanded="true"] span:nth-child(3){transform:translateY(-7px) rotate(-45deg)}

/* ---------- Hero + animated wallpaper ---------- */
.hero{position:relative;overflow:hidden;background:linear-gradient(180deg,#fff 0%,var(--light) 100%);padding:110px 0 96px}
.hero-wallpaper{position:absolute;inset:0;overflow:hidden;pointer-events:none}
.wallpaper-line{position:absolute;font-size:clamp(80px,14vw,220px);font-weight:800;letter-spacing:.04em;
  color:rgba(12,28,51,.04);white-space:nowrap;animation:drift 36s linear infinite}
.wallpaper-line.w2{animation-duration:48s;animation-direction:reverse;color:rgba(0,115,230,.035)}
.wallpaper-line.w3{animation-duration:60s}
@keyframes drift{from{transform:translateX(-12%)}to{transform:translateX(12%)}}
@media(prefers-reduced-motion:reduce){.wallpaper-line{animation:none}}
.hero-inner{position:relative;z-index:1;max-width:780px}
.hero h1{margin-bottom:.35em}
.hero .lead{margin-bottom:1.8em}
.hero-supporting{margin-top:30px;font-size:.82rem;font-weight:600;letter-spacing:.14em;text-transform:uppercase;color:var(--gray)}
/* interior page hero */
.page-hero{position:relative;overflow:hidden;background:var(--light);border-bottom:1px solid var(--border);padding:78px 0}
.page-hero .wallpaper-line{color:rgba(12,28,51,.035)}
.page-hero-inner{position:relative;z-index:1;max-width:760px}
.crumbs{font-size:.82rem;color:var(--gray);margin-bottom:18px;letter-spacing:.02em}
.crumbs a:hover{color:var(--blue)}

/* ---------- Generic grids / cards ---------- */
.grid{display:grid;gap:26px}
.grid-2{grid-template-columns:repeat(2,1fr)}
.grid-3{grid-template-columns:repeat(3,1fr)}
.grid-4{grid-template-columns:repeat(4,1fr)}
.card{background:#fff;border:1px solid var(--border);border-radius:12px;padding:34px;transition:box-shadow .2s,transform .2s}
.card:hover{box-shadow:0 18px 40px rgba(17,17,17,.08);transform:translateY(-3px)}
.card .label{font-size:.72rem;font-weight:700;letter-spacing:.16em;text-transform:uppercase;color:var(--blue);display:block;margin-bottom:12px}
.card h3{margin-bottom:.5em}
.card p{color:var(--gray);font-size:.97rem}
.card .more{display:inline-block;margin-top:6px;font-weight:700;font-size:.84rem;letter-spacing:.04em;color:var(--blue);text-transform:uppercase}
.card .more:hover{color:var(--blue-dark)}
.icon{width:46px;height:46px;border-radius:10px;background:var(--light);border:1px solid var(--border);display:flex;align-items:center;justify-content:center;margin-bottom:18px;color:var(--blue)}
.icon svg{width:24px;height:24px}

/* ---------- Section variants ---------- */
.bg-light{background:var(--light)}
.split{display:grid;grid-template-columns:1.05fr .95fr;gap:54px;align-items:center}
.feature-list{list-style:none;margin:0;padding:0}
.feature-list li{position:relative;padding:0 0 16px 34px;color:var(--black)}
.feature-list li::before{content:"";position:absolute;left:0;top:8px;width:16px;height:16px;border-radius:50%;
  background:var(--blue);box-shadow:0 0 0 4px rgba(0,115,230,.15)}
.feature-list li b{display:block}
.feature-list li span{color:var(--gray);font-size:.95rem}
.steps{counter-reset:step;list-style:none;margin:0;padding:0;display:grid;gap:18px}
.steps li{position:relative;padding:0 0 0 64px;min-height:44px}
.steps li::before{counter-increment:step;content:counter(step);position:absolute;left:0;top:0;width:44px;height:44px;
  border-radius:50%;background:var(--charcoal);color:#fff;font-weight:800;display:flex;align-items:center;justify-content:center}
.steps li b{display:block;margin-bottom:2px}
.steps li span{color:var(--gray);font-size:.95rem}

/* ---------- Testimonial band ---------- */
.testimonial{background:var(--charcoal);color:#fff;text-align:center;padding:104px 0}
.testimonial .stars{color:#ffc24b;font-size:1.3rem;letter-spacing:.18em;margin-bottom:24px}
.testimonial blockquote{margin:0 auto;max-width:880px;font-size:clamp(1.5rem,3vw,2.3rem);font-weight:700;
  line-height:1.32;letter-spacing:-.01em;color:#fff}
.testimonial .who{margin-top:30px;font-size:.78rem;font-weight:700;letter-spacing:.2em;text-transform:uppercase;color:#9aa3ad}

/* ---------- Article cards ---------- */
.article-card{background:#fff;border:1px solid var(--border);border-radius:12px;overflow:hidden;transition:box-shadow .2s,transform .2s}
.article-card:hover{box-shadow:0 18px 40px rgba(17,17,17,.08);transform:translateY(-3px)}
.article-thumb{aspect-ratio:16/10;background:linear-gradient(135deg,#e8edf3,#f6f7f9);position:relative}
.article-thumb::after{content:"";position:absolute;left:24px;bottom:24px;width:42px;height:42px;border-radius:10px;background:var(--blue);opacity:.85}
.article-card .body{padding:26px 28px 30px}
.article-card .label{font-size:.72rem;font-weight:700;letter-spacing:.16em;text-transform:uppercase;color:var(--blue)}
.article-card h3{font-size:1.12rem;margin:10px 0 8px}
.article-card p{color:var(--gray);font-size:.94rem;margin-bottom:14px}

/* ---------- CTA band ---------- */
.cta-band{background:var(--navy);color:#fff;border-radius:16px;padding:60px;text-align:center}
.cta-band h2{color:#fff}
.cta-band p{color:#c7d0db;max-width:60ch;margin:0 auto 26px}
.cta-band .btn-row{justify-content:center}

/* ---------- Calculator ---------- */
.calc-panel{background:var(--charcoal);color:#fff;border-radius:16px;padding:42px;display:grid;grid-template-columns:1.1fr .9fr;gap:42px}
.calc-fields{display:grid;grid-template-columns:1fr 1fr;gap:18px}
.field{display:flex;flex-direction:column;gap:7px}
.field label{font-size:.78rem;font-weight:600;letter-spacing:.04em;color:#c7cdd4}
.field input,.field select{padding:12px 14px;border-radius:8px;border:1px solid #394250;background:#1b2330;color:#fff;font:inherit;font-size:.95rem}
.field input:focus,.field select:focus{outline:2px solid var(--blue);border-color:var(--blue)}
.calc-out{background:#1b2330;border-radius:12px;padding:30px;display:flex;flex-direction:column;justify-content:center}
.calc-out .total{font-size:.78rem;letter-spacing:.16em;text-transform:uppercase;color:#9aa3ad}
.calc-out .big{font-size:clamp(2.2rem,4vw,3rem);font-weight:800;margin:6px 0 18px;color:#fff}
.calc-row{display:flex;justify-content:space-between;padding:10px 0;border-top:1px solid #2a3340;font-size:.95rem;color:#c7cdd4}
.calc-row b{color:#fff;font-weight:700}

/* ---------- Forms ---------- */
.form{background:#fff;border:1px solid var(--border);border-radius:14px;padding:36px}
.form-grid{display:grid;grid-template-columns:1fr 1fr;gap:18px}
.form .field label{color:var(--black)}
.form .field input,.form .field select,.form .field textarea{
  padding:13px 14px;border:1px solid var(--border);border-radius:8px;font:inherit;font-size:.96rem;background:#fff;color:var(--black)}
.form .field input:focus,.form .field select:focus,.form .field textarea:focus{outline:2px solid var(--blue);border-color:var(--blue)}
.form .full{grid-column:1/-1}
.form textarea{min-height:120px;resize:vertical}
.form-note{font-size:.86rem;color:var(--gray);margin-top:14px}
.form-ok{background:#e9f6ee;border:1px solid #b7e0c6;color:#176b3a;border-radius:10px;padding:14px 16px;margin-bottom:18px}
.hp{position:absolute;left:-9999px}

/* ---------- Accordion ---------- */
.acc{border:1px solid var(--border);border-radius:12px;overflow:hidden}
.acc + .acc{margin-top:14px}
.acc summary{list-style:none;cursor:pointer;padding:20px 24px;font-weight:700;font-size:1.04rem;
  display:flex;justify-content:space-between;align-items:center;gap:16px}
.acc summary::-webkit-details-marker{display:none}
.acc summary::after{content:"+";font-size:1.5rem;font-weight:600;color:var(--blue);transition:transform .2s}
.acc[open] summary::after{content:"\2212"}
.acc .acc-body{padding:0 24px 22px;color:var(--gray);max-width:80ch}

/* ---------- Glossary ---------- */
.glossary{display:grid;gap:14px}
.glossary .term{border:1px solid var(--border);border-radius:10px;padding:18px 22px}
.glossary .term b{color:var(--charcoal)}
.glossary .term span{color:var(--gray);display:block;font-size:.96rem}

/* ---------- Footer ---------- */
.site-footer{background:var(--charcoal);color:#aab2bd;padding:72px 0 34px;font-size:.92rem}
.footer-grid{display:grid;grid-template-columns:repeat(6,1fr);gap:30px}
.site-footer h4{color:#fff;font-size:.74rem;letter-spacing:.16em;text-transform:uppercase;margin-bottom:16px}
.site-footer a{display:block;color:#aab2bd;padding:5px 0}
.site-footer a:hover{color:#fff}
.footer-brand .l1{color:#fff;font-weight:800;font-size:1.05rem}
.footer-brand .l2{color:var(--blue);font-weight:700;font-size:.66rem;letter-spacing:.24em;margin-top:3px;margin-bottom:14px}
.footer-bottom{border-top:1px solid #2a3340;margin-top:46px;padding-top:26px;color:#8a939e;font-size:.82rem;line-height:1.7}
.footer-bottom .row{display:flex;justify-content:space-between;gap:20px;flex-wrap:wrap;margin-bottom:14px}
.eho{display:inline-flex;align-items:center;gap:8px;font-weight:600;color:#aab2bd}

/* ---------- Responsive ---------- */
@media(max-width:1040px){
  .footer-grid{grid-template-columns:repeat(3,1fr)}
}
@media(max-width:960px){
  .hamburger{display:flex;margin-left:auto}
  .nav-collapse{position:fixed;top:124px;left:0;right:0;background:#fff;border-bottom:1px solid var(--border);
    flex-direction:column;align-items:stretch;gap:0;padding:14px 24px 24px;justify-content:flex-start;
    transform:translateY(-12px);opacity:0;visibility:hidden;transition:.2s;box-shadow:0 24px 40px rgba(0,0,0,.08);max-height:calc(100vh - 124px);overflow:auto}
  body.nav-open .nav-collapse{transform:translateY(0);opacity:1;visibility:visible}
  .mainnav{flex-direction:column;align-items:stretch;gap:2px;width:100%}
  .mainnav a{padding:14px 8px;border-bottom:1px solid var(--light);font-size:1.02rem}
  .header-cta{flex-direction:column;align-items:stretch;width:100%;margin-top:16px;gap:10px}
  .header-cta .btn{width:100%;padding:14px;font-size:.84rem}
  .split{grid-template-columns:1fr;gap:32px}
  .calc-panel{grid-template-columns:1fr}
}
@media(max-width:760px){
  section{padding:60px 0}
  .grid-3,.grid-4{grid-template-columns:repeat(2,1fr)}
  .footer-grid{grid-template-columns:repeat(2,1fr)}
  .cta-band{padding:40px 24px}
  .topbar-left a:last-child{display:none}
}
@media(max-width:560px){
  .grid-2,.grid-3,.grid-4{grid-template-columns:1fr}
  .form-grid,.calc-fields{grid-template-columns:1fr}
  .footer-grid{grid-template-columns:1fr 1fr}
}

/* ---------- WCCI AI assistant ---------- */
.wcci-band{background:linear-gradient(180deg,#f3f8ff,#ffffff)}
.wcci-tag{display:inline-block;font-size:.64rem;font-weight:700;letter-spacing:.14em;text-transform:uppercase;color:var(--blue);background:#eaf2fe;border:1px solid #cfe0fb;border-radius:999px;padding:3px 9px;margin-right:8px}
.wcci-note{font-size:.82rem;color:var(--gray);line-height:1.6;margin-top:22px;max-width:92ch}
.wcci-cta{background:var(--navy);color:#fff;border-radius:16px;padding:48px}
.wcci-cta h2{color:#fff}
.wcci-cta p{color:#c7d0db;max-width:64ch}
.wcci-cta .eyebrow{color:#7fb1f5}
.wcci-cta .wcci-note{color:#9fb0c4}
.wcci-cta .wcci-tag{background:rgba(255,255,255,.08);border-color:rgba(255,255,255,.2);color:#cfe0fb}
.powered-wcci{color:var(--blue);font-weight:700;font-size:.72rem;letter-spacing:.12em;text-transform:uppercase;margin-top:14px}
.wcci-toolwrap{max-width:820px;margin:0 auto;background:#fff;border:1px solid var(--border);border-radius:16px;overflow:hidden;box-shadow:var(--shadow-sm)}
.wcci-tabs{display:flex;border-bottom:1px solid var(--border)}
.wcci-tab{flex:1;padding:16px;background:#fff;border:0;border-bottom:3px solid transparent;font:inherit;font-weight:700;font-size:.9rem;color:var(--gray);cursor:pointer}
.wcci-tab.active{color:var(--navy);border-bottom-color:var(--blue)}
.wcci-panel{padding:24px}
.hide{display:none}
.wcci-chat{min-height:280px;max-height:440px;overflow-y:auto;display:flex;flex-direction:column;gap:12px;padding:6px}
.wcci-msg{max-width:80%;padding:12px 16px;border-radius:14px;font-size:.96rem;line-height:1.5;white-space:pre-wrap}
.wcci-msg.bot{align-self:flex-start;background:var(--light);color:var(--charcoal);border-bottom-left-radius:4px}
.wcci-msg.user{align-self:flex-end;background:var(--blue);color:#fff;border-bottom-right-radius:4px}
.wcci-msg.note{align-self:center;background:#fff7e6;border:1px solid #ffe3a3;color:#7a5b00;font-size:.86rem;max-width:100%}
.wcci-chat-input{display:flex;gap:10px;margin-top:16px}
.wcci-chat-input input{flex:1;padding:13px 14px;border:1px solid var(--border);border-radius:8px;font:inherit}
.wcci-chat-input input:focus{outline:2px solid var(--blue);border-color:var(--blue)}
.wcci-result{margin-top:22px;border-top:1px solid var(--border);padding-top:22px}
.wcci-result h3{margin-top:18px}
.wcci-result .sum{display:grid;grid-template-columns:auto 1fr;gap:6px 18px;font-size:.94rem}
.wcci-result .sum b{color:var(--charcoal)}
.wcci-result ul{margin:8px 0 0;padding-left:20px}
.wcci-result li{margin-bottom:6px;color:var(--charcoal)}
@media(max-width:560px){.wcci-cta{padding:30px 22px}.wcci-msg{max-width:92%}}
.apply-note{font-size:.8rem;color:var(--gray);margin-top:12px;letter-spacing:.02em;line-height:1.5}
.apply-note.light{color:#aeb9c6}
.wcci-hero{padding:92px 0}
.wcci-split{display:grid;grid-template-columns:.82fr 1.18fr;gap:40px;align-items:start}
.wcci-split .wcci-toolwrap{max-width:none;margin:0}
.wcci-intro h3{margin-bottom:.4em}
.wcci-intro .feature-list{margin-top:18px}
.wcci-intro .feature-list li{padding-bottom:12px}
@media(max-width:860px){.wcci-split{grid-template-columns:1fr;gap:28px}}
.contact-lines{line-height:2.1}
.contact-lines a{color:var(--blue);font-weight:600}
.contact-lines.light a{color:#cfe0fb}
.footer-contact{margin-top:10px;line-height:2}
.footer-contact a{color:#fff}
.apply-support{margin-top:34px}
.apply-support h3{margin-bottom:.3em}
.cta-contact{margin-top:20px;color:#c7d0db;font-size:.95rem}
.cta-contact b{color:#fff}
/* ---------- Founder ---------- */
.founder-grid{display:grid;grid-template-columns:.85fr 1.15fr;gap:48px;align-items:center}
.founder-photo{border-radius:14px;overflow:hidden;border:1px solid var(--border);box-shadow:0 18px 44px rgba(17,17,17,.12);background:var(--light)}
.founder-photo img{display:block;width:100%;height:auto;aspect-ratio:4/5;object-fit:cover;object-position:center top}
.founder-cred{list-style:none;margin:20px 0 0;padding:0}
.founder-cred li{position:relative;padding:0 0 11px 26px;color:var(--black)}
.founder-cred li::before{content:"";position:absolute;left:0;top:9px;width:8px;height:8px;border-radius:50%;background:var(--blue)}
.founder-contact{margin-top:20px;line-height:2}
.founder-contact a{color:var(--blue);font-weight:600}
.founder-preview .founder-photo img{aspect-ratio:1/1}
@media(max-width:760px){
  .founder-grid{grid-template-columns:1fr;gap:26px}
  .founder-photo{max-width:440px;margin:0 auto}
}
"""

# ----------------------------------------------------------------------------
# JavaScript
# ----------------------------------------------------------------------------
JS = r"""/* West Coast Capital Mortgage Inc. — site scripts (no dependencies) */
(function(){
  "use strict";

  /* Mobile menu */
  var burger=document.getElementById('hamburger');
  if(burger){
    burger.addEventListener('click',function(){
      var open=document.body.classList.toggle('nav-open');
      burger.setAttribute('aria-expanded',open?'true':'false');
    });
    document.querySelectorAll('.nav-collapse a').forEach(function(a){
      a.addEventListener('click',function(){document.body.classList.remove('nav-open');burger.setAttribute('aria-expanded','false');});
    });
  }

  /* Smooth scroll for in-page anchors */
  document.querySelectorAll('a[href^="#"]').forEach(function(a){
    a.addEventListener('click',function(e){
      var id=a.getAttribute('href');
      if(id.length>1){var t=document.querySelector(id);if(t){e.preventDefault();t.scrollIntoView({behavior:'smooth',block:'start'});}}
    });
  });

  /* Contact / apply forms — front-end acknowledgement (no backend) */
  document.querySelectorAll('form[data-ack]').forEach(function(f){
    f.addEventListener('submit',function(e){
      e.preventDefault();
      var ok=f.querySelector('.form-ok');
      if(ok)ok.hidden=false;
      f.querySelectorAll('input,select,textarea,button').forEach(function(el){el.disabled=true;});
      if(ok)ok.scrollIntoView({behavior:'smooth',block:'center'});
    });
  });

  /* Mortgage payment calculator */
  function money(n){return '$'+(isFinite(n)?Math.round(n):0).toLocaleString('en-US');}
  function val(id){var el=document.getElementById(id);if(!el)return 0;return parseFloat((el.value||'').toString().replace(/[^0-9.\-]/g,''))||0;}
  function calc(){
    var price=val('c-price'),dpPct=val('c-down'),rate=val('c-rate'),term=val('c-term');
    var taxYr=val('c-tax'),insYr=val('c-ins'),hoa=val('c-hoa');
    var loan=Math.max(price-(price*dpPct/100),0);
    var r=rate/100/12,n=term*12;
    var pi=(r===0)?(n?loan/n:0):loan*r/(1-Math.pow(1+r,-n));
    var tax=taxYr/12,ins=insYr/12;
    var total=pi+tax+ins+hoa;
    set('c-out-total',money(total));
    set('c-out-pi',money(pi));
    set('c-out-tax',money(tax));
    set('c-out-ins',money(ins));
    set('c-out-hoa',money(hoa));
    set('c-out-loan',money(loan));
  }
  function set(id,v){var el=document.getElementById(id);if(el)el.textContent=v;}
  if(document.getElementById('c-price')){
    ['c-price','c-down','c-rate','c-term','c-tax','c-ins','c-hoa'].forEach(function(id){
      var el=document.getElementById(id);if(el){el.addEventListener('input',calc);el.addEventListener('change',calc);}
    });
    calc();
  }

  /* Year stamp */
  document.querySelectorAll('.year').forEach(function(el){el.textContent=new Date().getFullYear();});
})();
"""

# ----------------------------------------------------------------------------
# Shared chrome + builders
# ----------------------------------------------------------------------------
NAV_ITEMS = [
    ("buy.html", "Buy a Home", "buy"),
    ("refinance.html", "Refinance", "refinance"),
    ("loans.html", "Loans", "loans"),
    ("resources.html", "Resources", "resources"),
    ("about.html", "About Us", "about"),
]

def head(title, desc):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} | West Coast Capital Mortgage Inc.</title>
<meta name="description" content="{desc}">
<link rel="icon" type="image/svg+xml" href="assets/favicon.svg">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="styles.css">
</head>
<body>"""

def header(active):
    def navlink(href, label, key):
        if href.startswith("http"):
            return f'<a href="{href}" target="_blank" rel="noopener noreferrer">{label}</a>'
        cls = ' class="active"' if key == active else ''
        return f'<a href="{href}"{cls}>{label}</a>'
    links = "".join(navlink(h, l, k) for h, l, k in NAV_ITEMS)
    return f"""
<div class="topbar">
  <div class="wrap topbar-inner">
    <nav class="topbar-left" aria-label="Utility">
      <a href="loans.html">Mortgage</a>
      <a href="buy.html">Home Search</a>
    </nav>
    <div class="topbar-right">
      <div class="lang-switch" role="group" aria-label="Language">
        <button type="button" data-lang="en">EN</button>
        <button type="button" data-lang="es">ES</button>
        <button type="button" data-lang="ru">RU</button>
      </div>
    </div>
  </div>
</div>
<header class="site-header">
  <div class="wrap header-inner">
    <!-- Replace with <img src="assets/logo.png" alt="West Coast Capital Mortgage Inc."> when ready -->
    <a class="logo" href="index.html" aria-label="West Coast Capital Mortgage Inc. home">
      <span class="l1">WEST COAST CAPITAL</span>
      <span class="l2">MORTGAGE INC.</span>
    </a>
    <div class="nav-collapse" id="navc">
      <nav class="mainnav" aria-label="Primary">{links}</nav>
      <div class="header-cta">
        <a class="btn btn-blue" href="{APPLY_URL}" target="_blank" rel="noopener noreferrer">Apply Now</a>
      </div>
    </div>
    <button class="hamburger" id="hamburger" aria-label="Menu" aria-expanded="false" aria-controls="navc">
      <span></span><span></span><span></span>
    </button>
  </div>
</header>"""

def footer():
    def col(title, items):
        def fl(t, h):
            if h.startswith("http"):
                return f'<a href="{h}" target="_blank" rel="noopener noreferrer">{t}</a>'
            return f'<a href="{h}">{t}</a>'
        links = "".join(fl(t, h) for t, h in items)
        return f'<div><h4>{title}</h4>{links}</div>'
    cols = "".join([
        f'<div class="footer-brand"><div class="l1">WEST COAST CAPITAL</div><div class="l2">MORTGAGE INC.</div>'
        f'<p style="color:#aab2bd;font-size:.9rem">Modern mortgage guidance for buying, refinancing, and building equity.</p>'
        f'<p class="footer-contact">{contact_block()}</p></div>',
        col("Buy A Home", [("Homebuying Guide","homebuying-guide.html"),("Mortgage Pre-Approval","apply.html"),
            ("First-Time Homebuyers","first-time-homebuyer.html"),("Down Payment Assistance","buy.html"),
            ("Home Purchase Loans","loans.html")]),
        col("Refinance", [("Refinancing Guide","refinancing-guide.html"),("Refinance Mortgage Rates","rates.html"),
            ("Cash-Out Refinance","refinance.html"),("Rate-and-Term Refinance","refinance.html")]),
        col("Loans", [("Conventional Loans","conventional-loans.html"),("FHA Loans","fha-loans.html"),
            ("VA Loans","va-loans.html"),("Jumbo Loans","jumbo-loans.html"),("Non-QM Loans","non-qm-loans.html"),
            ("Bank Statement Loans","bank-statement-loans.html"),("DSCR Loans","dscr-loans.html"),
            ("Investment Property Loans","investment-property-loans.html")]),
        col("Resources", [("WCCI.Online AI Mortgage Review",WCCI_URL),("Mortgage Calculators","calculators.html"),("Mortgage Articles","mortgage-articles.html"),
            ("Mortgage Glossary","glossary.html"),("Mortgage FAQ","faq.html"),("Mortgage Videos","resources.html"),
            ("Rate Watch","rates.html")]),
        col("About Us", [("About West Coast Capital Mortgage","about.html"),("Contact Us","contact.html"),
            ("Find a Loan Officer",AGENT_URL),("Licensing & Disclosures","about.html")]),
    ])
    return f"""
<footer class="site-footer">
  <div class="wrap">
    <div class="footer-grid">{cols}</div>
    <div class="footer-bottom">
      <div class="row">
        <nav aria-label="Legal">
          <a href="about.html" style="display:inline;margin-right:18px">Licensing and Disclosures</a>
          <a href="https://www.nmlsconsumeraccess.org/" target="_blank" rel="noopener noreferrer" style="display:inline">NMLS Consumer Access</a>
        </nav>
        <span class="eho">&#8962; Equal Housing Opportunity</span>
      </div>
      <p>West Coast Capital Mortgage Inc. NMLS #{NMLS}. Equal Housing Opportunity. Information is provided for
      educational purposes only and is not a commitment to lend. All loans are subject to credit, income, property,
      and underwriting approval.</p>
      <p>&copy; <span class="year"></span> West Coast Capital Mortgage Inc.</p>
    </div>
  </div>
</footer>
<script src="i18n.js"></script>
<script src="script.js"></script>
</body>
</html>"""

def page(title, desc, active, body):
    return head(title, desc) + header(active) + body + footer()

# ---- content builders ----
def page_hero(title, sub, crumb=None):
    cr = f'<div class="crumbs"><a href="index.html">Home</a> &nbsp;/&nbsp; {crumb}</div>' if crumb else ""
    return f"""
<section class="page-hero">
  <div class="hero-wallpaper" aria-hidden="true">
    <div class="wallpaper-line" style="top:18%">WEST COAST CAPITAL MORTGAGE</div>
    <div class="wallpaper-line w2" style="top:58%">WEST COAST CAPITAL MORTGAGE</div>
  </div>
  <div class="wrap page-hero-inner">
    {cr}
    <h1>{title}</h1>
    <p class="lead">{sub}</p>
  </div>
</section>"""

def card(label, h, body, cta, href):
    lab = f'<span class="label">{label}</span>' if label else ""
    return (f'<a class="card" href="{href}">{lab}<h3>{h}</h3><p>{body}</p>'
            f'<span class="more">{cta} <span aria-hidden="true">&rarr;</span></span></a>')

def card_ext(label, h, body, cta, href):
    lab = f'<span class="label">{label}</span>' if label else ""
    return (f'<a class="card" href="{href}" target="_blank" rel="noopener noreferrer">{lab}<h3>{h}</h3><p>{body}</p>'
            f'<span class="more">{cta} <span aria-hidden="true">&rarr;</span></span></a>')

def accordion(items):
    out = []
    for q, a in items:
        out.append(f'<details class="acc"><summary>{q}</summary><div class="acc-body">{a}</div></details>')
    return "".join(out)

def btn(label, href, cls, lg=True):
    size = " btn-lg" if lg else ""
    if href.startswith("http"):
        return f'<a class="btn{size} {cls}" href="{href}" target="_blank" rel="noopener noreferrer">{label}</a>'
    return f'<a class="btn{size} {cls}" href="{href}">{label}</a>'

def apply_note(light=False):
    return f'<p class="apply-note{" light" if light else ""}">{APPLY_NOTE_TEXT}</p>'

def cta_band(h="Ready to take the next step?",
             p="Start with a short mortgage intake and we will help you understand your options.",
             b1=("Start Short Application","apply.html","btn-blue"),
             b2=("Contact a Loan Officer","loan-officer.html","btn-outline-light"),
             note=False):
    note_html = apply_note(light=True) if note else ""
    return f"""
<section><div class="wrap"><div class="cta-band">
  <h2>{h}</h2><p>{p}</p>
  <div class="btn-row">{btn(b1[0], b1[1], b1[2])}{btn(b2[0], b2[1], b2[2])}</div>
  {note_html}
</div></div></section>"""

PAGES = {}

# ---- WCCI (AI Mortgage Assistant) builders ----
WCCI_DISCLOSURE = ("WCCI.Online provides preliminary educational mortgage guidance only and is not a loan "
    "approval, rate quote, rate lock, or commitment to lend.")
WCCI_DISCLOSURE_FULL = ("WCCI.Online provides preliminary educational mortgage guidance only. It is not a loan "
    "approval, loan denial, Loan Estimate, rate quote, rate lock, or commitment to lend. All mortgage options "
    "are subject to borrower qualification, property review, documentation, and underwriting approval by "
    "licensed mortgage professionals.")

def wcci_disclosure():
    return (f'<p class="wcci-note">{WCCI_DISCLOSURE}</p>')

def wcci_cta(headline, text, label="Start AI Review", href="ai-mortgage-review.html"):
    return f"""
<section><div class="wrap"><div class="wcci-cta">
  <span class="eyebrow" style="color:var(--blue)">WCCI.Online Mortgage Intelligence</span>
  <h2>{headline}</h2>
  <p>{text}</p>
  <div class="btn-row"><a class="btn btn-lg btn-blue" href="{href}">{label}</a>
    <a class="btn btn-lg btn-outline" href="loan-officer.html">Talk to a Loan Officer</a></div>
  {wcci_disclosure()}
</div></div></section>"""


# ---------------- Homepage ----------------
def _home():
    journey = "".join([
        card("Purchase", "Buy a home",
             "Buying a home is a big decision. We help you understand your options, prepare your financing, and move forward with confidence.",
             "Learn more", "buy.html"),
        card("Refinance", "Mortgage refinance",
             "Explore rate-and-term refinance, cash-out options, and strategies that may help lower your payment or access equity.",
             "Lock in your rate", "refinance.html"),
        card("Equity", "Home equity loan",
             "Use your home equity to support renovations, investments, debt consolidation, or major financial goals.",
             "Get cash now", "heloc.html"),
    ])
    resources = "".join([
        card("", "Mortgage calculators", "Take the guesswork out of financing and estimate your monthly payment.", "See more", "calculators.html"),
        card("", "First-Time Homebuyer Hub", "Learn how to prepare, qualify, and buy with confidence.", "See more", "first-time-homebuyer.html"),
        card("", "Homebuying Guide", "Discover the step-by-step process of getting the keys.", "See more", "homebuying-guide.html"),
        card("", "Refinancing Guide", "Understand when refinancing may make sense.", "See more", "refinancing-guide.html"),
    ])
    programs = "".join([
        card("Conventional", "Conventional Loans", "Flexible financing for well-qualified buyers, with options as low as 3% down.", "Learn more", "conventional-loans.html"),
        card("FHA", "FHA Loans", "Lower down payments and flexible credit guidelines — popular with first-time buyers.", "Learn more", "fha-loans.html"),
        card("VA", "VA Loans", "$0 down and no monthly mortgage insurance for eligible veterans and service members.", "Learn more", "va-loans.html"),
        card("Jumbo", "Jumbo Loans", "Financing above conforming limits for higher-priced properties.", "Learn more", "jumbo-loans.html"),
        card("Non-QM", "Non-QM Loans", "Alternative qualification paths for borrowers with unique income profiles.", "Learn more", "non-qm-loans.html"),
        card("Self-Employed", "Bank Statement Loans", "Qualify using bank deposits instead of traditional tax-return income.", "Learn more", "bank-statement-loans.html"),
        card("Investors", "DSCR Loans", "Qualify investment properties on rental cash flow rather than personal income.", "Learn more", "dscr-loans.html"),
        card("Investors", "Investment Property Loans", "Financing built for rentals, second homes, and portfolio growth.", "Learn more", "investment-property-loans.html"),
    ])
    tools = "".join([
        card("", "Mortgage Payment Calculator", "Estimate principal, interest, taxes, and insurance.", "Open", "calculators.html"),
        card("", "Affordability Calculator", "See a comfortable price range based on your income.", "Open", "calculators.html"),
        card("", "Refinance Calculator", "Compare your current loan with a potential new one.", "Open", "calculators.html"),
        card("", "Cash-Out Calculator", "Estimate how much equity you may be able to access.", "Open", "calculators.html"),
        card("", "Rate Watch", "Request a personalized quote based on today&rsquo;s market.", "Open", "rates.html"),
        card("", "Short Application", "Start a quick mortgage intake in minutes.", "Open", "apply.html"),
        card_ext("WCCI", "WCCI.Online AI Mortgage Review", "Want to organize your scenario before applying? Start a quick AI-powered mortgage review.", "Open WCCI.Online", WCCI_URL),
    ])
    def art(label, h, href):
        return (f'<a class="article-card" href="{href}"><div class="article-thumb"></div>'
                f'<div class="body"><span class="label">{label}</span><h3>{h}</h3>'
                f'<p>A clear, borrower-friendly explanation to help you make a confident decision.</p>'
                f'<span class="more" style="color:var(--blue);font-weight:700;font-size:.84rem;letter-spacing:.04em;text-transform:uppercase">Read article <span aria-hidden="true">&rarr;</span></span></div></a>')
    articles = "".join([
        art("Preapproval", "How to Get Preapproved for a Mortgage", "mortgage-articles.html"),
        art("Refinance", "What Is a Cash-Out Refinance?", "mortgage-articles.html"),
        art("Costs", "How Much Does It Cost to Refinance a Mortgage?", "mortgage-articles.html"),
    ])
    return f"""
<section class="hero">
  <div class="hero-wallpaper" aria-hidden="true">
    <div class="wallpaper-line" style="top:6%">WEST COAST CAPITAL MORTGAGE</div>
    <div class="wallpaper-line w2" style="top:40%">WEST COAST CAPITAL MORTGAGE</div>
    <div class="wallpaper-line w3" style="top:74%">WEST COAST CAPITAL MORTGAGE</div>
  </div>
  <div class="wrap hero-inner">
    <span class="eyebrow">West Coast Capital Mortgage Inc.</span>
    <h1>Start Your Financing Journey</h1>
    <p class="lead">Clear mortgage guidance, smart loan solutions, and modern tools to help you move forward with confidence.</p>
    <div class="btn-row">
      <a class="btn btn-lg btn-black" href="{APPLY_URL}" target="_blank" rel="noopener noreferrer">Get Preapproved</a>
      <a class="btn btn-lg btn-outline" href="calculators.html">View Mortgage Tools</a>
    </div>
    <p class="apply-note">{APPLY_NOTE_TEXT}</p>
    <p class="hero-supporting">Purchase &bull; Refinance &bull; Jumbo &bull; FHA &bull; VA &bull; Non-QM &bull; DSCR</p>
  </div>
</section>

<section><div class="wrap">
  <div class="section-head"><span class="eyebrow">Where to begin</span><h2>Start your financing journey</h2>
  <p class="lead">Tell us your goal and we&rsquo;ll point you to the right path &mdash; whether you&rsquo;re buying, refinancing, or tapping equity.</p></div>
  <div class="grid grid-3">{journey}</div>
</div></section>

<section class="testimonial">
  <div class="wrap">
    <div class="stars" aria-hidden="true">&#9733;&#9733;&#9733;&#9733;&#9733;</div>
    <blockquote>&ldquo;I received clear guidance, competitive loan options, and a smooth process from start to finish.&rdquo;</blockquote>
    <div class="who">WCCM Client</div>
  </div>
</section>

<section><div class="wrap">
  <div class="section-head"><span class="eyebrow">Learn</span><h2>Mortgage resources</h2></div>
  <div class="grid grid-2">{resources}</div>
</div></section>

<section class="bg-light"><div class="wrap">
  <div class="section-head"><span class="eyebrow">Programs</span><h2>Loan programs built around you</h2>
  <p class="lead">From first-time buyers to seasoned investors, we match you with financing that fits your situation.</p></div>
  <div class="grid grid-4">{programs}</div>
</div></section>

<section><div class="wrap">
  <div class="section-head"><span class="eyebrow">Tools</span><h2>Mortgage tools</h2></div>
  <div class="grid grid-3">{tools}</div>
</div></section>

<section class="bg-light"><div class="wrap">
  <div class="section-head"><span class="eyebrow">Insights</span><h2>Mortgage articles</h2></div>
  <div class="grid grid-3">{articles}</div>
</div></section>

<section><div class="wrap">
  <div class="founder-grid founder-preview">
    <div class="founder-photo"><img src="assets/anatoliy-kanevsky.png" alt="Anatoliy Kanevsky, founder of West Coast Capital Mortgage Inc." loading="lazy"></div>
    <div>
      <span class="eyebrow" style="color:var(--blue)">Our founder</span>
      <h2>Mortgage guidance with real estate experience.</h2>
      <p class="lead">West Coast Capital Mortgage is led by Anatoliy Kanevsky, a mortgage and real estate professional with experience across lending, brokerage, luxury residential development, and complex borrower scenarios.</p>
      <a class="btn btn-blue" href="about.html#anatoliy">Meet Anatoliy</a>
    </div>
  </div>
</div></section>

<section class="bg-light"><div class="wrap center">
  <span class="eyebrow">Talk to us</span>
  <h2>Speak with West Coast Capital Mortgage</h2>
  <p class="contact-lines" style="font-size:1.05rem">{contact_block("Office")}</p>
</div></section>

{cta_band()}
"""
PAGES["index.html"] = dict(title="Home Loans, Refinance & Mortgage Tools",
    desc="West Coast Capital Mortgage Inc. — clear mortgage guidance, smart loan solutions, and modern tools for buying, refinancing, and building equity.",
    nav="", body=_home())

# ---------------- Buy a Home ----------------
def _buy():
    steps = """<ol class="steps">
      <li><b>Review your finances</b><span>Understand income, debts, and savings before you shop.</span></li>
      <li><b>Get preapproved</b><span>Know your budget and show sellers you&rsquo;re ready.</span></li>
      <li><b>Choose a loan program</b><span>Match the right financing to your goals.</span></li>
      <li><b>Find your home</b><span>Shop with a clear price range in mind.</span></li>
      <li><b>Make an offer &amp; close</b><span>We guide underwriting through to the keys.</span></li>
    </ol>"""
    faqs = accordion([
        ("How much do I need for a down payment?", "It depends on the loan program. Some conventional loans start at 3% down, FHA at 3.5%, and VA and certain USDA loans may allow $0 down for eligible borrowers."),
        ("What is preapproval?", "Preapproval is a lender&rsquo;s assessment of how much you may be able to borrow based on a review of your credit, income, and assets. It strengthens your offer."),
        ("How long does buying a home take?", "Timelines vary, but once you&rsquo;re under contract, many purchases close in roughly 30&ndash;45 days."),
    ])
    return page_hero("Buy a Home", "Buying a home starts with the right mortgage plan. We help you prepare, qualify, and move forward with confidence.", "Buy a Home") + f"""
<section><div class="wrap split">
  <div>
    <span class="eyebrow">Purchase loans</span>
    <h2>Financing made clear</h2>
    <p class="lead">A purchase loan helps you buy a primary residence, second home, or investment property. We&rsquo;ll compare programs, explain the trade-offs, and prepare your financing so you can shop with certainty.</p>
    <div class="btn-row"><a class="btn btn-blue" href="{APPLY_URL}" target="_blank" rel="noopener noreferrer">Get Preapproved</a><a class="btn btn-outline" href="loans.html">Explore Loan Programs</a></div>
    {apply_note()}
  </div>
  <ul class="feature-list">
    <li><b>First-time buyer support</b><span>Step-by-step guidance and education from day one.</span></li>
    <li><b>Low-down-payment options</b><span>Programs designed to reduce your upfront cash.</span></li>
    <li><b>Clear cost estimates</b><span>Understand your monthly payment before you commit.</span></li>
    <li><b>Dedicated loan advisor</b><span>A licensed professional from preapproval to closing.</span></li>
  </ul>
</div></section>
<section class="bg-light"><div class="wrap">
  <div class="section-head"><span class="eyebrow">The path</span><h2>Steps to buy a home</h2></div>
  {steps}
  <div style="margin-top:34px"><a class="btn btn-outline" href="homebuying-guide.html">See the full 12-step guide</a></div>
</div></section>
<section><div class="wrap split">
  <ul class="feature-list">
    <li><b>Down payment basics</b><span>Sources can include savings, gifts, and assistance programs.</span></li>
    <li><b>Credit guidance</b><span>We&rsquo;ll explain what affects your rate and approval.</span></li>
    <li><b>Budget clarity</b><span>Estimate taxes, insurance, and total monthly cost.</span></li>
  </ul>
  <div>
    <span class="eyebrow">Get ready</span>
    <h2>First-time buyer support</h2>
    <p class="lead">New to the process? Our First-Time Homebuyer Hub walks you through preparation, credit, down payment, and choosing the right loan.</p>
    <a class="btn btn-blue" href="first-time-homebuyer.html">Visit the Homebuyer Hub</a>
  </div>
</div></section>
<section class="bg-light"><div class="wrap">
  <div class="section-head"><span class="eyebrow">FAQ</span><h2>Buying a home questions</h2></div>
  {faqs}
</div></section>
{cta_band(b1=("Get Preapproved",APPLY_URL,"btn-blue"), note=True)}
"""
PAGES["buy.html"] = dict(title="Buy a Home", desc="Buying a home starts with the right mortgage plan — preapproval, loan programs, down payment basics, and first-time buyer support.", nav="buy", body=_buy())

# ---------------- Refinance ----------------
def _refi():
    faqs = accordion([
        ("How do I know if refinancing is worth it?", "Compare your monthly savings against closing costs to find your break-even point &mdash; the month when savings overtake costs. If you plan to stay past it, refinancing may make sense."),
        ("What is a cash-out refinance?", "A cash-out refinance replaces your mortgage with a larger loan and returns the difference to you in cash, using your home&rsquo;s equity."),
        ("How long does a refinance take?", "Many refinances close in roughly 30 days. Streamlined options for certain FHA and VA loans can move faster."),
    ])
    return page_hero("Refinance", "Lower your rate, shorten your term, or access equity by replacing your current loan with a better-fitting one.", "Refinance") + f"""
<section><div class="wrap">
  <div class="section-head"><span class="eyebrow">Overview</span><h2>Why borrowers refinance</h2>
  <p class="lead">Refinancing replaces your current mortgage with a new one. Depending on your goals, it can reduce your payment, change your term, or convert equity into cash.</p></div>
  <div class="grid grid-3">
    {card("Rate-and-Term","Lower your rate or term","Adjust your interest rate, loan term, or both &mdash; a common way to reduce your monthly payment or pay off sooner.","Learn more","refinancing-guide.html")}
    {card("Cash-Out","Access your equity","Borrow against the equity you&rsquo;ve built for renovations, debt consolidation, or other goals.","Learn more","refinancing-guide.html")}
    {card("Streamline","FHA &amp; VA options","Eligible FHA and VA borrowers may qualify for simplified refinance programs.","Learn more","va-loans.html")}
  </div>
</div></section>
<section class="bg-light"><div class="wrap split">
  <div>
    <span class="eyebrow">Do the math</span>
    <h2>Understanding break-even</h2>
    <p class="lead">Your break-even point is when your accumulated monthly savings cover the cost of refinancing. Staying in the home beyond that point is where the savings begin.</p>
    <a class="btn btn-blue" href="calculators.html">Open the Refinance Calculator</a>
  </div>
  <ul class="feature-list">
    <li><b>Refinance checklist</b><span>Recent pay stubs and W-2s or tax returns.</span></li>
    <li><span>Statements for current mortgage and assets.</span></li>
    <li><span>Homeowners insurance information.</span></li>
    <li><span>A clear goal: lower payment, shorter term, or cash out.</span></li>
  </ul>
</div></section>
<section><div class="wrap">
  <div class="section-head"><span class="eyebrow">FAQ</span><h2>Refinance questions</h2></div>
  {faqs}
</div></section>
{cta_band(h="Thinking about refinancing?",p="Request a personalized quote and we&rsquo;ll help you weigh the numbers.",b1=("Request a Rate Quote","rates.html","btn-blue"))}
"""
PAGES["refinance.html"] = dict(title="Refinance", desc="Refinance to lower your rate, shorten your term, or access equity. Learn rate-and-term, cash-out, and break-even basics.", nav="refinance", body=_refi())

# ---------------- Loans (category grid) ----------------
def _loans():
    items = [
        ("Conventional","Conventional Loans","Flexible terms for well-qualified buyers.","conventional-loans.html"),
        ("FHA","FHA Loans","Low down payments and flexible credit.","fha-loans.html"),
        ("VA","VA Loans","$0 down for eligible veterans.","va-loans.html"),
        ("Jumbo","Jumbo Loans","Financing above conforming limits.","jumbo-loans.html"),
        ("Non-QM","Non-QM Loans","Alternative qualification paths.","non-qm-loans.html"),
        ("Self-Employed","Bank Statement Loans","Qualify on bank deposits.","bank-statement-loans.html"),
        ("Investors","DSCR Loans","Qualify on rental cash flow.","dscr-loans.html"),
        ("Equity","HELOC / Home Equity","Tap equity for flexible needs.","heloc.html"),
        ("Investors","Investment Property Loans","Financing for rentals and portfolios.","investment-property-loans.html"),
        ("Self-Employed","Self-Employed Programs","Options for business owners.","self-employed-borrowers.html"),
    ]
    grid = "".join(card(l, h, d, "Learn more", href) for l,h,d,href in items)
    return page_hero("Loan Programs", "A full range of mortgage solutions &mdash; from first-time buyers to seasoned investors. Find the program built around your situation.", "Loan Programs") + f"""
<section><div class="wrap">
  <div class="grid grid-3">{grid}</div>
</div></section>
{cta_band()}
"""
PAGES["loans.html"] = dict(title="Loan Programs", desc="Explore conventional, FHA, VA, jumbo, Non-QM, bank statement, DSCR, HELOC, and investment property loan programs.", nav="loans", body=_loans())

# ---------------- Loan detail pages (shared template) ----------------
def loan_page(crumb, title, sub, intro, highlights, reqs, benefits, faqs):
    hl = "".join(f'<div class="card center"><h3 style="color:var(--blue)">{a}</h3><p style="margin:0">{b}</p></div>' for a,b in highlights)
    req = "".join(f"<li>{x}</li>" for x in reqs)
    ben = "".join(f"<li>{x}</li>" for x in benefits)
    return page_hero(title, sub, crumb) + f"""
<section><div class="wrap">
  <div class="grid grid-4">{hl}</div>
</div></section>
<section style="padding-top:0"><div class="wrap split">
  <div>
    <span class="eyebrow">Overview</span>
    <h2>What it is</h2>
    {intro}
    <div class="btn-row"><a class="btn btn-blue" href="apply.html">Get Preapproved</a><a class="btn btn-outline" href="loans.html">All Loan Programs</a></div>
  </div>
  <div>
    <h3>Typical requirements</h3>
    <ul class="feature-list">{req}</ul>
    <h3 style="margin-top:30px">Potential benefits</h3>
    <ul class="feature-list">{ben}</ul>
  </div>
</div></section>
<section class="bg-light"><div class="wrap">
  <div class="section-head"><span class="eyebrow">FAQ</span><h2>Common questions</h2></div>
  {accordion(faqs)}
</div></section>
{wcci_cta("Not sure which loan program fits?", "Start with a WCCI AI Mortgage Review to organize your income, property, credit, and loan goals before speaking with a licensed mortgage professional.")}
{cta_band()}
"""

PAGES["conventional-loans.html"] = dict(title="Conventional Loans", nav="loans",
  desc="Conventional loans offer flexible terms and competitive rates for well-qualified buyers, with options as low as 3% down.",
  body=loan_page("Conventional Loans","Conventional Loans",
    "Flexible, widely used financing for well-qualified buyers &mdash; available for primary homes, second homes, and investment properties.",
    "<p>A conventional loan is not insured or guaranteed by the federal government. These loans follow guidelines set by Fannie Mae and Freddie Mac and remain the most popular financing choice for buyers with solid credit.</p><p>Down payments can start as low as 3% for qualifying buyers, though putting 20% down lets you avoid private mortgage insurance (PMI) entirely.</p>",
    [("3%","Minimum down for qualified buyers"),("620+","Typical minimum credit score"),("PMI","Removable at 20% equity"),("3 types","Primary, second, investment")],
    ["A credit score generally of 620 or higher","A down payment of 3%&ndash;20% depending on the program","A debt-to-income ratio generally at or below 43%","Steady, verifiable income and employment"],
    ["Available for primary, second, and investment properties","No upfront mortgage insurance fee like FHA","PMI can be removed once you reach 20% equity","Higher loan limits than FHA in most areas"],
    [("How much do I need to put down?","As little as 3% for qualified buyers, though 20% avoids PMI. We&rsquo;ll help you find the right balance for your budget."),
     ("What credit score do I need?","Generally 620 or higher. Stronger scores typically unlock better pricing.")]))

PAGES["fha-loans.html"] = dict(title="FHA Loans", nav="loans",
  desc="FHA loans offer low down payments and flexible credit guidelines, making them popular with first-time homebuyers.",
  body=loan_page("FHA Loans","FHA Loans",
    "Lower down payments and flexible credit requirements &mdash; one of the most accessible paths to homeownership, especially for first-time buyers.",
    "<p>FHA loans are insured by the Federal Housing Administration and offered by FHA-approved lenders. Because the government insures the loan, lenders can offer more flexible qualification standards.</p><p>FHA loans require an upfront mortgage insurance premium plus an annual premium paid monthly &mdash; factor this into your monthly cost when comparing programs.</p>",
    [("3.5%","Down with a 580+ score"),("580","Typical minimum credit score"),("MIP","Upfront + annual premium"),("Gifts","Allowed for down payment")],
    ["A credit score as low as 580 with 3.5% down (or 500&ndash;579 with 10% down)","A debt-to-income ratio typically up to 43%","Steady employment and verifiable income","The home must be your primary residence"],
    ["Down payments as low as 3.5%","Flexible credit requirements","Gift funds allowed for the down payment","Great for first-time buyers"],
    [("Can I use gift money for my down payment?","Yes &mdash; FHA allows your entire down payment to come from an eligible gift, such as from family."),
     ("Is FHA only for first-time buyers?","No. While popular with first-timers, FHA loans are available to any qualified buyer purchasing a primary residence.")]))

PAGES["va-loans.html"] = dict(title="VA Loans", nav="loans",
  desc="VA loans offer $0 down and no monthly mortgage insurance for eligible veterans, service members, and their families.",
  body=loan_page("VA Loans","VA Loans",
    "$0 down and no monthly mortgage insurance for eligible veterans, active-duty service members, and their families.",
    "<p>VA loans are guaranteed by the U.S. Department of Veterans Affairs. The VA guarantees a portion of the loan, allowing approved lenders to offer $0 down financing with competitive rates and no private mortgage insurance.</p><p>Eligible borrowers will need a valid Certificate of Eligibility (COE) based on their service.</p>",
    [("$0","Down for eligible borrowers"),("No PMI","Ever"),("IRRRL","Streamline refinance option"),("COE","Confirms eligibility")],
    ["A valid Certificate of Eligibility (COE) based on service","Sufficient income to cover the mortgage and expenses","A satisfactory credit profile (lenders set their own standards)"],
    ["$0 down payment for eligible borrowers","No private mortgage insurance","Competitive interest rates","No prepayment penalty"],
    [("Do I need a down payment?","Most eligible borrowers can finance 100% of the purchase price with $0 down."),
     ("How do I get my Certificate of Eligibility?","We help you request your COE as part of the application &mdash; it confirms your VA loan entitlement based on your service.")]))

PAGES["jumbo-loans.html"] = dict(title="Jumbo Loans", nav="loans",
  desc="Jumbo loans provide financing above conforming loan limits for higher-priced properties.",
  body=loan_page("Jumbo Loans","Jumbo Loans",
    "Financing above conforming loan limits &mdash; ideal for higher-priced and high-cost-area properties.",
    "<p>A jumbo loan exceeds the limits set by the Federal Housing Finance Agency. While they are non-conforming, jumbo loans remain essential for purchasing higher-priced homes and typically require stronger credit and reserves.</p><p>For strong borrowers, jumbo pricing is often very competitive with conforming loans.</p>",
    [("High","Above conforming limits"),("700+","Typical credit score"),("10&ndash;20%+","Typical down payment"),("Reserves","Often required")],
    ["A strong credit score, generally 700 or higher","A larger down payment (often 10&ndash;20%+)","Significant cash reserves","Full documentation of income and assets"],
    ["Finance high-value properties in a single loan","Competitive rates for strong borrowers","Fixed and adjustable options","Available for primary, second, and investment homes"],
    [("How much can I borrow?","Jumbo amounts can run well into the millions depending on your profile. We&rsquo;ll review what you may qualify for."),
     ("Are jumbo rates higher?","Not necessarily &mdash; for strong borrowers, jumbo rates are often very competitive with conforming loans.")]))

PAGES["non-qm-loans.html"] = dict(title="Non-QM Loans", nav="loans",
  desc="Non-QM loans offer alternative qualification paths for borrowers whose income doesn't fit traditional guidelines.",
  body=loan_page("Non-QM Loans","Non-QM Loans",
    "Alternative qualification paths for self-employed borrowers, investors, and others whose income doesn&rsquo;t fit traditional guidelines.",
    "<p>Non-QM (non-qualified mortgage) loans use flexible documentation and underwriting that fall outside standard agency rules. They&rsquo;re built for borrowers with strong financial profiles whose income is hard to document with traditional pay stubs and tax returns.</p><p>Common examples include bank statement loans, DSCR loans, and asset-based programs.</p>",
    [("Flexible","Documentation options"),("Self-employed","A common fit"),("Investors","Property cash-flow paths"),("Custom","Underwriting")],
    ["Alternative income documentation (bank statements, assets, or rental income)","A reasonable down payment, often larger than agency loans","A solid credit profile and reserves","A clear explanation of your income story"],
    ["Qualify when traditional income docs don&rsquo;t fit","Options for self-employed and investor borrowers","Flexible underwriting","Financing for unique scenarios"],
    [("Who are Non-QM loans for?","Self-employed borrowers, real estate investors, and others with non-traditional income who can demonstrate ability to repay."),
     ("Are rates higher than conventional?","They can be, reflecting the flexible underwriting. We&rsquo;ll compare options so you can decide what fits.")]))

PAGES["bank-statement-loans.html"] = dict(title="Bank Statement Loans", nav="loans",
  desc="Bank statement loans let self-employed borrowers qualify using bank deposits instead of traditional tax-return income.",
  body=loan_page("Bank Statement Loans","Bank Statement Loans",
    "Designed for self-employed borrowers &mdash; qualify using your bank deposits instead of traditional tax-return income.",
    "<p>If you&rsquo;re self-employed, your tax returns may not reflect your true earning power after deductions. A bank statement loan lets you qualify based on deposits over a recent period (often 12&ndash;24 months) rather than net income on tax returns.</p>",
    [("12&ndash;24 mo","Statements reviewed"),("Self-employed","Built for owners"),("No W-2","Required"),("Flexible","Income view")],
    ["Typically 12&ndash;24 months of personal or business bank statements","Evidence of self-employment","A solid credit profile","A down payment that fits the program"],
    ["Qualify on cash flow, not net taxable income","Ideal for business owners and freelancers","No tax returns required for income","Flexible program structures"],
    [("How many months of statements do I need?","Most programs review 12 to 24 months of deposits to establish qualifying income."),
     ("Can I use business accounts?","Yes &mdash; many programs accept personal or business bank statements, with adjustments for business expenses.")]))

PAGES["dscr-loans.html"] = dict(title="DSCR Loans", nav="loans",
  desc="DSCR loans let real estate investors qualify based on a property's rental cash flow rather than personal income.",
  body=loan_page("DSCR Loans","DSCR Loans",
    "Built for real estate investors &mdash; qualify investment properties on rental cash flow rather than personal income.",
    "<p>DSCR stands for Debt-Service Coverage Ratio. These loans qualify the property based on whether its rental income covers the mortgage payment, rather than relying on your personal income documentation.</p><p>A DSCR of 1.0 means rent equals the payment; higher ratios indicate stronger cash flow.</p>",
    [("DSCR","Income = property"),("Investors","Built for portfolios"),("No DTI","Personal income optional"),("Scale","Grow your holdings")],
    ["An investment (non-owner-occupied) property","Rental income that supports the debt-service coverage ratio","A down payment consistent with investor programs","A solid credit profile and reserves"],
    ["Qualify on property cash flow, not personal income","Streamlined documentation for investors","Finance multiple properties over time","Available for short- and long-term rentals"],
    [("What DSCR do I need?","Many programs look for a ratio at or above 1.0, though some allow lower with compensating factors. We&rsquo;ll review your scenario."),
     ("Can I use this for short-term rentals?","Often yes &mdash; some DSCR programs consider short-term rental income. Guidelines vary by program.")]))

PAGES["heloc.html"] = dict(title="HELOC & Home Equity", nav="loans",
  desc="Explore HELOC and home equity options to access the equity you've built for renovations, consolidation, or major goals.",
  body=loan_page("HELOC / Home Equity","HELOC &amp; Home Equity",
    "Tap the equity you&rsquo;ve built &mdash; for renovations, debt consolidation, investments, or major financial goals.",
    "<p>Home equity financing lets you borrow against the difference between your home&rsquo;s value and what you owe. A HELOC (home equity line of credit) works like a revolving line you draw from as needed, while a home equity loan provides a lump sum.</p>",
    [("Equity","Put it to work"),("HELOC","Revolving access"),("Lump sum","Fixed option"),("Flexible","Many uses")],
    ["Sufficient equity in your home","A solid credit profile","Verifiable income and manageable debt","A clear purpose for the funds"],
    ["Access cash without refinancing your first mortgage","Flexible draw options with a HELOC","Potentially lower rates than unsecured debt","Use funds for renovations, consolidation, and more"],
    [("HELOC or home equity loan?","A HELOC offers flexible, revolving access; a home equity loan provides a fixed lump sum. The right choice depends on how you&rsquo;ll use the funds."),
     ("How much can I borrow?","It depends on your equity, credit, and the program. We&rsquo;ll help you estimate your available options.")]))

PAGES["investment-property-loans.html"] = dict(title="Investment Property Loans", nav="loans",
  desc="Financing built for rental properties, second homes, and portfolio growth.",
  body=loan_page("Investment Property Loans","Investment Property Loans",
    "Financing built for rentals, second homes, and portfolio growth &mdash; with options for every type of investor.",
    "<p>Investment property loans help you purchase or refinance non-owner-occupied real estate. Depending on your strategy, you might use conventional investor financing, a DSCR loan based on rental cash flow, or a Non-QM program.</p>",
    [("Rentals","Long &amp; short term"),("DSCR","Cash-flow paths"),("Portfolio","Scale over time"),("Options","Conventional + Non-QM")],
    ["A non-owner-occupied property","A down payment consistent with investor programs","Reserves and a solid credit profile","Documentation appropriate to the chosen program"],
    ["Multiple financing paths for investors","Qualify on rental income with DSCR programs","Build and scale a rental portfolio","Options for second homes and vacation rentals"],
    [("Which program is best for investors?","It depends on your income documentation and strategy. DSCR loans qualify on rental cash flow; conventional and Non-QM options may also fit."),
     ("How much down payment is required?","Investment properties typically require a larger down payment than primary residences. We&rsquo;ll outline the specifics for your scenario.")]))

PAGES["self-employed-borrowers.html"] = dict(title="Self-Employed Borrowers", nav="loans",
  desc="Mortgage options for self-employed borrowers, including bank statement and Non-QM programs.",
  body=loan_page("Self-Employed Borrowers","Mortgage Options for Self-Employed Borrowers",
    "Being your own boss shouldn&rsquo;t make financing harder. We offer programs designed around how entrepreneurs actually earn.",
    "<p>Self-employed borrowers often show lower net income after deductions, which can complicate traditional qualification. We work with bank statement loans, Non-QM programs, and asset-based options to present your income accurately.</p>",
    [("Owners","Built for you"),("Bank stmt","Qualify on deposits"),("Non-QM","Flexible paths"),("Assets","Alternative options")],
    ["Evidence of self-employment","Bank statements, assets, or returns depending on program","A solid credit profile and reserves","A clear picture of your income"],
    ["Programs that reflect real business cash flow","No reliance on net taxable income for some options","Flexible documentation","Guidance from advisors who understand entrepreneurs"],
    [("What documents will I need?","It depends on the program &mdash; often bank statements, asset statements, or business documentation rather than just tax returns."),
     ("Can I qualify with a newer business?","Often yes, though guidelines vary. We&rsquo;ll review your time in business and income history.")]))

# ---------------- Calculators ----------------
def _calc():
    field = lambda i,l,v,t="number",extra="": f'<div class="field"><label for="{i}">{l}</label><input id="{i}" type="{t}" value="{v}" {extra}></div>'
    term = '<div class="field"><label for="c-term">Loan term (years)</label><select id="c-term"><option>30</option><option>20</option><option>15</option><option>10</option></select></div>'
    more = "".join([
        card("","Affordability Calculator","See a comfortable price range based on your income.","Open","calculators.html"),
        card("","Refinance Calculator","Compare your current loan with a potential new one.","Open","calculators.html"),
        card("","Cash-Out Calculator","Estimate how much equity you may be able to access.","Open","calculators.html"),
        card("","Amortization Calculator","See how your balance pays down over time.","Open","calculators.html"),
        card("","Down Payment Calculator","Plan how much to put down on your home.","Open","calculators.html"),
    ])
    return page_hero("Mortgage Calculators", "Estimate your monthly payment and explore scenarios. Figures are estimates for educational purposes and not an offer to lend.", "Calculators") + f"""
<section><div class="wrap">
  <div class="calc-panel">
    <div>
      <h3 style="color:#fff">Mortgage Payment Calculator</h3>
      <div class="calc-fields">
        {field("c-price","Home price ($)","450000")}
        {field("c-down","Down payment (%)","20")}
        {field("c-rate","Interest rate (%)","6.5",extra='step="0.01"')}
        {term}
        {field("c-tax","Property tax / year ($)","5400")}
        {field("c-ins","Insurance / year ($)","1500")}
        {field("c-hoa","HOA / month ($)","0")}
      </div>
    </div>
    <div class="calc-out">
      <span class="total">Estimated total monthly payment</span>
      <span class="big" id="c-out-total">$0</span>
      <div class="calc-row"><span>Principal &amp; interest</span><b id="c-out-pi">$0</b></div>
      <div class="calc-row"><span>Property tax</span><b id="c-out-tax">$0</b></div>
      <div class="calc-row"><span>Insurance</span><b id="c-out-ins">$0</b></div>
      <div class="calc-row"><span>HOA</span><b id="c-out-hoa">$0</b></div>
      <div class="calc-row"><span>Loan amount</span><b id="c-out-loan">$0</b></div>
    </div>
  </div>
  <p class="form-note">Estimates only and not an offer to lend. Your actual payment depends on your full financial profile, program, and current market conditions.</p>
</div></section>
{wcci_cta("Want help interpreting the numbers?", "Use WCCI.Online to review your mortgage scenario and organize the questions a loan officer will need to answer.", "Review My Scenario")}
<section class="bg-light"><div class="wrap">
  <div class="section-head"><span class="eyebrow">More tools</span><h2>Additional mortgage calculators</h2></div>
  <div class="grid grid-3">{more}</div>
</div></section>
{cta_band(h="Want a real number?",p="Request a personalized quote and we&rsquo;ll factor in today&rsquo;s market and your profile.",b1=("Request a Rate Quote","rates.html","btn-blue"))}
"""
PAGES["calculators.html"] = dict(title="Mortgage Calculators", desc="Estimate your monthly mortgage payment with our calculator, plus affordability, refinance, cash-out, and amortization tools.", nav="resources", body=_calc())

# ---------------- Rates ----------------
def _rates():
    return page_hero("Mortgage Rates", "Mortgage rates change daily. The most accurate number is a personalized quote based on your profile.", "Mortgage Rates") + f"""
<section><div class="wrap split">
  <div>
    <span class="eyebrow">Today&rsquo;s market</span>
    <h2>Request today&rsquo;s rate quote</h2>
    <p class="lead">Mortgage rates change daily based on market conditions, loan program, credit profile, occupancy, property type, loan amount, and other factors. Rather than post a number that may not apply to you, we&rsquo;ll prepare a personalized quote.</p>
    <div class="btn-row"><a class="btn btn-blue" href="contact.html">Request a Quote</a><a class="btn btn-outline" href="loan-officer.html">Talk to a Loan Officer</a></div>
  </div>
  <ul class="feature-list">
    <li><b>What affects your rate</b><span>Credit profile and history.</span></li>
    <li><span>Loan program and term.</span></li>
    <li><span>Down payment and loan-to-value.</span></li>
    <li><span>Occupancy and property type.</span></li>
    <li><span>Loan amount and overall market conditions.</span></li>
  </ul>
</div></section>
<section class="bg-light"><div class="wrap">
  <div class="section-head"><span class="eyebrow">Strategy</span><h2>Rate strategy</h2>
  <p class="lead">A lower rate isn&rsquo;t always the lowest total cost. We&rsquo;ll help you weigh points, closing costs, and how long you plan to stay so the structure fits your goals.</p></div>
  <div class="grid grid-3">
    {card("","Compare scenarios","Look at multiple structures side by side before deciding.","Use calculators","calculators.html")}
    {card("","Understand points","Decide whether paying points to lower your rate makes sense.","Learn more","mortgage-articles.html")}
    {card("","Plan your timeline","Your time horizon affects which option costs less overall.","Talk to us","loan-officer.html")}
  </div>
</div></section>
{cta_band(h="Get a personalized rate quote",p="No fake live rates &mdash; just a real quote built around your situation.",b1=("Request a Quote","contact.html","btn-blue"))}
"""
PAGES["rates.html"] = dict(title="Mortgage Rates", desc="Mortgage rates change daily. Request a personalized rate quote and learn what factors affect your rate.", nav="resources", body=_rates())

# ---------------- Resources ----------------
def _resources():
    items = [
        ("Mortgage Calculators","Estimate payments and run scenarios.","calculators.html"),
        ("First-Time Homebuyer Hub","Prepare, qualify, and buy with confidence.","first-time-homebuyer.html"),
        ("Homebuying Guide","The step-by-step path to the keys.","homebuying-guide.html"),
        ("Refinancing Guide","Understand when refinancing makes sense.","refinancing-guide.html"),
        ("Mortgage Articles","Plain-English guides and explainers.","mortgage-articles.html"),
        ("Mortgage Glossary","Key mortgage terms, defined simply.","glossary.html"),
        ("Mortgage FAQ","Answers to common borrower questions.","faq.html"),
    ]
    grid = "".join(card("", h, d, "Explore", href) for h,d,href in items) + card_ext("WCCI", "WCCI.Online AI Mortgage Review", "A quick AI-assisted way to prepare your mortgage questions before speaking with us.", "Open Tool", WCCI_URL)
    return page_hero("Mortgage Resources", "Tools, guides, and answers to help you make confident decisions about your home loan.", "Mortgage Resources") + f"""
<section><div class="wrap"><div class="grid grid-3">{grid}</div></div></section>
{cta_band()}
"""
PAGES["resources.html"] = dict(title="Mortgage Resources", desc="Mortgage calculators, first-time homebuyer hub, homebuying and refinancing guides, articles, glossary, and FAQ.", nav="resources", body=_resources())

# ---------------- First-time homebuyer ----------------
def _ftb():
    faqs = accordion([
        ("How much do I need to save?","Beyond the down payment, plan for closing costs and reserves. We&rsquo;ll help you build a realistic target."),
        ("Does my credit need to be perfect?","No. Many programs work with a range of credit profiles &mdash; we&rsquo;ll explain what affects your options."),
        ("What loan is best for first-time buyers?","It depends on your finances and goals. FHA and conventional low-down-payment programs are common starting points."),
    ])
    return page_hero("First-Time Homebuyer Hub", "Everything you need to prepare, qualify, and buy your first home with confidence.", "First-Time Homebuyer Hub") + f"""
<section><div class="wrap">
  <div class="grid grid-3">
    {card("Step 1","How to prepare","Review your finances, build savings, and set a realistic budget.","Get started","apply.html")}
    {card("Step 2","Credit basics","Understand what lenders look for and how to strengthen your profile.","Learn more","glossary.html")}
    {card("Step 3","Down payment","Explore how much you need and where the funds can come from.","Use calculators","calculators.html")}
    {card("Step 4","Pre-approval","Know your budget and shop with a stronger offer.","Get preapproved","apply.html")}
    {card("Step 5","Choose your loan","Match the right program to your situation.","See programs","loans.html")}
    {card("Step 6","Make your move","Find a home, make an offer, and close with guidance.","Read the guide","homebuying-guide.html")}
  </div>
</div></section>
<section class="bg-light"><div class="wrap">
  <div class="section-head"><span class="eyebrow">FAQ</span><h2>First-time buyer questions</h2></div>
  {faqs}
</div></section>
{cta_band(b1=("Get Preapproved",APPLY_URL,"btn-blue"), note=True)}
"""
PAGES["first-time-homebuyer.html"] = dict(title="First-Time Homebuyer Hub", desc="Prepare, qualify, and buy your first home: credit basics, down payment, pre-approval, and choosing the right loan.", nav="resources", body=_ftb())

# ---------------- Homebuying guide (12 steps accordion) ----------------
def _guide():
    steps = [
        ("1. Review your finances","Take stock of income, debts, and savings to understand what you can comfortably afford."),
        ("2. Check your credit","Review your credit reports and scores, and address any issues early."),
        ("3. Estimate your budget","Use calculators to estimate a monthly payment that fits your life."),
        ("4. Get preapproved","A preapproval clarifies your budget and strengthens your offers."),
        ("5. Choose your loan program","Compare conventional, FHA, VA, and other programs with your advisor."),
        ("6. Find a real estate agent","Partner with an agent who knows your target market."),
        ("7. Shop for homes","Tour homes within your price range and priorities."),
        ("8. Make an offer","Submit a competitive offer with your preapproval in hand."),
        ("9. Complete the appraisal","The lender orders an appraisal to confirm the home&rsquo;s value."),
        ("10. Go through underwriting","Underwriting verifies your documents and finalizes approval."),
        ("11. Review the closing disclosure","Review your final terms and costs at least three business days before closing."),
        ("12. Close and get the keys","Sign your documents, fund the loan, and take ownership of your home."),
    ]
    return page_hero("How to Buy a House", "A clear, 12-step roadmap from reviewing your finances to getting the keys.", "Homebuying Guide") + f"""
<section><div class="wrap" style="max-width:860px">
  {accordion(steps)}
</div></section>
{cta_band(b1=("Get Preapproved",APPLY_URL,"btn-blue"), note=True)}
"""
PAGES["homebuying-guide.html"] = dict(title="How to Buy a House", desc="A 12-step homebuying guide: from reviewing your finances and getting preapproved to closing and getting the keys.", nav="resources", body=_guide())

# ---------------- Refinancing guide ----------------
def _refguide():
    faqs = accordion([
        ("When does refinancing make sense?","Often when you can lower your rate or payment, shorten your term, or access needed equity &mdash; and you&rsquo;ll stay past your break-even point."),
        ("When might it not make sense?","If you&rsquo;ll move before reaching break-even, or if costs outweigh the benefit, refinancing may not be worth it."),
        ("What does it cost to refinance?","Closing costs typically include lender, appraisal, title, and recording fees. We&rsquo;ll lay them out clearly."),
    ])
    return page_hero("Refinancing Guide", "Understand the why, the math, and the timing so you can decide with confidence.", "Refinancing Guide") + f"""
<section><div class="wrap">
  <div class="grid grid-3">
    {card("","Why refinance","Lower your rate or payment, shorten your term, or access equity.","Learn more","refinance.html")}
    {card("","Cash-out vs rate-and-term","Know the difference and which fits your goal.","Compare","refinance.html")}
    {card("","Costs &amp; break-even","Understand fees and when savings overtake them.","Use calculator","calculators.html")}
  </div>
</div></section>
<section class="bg-light"><div class="wrap">
  <div class="section-head"><span class="eyebrow">FAQ</span><h2>Refinancing questions</h2></div>
  {faqs}
</div></section>
{cta_band(h="Should you refinance?",p="We&rsquo;ll run the numbers with you and explain your options clearly.",b1=("Request a Rate Quote","rates.html","btn-blue"))}
"""
PAGES["refinancing-guide.html"] = dict(title="Refinancing Guide", desc="Why refinance, cash-out vs rate-and-term, costs, break-even, and when refinancing may not make sense.", nav="resources", body=_refguide())

# ---------------- Mortgage articles ----------------
def _articles():
    arts = [
        ("Preapproval","How to Get Preapproved for a Mortgage"),
        ("Refinance","What Is a Cash-Out Refinance?"),
        ("Costs","How Much Does It Cost to Refinance?"),
        ("Programs","FHA vs Conventional Loans"),
        ("Investors","How DSCR Loans Work"),
        ("Self-Employed","Mortgage Tips for Self-Employed Borrowers"),
        ("Rates","What Affects Mortgage Rates?"),
        ("Down Payment","How Much Down Payment Do You Need?"),
    ]
    cards = "".join(
        f'<a class="article-card" href="#"><div class="article-thumb"></div><div class="body">'
        f'<span class="label">{l}</span><h3>{h}</h3>'
        f'<p>A clear, borrower-friendly explanation to help you decide with confidence.</p></div></a>'
        for l,h in arts)
    return page_hero("Mortgage Articles", "Plain-English guides and explainers to help you make smart, confident decisions.", "Mortgage Articles") + f"""
<section><div class="wrap"><div class="grid grid-3">{cards}</div></div></section>
{cta_band()}
"""
PAGES["mortgage-articles.html"] = dict(title="Mortgage Articles", desc="Plain-English mortgage articles: preapproval, cash-out refinance, refinance costs, FHA vs conventional, DSCR loans, and more.", nav="resources", body=_articles())

# ---------------- Glossary ----------------
def _glossary():
    terms = [
        ("APR","The annual percentage rate reflects your interest rate plus certain costs, expressed as a yearly rate."),
        ("Appraisal","A professional estimate of a home&rsquo;s market value, ordered by the lender."),
        ("Closing Costs","Fees paid at closing, such as lender, title, appraisal, and recording charges."),
        ("Debt-to-Income Ratio","Your monthly debt payments divided by gross monthly income, used in qualification."),
        ("Escrow","An account that holds funds for property taxes and insurance, paid as part of your monthly payment."),
        ("FHA","A loan insured by the Federal Housing Administration, known for flexible qualification."),
        ("Jumbo Loan","Financing that exceeds conforming loan limits set by the FHFA."),
        ("Loan Estimate","A standardized form outlining your estimated loan terms and costs."),
        ("LTV","Loan-to-value &mdash; the loan amount divided by the property value."),
        ("Mortgage Insurance","Coverage that protects the lender; often required with lower down payments."),
        ("Preapproval","A lender&rsquo;s assessment of how much you may be able to borrow."),
        ("Rate Lock","An agreement to hold a specific interest rate for a set period."),
        ("Underwriting","The lender&rsquo;s process of verifying your information and approving the loan."),
    ]
    rows = "".join(f'<div class="term"><b>{t}</b><span>{d}</span></div>' for t,d in terms)
    return page_hero("Mortgage Glossary", "Key mortgage terms defined in plain language.", "Mortgage Glossary") + f"""
<section><div class="wrap" style="max-width:860px"><div class="glossary">{rows}</div></div></section>
{cta_band()}
"""
PAGES["glossary.html"] = dict(title="Mortgage Glossary", desc="Plain-language definitions of key mortgage terms: APR, appraisal, escrow, LTV, underwriting, and more.", nav="resources", body=_glossary())

# ---------------- FAQ ----------------
def _faq():
    cats = [
        ("Buying a home", [
            ("How much do I need for a down payment?","It varies by program &mdash; some start as low as 3%, with $0-down options for eligible VA borrowers."),
            ("What is preapproval?","A lender&rsquo;s assessment of how much you may borrow, which strengthens your offer."),
        ]),
        ("Refinancing", [
            ("How do I know if it&rsquo;s worth it?","Compare monthly savings to closing costs to find your break-even point."),
            ("What is cash-out?","Replacing your mortgage with a larger loan and taking the difference in cash."),
        ]),
        ("Loan programs", [
            ("Which program is right for me?","It depends on your finances and goals &mdash; we&rsquo;ll compare options with you."),
            ("Do you offer self-employed programs?","Yes &mdash; including bank statement and Non-QM options."),
        ]),
        ("Rates", [
            ("Why don&rsquo;t you post live rates?","Rates change daily and depend on your profile; a personalized quote is more accurate."),
        ]),
        ("Documents", [
            ("What will I need to provide?","Typically income, asset, and identity documentation &mdash; the exact list depends on your program."),
        ]),
        ("Closing process", [
            ("How long does closing take?","Many loans close in roughly 30&ndash;45 days once under contract."),
        ]),
    ]
    out = []
    for title, items in cats:
        out.append(f'<h3 style="margin-top:36px">{title}</h3>{accordion(items)}')
    return page_hero("Mortgage FAQ", "Answers to common questions about buying, refinancing, programs, rates, documents, and closing.", "Mortgage FAQ") + f"""
<section><div class="wrap" style="max-width:860px">{''.join(out)}</div></section>
{cta_band()}
"""
PAGES["faq.html"] = dict(title="Mortgage FAQ", desc="Frequently asked mortgage questions about buying a home, refinancing, loan programs, rates, documents, and closing.", nav="resources", body=_faq())

# ---------------- Apply ----------------
def _apply():
    form = """
<form class="form" data-ack novalidate>
  <div class="form-ok" hidden>Thank you. This is not a full loan application &mdash; a licensed mortgage professional will follow up to discuss next steps.</div>
  <input type="text" class="hp" tabindex="-1" autocomplete="off" aria-hidden="true" name="company">
  <div class="form-grid">
    <div class="field"><label for="fn">First name</label><input id="fn" name="fn" required></div>
    <div class="field"><label for="ln">Last name</label><input id="ln" name="ln" required></div>
    <div class="field"><label for="em">Email</label><input id="em" type="email" name="em" required></div>
    <div class="field"><label for="ph">Phone</label><input id="ph" type="tel" name="ph" required></div>
    <div class="field"><label for="goal">Loan goal</label><select id="goal" name="goal"><option>Buy a Home</option><option>Refinance</option><option>Home Equity</option><option>Investment Property</option></select></div>
    <div class="field"><label for="price">Estimated price / value ($)</label><input id="price" type="number" name="price"></div>
    <div class="field"><label for="dp">Down payment / equity ($)</label><input id="dp" type="number" name="dp"></div>
    <div class="field"><label for="cr">Credit range</label><select id="cr" name="cr"><option>Excellent (740+)</option><option>Good (680&ndash;739)</option><option>Fair (620&ndash;679)</option><option>Below 620</option><option>Not sure</option></select></div>
    <div class="field"><label for="emp">Employment type</label><select id="emp" name="emp"><option>W-2 employee</option><option>Self-employed</option><option>Retired</option><option>Other</option></select></div>
    <div class="field full"><label for="msg">Message</label><textarea id="msg" name="msg"></textarea></div>
  </div>
  <div style="margin-top:20px"><button class="btn btn-blue btn-lg" type="submit">Submit Request</button></div>
  <p class="form-note">This is not a full loan application. A licensed mortgage professional will follow up to discuss next steps. NMLS #%s &middot; Equal Housing Opportunity.</p>
</form>""" % NMLS
    return page_hero("Start Your Application", "Ready to move forward? Start the full 1003 application below &mdash; a licensed mortgage professional reviews every submission.", "Apply Now") + f"""
<section><div class="wrap" style="max-width:880px;text-align:center">
  <a class="btn btn-lg btn-blue" href="{APPLY_URL}" target="_blank" rel="noopener noreferrer">Start Full 1003 Application</a>
  {apply_note()}
  <p class="muted" style="margin-top:20px">Not ready for the full application? Try WCCI.Online AI Mortgage Review first. <a href="{WCCI_URL}" target="_blank" rel="noopener noreferrer" style="color:var(--blue);font-weight:600">Open WCCI.Online</a></p>
  <p class="wcci-note" style="margin-top:8px">{WCCI_DISCLOSURE}</p>
  <div class="apply-support"><h3>Questions before applying?</h3><p class="contact-lines">{contact_block()}</p></div>
</div></section>
<section id="apply-form" class="bg-light"><div class="wrap" style="max-width:880px">
  <div class="section-head center"><h2>Or send a quick request</h2><p class="lead">Prefer we reach out first? Share a few details and a licensed professional will follow up.</p></div>
  {form}
</div></section>
"""
PAGES["apply.html"] = dict(title="Start Your Application", desc="Start a short mortgage intake. No obligation — a licensed mortgage professional will follow up to discuss your options.", nav="", body=_apply())

# ---------------- Loan officer ----------------
def _lo():
    form = f"""
<form class="form" data-ack novalidate>
  <div class="form-ok" hidden>Thanks! A loan advisor will reach out shortly.</div>
  <input type="text" class="hp" tabindex="-1" autocomplete="off" aria-hidden="true" name="company">
  <div class="form-grid">
    <div class="field"><label for="lname">Name</label><input id="lname" name="name" required></div>
    <div class="field"><label for="lemail">Email</label><input id="lemail" type="email" name="email" required></div>
    <div class="field"><label for="lphone">Phone</label><input id="lphone" type="tel" name="phone"></div>
    <div class="field"><label for="ltopic">I&rsquo;d like to discuss</label><select id="ltopic" name="topic"><option>Buying a home</option><option>Refinancing</option><option>Loan programs</option><option>General question</option></select></div>
    <div class="field full"><label for="lmsg">Message</label><textarea id="lmsg" name="message"></textarea></div>
  </div>
  <div style="margin-top:20px"><button class="btn btn-blue btn-lg" type="submit">Request a Call</button></div>
</form>"""
    return page_hero("Find a Loan Officer", "Speak with a licensed loan advisor who will guide you from first questions to closing.", "Find a Loan Officer") + f"""
<section><div class="wrap split">
  <div>
    <span class="eyebrow">We&rsquo;re here to help</span>
    <h2>Speak with a loan advisor</h2>
    <p class="lead">Whether you&rsquo;re just exploring or ready to apply, a licensed professional will help you understand your options with no pressure.</p>
    <p class="contact-lines">{contact_block()}</p>
    <a class="btn btn-blue" href="{APPLY_URL}" target="_blank" rel="noopener noreferrer">Start an Application</a>
  </div>
  {form}
</div></section>
"""
PAGES["loan-officer.html"] = dict(title="Find a Loan Officer", desc="Speak with a licensed loan advisor at West Coast Capital Mortgage to discuss buying, refinancing, and loan programs.", nav="loan-officer", body=_lo())

# ---------------- About ----------------
def _about():
    return page_hero("About West Coast Capital Mortgage", "A modern mortgage company built on clear guidance, smart solutions, and a borrower-first experience.", "About Us") + f"""
<section><div class="wrap split">
  <div>
    <span class="eyebrow">Who we are</span>
    <h2>Company overview</h2>
    <p class="lead">West Coast Capital Mortgage Inc. is a modern mortgage company focused on helping people buy homes, refinance, and build equity with confidence. We pair efficient technology with experienced, licensed guidance.</p>
    <p class="muted">Our mission is simple: make financing clear, honest, and built around your goals.</p>
  </div>
  <ul class="feature-list">
    <li><b>Clear guidance</b><span>Straight answers and transparent options.</span></li>
    <li><b>Smart solutions</b><span>A full range of programs for every borrower.</span></li>
    <li><b>Technology + people</b><span>Modern tools backed by real advisors.</span></li>
    <li><b>Borrower-first</b><span>No hype, no pressure &mdash; just a smooth process.</span></li>
  </ul>
</div></section>
<section id="anatoliy"><div class="wrap">
  <div class="section-head"><span class="eyebrow" style="color:var(--blue)">Founder &amp; Mortgage Professional</span><h2>Meet Anatoliy Kanevsky</h2></div>
  <div class="founder-grid">
    <div class="founder-photo"><img src="assets/anatoliy-kanevsky.png" alt="Anatoliy Kanevsky, founder of West Coast Capital Mortgage Inc." loading="lazy"></div>
    <div>
      <p>Anatoliy Kanevsky is the founder of West Coast Capital Mortgage Inc. and a California real estate and mortgage professional with decades of experience helping borrowers, investors, and real estate clients navigate complex financing decisions.</p>
      <p>His background combines mortgage lending, real estate brokerage, luxury residential development, and real-world deal analysis. That perspective allows West Coast Capital Mortgage to approach every client scenario with both lending discipline and practical real estate experience.</p>
      <p>Whether a client is buying a primary residence, refinancing, purchasing a luxury property, financing an investment property, or exploring self-employed, Non-QM, jumbo, FHA, VA, or DSCR options, Anatoliy&rsquo;s focus is simple: clear guidance, smart structure, and a mortgage strategy that fits the client&rsquo;s actual situation.</p>
      <ul class="founder-cred">
        <li>California Real Estate Broker</li>
        <li>Mortgage professional since 2001</li>
        <li>Luxury real estate and development experience</li>
        <li>Purchase, refinance, jumbo, Non-QM, DSCR, and self-employed borrower strategy</li>
        <li>Founder, West Coast Capital Mortgage Inc.</li>
      </ul>
      <p class="founder-contact"><b>Anatoliy Direct:</b> <a href="tel:{DIRECT_TEL}">{DIRECT_PHONE}</a><br><b>Email:</b> <a href="mailto:{EMAIL}">{EMAIL}</a></p>
      <div class="btn-row" style="margin-top:18px"><a class="btn btn-blue" href="contact.html">Contact Anatoliy</a><a class="btn btn-outline" href="{APPLY_URL}" target="_blank" rel="noopener noreferrer">Start Application</a></div>
    </div>
  </div>
</div></section>
<section class="bg-light"><div class="wrap">
  <div class="section-head center"><span class="eyebrow">Why WCCM</span><h2>Why borrowers choose us</h2></div>
  <div class="grid grid-3">
    {card("","Mortgage solutions","Conventional, FHA, VA, jumbo, Non-QM, DSCR, and more.","See programs","loans.html")}
    {card("","Modern tools","Calculators and a short application to move quickly.","Try our tools","calculators.html")}
    {card("","Human guidance","Licensed advisors who explain every step.","Talk to us","loan-officer.html")}
  </div>
  <p class="form-note center" style="margin-top:30px">West Coast Capital Mortgage Inc. NMLS #{NMLS}. Equal Housing Opportunity. This is not a commitment to lend. All loans are subject to credit, income, property, and underwriting approval.</p>
</div></section>
{cta_band()}
"""
PAGES["about.html"] = dict(title="About West Coast Capital Mortgage", desc="West Coast Capital Mortgage Inc. is a modern mortgage company built on clear guidance, smart loan solutions, and a borrower-first experience.", nav="about", body=_about())

# ---------------- Contact ----------------
def _contact():
    form = f"""
<form class="form" data-ack novalidate>
  <div class="form-ok" hidden>Thanks! Your message has been sent &mdash; we&rsquo;ll be in touch shortly.</div>
  <input type="text" class="hp" tabindex="-1" autocomplete="off" aria-hidden="true" name="company">
  <div class="form-grid">
    <div class="field"><label for="cname">Name</label><input id="cname" name="name" required></div>
    <div class="field"><label for="cemail">Email</label><input id="cemail" type="email" name="email" required></div>
    <div class="field"><label for="cphone">Phone</label><input id="cphone" type="tel" name="phone"></div>
    <div class="field"><label for="csubject">Subject</label><input id="csubject" name="subject"></div>
    <div class="field full"><label for="cmsg">Message</label><textarea id="cmsg" name="message" required></textarea></div>
  </div>
  <div style="margin-top:20px"><button class="btn btn-blue btn-lg" type="submit">Send Message</button></div>
</form>"""
    return page_hero("Contact Us", "Questions about rates, programs, or your application? Reach out and we&rsquo;ll get back to you fast.", "Contact Us") + f"""
<section><div class="wrap split">
  <div>
    <span class="eyebrow">Get in touch</span>
    <h2>We&rsquo;re here to help</h2>
    <p class="lead">We&rsquo;re here to make your home financing simple and clear.</p>
    <p class="contact-lines">{contact_block()}</p>
    <p class="muted">Equal Housing Opportunity &middot; NMLS #{NMLS}</p>
  </div>
  {form}
</div></section>
"""
PAGES["contact.html"] = dict(title="Contact Us", desc="Contact West Coast Capital Mortgage Inc. with questions about rates, loan programs, or your application.", nav="", body=_contact())

# ---------------- Make a payment ----------------
def _payment():
    return page_hero("Make a Payment", "Manage your mortgage payment and find borrower support resources.", "Make a Payment") + f"""
<section><div class="wrap split">
  <div>
    <span class="eyebrow">Servicing</span>
    <h2>Payment portal</h2>
    <p class="lead">Access your servicing portal to view your balance, schedule payments, and manage your account. (Portal link placeholder &mdash; connect your servicer here.)</p>
    <div class="btn-row"><a class="btn btn-blue" href="#">Open Payment Portal</a><a class="btn btn-outline" href="contact.html">Borrower Support</a></div>
  </div>
  <ul class="feature-list">
    <li><b>Borrower support</b><span>Questions about your statement or escrow? We can help.</span></li>
    <li><b>Account management</b><span>Update your contact and payment preferences.</span></li>
    <li><b>Important note</b><span>If your loan is serviced by another institution, please follow the payment instructions from your loan servicer.</span></li>
  </ul>
</div></section>
<section class="bg-light"><div class="wrap"><div class="cta-band" style="background:var(--charcoal)">
  <h2>Need help with your payment?</h2>
  <p>Our team can point you to the right servicer and answer general questions.</p>
  <div class="btn-row"><a class="btn btn-lg btn-blue" href="contact.html">Contact Support</a></div>
</div></div></section>
"""
# payment.html intentionally not generated (Make a Payment removed sitewide).

# ---------------- WCCI AI Mortgage Review (dedicated page) ----------------
def _airev():
    return page_hero("Prepare your mortgage scenario before you apply.",
        "WCCI.Online is our AI-powered mortgage review tool. It can help you organize your goals and questions before speaking with West Coast Capital Mortgage.",
        "AI Mortgage Review") + f"""
<section><div class="wrap" style="max-width:760px;text-align:center">
  <span class="eyebrow" style="color:var(--blue)">WCCI.Online AI Mortgage Review</span>
  <h2>Start a quick AI mortgage review</h2>
  <p class="lead" style="margin-left:auto;margin-right:auto">Use WCCI.Online to organize your scenario and questions, then come back to apply with West Coast Capital Mortgage. It&rsquo;s an optional shortcut &mdash; not required to apply.</p>
  <div class="btn-row" style="justify-content:center">
    <a class="btn btn-lg btn-blue" href="{WCCI_URL}" target="_blank" rel="noopener noreferrer">Open WCCI.Online</a>
    <a class="btn btn-lg btn-outline" href="{APPLY_URL}" target="_blank" rel="noopener noreferrer">Start Full Application</a>
  </div>
  <p class="apply-note">{APPLY_NOTE_TEXT}</p>
  <p class="wcci-note" style="margin-top:18px;display:inline-block;text-align:left">{WCCI_DISCLOSURE_FULL}</p>
</div></section>
"""

PAGES["ai-mortgage-review.html"] = dict(title="WCCI.Online AI Mortgage Review",
    desc="WCCI AI Mortgage Assistant by West Coast Capital Mortgage — organize your goals, review your scenario, and prepare a document checklist before speaking with a licensed mortgage professional. Preliminary educational guidance only.",
    nav="", body=_airev())

# >>> INSERT PAGES HERE <<<

# ----------------------------------------------------------------------------
# Write everything
# ----------------------------------------------------------------------------
def main():
    os.makedirs(os.path.join(OUT, "assets"), exist_ok=True)
    with open(os.path.join(OUT, "styles.css"), "w", encoding="utf-8") as f: f.write(CSS)
    with open(os.path.join(OUT, "script.js"), "w", encoding="utf-8") as f: f.write(JS)
    # favicon
    fav = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">'
           '<rect width="64" height="64" rx="12" fill="#0c1c33"/>'
           '<path d="M14 20 L20 44 L26 28 L32 44 L38 20" fill="none" stroke="#0073e6" stroke-width="5" '
           'stroke-linejoin="round" stroke-linecap="round"/>'
           '<rect x="40" y="20" width="5" height="24" fill="#fff"/></svg>')
    with open(os.path.join(OUT, "assets", "favicon.svg"), "w", encoding="utf-8") as f: f.write(fav)
    # placeholder logo (SVG stand-in for assets/logo.png)
    logo = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 64">'
            '<text x="0" y="26" font-family="Inter,Arial" font-size="20" font-weight="800" fill="#0c1c33">WEST COAST CAPITAL</text>'
            '<text x="0" y="50" font-family="Inter,Arial" font-size="12" font-weight="700" letter-spacing="6" fill="#0073e6">MORTGAGE INC.</text></svg>')
    with open(os.path.join(OUT, "assets", "logo.svg"), "w", encoding="utf-8") as f: f.write(logo)
    with open(os.path.join(OUT, "assets", "README.txt"), "w", encoding="utf-8") as f:
        f.write("Replace logo.svg with your own logo.png and update the <a class=\"logo\"> markup in each page header.\n")

    count = 0
    for name, p in PAGES.items():
        html = page(p["title"], p["desc"], p.get("nav",""), p["body"])
        with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
            f.write(html)
        count += 1
    print(f"Wrote {count} pages + styles.css + script.js + assets/ into {OUT}")

if __name__ == "__main__":
    main()
