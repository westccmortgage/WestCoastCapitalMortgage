/* West Coast Capital Mortgage — site scripts */
(function(){
  "use strict";

  /* ---------- i18n helper ---------- */
  function L(key){return (window.I18N&&window.I18N.t)?window.I18N.t(key):'';}

  /* ---------- Mobile nav ---------- */
  var burger=document.getElementById('burger');
  var menu=document.getElementById('menu');
  if(burger&&menu){burger.addEventListener('click',function(){menu.classList.toggle('open');});}

  /* ---------- Scroll reveal ---------- */
  var io=new IntersectionObserver(function(es){
    es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target);}});
  },{threshold:.12});
  document.querySelectorAll('.fade').forEach(function(el){io.observe(el);});

  /* ---------- Number helpers ---------- */
  function money(n){return '$'+Math.round(n).toLocaleString('en-US');}
  function money2(n){return '$'+n.toLocaleString('en-US',{minimumFractionDigits:2,maximumFractionDigits:2});}
  function num(id){var el=document.getElementById(id);if(!el)return 0;return parseFloat((el.value||'').toString().replace(/[^0-9.\-]/g,''))||0;}
  function pmt(principal,annualRate,years){
    var r=annualRate/100/12, n=years*12;
    if(r===0)return principal/n;
    return principal*r/(1-Math.pow(1+r,-n));
  }

  /* ---------- Calculators ---------- */
  // Tab switching
  document.querySelectorAll('.calc-tab').forEach(function(tab){
    tab.addEventListener('click',function(){
      var target=tab.getAttribute('data-calc');
      document.querySelectorAll('.calc-tab').forEach(function(t){t.classList.remove('active');});
      tab.classList.add('active');
      document.querySelectorAll('.calc-panel').forEach(function(p){p.classList.add('hide');});
      var panel=document.getElementById('panel-'+target);
      if(panel)panel.classList.remove('hide');
    });
  });

  // Purchase / payment calculator
  function calcPurchase(){
    var price=num('p-price'), dpPct=num('p-down'), rate=num('p-rate'), term=num('p-term');
    var taxPct=num('p-tax'), insYr=num('p-ins'), hoa=num('p-hoa');
    var down=price*dpPct/100, loan=price-down;
    var pi=pmt(loan,rate,term);
    var tax=price*(taxPct/100)/12, ins=insYr/12;
    var pmi=(dpPct<20)?(loan*0.005)/12:0;
    var total=pi+tax+ins+hoa+pmi;
    set('p-out-total',money2(total));
    set('p-out-pi',money2(pi));
    set('p-out-tax',money2(tax));
    set('p-out-ins',money2(ins+pmi));
    set('p-out-loan',money(loan));
    set('p-out-down',money(down));
  }
  // Refinance
  function calcRefi(){
    var bal=num('r-balance'), oldR=num('r-oldrate'), newR=num('r-newrate'), term=num('r-term'), costs=num('r-costs');
    var oldP=pmt(bal,oldR,term), newP=pmt(bal,newR,term);
    var save=oldP-newP;
    var months=save>0?Math.ceil(costs/save):0;
    set('r-out-new',money2(newP));
    set('r-out-save',money2(Math.max(save,0)));
    set('r-out-break',months>0?months+(L('moSuffix')||' mo'):'—');
    set('r-out-year',money(Math.max(save,0)*12));
  }
  // Affordability
  function calcAfford(){
    var income=num('a-income'), debts=num('a-debts'), dp=num('a-down'), rate=num('a-rate'), term=num('a-term');
    var dtiMax=0.43;
    var maxPmt=(income/12)*dtiMax-debts;
    if(maxPmt<0)maxPmt=0;
    // assume ~25% of payment is taxes/ins
    var piBudget=maxPmt*0.78;
    var r=rate/100/12, n=term*12;
    var loan=r>0?piBudget*(1-Math.pow(1+r,-n))/r:piBudget*n;
    var price=loan+dp;
    set('a-out-price',money(price));
    set('a-out-pmt',money2(maxPmt));
    set('a-out-loan',money(loan));
  }
  // Rent vs Buy
  function calcRvb(){
    var rent=num('v-rent'), price=num('v-price'), dpPct=num('v-down'), rate=num('v-rate'), years=num('v-years');
    var appr=num('v-appr');
    var down=price*dpPct/100, loan=price-down;
    var pi=pmt(loan,rate,30);
    var monthlyOwn=pi+price*0.0125/12+price*0.004/12; // tax+ins+maint approx
    var rentTotal=0, rr=rent;
    for(var i=0;i<years;i++){rentTotal+=rr*12;rr*=1.03;}
    var ownTotal=down+monthlyOwn*12*years;
    var futureVal=price*Math.pow(1+appr/100,years);
    var equity=futureVal-loan*0.85; // rough remaining balance
    var netOwn=ownTotal-equity;
    set('v-out-rent',money(rentTotal));
    set('v-out-own',money(Math.max(netOwn,0)));
    set('v-out-verdict',netOwn<rentTotal?(L('buyWins')||'Buying wins'):(L('rentWins')||'Renting wins'));
    set('v-out-equity',money(Math.max(equity,0)));
  }
  function set(id,val){var el=document.getElementById(id);if(el)el.textContent=val;}

  function bindCalc(ids,fn){
    ids.forEach(function(id){var el=document.getElementById(id);if(el){el.addEventListener('input',fn);el.addEventListener('change',fn);}});
  }
  if(document.getElementById('p-price')){bindCalc(['p-price','p-down','p-rate','p-term','p-tax','p-ins','p-hoa'],calcPurchase);calcPurchase();}
  if(document.getElementById('r-balance')){bindCalc(['r-balance','r-oldrate','r-newrate','r-term','r-costs'],calcRefi);calcRefi();}
  if(document.getElementById('a-income')){bindCalc(['a-income','a-debts','a-down','a-rate','a-term'],calcAfford);calcAfford();}
  if(document.getElementById('v-rent')){bindCalc(['v-rent','v-price','v-down','v-rate','v-years','v-appr'],calcRvb);calcRvb();}

  /* ---------- Apply wizard ---------- */
  var wiz=document.getElementById('wizard');
  if(wiz){
    var steps=wiz.querySelectorAll('.wiz-step');
    var bars=wiz.querySelectorAll('.wb');
    var cur=0;
    function show(i){
      steps.forEach(function(s,idx){s.classList.toggle('active',idx===i);});
      bars.forEach(function(b,idx){b.classList.toggle('active',idx===i);b.classList.toggle('done',idx<i);});
      document.getElementById('wiz-back').style.visibility=i===0?'hidden':'visible';
      var next=document.getElementById('wiz-next');
      next.textContent=(i===steps.length-2)?(L('wizSubmit')||'Submit application'):(L('wizContinue')||'Continue');
      next.classList.toggle('hide',i===steps.length-1);
      document.getElementById('wiz-back').classList.toggle('hide',i===steps.length-1);
      cur=i;
      wiz.scrollIntoView({behavior:'smooth',block:'start'});
    }
    wiz.querySelectorAll('.choice').forEach(function(c){
      c.addEventListener('click',function(){
        var group=c.getAttribute('data-group');
        wiz.querySelectorAll('.choice[data-group="'+group+'"]').forEach(function(x){x.classList.remove('sel');});
        c.classList.add('sel');
      });
    });
    document.getElementById('wiz-next').addEventListener('click',function(){
      if(cur<steps.length-2){show(cur+1);}
      else{show(steps.length-1);} // success
    });
    document.getElementById('wiz-back').addEventListener('click',function(){if(cur>0)show(cur-1);});
    show(0);
    // Refresh the dynamic Continue/Submit label when language changes.
    if(window.I18N&&window.I18N.onChange)window.I18N.onChange(function(){
      var next=document.getElementById('wiz-next');
      if(next)next.textContent=(cur===steps.length-2)?(L('wizSubmit')||'Submit application'):(L('wizContinue')||'Continue');
    });
  }

  /* ---------- Contact / apply mailto fallback ---------- */
  document.querySelectorAll('form[data-mailto]').forEach(function(f){
    f.addEventListener('submit',function(e){
      e.preventDefault();
      var ok=f.querySelector('.form-ok');
      if(ok)ok.classList.remove('hide');
      f.querySelectorAll('input,textarea,select,button').forEach(function(el){el.disabled=true;});
    });
  });

  /* ---------- AI chat ---------- */
  var fab=document.getElementById('chat-fab'),panel=document.getElementById('chat-panel');
  if(fab&&panel){
    var body=document.getElementById('chat-body');
    var input=document.getElementById('chat-text');
    function add(text,who){
      var d=document.createElement('div');d.className='msg '+who;d.textContent=text;body.appendChild(d);body.scrollTop=body.scrollHeight;
    }
    // Map a user message to a reply key; the localized text comes from i18n.
    function replyKey(q){
      q=q.toLowerCase();
      if(/rate|interest|tasa|ставк/.test(q))return 'rates';
      else if(/fha/.test(q))return 'fha';
      else if(/va\b|veteran|ветеран/.test(q))return 'va';
      else if(/jumbo|джамбо/.test(q))return 'jumbo';
      else if(/down ?payment|inicial|взнос/.test(q))return 'down';
      else if(/refinanc|refinanci|рефинанс/.test(q))return 'refi';
      else if(/credit|score|crédito|кредит|рейтинг/.test(q))return 'credit';
      else if(/pre.?qual|pre.?approv|qualify|start|apply|preaprob|предодобр|заявку/.test(q))return 'prequal';
      else if(/contact|call|phone|talk|human|agent|officer|llam|teléfono|звон|телефон/.test(q))return 'contact';
      else if(/hello|hi\b|hey|hola|привет|здрав/.test(q))return 'hello';
      else if(/usda/.test(q))return 'usda';
      else if(/reverse|inversa|обратн/.test(q))return 'reverse';
      return 'botDefault';
    }
    function t(key){return (window.I18N&&window.I18N.t)?window.I18N.t(key):'';}
    function botReply(text,key){
      var a=t(key||replyKey(text));
      setTimeout(function(){add(a,'bot');},500);
    }
    function send(text,key){if(!text.trim())return;add(text,'user');input.value='';botReply(text,key);}
    fab.addEventListener('click',function(){
      panel.classList.toggle('open');
      if(panel.classList.contains('open')&&!body.dataset.init){
        body.dataset.init='1';
        add(t('chatGreeting'),'bot');
      }
    });
    document.getElementById('chat-close').addEventListener('click',function(){panel.classList.remove('open');});
    document.getElementById('chat-send').addEventListener('click',function(){send(input.value);});
    input.addEventListener('keydown',function(e){if(e.key==='Enter')send(input.value);});
    document.querySelectorAll('.chat-quick button').forEach(function(b){
      b.addEventListener('click',function(){send(b.textContent,b.getAttribute('data-reply'));});
    });
  }

  /* ---------- Year ---------- */
  document.querySelectorAll('.year').forEach(function(el){el.textContent=new Date().getFullYear();});

  /* ---------- Recompute calculator verdicts/units when language changes ---------- */
  if(window.I18N&&window.I18N.onChange)window.I18N.onChange(function(){
    if(document.getElementById('p-price'))calcPurchase();
    if(document.getElementById('r-balance'))calcRefi();
    if(document.getElementById('a-income'))calcAfford();
    if(document.getElementById('v-rent'))calcRvb();
  });
})();
