/* West Coast Capital Mortgage — site scripts */
(function(){
  "use strict";

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
    set('r-out-break',months>0?months+' mo':'—');
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
    set('v-out-verdict',netOwn<rentTotal?'Buying wins':'Renting wins');
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
      next.textContent=(i===steps.length-2)?'Submit application':'Continue';
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
    function botReply(q){
      q=q.toLowerCase();
      var a;
      if(/rate|interest/.test(q))a="Today's sample rates: 30-yr fixed ~6.49%, 15-yr ~5.74%, FHA ~6.13%. Rates change daily and depend on your credit, down payment, and loan type. Want a personalized quote? I can have a loan officer reach out — just share your name and phone, or call (310) 654-1577.";
      else if(/fha/.test(q))a="FHA loans are great for first-time buyers — as little as 3.5% down and flexible credit requirements. They do carry mortgage insurance. Want me to start a quick pre-qualification?";
      else if(/va\b|veteran/.test(q))a="VA loans offer $0 down for eligible veterans and active-duty service members, with no PMI. You'll need a Certificate of Eligibility. Shall I connect you with our VA specialist?";
      else if(/jumbo/.test(q))a="Jumbo loans finance amounts above the conforming limit — ideal for higher-priced LA properties. They typically need stronger credit and reserves. I can outline what you'd qualify for.";
      else if(/down ?payment/.test(q))a="Down payments range from 0% (VA/USDA) to 3.5% (FHA) to 3–20% (conventional). Less than 20% usually adds mortgage insurance. Tell me the price range and I'll estimate it.";
      else if(/refinanc/.test(q))a="Refinancing can lower your rate, shorten your term, or tap equity. The break-even is when your monthly savings cover closing costs. Try our refinance calculator, or I can run the numbers with you.";
      else if(/credit|score/.test(q))a="Minimums vary: FHA from ~580, conventional ~620, jumbo ~700+. Even with lower scores there are options. Want me to flag this for a loan officer review?";
      else if(/pre.?qual|pre.?approv|qualify|start|apply/.test(q))a="Great — getting pre-approved takes about 10 minutes. Head to our Apply page, or share your name, phone, and the loan type you're after and I'll pass it to our team.";
      else if(/contact|call|phone|talk|human|agent|officer/.test(q))a="You can reach West Coast Capital Mortgage at (310) 654-1577, or leave your name and number here and a licensed loan officer will call you back shortly.";
      else if(/hello|hi\b|hey/.test(q))a="Hi! I'm the West Coast Capital Mortgage assistant. I can help with rates, loan programs (FHA, VA, USDA, Jumbo, Conventional), down payments, and getting pre-approved. What are you looking into?";
      else if(/usda/.test(q))a="USDA loans offer $0 down for eligible rural and some suburban areas, with low mortgage insurance. Eligibility depends on location and income. Want me to check if your area qualifies?";
      else if(/reverse/.test(q))a="Reverse mortgages let homeowners 62+ convert equity into cash without monthly payments. They're worth discussing carefully — I can connect you with our specialist.";
      else a="That's a great question. A licensed loan officer can give you the most accurate answer. Call (310) 654-1577, or share your name and phone and we'll reach out. Meanwhile, you can also start an application or try our calculators.";
      setTimeout(function(){add(a,'bot');},500);
    }
    function send(text){if(!text.trim())return;add(text,'user');input.value='';botReply(text);}
    fab.addEventListener('click',function(){
      panel.classList.toggle('open');
      if(panel.classList.contains('open')&&!body.dataset.init){
        body.dataset.init='1';
        add("👋 Hi! I'm your West Coast Capital Mortgage assistant. Ask me about rates, loan programs, or getting pre-approved.",'bot');
      }
    });
    document.getElementById('chat-close').addEventListener('click',function(){panel.classList.remove('open');});
    document.getElementById('chat-send').addEventListener('click',function(){send(input.value);});
    input.addEventListener('keydown',function(e){if(e.key==='Enter')send(input.value);});
    document.querySelectorAll('.chat-quick button').forEach(function(b){
      b.addEventListener('click',function(){send(b.textContent);});
    });
  }

  /* ---------- Founder photo: auto-detect extension ---------- */
  var founders=document.querySelectorAll('.js-founder');
  if(founders.length){
    var cands=['founder.jpg','founder.jpeg','founder.png','founder.webp','founder.JPG','founder.PNG'];
    (function tryNext(i){
      if(i>=cands.length)return;
      var im=new Image();
      im.onload=function(){founders.forEach(function(el){el.style.backgroundImage="url('assets/img/photos/"+cands[i]+"')";});};
      im.onerror=function(){tryNext(i+1);};
      im.src="assets/img/photos/"+cands[i];
    })(0);
  }

  /* ---------- Year ---------- */
  document.querySelectorAll('.year').forEach(function(el){el.textContent=new Date().getFullYear();});
})();
