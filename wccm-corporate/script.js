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
        document.getElementById('bank-statement-review').scrollIntoView({behavior:'smooth',block:'start'});
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
    band.parentNode.insertBefore(section,band);

    /* Keep the first high-intent CTA on the page the visitor paid to land on. */
    var firstCta=document.querySelector('a.btn.btn-blue[href="apply.html"],a.btn.btn-blue[href="/apply"],a.btn.btn-blue[href="../../apply.html"]');
    if(firstCta){
      firstCta.setAttribute('href','#'+config.id);
      firstCta.textContent=config.button;
      firstCta.addEventListener('click',function(e){
        e.preventDefault();
        section.scrollIntoView({behavior:'smooth',block:'start'});
      });
    }
  }
  injectProgramLeadForm();

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
        section.scrollIntoView({behavior:'smooth',block:'start'});
        var first=section.querySelector('input:not([type="hidden"]):not(.hp),select,textarea');
        if(first)setTimeout(function(){try{first.focus({preventScroll:true});}catch(err){first.focus();}},450);
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
    f.addEventListener('submit',function(e){
      e.preventDefault();
      if(f.hasAttribute('data-validate')&&!validateForm(f))return;
      if(f.dataset.submitting==='true'||f.dataset.submitted==='true')return;
      f.dataset.submitting='true';
      addAttribution(f);
      var ok=f.querySelector('.form-ok');
      var submitError=f.querySelector('.form-error-summary');
      var btn=f.querySelector('button[type="submit"]');
      var data=new FormData(f);
      if(submitError){submitError.hidden=true;submitError.textContent='';}
      if(btn)btn.disabled=true;
      fetch('/',{method:'POST',headers:{'Content-Type':'application/x-www-form-urlencoded'},body:new URLSearchParams(data).toString()})
        .then(function(r){
          if(!r.ok)throw new Error('Submission was not accepted ('+r.status+')');
          if(f.dataset.submitted==='true')return;
          f.dataset.submitted='true';
          f.dataset.submitting='false';
          if(f.dataset.conversionFired!=='true'){
            f.dataset.conversionFired='true';
            var eventId='wccm-'+Date.now()+'-'+Math.random().toString(36).slice(2,10);
            f.dataset.leadEventId=eventId;
            pushEvent('wccm_lead_submit',{
              lead_event_id:eventId,
              form_name:f.getAttribute('name')||'lead_form',
              page_path:window.location.pathname,
              program_interest:(f.querySelector('[name="program_interest"]')||{}).value||'',
              utm_source:attributionValue('utm_source'),
              utm_campaign:attributionValue('utm_campaign'),
              gclid:attributionValue('gclid')
            });
          }
          if(ok)ok.hidden=false;
          f.querySelectorAll('input,select,textarea,button').forEach(function(el){el.disabled=true;});
          if(ok)ok.scrollIntoView({behavior:'smooth',block:'center'});
        })
        .catch(function(){
          f.dataset.submitting='false';
          if(btn)btn.disabled=false;
          if(submitError){
            submitError.textContent='Your request was not sent. Please try again or call us at 310-654-1577.';
            submitError.hidden=false;
            submitError.scrollIntoView({behavior:'smooth',block:'center'});
          }else{
            alert('Your request was not sent. Please try again or call us at 310-654-1577.');
          }
        });
    });
  });

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
