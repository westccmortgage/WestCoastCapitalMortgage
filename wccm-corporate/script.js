/* West Coast Capital Mortgage Inc. — site scripts (no dependencies) */
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
      var btn=f.querySelector('button[type="submit"]');
      var data=new FormData(f);
      if(btn)btn.disabled=true;
      fetch('/',{method:'POST',headers:{'Content-Type':'application/x-www-form-urlencoded'},body:new URLSearchParams(data).toString()})
        .then(function(r){
          if(!r.ok)throw new Error('Submission was not accepted ('+r.status+')');
          if(ok)ok.hidden=false;
          f.querySelectorAll('input,select,textarea,button').forEach(function(el){el.disabled=true;});
          if(ok)ok.scrollIntoView({behavior:'smooth',block:'center'});
        })
        .catch(function(){
          if(btn)btn.disabled=false;
          alert('Something went wrong. Please try again or call us at 310-654-1577.');
        });
    });
  });

  /* Mortgage payment calculator */
  function money(n){return '$'+(isFinite(n)?Math.round(n):0).toLocaleString('en-US');}
  function val(id){var el=document.getElementById(id);if(!el)return 0;return parseFloat((el.value||'').toString().replace(/[^0-9.\-]/g,''))||0;}
  function calc(){
    var price=val('c-price'),dpPct=val('c-down'),rate=val('c-rate'),term=val('c-term');
    var taxYr=val('c-tax'),insYr=val('c-ins'),hoa=val('c-hoa');
    var hint=document.getElementById('c-out-hint');
    // Require home price, interest rate, and loan term before showing any dollar estimate.
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
