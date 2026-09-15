/* West Coast Capital Mortgage — site scripts (no dependencies) */
(function(){
  "use strict";

  /* Lightweight attribution + conversion event layer.
     This works before GTM/Google Ads is installed: Netlify form submissions still
     retain attribution fields, and the dataLayer events are ready to consume later. */
  window.dataLayer=window.dataLayer||[];
  function pushEvent(name,detail){
    var payload=detail||{};
    payload.event=name;
    window.dataLayer.push(payload);
  }
  function param(name){
    try{return new URLSearchParams(window.location.search).get(name)||'';}catch(e){return '';}
  }
  var attributionKeys=['utm_source','utm_medium','utm_campaign','utm_term','utm_content','gclid','gbraid','wbraid'];
  function storeAttribution(){
    try{
      attributionKeys.forEach(function(k){var v=param(k);if(v)sessionStorage.setItem('wccm_'+k,v);});
      if(!sessionStorage.getItem('wccm_landing_page'))sessionStorage.setItem('wccm_landing_page',window.location.href);
      if(!sessionStorage.getItem('wccm_referrer'))sessionStorage.setItem('wccm_referrer',document.referrer||'direct');
    }catch(e){}
  }
  function attributionValue(name){
    var direct=param(name);
    if(direct)return direct;
    try{return sessionStorage.getItem('wccm_'+name)||'';}catch(e){return '';}
  }
  function ensureHidden(form,name,value){
    if(!value)return;
    var el=form.querySelector('input[name="'+name+'"]');
    if(!el){el=document.createElement('input');el.type='hidden';el.name=name;form.appendChild(el);}
    el.value=value;
  }
  function addAttribution(form){
    attributionKeys.forEach(function(k){ensureHidden(form,k,attributionValue(k));});
    var landing='';var ref='';
    try{landing=sessionStorage.getItem('wccm_landing_page')||window.location.href;ref=sessionStorage.getItem('wccm_referrer')||document.referrer||'direct';}catch(e){landing=window.location.href;ref=document.referrer||'direct';}
    ensureHidden(form,'landing_page',landing);
    ensureHidden(form,'conversion_page',window.location.href);
    ensureHidden(form,'source_path',window.location.pathname);
    ensureHidden(form,'referrer',ref);
  }
  storeAttribution();

  /* ------------------------------------------------------------------------
     Reliable delivery + partial-lead capture engine.
     Netlify only stores fields declared in a registered form's static HTML —
     the schema twins built by tools/install_wccm_ads_readiness.py and the
     static form in tools/install_early_845k_readiness.py — so every field
     referenced below (submission_id, the partial-lead fields) must also be
     declared there or Netlify silently drops it.
     Written in ES5 and feature-detected throughout: paid mobile traffic
     includes iPhone/Safari, and this must not throw on an older engine. */
  var PENDING_KEY='wccm_pending_leads';
  var SENT_KEY='wccm_sent_lead_ids';
  var PENDING_MAX_AGE_MS=7*24*60*60*1000;
  var PENDING_MAX_ATTEMPTS=6;
  var RETRY_DELAYS=[1500,4000];
  var SUBMIT_TIMEOUT_MS=12000;
  var INFLIGHT_BEACON_MS=3000;
  var activeSubmits={};
  var partialCapableEntries=[];
  var EXCLUDE_PARTIAL_NAMES={'mortgage-partner-inquiry':1,'sms-optin':1};

  function makeId(){
    return 'wccm-'+Date.now().toString(36)+'-'+Math.random().toString(36).slice(2,10)+Math.random().toString(36).slice(2,6);
  }
  function lsRead(key){try{return window.localStorage.getItem(key);}catch(e){return null;}}
  function lsWrite(key,value){try{window.localStorage.setItem(key,value);}catch(e){}}
  function readJsonList(key){
    try{
      var raw=window.localStorage.getItem(key);
      var list=raw?JSON.parse(raw):[];
      return (Object.prototype.toString.call(list)==='[object Array]')?list:[];
    }catch(e){return [];}
  }
  function readPending(){return readJsonList(PENDING_KEY);}
  function writePending(list){lsWrite(PENDING_KEY,JSON.stringify(list));}
  function hasFiredConversion(id){
    var list=readJsonList(SENT_KEY);
    for(var i=0;i<list.length;i++){if(list[i]===id)return true;}
    return false;
  }
  function markConversionFired(id){
    if(!id)return;
    var list=readJsonList(SENT_KEY);
    var found=false;
    for(var i=0;i<list.length;i++){if(list[i]===id){found=true;break;}}
    if(!found){
      list.push(id);
      if(list.length>60)list=list.slice(list.length-60);
      lsWrite(SENT_KEY,JSON.stringify(list));
    }
  }
  /* Manual application/x-www-form-urlencoded encoder. Deliberately avoids
     `new URLSearchParams(new FormData(form))` — Safari's support for building
     URLSearchParams from an iterable/FormData has been inconsistent, and a
     silently-empty body would look like a success (2xx) while carrying no
     lead data. This works the same on every engine back to ES5. */
  function formToObject(form){
    var obj={},els=form.elements;
    for(var i=0;i<els.length;i++){
      var el=els[i];
      if(!el.name||el.disabled)continue;
      var type=(el.type||'').toLowerCase();
      if(type==='submit'||type==='button'||type==='reset'||type==='file')continue;
      if((type==='checkbox'||type==='radio')&&!el.checked)continue;
      obj[el.name]=el.value==null?'':el.value;
    }
    return obj;
  }
  function encodePairs(obj){
    var parts=[];
    for(var k in obj){
      if(!Object.prototype.hasOwnProperty.call(obj,k))continue;
      parts.push(encodeURIComponent(k)+'='+encodeURIComponent(obj[k]==null?'':obj[k]));
    }
    return parts.join('&');
  }
  function ensureSubmissionId(form){
    var el=form.querySelector('input[name="submission_id"]');
    if(!el){el=document.createElement('input');el.type='hidden';el.name='submission_id';form.appendChild(el);}
    if(!el.value)el.value=makeId();
    return el.value;
  }
  /* AbortController shipped in Safari 12.1; still feature-detect so a very
     old engine degrades to "no client-side timeout" instead of throwing. */
  function withTimeout(ms){
    if(typeof window.AbortController==='function'){
      var ac=new AbortController();
      var timer=setTimeout(function(){try{ac.abort();}catch(e){}},ms);
      return {signal:ac.signal,cancel:function(){clearTimeout(timer);}};
    }
    return {signal:undefined,cancel:function(){}};
  }
  function persistPending(record){
    var list=readPending(),kept=[],i;
    for(i=0;i<list.length;i++){if(list[i]&&list[i].id!==record.id)kept.push(list[i]);}
    kept.push(record);
    writePending(kept);
  }
  function removePending(id){
    var list=readPending(),kept=[],i;
    for(i=0;i<list.length;i++){if(list[i]&&list[i].id!==id)kept.push(list[i]);}
    writePending(kept);
  }
  function statusEl(form){
    var el=form.querySelector('.form-status');
    if(!el){
      el=document.createElement('div');
      el.className='form-status';
      el.setAttribute('role','status');
      el.setAttribute('aria-live','polite');
      el.hidden=true;
      var anchor=form.querySelector('.form-error-summary')||form.querySelector('.form-ok');
      if(anchor&&anchor.parentNode)anchor.parentNode.insertBefore(el,anchor);
      else form.insertBefore(el,form.firstChild);
    }
    return el;
  }
  function setStatus(form,text){
    var el=statusEl(form);
    if(text){el.textContent=text;el.hidden=false;}else{el.hidden=true;el.textContent='';}
  }
  function fireConversionOnce(form,record,isResend){
    if(!record||!record.id)return;
    if(record.formName==='mortgage-partner-inquiry')return;
    if(hasFiredConversion(record.id))return;
    markConversionFired(record.id);
    if(form&&form.dataset)form.dataset.conversionFired='true';
    var detail={
      lead_event_id:record.id,
      form_name:record.formName||'lead_form',
      page_path:record.pagePath||window.location.pathname,
      program_interest:record.programInterest||'',
      utm_source:attributionValue('utm_source'),
      utm_campaign:attributionValue('utm_campaign'),
      gclid:attributionValue('gclid')
    };
    if(isResend)detail.delivery='resend';
    pushEvent('wccm_lead_submit',detail);
  }
  function beaconInflightSubmits(){
    var now=Date.now();
    for(var id in activeSubmits){
      if(!Object.prototype.hasOwnProperty.call(activeSubmits,id))continue;
      var entry=activeSubmits[id];
      if(entry.resolved)continue;
      if(now-entry.startedAt<INFLIGHT_BEACON_MS)continue;
      if(navigator.sendBeacon){
        try{navigator.sendBeacon('/',new Blob([entry.body],{type:'application/x-www-form-urlencoded'}));}catch(e){}
      }
    }
  }
  /* Retry engine shared by a live submit and a stored-lead resend. Up to three
     attempts total (~1.5s, then ~4s backoff), a ~12s timeout per attempt, and
     the pending record is written to storage before the first byte goes out
     so a killed tab or a failed run can still be resent later. */
  function attemptSubmit(record,isResend,cb){
    cb=cb||{};
    record.attempts=(record.attempts||0)+1;
    persistPending(record);
    var entry={startedAt:Date.now(),body:record.body,resolved:false};
    activeSubmits[record.id]=entry;
    var t=withTimeout(SUBMIT_TIMEOUT_MS);
    if(cb.onStatus)cb.onStatus(record.attempts>1?'Still sending — please keep this page open…':'Sending…');
    var opts={method:'POST',headers:{'Content-Type':'application/x-www-form-urlencoded'},body:record.body,keepalive:true};
    if(t.signal)opts.signal=t.signal;
    fetch('/',opts).then(function(r){
      t.cancel();
      entry.resolved=true;
      if(!r.ok){throw new Error('Submission was not accepted ('+r.status+')');}
      removePending(record.id);
      fireConversionOnce(null,record,isResend);
      if(cb.onSuccess)cb.onSuccess();
    }).catch(function(){
      t.cancel();
      entry.resolved=true;
      if(record.attempts<3){
        var delay=RETRY_DELAYS[record.attempts-1]||4000;
        if(cb.onStatus)cb.onStatus('Still sending — please keep this page open…');
        setTimeout(function(){attemptSubmit(record,isResend,cb);},delay);
      }else{
        persistPending(record);
        if(cb.onFail)cb.onFail();
      }
    });
  }
  /* Resend anything still pending: on load, when connectivity returns, when
     the tab becomes visible again, and on a bfcache (pageshow persisted)
     restore, which does not re-run this script. */
  function tryResendAll(){
    var list=readPending(),now=Date.now(),kept=[],toSend=[],i;
    for(i=0;i<list.length;i++){
      var r=list[i];
      if(!r||!r.id||!r.body)continue;
      if(now-(r.createdAt||0)>PENDING_MAX_AGE_MS)continue;
      if((r.attempts||0)>=PENDING_MAX_ATTEMPTS)continue;
      if(hasFiredConversion(r.id))continue;
      kept.push(r);
      if(!activeSubmits[r.id]||activeSubmits[r.id].resolved)toSend.push(r);
    }
    writePending(kept);
    toSend.forEach(function(r,idx){
      setTimeout(function(){attemptSubmit(r,true,{});},idx*300);
    });
  }

  function plausibleEmail(v){return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test((v||'').trim());}
  function plausiblePhone(v){return ((v||'').replace(/\D/g,'')).length>=10;}
  function stateContext(){return param('state').toUpperCase()==='FL'?'FL':'CA';}
  function labelTextFor(form,el){
    if(el.id){
      var labels=form.querySelectorAll('label[for]');
      for(var i=0;i<labels.length;i++){if(labels[i].htmlFor===el.id)return labels[i].textContent.replace(/\s+/g,' ').trim();}
    }
    var wrap=el.closest?el.closest('.field'):null;
    if(wrap){var l2=wrap.querySelector('label');if(l2)return l2.textContent.replace(/\s+/g,' ').trim();}
    return '';
  }
  /* Builds one partial-lead payload from the form's CURRENT field values.
     Read live at hide/pagehide time rather than from cached "did they type"
     flags — iOS autofill and some native pickers fill a field without firing
     an `input` event, so a listener-only approach misses those visitors. */
  function buildPartialPayload(form,reason){
    var emailEl=form.querySelector('input[type="email"]');
    var phoneEl=form.querySelector('input[type="tel"]');
    var emailVal=emailEl?emailEl.value.trim():'';
    var phoneVal=phoneEl?phoneEl.value.trim():'';
    if(!plausibleEmail(emailVal)&&!plausiblePhone(phoneVal))return null;
    var fullNameEl=form.querySelector('[name="full_name"],[name="name"]');
    var firstEl=form.querySelector('[name="first_name"],[name="fn"]');
    var lastEl=form.querySelector('[name="last_name"],[name="ln"]');
    var firstVal=firstEl?firstEl.value.trim():(fullNameEl?(fullNameEl.value.trim().split(/\s+/)[0]||''):'');
    var lastVal=lastEl?lastEl.value.trim():(fullNameEl?fullNameEl.value.trim().split(/\s+/).slice(1).join(' '):'');
    var nameVal=fullNameEl?fullNameEl.value.trim():(firstVal+' '+lastVal).replace(/\s+/g,' ').trim();
    var excluded=[emailEl,phoneEl,fullNameEl,firstEl,lastEl].filter(function(el){return !!el;});
    var programEl=form.querySelector('[name="program_interest"]');
    var skipNames={company:1,'form-name':1,submission_id:1,utm_source:1,utm_medium:1,utm_campaign:1,utm_term:1,
      utm_content:1,gclid:1,gbraid:1,wbraid:1,landing_page:1,conversion_page:1,source_path:1,referrer:1,program_interest:1};
    var detailParts=[];
    var visible=form.querySelectorAll('input:not([type="hidden"]):not(.hp),select,textarea');
    for(var i=0;i<visible.length;i++){
      var el=visible[i];
      if(excluded.indexOf(el)>=0)continue;
      if(el.name&&skipNames[el.name])continue;
      var v=(el.value||'').toString().trim();
      if(!v)continue;
      detailParts.push((labelTextFor(form,el)||el.name||el.id||'field')+': '+v);
    }
    var landing,ref;
    try{landing=sessionStorage.getItem('wccm_landing_page')||window.location.href;}catch(e){landing=window.location.href;}
    try{ref=sessionStorage.getItem('wccm_referrer')||document.referrer||'direct';}catch(e){ref=document.referrer||'direct';}
    return {
      'form-name':'partial-lead',
      company:'',
      source_form:form.getAttribute('name')||'',
      page_path:window.location.pathname,
      state_context:stateContext(),
      name:nameVal,
      first_name:firstVal,
      last_name:lastVal,
      email:emailVal,
      phone:phoneVal,
      program_interest:programEl?programEl.value:'',
      details:detailParts.join('; '),
      submission_id:ensureSubmissionId(form),
      partial_reason:reason||'',
      status:'PARTIAL - visitor did not submit',
      sms_consent:'not given - form not submitted',
      utm_source:attributionValue('utm_source'),
      utm_medium:attributionValue('utm_medium'),
      utm_campaign:attributionValue('utm_campaign'),
      utm_term:attributionValue('utm_term'),
      utm_content:attributionValue('utm_content'),
      gclid:attributionValue('gclid'),
      gbraid:attributionValue('gbraid'),
      wbraid:attributionValue('wbraid'),
      landing_page:landing,
      referrer:ref
    };
  }
  function sendEncoded(body){
    if(navigator.sendBeacon){
      var ok=false;
      try{ok=navigator.sendBeacon('/',new Blob([body],{type:'application/x-www-form-urlencoded'}));}catch(e){}
      if(ok)return;
    }
    try{fetch('/',{method:'POST',headers:{'Content-Type':'application/x-www-form-urlencoded'},body:body,keepalive:true}).catch(function(){});}catch(e){}
  }
  function maybeSendPartial(entry,reason){
    var form=entry.form;
    if(form.dataset.submitted==='true')return;
    // A real attempt is already in flight for this form; its own sendBeacon
    // fallback (see beaconInflightSubmits) already carries the full payload,
    // so skip the redundant partial-lead record while it is pending.
    if(form.dataset.submitting==='true')return;
    if(entry.count>=3)return;
    var payload=buildPartialPayload(form,reason);
    if(!payload)return;
    var sig=payload.email+'|'+payload.phone+'|'+payload.name+'|'+payload.details;
    if(sig===entry.lastSig)return;
    entry.count+=1;
    entry.lastSig=sig;
    sendEncoded(encodePairs(payload));
  }

  /* Shared "take me to the lead form" behavior for the mobile bar, program
     card taps, and every in-page CTA that scrolls to the form. iOS Safari
     only opens the keyboard for a focus() call made synchronously inside the
     tap handler, so focus happens first (with preventScroll) and the smooth
     scroll follows — not the other way around, and never inside a timeout. */
  function activateLeadForm(form){
    if(!form)return;
    var fields=form.querySelectorAll('input:not([type="hidden"]):not(.hp),select,textarea');
    var target=null;
    for(var i=0;i<fields.length;i++){
      if(fields[i].required&&!(fields[i].value||'').toString().trim()){target=fields[i];break;}
    }
    if(!target)target=form.querySelector('button[type="submit"]');
    if(target){
      try{target.focus({preventScroll:true});}catch(err){try{target.focus();}catch(e2){}}
    }
    var section=(form.closest&&form.closest('section'))||form;
    if(section.scrollIntoView)section.scrollIntoView({behavior:'smooth',block:'start'});
    form.classList.remove('wccm-pulse');
    void form.offsetWidth;
    form.classList.add('wccm-pulse');
    setTimeout(function(){form.classList.remove('wccm-pulse');},1300);
  }
  function markMobileBarDone(){
    var mab=document.querySelector('.mobile-action-bar .mab-cta');
    if(!mab||mab.classList.contains('mab-done'))return;
    mab.classList.add('mab-done');
    mab.setAttribute('aria-disabled','true');
    mab.textContent='Request sent ✓';
    mab.addEventListener('click',function(e){e.preventDefault();});
  }
  /* ---------------------------------------------------------------------- */

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

  /* Paid-search landing-page capture for the highest-priority California intent.
     Reuse the already-registered Netlify "apply" form so no new backend setup is
     required; program + page attribution distinguish these submissions. */
  function injectBankStatementLeadForm(){
    var path=(window.location.pathname||'').replace(/\.html$/,'').replace(/\/$/,'');
    if(path!='/bank-statement-loans')return;
    if(document.getElementById('bank-statement-review'))return;
    var faq=document.querySelector('section.bg-light');
    if(!faq)return;
    var section=document.createElement('section');
    section.id='bank-statement-review';
    section.className='bg-light';
    section.innerHTML='\
      <div class="wrap" style="max-width:920px">\
        <div class="section-head center">\
          <span class="eyebrow">Bank Statement Review</span>\
          <h2>See whether a bank-statement path fits your California scenario</h2>\
          <p class="lead">Share the basics. A licensed mortgage professional will review the scenario before discussing any program, pricing, or qualification.</p>\
        </div>\
        <form id="bank-statement-lead-form" class="form" data-ack data-validate name="bank-statement-lead" netlify netlify-honeypot="company" novalidate>\
          <input type="hidden" name="form-name" value="bank-statement-lead">\
          <input type="text" class="hp" tabindex="-1" autocomplete="off" aria-hidden="true" name="company">\
          <input type="hidden" name="program_interest" value="Bank Statement / Self-Employed">\
          <div class="form-error-summary" role="alert" aria-live="assertive" hidden></div>\
          <div class="form-ok" role="status" aria-live="polite" hidden>Thank you. A licensed mortgage professional will review your bank-statement scenario and follow up.</div>\
          <div class="form-grid">\
            <div class="field"><label for="bs-goal">Loan goal</label><select id="bs-goal" name="goal"><option>Buy a Home</option><option>Refinance</option><option>Investment Property</option></select></div>\
            <div class="field"><label for="bs-area">California city / county</label><input id="bs-area" name="property_area" autocomplete="address-level2" data-error-required="Enter a California city or county." required></div>\
            <div class="field"><label for="bs-loan">Estimated loan amount ($)</label><input id="bs-loan" type="number" min="0" step="1000" name="loan_amount"></div>\
            <div class="field"><label for="bs-statements">Statements available</label><select id="bs-statements" name="statements_available"><option>12 months</option><option>24 months</option><option>Personal statements</option><option>Business statements</option><option>Personal + business</option><option>Not sure yet</option></select></div>\
            <div class="field"><label for="bs-years">Years self-employed</label><select id="bs-years" name="self_employed_years"><option>Less than 1 year</option><option>1–2 years</option><option>2–5 years</option><option>5+ years</option></select></div>\
            <div class="field"><label for="bs-name">Full name</label><input id="bs-name" name="full_name" autocomplete="name" minlength="2" data-error-required="Enter your full name." required></div>\
            <div class="field"><label for="bs-email">Email</label><input id="bs-email" type="email" name="email" autocomplete="email" data-error-required="Enter your email address." required></div>\
            <div class="field"><label for="bs-phone">Phone</label><input id="bs-phone" type="tel" name="phone" autocomplete="tel" inputmode="tel" data-error-required="Enter your phone number." required></div>\
            <div class="field full"><label for="bs-notes">Anything important about the income or property?</label><textarea id="bs-notes" name="message" placeholder="For example: business type, approximate monthly deposits, purchase timing, or property type."></textarea></div>\
          </div>\
          <div style="margin-top:20px"><button class="btn btn-blue btn-lg" type="submit">Request Bank Statement Review</button></div>\
          <p class="form-note">This is not a loan application, approval, rate quote, or commitment to lend. Programs and eligibility are subject to borrower, property, documentation, lender, licensing, and underwriting review. West Coast Capital Mortgage Inc. · NMLS #2817729 · CA DRE Corporation License #02440065 · Equal Housing Opportunity.</p>\
        </form>\
      </div>';
    faq.parentNode.insertBefore(section,faq);

    /* Make the first high-intent CTA keep paid visitors on the relevant page. */
    var firstCta=document.querySelector('a.btn.btn-blue[href="apply.html"]');
    if(firstCta){
      firstCta.setAttribute('href','#bank-statement-review');
      firstCta.textContent='Request Bank Statement Review';
      firstCta.addEventListener('click',function(e){
        e.preventDefault();
        activateLeadForm(document.getElementById('bank-statement-lead-form'));
      });
    }
  }
  injectBankStatementLeadForm();

  /* Paid search points at program pages that had no capture form at all, so the
     only next step was an off-site application. Each entry below builds one
     on-page form. Field names must match the hidden schema twins that
     tools/install_wccm_ads_readiness.py writes into the static HTML, because
     Netlify stores only the fields of a registered form. */
  var CITY_FIELD={name:'property_area',label:'California city / county',required:'Enter a California city or county.',autocomplete:'address-level2'};
  var AMOUNT_FIELD={name:'loan_amount',label:'Estimated loan amount ($)',type:'number',min:'0',step:'1000'};
  var CONTACT_FIELDS=[
    {name:'full_name',label:'Full name',required:'Enter your full name.',autocomplete:'name',minlength:'2'},
    {name:'email',label:'Email',type:'email',required:'Enter your email address.',autocomplete:'email'},
    {name:'phone',label:'Phone',type:'tel',required:'Enter your phone number.',autocomplete:'tel',inputmode:'tel'}
  ];
  function notesField(placeholder){
    return {name:'message',label:'Anything else we should know?',textarea:true,full:true,placeholder:placeholder};
  }

  var PROGRAM_LEAD_FORMS={
    '/':{
      id:'mortgage-review',formName:'mortgage-lead',programInterest:'General mortgage inquiry',
      eyebrow:'Mortgage Review',heading:'Talk with a licensed California mortgage broker',
      lead:'Share the basics and a licensed mortgage professional will review your scenario before discussing any program, pricing, or qualification.',
      button:'Request a Mortgage Review',
      fields:[
        {name:'goal',label:'What do you need?',options:['Buy a home','Refinance','Cash-out refinance','Investment property','Not sure yet']},
        CITY_FIELD,AMOUNT_FIELD,
        {name:'timeline',label:'Timeline',options:['As soon as possible','1-3 months','3-6 months','Just researching']}
      ].concat(CONTACT_FIELDS,[notesField('For example: property type, employment, or what you are trying to solve.')])
    },
    '/jumbo-loans':{
      id:'jumbo-review',formName:'jumbo-lead',programInterest:'Jumbo',
      eyebrow:'Jumbo Review',heading:'See whether a jumbo loan fits your California purchase or refinance',
      lead:'Share the basics. A licensed mortgage professional will review the scenario before discussing any program, pricing, or qualification.',
      button:'Request a Jumbo Review',
      fields:[
        {name:'goal',label:'Loan goal',options:['Buy a home','Refinance','Cash-out refinance','Second home','Investment property']},
        CITY_FIELD,
        {name:'purchase_price',label:'Purchase price or property value ($)',type:'number',min:'0',step:'10000'},
        AMOUNT_FIELD,
        {name:'income_documentation',label:'How is income documented?',options:['W-2 / salaried','Self-employed, tax returns','Bank statements','Asset depletion','Not sure yet']}
      ].concat(CONTACT_FIELDS,[notesField('For example: property type, timing, or anything unusual about the income.')])
    },
    '/dscr-loans':{
      id:'dscr-review',formName:'dscr-lead',programInterest:'DSCR / Investor',
      eyebrow:'DSCR Review',heading:'See whether the rent supports a DSCR loan on your property',
      lead:'Share the basics. A licensed mortgage professional will review the scenario before discussing any program, pricing, or qualification.',
      button:'Request a DSCR Review',
      fields:[
        {name:'goal',label:'Loan goal',options:['Purchase','Refinance','Cash-out refinance','Portfolio / multiple properties']},
        CITY_FIELD,
        {name:'property_type',label:'Property type',options:['Single-family','Condo','2-4 units','5+ units','Short-term rental']},
        {name:'monthly_rent',label:'Actual or expected monthly rent ($)',type:'number',min:'0',step:'50'},
        AMOUNT_FIELD,
        {name:'vesting',label:'Title held in',options:['Personal name','LLC or entity','Not decided yet']}
      ].concat(CONTACT_FIELDS,[notesField('For example: current occupancy, rehab plans, or how many properties you already own.')])
    },
    '/self-employed-borrowers':{
      id:'self-employed-review',formName:'self-employed-lead',programInterest:'Self-employed',
      eyebrow:'Self-Employed Review',heading:'See which self-employed path fits your California scenario',
      lead:'Share the basics. A licensed mortgage professional will review the scenario before discussing any program, pricing, or qualification.',
      button:'Request a Self-Employed Review',
      fields:[
        {name:'goal',label:'Loan goal',options:['Buy a home','Refinance','Cash-out refinance','Investment property']},
        CITY_FIELD,AMOUNT_FIELD,
        {name:'income_documentation',label:'How would you document income?',options:['Bank statements','Profit and loss','1099s','Tax returns','Assets','Not sure yet']},
        {name:'self_employed_years',label:'Years self-employed',options:['Less than 1 year','1-2 years','2-5 years','5+ years']}
      ].concat(CONTACT_FIELDS,[notesField('For example: business type, approximate monthly deposits, or purchase timing.')])
    }
  };
  PROGRAM_LEAD_FORMS['/loans/jumbo/los-angeles-county']=PROGRAM_LEAD_FORMS['/jumbo-loans'];
  PROGRAM_LEAD_FORMS['/loans/dscr/los-angeles-metro']=PROGRAM_LEAD_FORMS['/dscr-loans'];

  /* Explicit Florida landing URLs keep the existing California paths intact. */
  var FLORIDA_LANDINGS={
    '/bank-statement-loans':'Florida Bank Statement Loans',
    '/self-employed-borrowers':'Florida Self-Employed Mortgages',
    '/dscr-loans':'Florida DSCR Loans',
    '/jumbo-loans':'Florida Jumbo Loans',
    '/florida-condo-financing':'Florida Condo Financing',
    '/foreign-national-loans':'Florida Foreign National Loans'
  };
  var floridaLanding=!!FLORIDA_LANDINGS[leadFormPath()] &&
    (param('state').toUpperCase()==='FL'||leadFormPath()==='/florida-condo-financing');
  if(floridaLanding){
    ['/florida-condo-financing','/foreign-national-loans'].forEach(function(path){
      var condo=path==='/florida-condo-financing';
      PROGRAM_LEAD_FORMS[path]=Object.assign({},PROGRAM_LEAD_FORMS['/'],{
        id:condo?'florida-condo-review':'foreign-national-review',
        programInterest:condo?'Florida / Condo':'Florida / Foreign National',
        eyebrow:condo?'Florida Condo Review':'Florida Foreign National Review',
        heading:condo?'Review the borrower and the Florida condo project':'Review your Florida property and international-buyer scenario',
        button:condo?'Request a Condo Review':'Request a Foreign National Review',
        fields:PROGRAM_LEAD_FORMS['/'].fields.slice(0,-1).concat([
          notesField(condo?'Property address, intended use, and any known HOA or project questions.':'Intended property use, country of residence, and available income documentation. Do not enter passport or account numbers.')
        ])
      });
    });
  }

  function buildLeadField(spec,idPrefix){
    var wrap=document.createElement('div');
    wrap.className=spec.full?'field full':'field';
    var id=idPrefix+'-'+spec.name.replace(/_/g,'-');
    var label=document.createElement('label');
    label.setAttribute('for',id);
    label.textContent=spec.label;
    var control;
    if(spec.options){
      control=document.createElement('select');
      spec.options.forEach(function(text){
        var option=document.createElement('option');
        option.textContent=text;
        control.appendChild(option);
      });
    }else if(spec.textarea){
      control=document.createElement('textarea');
      if(spec.placeholder)control.setAttribute('placeholder',spec.placeholder);
    }else{
      control=document.createElement('input');
      if(spec.type)control.setAttribute('type',spec.type);
      ['min','step','minlength','autocomplete','inputmode'].forEach(function(attr){
        if(spec[attr])control.setAttribute(attr,spec[attr]);
      });
    }
    control.id=id;
    control.setAttribute('name',spec.name);
    if(spec.required){
      control.setAttribute('required','');
      control.setAttribute('data-error-required',spec.required);
    }
    wrap.appendChild(label);
    wrap.appendChild(control);
    return wrap;
  }

  /* Pages resolve as both /dscr-loans and /dscr-loans.html, and the homepage as
     both / and /index.html, so normalise before matching a config. */
  function leadFormPath(){
    var path=(window.location.pathname||'/').replace(/\.html$/,'').replace(/\/index$/,'/');
    path=path.replace(/(.)\/$/,'$1');
    return path||'/';
  }

  function injectProgramLeadForm(){
    var path=leadFormPath();
    var config=PROGRAM_LEAD_FORMS[path];
    if(!config)return;
    if(document.getElementById(config.id))return;
    var band=document.querySelector('.cta-band');
    if(!band)return;

    var section=document.createElement('section');
    section.id=config.id;
    section.className='bg-light';
    var wrap=document.createElement('div');
    wrap.className='wrap';
    wrap.style.maxWidth='920px';
    var head=document.createElement('div');
    head.className='section-head center';
    head.innerHTML='<span class="eyebrow"></span><h2></h2><p class="lead"></p>';
    head.querySelector('.eyebrow').textContent=config.eyebrow;
    head.querySelector('h2').textContent=config.heading;
    head.querySelector('.lead').textContent=config.lead;

    var form=document.createElement('form');
    form.id=config.formName+'-form';
    form.className='form';
    form.setAttribute('data-ack','');
    form.setAttribute('data-validate','');
    form.setAttribute('name',config.formName);
    form.setAttribute('netlify','');
    form.setAttribute('netlify-honeypot','company');
    form.setAttribute('novalidate','');
    form.innerHTML='\
      <input type="hidden" name="form-name">\
      <input type="text" class="hp" tabindex="-1" autocomplete="off" aria-hidden="true" name="company">\
      <input type="hidden" name="program_interest">\
      <div class="form-error-summary" role="alert" aria-live="assertive" hidden></div>\
      <div class="form-ok" role="status" aria-live="polite" hidden>Thank you. A licensed mortgage professional will review your scenario and follow up.</div>\
      <div class="form-grid"></div>\
      <div style="margin-top:20px"><button class="btn btn-blue btn-lg" type="submit"></button></div>\
      <p class="form-note">This is not a loan application, approval, rate quote, or commitment to lend. Programs and eligibility are subject to borrower, property, documentation, lender, licensing, and underwriting review. West Coast Capital Mortgage Inc. — NMLS #2817729 — CA DRE Corporation License #02440065 — Equal Housing Opportunity.</p>';
    form.querySelector('[name="form-name"]').value=config.formName;
    form.querySelector('[name="program_interest"]').value=config.programInterest;
    form.querySelector('button[type="submit"]').textContent=config.button;
    var grid=form.querySelector('.form-grid');
    config.fields.forEach(function(spec){
      grid.appendChild(buildLeadField(spec,config.id));
    });

    wrap.appendChild(head);
    wrap.appendChild(form);
    section.appendChild(wrap);
    // Insert as a sibling of the CTA band's own top-level <section>, not
    // nested inside its wrap div. The homepage's compact-funnel layout hides
    // every direct-child <section> of body except a short exemption list
    // (see styles.css "body:has(.mortgage-compact-hero) > section:not(...)")
    // — nesting this section inside that band's section left it a descendant
    // of an element display:none hides, so it rendered at 0x0 and was
    // unreachable. #mortgage-review is exempted alongside the others.
    var bandSection=band.closest('section');
    var insertBeforeEl=(bandSection&&bandSection.parentNode)?bandSection:band;
    insertBeforeEl.parentNode.insertBefore(section,insertBeforeEl);

    /* Keep the first high-intent CTA on the page the visitor paid to land on. */
    var firstCta=document.querySelector('a.btn.btn-blue[href="apply.html"],a.btn.btn-blue[href="/apply"],a.btn.btn-blue[href="../../apply.html"]');
    if(firstCta){
      firstCta.setAttribute('href','#'+config.id);
      firstCta.textContent=config.button;
      firstCta.addEventListener('click',function(e){
        e.preventDefault();
        activateLeadForm(form);
      });
    }
  }
  injectProgramLeadForm();

  function adaptFloridaLeadPage(){
    if(!floridaLanding)return;
    var h1=document.querySelector('h1');
    if(h1)h1.textContent=FLORIDA_LANDINGS[leadFormPath()];
    document.title=FLORIDA_LANDINGS[leadFormPath()]+' | West Coast Capital Mortgage';
    document.querySelectorAll('.compare-wrap').forEach(function(wrap){wrap.style.overflowX='auto';});
    document.querySelectorAll('section .btn').forEach(function(button){
      button.style.whiteSpace='normal';
      button.style.maxWidth='100%';
    });
    var form=document.querySelector('form[data-ack]');
    var section=form&&form.closest('section');
    if(!section)return;
    var submit=form.querySelector('button[type="submit"]');
    submit.style.whiteSpace='normal';
    submit.style.maxWidth='100%';
    var heading=section.querySelector('h2');
    if(heading)heading.textContent=heading.textContent.replace(/California/g,'Florida');
    var area=form.querySelector('[name="property_area"]');
    if(area){
      var label=form.querySelector('label[for="'+area.id+'"]');
      if(label)label.textContent='Florida property city / county';
      area.setAttribute('data-error-required','Enter the Florida property city or county.');
    }
    var program=form.querySelector('[name="program_interest"]');
    if(program&&!/^Florida \/ /.test(program.value))program.value='Florida / '+program.value;
    document.querySelectorAll('h2').forEach(function(title){
      if(/by California|by California county|Same Financing Strategy in Washington and New York/.test(title.textContent)){
        var unrelated=title.closest('section');
        if(unrelated)unrelated.hidden=true;
      }
    });
    var hero=h1&&h1.closest('section');
    if(hero&&!hero.querySelector('a[href="#'+section.id+'"]')){
      var cta=document.createElement('a');
      cta.className='btn btn-blue btn-lg';
      cta.href='#'+section.id;
      cta.textContent=form.querySelector('button[type="submit"]').textContent;
      cta.style.marginTop='20px';
      cta.style.whiteSpace='normal';
      cta.style.maxWidth='100%';
      cta.addEventListener('click',function(e){e.preventDefault();activateLeadForm(form);});
      h1.parentNode.appendChild(cta);
    }
  }
  adaptFloridaLeadPage();

  /* On phones the sticky header hides the number and the CTA behind the
     hamburger, so scrolling visitors lose both. Give them a persistent bar. */
  function injectMobileActionBar(){
    if(document.querySelector('.mobile-action-bar'))return;
    var path=leadFormPath();
    if(path==='/sms-optin'||path==='/sms-terms'||path==='/rate-tools'||path==='/preview')return;

    var target=document.querySelector('form[data-ack]');
    var section=target?target.closest('section'):null;
    var bar=document.createElement('div');
    bar.className='mobile-action-bar';

    var call=document.createElement('a');
    call.className='mab-call';
    call.setAttribute('href','tel:3106541577');
    call.setAttribute('data-mab','call');
    call.textContent='Call 310-654-1577';

    var cta=document.createElement('a');
    cta.className='mab-cta';
    if(section&&section.id){
      cta.setAttribute('href','#'+section.id);
      cta.textContent='Request a Review';
      cta.addEventListener('click',function(e){
        e.preventDefault();
        activateLeadForm(target);
      });
    }else{
      cta.setAttribute('href',document.querySelector('a[href$="apply.html"]')?
        (document.querySelector('a[href$="apply.html"]').getAttribute('href')):'/apply');
      cta.textContent='Get Started';
    }

    bar.appendChild(call);
    bar.appendChild(cta);
    document.body.appendChild(bar);
    document.body.classList.add('has-mobile-action-bar');
  }
  injectMobileActionBar();

  /* iOS: the on-screen keyboard covers a fixed bottom bar (and often the
     submit button behind it), so hide the bar while a lead-form field has
     focus. A short delay on blur means tapping from a field to the submit
     button does not flash the bar back on mid-tap. */
  (function(){
    var bar=document.querySelector('.mobile-action-bar');
    if(!bar)return;
    var hideTimer=null;
    document.addEventListener('focusin',function(e){
      var t=e.target;
      if(!t||!t.closest||!t.closest('form[data-ack]'))return;
      if(hideTimer){clearTimeout(hideTimer);hideTimer=null;}
      bar.classList.add('mab-hide');
    });
    document.addEventListener('focusout',function(e){
      var t=e.target;
      if(!t||!t.closest||!t.closest('form[data-ack]'))return;
      if(hideTimer)clearTimeout(hideTimer);
      hideTimer=setTimeout(function(){bar.classList.remove('mab-hide');hideTimer=null;},250);
    });
  })();

  /* Clarity recordings showed mobile visitors tapping benefit/comparison
     cards as if they were buttons. Make the plain (non-interactive) ones
     behave like a link to the on-page lead form. */
  function enableLeadCards(){
    var leadForm=document.querySelector('form[data-ack]');
    if(!leadForm)return;
    document.querySelectorAll('.grid .card').forEach(function(card){
      if(card.tagName==='A'||card.tagName==='BUTTON')return;
      if(card.querySelector('a,button,input,details'))return;
      if(card.hasAttribute('data-lead-link'))return;
      card.setAttribute('data-lead-link','');
      card.setAttribute('role','link');
      card.setAttribute('tabindex','0');
      card.style.cursor='pointer';
      var cta=document.createElement('span');
      cta.className='more';
      cta.textContent='Check your scenario →';
      card.appendChild(cta);
      function go(){activateLeadForm(leadForm);}
      card.addEventListener('click',function(e){
        if(e.target&&e.target.closest&&e.target.closest('a,button'))return;
        go();
      });
      card.addEventListener('keydown',function(e){
        var key=e.key||'';
        if(key==='Enter'||key===' '||key==='Spacebar'||e.keyCode===13||e.keyCode===32){
          e.preventDefault();
          go();
        }
      });
    });
  }
  enableLeadCards();

  function fieldErrorMessage(field){
    var value=(field.value||'').trim();
    if(field.required&&!value)return field.getAttribute('data-error-required')||'This field is required.';
    if(!value)return '';
    if(field.type==='email'&&!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value))return 'Enter a valid email address.';
    if(field.type==='tel'){
      var digits=value.replace(/\D/g,'');
      if(digits.length<10||digits.length>15)return 'Enter a valid phone number with 10 to 15 digits.';
    }
    if(field.minLength>0&&value.length<field.minLength)return 'Enter at least '+field.minLength+' characters.';
    if(field.type==='number'&&!field.checkValidity())return 'Enter a valid amount.';
    return '';
  }
  function fieldErrorElement(field){
    var id=(field.id||field.name||'field')+'-error';
    var error=document.getElementById(id);
    if(!error){
      error=document.createElement('p');
      error.id=id;
      error.className='field-error';
      error.setAttribute('role','alert');
      error.hidden=true;
      (field.closest('.field')||field.parentNode).appendChild(error);
    }
    if(!field.getAttribute('aria-describedby'))field.setAttribute('aria-describedby',id);
    return error;
  }
  function showFieldError(field,message){
    var error=fieldErrorElement(field);
    error.textContent=message;
    error.hidden=!message;
    if(message)field.setAttribute('aria-invalid','true');
    else field.removeAttribute('aria-invalid');
  }
  function validateField(field){
    var message=fieldErrorMessage(field);
    showFieldError(field,message);
    return !message;
  }
  function validateForm(form){
    var firstInvalid=null;
    form.querySelectorAll('input:not([type="hidden"]):not(.hp),select,textarea').forEach(function(field){
      if(!validateField(field)&&!firstInvalid)firstInvalid=field;
    });
    if(firstInvalid){
      firstInvalid.focus();
      firstInvalid.scrollIntoView({behavior:'smooth',block:'center'});
      return false;
    }
    return true;
  }

  /* Contact / apply forms — Netlify submission + attribution */
  document.querySelectorAll('form[data-ack]').forEach(function(f){
    addAttribution(f);
    ensureSubmissionId(f);
    // Every handled form must validate, including legacy forms with novalidate.
    f.setAttribute('data-validate','');
    if(f.hasAttribute('data-validate')){
      f.querySelectorAll('input:not([type="hidden"]):not(.hp),select,textarea').forEach(function(field){
        fieldErrorElement(field);
        field.addEventListener('blur',function(){validateField(field);});
        field.addEventListener('input',function(){if(field.getAttribute('aria-invalid')==='true')validateField(field);});
        field.addEventListener('change',function(){if(field.getAttribute('aria-invalid')==='true')validateField(field);});
      });
    }

    var formName=f.getAttribute('name')||'';
    if(!EXCLUDE_PARTIAL_NAMES[formName]){
      partialCapableEntries.push({form:f,count:0,lastSig:''});
    }

    f.addEventListener('submit',function(e){
      e.preventDefault();
      if(f.hasAttribute('data-validate')&&!validateForm(f))return;
      if(f.dataset.submitting==='true'||f.dataset.submitted==='true')return;
      f.dataset.submitting='true';
      addAttribution(f);
      var submissionId=ensureSubmissionId(f);
      var ok=f.querySelector('.form-ok');
      var submitError=f.querySelector('.form-error-summary');
      var btn=f.querySelector('button[type="submit"]');
      if(submitError){submitError.hidden=true;submitError.textContent='';}
      if(btn)btn.disabled=true;

      var record={
        id:submissionId,
        formName:formName,
        pagePath:window.location.pathname,
        programInterest:(f.querySelector('[name="program_interest"]')||{}).value||'',
        body:encodePairs(formToObject(f)),
        createdAt:Date.now(),
        attempts:0
      };

      attemptSubmit(record,false,{
        onStatus:function(text){setStatus(f,text);},
        onSuccess:function(){
          f.dataset.submitting='false';
          f.dataset.submitted='true';
          setStatus(f,'');
          if(ok)ok.hidden=false;
          f.querySelectorAll('input,select,textarea,button').forEach(function(el){el.disabled=true;});
          if(ok)ok.scrollIntoView({behavior:'smooth',block:'center'});
          if(f===document.querySelector('form[data-ack]'))markMobileBarDone();
        },
        onFail:function(){
          f.dataset.submitting='false';
          if(btn)btn.disabled=false;
          setStatus(f,'');
          if(submitError){
            submitError.textContent='Your request was not sent. Please try again or call us at 310-654-1577.';
            submitError.hidden=false;
            submitError.scrollIntoView({behavior:'smooth',block:'center'});
          }else{
            alert('Your request was not sent. Please try again or call us at 310-654-1577.');
          }
        }
      });
    });
  });

  /* Resend / partial-capture triggers. `pagehide` and `visibilitychange` are
     both wired because neither fires reliably alone across iOS Safari, tab
     close, and app-switch; `pageshow` with `persisted` catches a bfcache
     restore, which resumes the page without re-running this script. */
  document.addEventListener('visibilitychange',function(){
    if(document.visibilityState==='hidden'||document.hidden){
      beaconInflightSubmits();
      partialCapableEntries.forEach(function(entry){maybeSendPartial(entry,'visibilitychange');});
    }else{
      tryResendAll();
    }
  });
  window.addEventListener('pagehide',function(){
    beaconInflightSubmits();
    partialCapableEntries.forEach(function(entry){maybeSendPartial(entry,'pagehide');});
  });
  window.addEventListener('pageshow',function(e){
    if(e.persisted)tryResendAll();
  });
  window.addEventListener('online',tryResendAll);
  try{tryResendAll();}catch(e){}

  /* High-intent click events for future Google Ads / GTM conversion mapping. */
  document.addEventListener('click',function(e){
    var a=e.target.closest&&e.target.closest('a');
    if(!a)return;
    var href=a.getAttribute('href')||'';
    if(href.indexOf('tel:')===0){
      pushEvent('wccm_phone_click',{page_path:window.location.pathname,phone_number:href.replace('tel:','')});
    }
    if(/my1003app\.com/i.test(href)){
      pushEvent('wccm_application_start',{page_path:window.location.pathname,destination:href});
    }
  });

  /* Mortgage payment calculator */
  function money(n){return '$'+(isFinite(n)?Math.round(n):0).toLocaleString('en-US');}
  function val(id){var el=document.getElementById(id);if(!el)return 0;return parseFloat((el.value||'').toString().replace(/[^0-9.\-]/g,''))||0;}
  function calc(){
    var price=val('c-price'),dpPct=val('c-down'),rate=val('c-rate'),term=val('c-term');
    var taxYr=val('c-tax'),insYr=val('c-ins'),hoa=val('c-hoa');
    var hint=document.getElementById('c-out-hint');
    if(!(price>0&&rate>0&&term>0)){
      set('c-out-total','');
      if(hint)hint.style.display='';
      ['c-out-pi','c-out-tax','c-out-ins','c-out-hoa','c-out-loan'].forEach(function(id){set(id,'—');});
      return;
    }
    if(hint)hint.style.display='none';
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

  /* Sample rate boards (homepage snapshot + Today's Rates page) — read assets/rates.json */
  document.querySelectorAll('.rate-board[data-src]').forEach(function(rb){
    var lim=parseInt(rb.getAttribute('data-limit')||'0',10);
    var more=rb.getAttribute('data-more');
    fetch(rb.getAttribute('data-src'),{cache:'no-store'}).then(function(r){return r.json();}).then(function(d){
      if(!d||!d.products||!d.products.length){throw 0;}
      var list=(lim>0)?d.products.slice(0,lim):d.products;
      var rows=list.map(function(p){
        var rate=(typeof p.rate==='number')?(p.rate.toFixed(3).replace(/0+$/,'').replace(/\.$/,'')+'%'):p.rate;
        return '<div class="rate-row"><span class="rate-name">'+p.name+'</span><span class="rate-val">'+rate+'</span></div>';
      }).join('');
      var html='<div class="rate-table">'+rows+'</div>';
      if(d.effective) html+='<p class="rate-effective">Effective '+d.effective+'</p>';
      if(more) html+='<p style="margin-top:10px"><a href="'+more+'" style="color:var(--blue);font-weight:600">See all rates →</a></p>';
      rb.innerHTML=html;
    }).catch(function(){
      rb.innerHTML='<p class="muted">Current sample rates are updated regularly. <a href="contact.html" style="color:var(--blue);font-weight:600">Request today’s rate quote →</a></p>';
    });
  });

  /* Year stamp */
  document.querySelectorAll('.year').forEach(function(el){el.textContent=new Date().getFullYear();});
})();
