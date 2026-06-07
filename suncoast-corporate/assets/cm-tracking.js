/* California Mortgage tracking (shared, Supabase-only via REST). Privacy-conscious. */
(function(){
  "use strict";
  var CFG=window.CM_CONFIG||{}, URL=CFG.SUPABASE_URL||"", KEY=CFG.SUPABASE_ANON_KEY||"";
  var SITE=CFG.SITE||location.hostname, ACCENT=CFG.ACCENT||"#0073e6";
  function g(k){try{return localStorage.getItem(k);}catch(e){return null;}}
  function s(k,v){try{localStorage.setItem(k,v);}catch(e){}}
  function uuid(){if(window.crypto&&crypto.randomUUID)return crypto.randomUUID();
    return "xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx".replace(/[xy]/g,function(c){var r=Math.random()*16|0,v=c==="x"?r:(r&3|8);return v.toString(16);});}
  function cookie(n,v,d){try{var e=new Date();e.setTime(e.getTime()+d*864e5);document.cookie=n+"="+encodeURIComponent(v)+";expires="+e.toUTCString()+";path=/;SameSite=Lax";}catch(_){}}
  function vid(){var v=g("visitor_id");if(!v){v=uuid();s("visitor_id",v);cookie("visitor_id",v,365);}return v;}
  function consent(){return g("cookie_consent_status");}
  function captureFirst(){if(g("cm_first_visit_at"))return;
    s("cm_first_visit_at",new Date().toISOString());s("cm_visit_count","1");
    s("cm_landing_page",location.href);s("cm_referrer",document.referrer||"");
    var p=new URLSearchParams(location.search);
    s("cm_utm",JSON.stringify({utm_source:p.get("utm_source")||"",utm_medium:p.get("utm_medium")||"",utm_campaign:p.get("utm_campaign")||"",utm_content:p.get("utm_content")||"",utm_term:p.get("utm_term")||""}));}
  function utm(){try{return JSON.parse(g("cm_utm")||"{}");}catch(e){return{};}}
  function vcount(){return parseInt(g("cm_visit_count")||"1",10);}
  function insert(table,row){if(!URL||!KEY)return;try{fetch(URL+"/rest/v1/"+table,{method:"POST",headers:{apikey:KEY,Authorization:"Bearer "+KEY,"Content-Type":"application/json",Prefer:"return=minimal"},body:JSON.stringify(row)}).catch(function(){});}catch(e){}}
  function track(name,data){if(consent()!=="accepted")return;insert("visitor_events",{visitor_id:vid(),site:SITE,event_name:name,page_path:location.pathname,event_data:data||{}});}
  window.CMTrack=track;
  function record(){var st=consent();var b={visitor_id:vid(),consent_status:st,site:SITE,first_visit_at:g("cm_first_visit_at"),last_visit_at:new Date().toISOString(),visit_count:vcount()};
    if(st!=="accepted")return b;var u=utm();
    b.landing_page=g("cm_landing_page")||"";b.referrer=g("cm_referrer")||"";b.utm_source=u.utm_source||"";b.utm_medium=u.utm_medium||"";b.utm_campaign=u.utm_campaign||"";b.utm_content=u.utm_content||"";b.utm_term=u.utm_term||"";b.user_agent=navigator.userAgent||"";b.screen_size=window.screen?screen.width+"x"+screen.height:"";return b;}
  function saveVisitorOnce(){if(g("cm_visitor_saved")==="1")return;insert("visitors",record());s("cm_visitor_saved","1");}
  function initEvents(){if(consent()!=="accepted")return;
    track("page_view",{page:location.pathname,referrer:document.referrer||"",screen_size:window.screen?screen.width+"x"+screen.height:""});
    document.addEventListener("click",function(e){
      var a=e.target.closest&&e.target.closest("a");
      if(a){var h=a.getAttribute("href")||"";
        if(h.indexOf("wcci.online")!==-1)track("ai_review_clicked",{href:h});
        else if(/my1003app|myagentloans|\/register/.test(h))track("apply_clicked",{href:h});
        else if(h.indexOf("tel:")===0)track("phone_clicked",{href:h});
        else if(h.indexOf("mailto:")===0)track("email_clicked",{href:h});}
      var lang=e.target.closest&&e.target.closest("[data-lang]");
      if(lang)track("language_switch",{lang:lang.getAttribute("data-lang")});
    },true);}
  function styleBanner(){var css='#cmConsent{position:fixed;left:0;right:0;bottom:0;z-index:9999;padding:0 16px 16px;transform:translateY(120%);transition:transform .35s ease}#cmConsent.show{transform:none}'
    +'.cmc-in{max-width:1040px;margin:0 auto;display:flex;gap:1.4rem;align-items:center;background:#0c1c33;color:#e8eef6;border:1px solid rgba(255,255,255,.14);border-radius:14px;box-shadow:0 20px 50px rgba(0,0,0,.4);padding:1.1rem 1.3rem;font-family:Inter,system-ui,sans-serif}'
    +'.cmc-in h3{margin:0 0 .25rem;font-size:1.1rem;color:#fff}.cmc-in p{margin:0;font-size:.9rem;line-height:1.5;color:#c3cdda}'
    +'.cmc-act{display:flex;gap:10px;flex:0 0 auto}.cmc-b{cursor:pointer;border-radius:8px;font-weight:600;font-size:.9rem;padding:.65rem 1.2rem;border:1px solid transparent}'
    +'.cmc-ess{background:transparent;color:#e8eef6;border-color:rgba(255,255,255,.35)}.cmc-acc{background:'+ACCENT+';color:#fff}'
    +'@media(max-width:760px){.cmc-in{flex-direction:column;align-items:stretch}.cmc-act{flex-direction:column}.cmc-b{width:100%}}';
    var st=document.createElement("style");st.textContent=css;document.head.appendChild(st);}
  function banner(){if(document.getElementById("cmConsent"))return;styleBanner();
    var d=document.createElement("div");d.id="cmConsent";d.setAttribute("role","dialog");d.setAttribute("aria-label","Cookie consent");
    d.innerHTML='<div class="cmc-in"><div><h3>Personalized Mortgage Guidance</h3><p>We use cookies and analytics to remember your visit, improve your experience, and understand which mortgage topics are helpful. You can continue with essential cookies only or allow full experience tracking.</p></div><div class="cmc-act"><button type="button" class="cmc-b cmc-ess" data-c="essential">Essential Only</button><button type="button" class="cmc-b cmc-acc" data-c="accepted">Accept &amp; Continue</button></div></div>';
    document.body.appendChild(d);requestAnimationFrame(function(){d.classList.add("show");});
    Array.prototype.forEach.call(d.querySelectorAll("[data-c]"),function(b){b.addEventListener("click",function(){
      var c=b.getAttribute("data-c");s("cookie_consent_status",c);s("cookie_consent_timestamp",new Date().toISOString());cookie("cookie_consent_status",c,365);
      d.classList.remove("show");setTimeout(function(){d.remove();},300);saveVisitorOnce();if(c==="accepted")initEvents();});});}
  vid();captureFirst();
  if(consent()){if(consent()==="accepted"){s("cm_visit_count",String(vcount()+1));saveVisitorOnce();initEvents();}else{saveVisitorOnce();}}
  else{banner();}
})();
