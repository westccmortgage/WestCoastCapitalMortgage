/* California Mortgage — EN / ES / RU / ZH language support.
   Text-node translation engine: any English source string listed in DICT is
   translated wherever it appears in the page. Language persists in localStorage.
   To extend coverage, just add more "English": ["es","ru","zh"] entries. */
(function () {
  "use strict";
  var LANGS = ["en", "es", "ru", "zh"], STORE = "cmLang";

  var DICT = {
    /* ===== Navigation ===== */
    "Concierge": ["Conserjería", "Консьерж", "礼宾服务"],
    "How It Works": ["Cómo Funciona", "Как это работает", "运作方式"],
    "Education": ["Educación", "Обучение", "知识中心"],
    "About": ["Acerca de", "О нас", "关于我们"],
    "Contact": ["Contacto", "Контакты", "联系方式"],

    /* ===== Buttons / CTAs ===== */
    "Start My Scenario": ["Iniciar Mi Escenario", "Начать мой сценарий", "开始我的方案"],
    "Talk to a Mortgage Professional": ["Hablar con un Profesional Hipotecario", "Связаться с ипотечным специалистом", "联系房贷专家"],
    "Start Application": ["Iniciar Solicitud", "Начать заявку", "开始申请"],
    "Get Free Pre-Approval": ["Obtenga Preaprobación Gratis", "Бесплатное предодобрение", "免费预批"],
    "Get Pre-Approved": ["Obtenga Preaprobación", "Получить предодобрение", "获取预批"],
    "Get a Free Pre-Approval": ["Obtenga una Preaprobación Gratis", "Получить бесплатное предодобрение", "获取免费预批"],
    "Contact a Mortgage Professional": ["Contactar a un Profesional Hipotecario", "Связаться с ипотечным специалистом", "联系房贷专家"],

    /* ===== Hero ===== */
    "California Mortgage Concierge": ["Conserjería Hipotecaria de California", "Ипотечный консьерж Калифорнии", "加州房贷礼宾服务"],
    "Mortgage Guidance": ["Orientación Hipotecaria", "Ипотечное сопровождение", "房贷指导"],
    "Starts Here": ["Comienza Aquí", "начинается здесь", "从这里开始"],
    "Start with your situation — purchase, refinance, lower payment, investment property, self-employed income, or a difficult loan scenario. Answer a few simple questions and we'll help organize your mortgage path before connecting you with AI review or a licensed mortgage professional.": [
      "Comience con su situación: compra, refinanciamiento, pago más bajo, propiedad de inversión, ingresos por cuenta propia o un escenario de préstamo difícil. Responda unas preguntas sencillas y le ayudaremos a organizar su camino hipotecario antes de conectarlo con una revisión por IA o un profesional hipotecario con licencia.",
      "Начните со своей ситуации — покупка, рефинансирование, снижение платежа, инвестиционная недвижимость, доход самозанятого или сложный кредитный сценарий. Ответьте на несколько простых вопросов, и мы поможем организовать ваш ипотечный путь, прежде чем связать вас с обзором ИИ или лицензированным ипотечным специалистом.",
      "从您的情况开始——购房、再融资、降低月供、投资房产、自雇收入或复杂的贷款情形。回答几个简单的问题，我们将帮助您理清房贷方案，然后为您对接AI审阅或持牌房贷专业人士。"
    ],
    "No credit check to start. | No pressure. | No full application required.": [
      "Sin verificación de crédito para empezar. | Sin presión. | Sin solicitud completa.",
      "Без проверки кредита для старта. | Без давления. | Без полной заявки.",
      "开始时无需信用查询。 | 没有压力。 | 无需完整申请。"
    ],
    "You don't need to know the loan program. Start with the situation.": [
      "No necesita conocer el programa de préstamo. Comience con la situación.",
      "Вам не нужно знать кредитную программу. Начните с ситуации.",
      "您无需了解贷款项目。从您的情况开始即可。"
    ],

    /* ===== Section eyebrows / common headings ===== */
    "Financial Navigator": ["Navegador Financiero", "Финансовый навигатор", "财务导航"],
    "Your Financial Navigator": ["Su Navegador Financiero", "Ваш финансовый навигатор", "您的财务导航"],
    "Real People Behind the Guidance": ["Personas Reales Detrás de la Orientación", "Реальные люди за консультацией", "指导背后的真实团队"]
  };

  function tt(s) { return s.replace(/[‘’]/g, "'").replace(/[“”]/g, '"').replace(/[–—]/g, "-"); }
  function norm(s) { return tt(s).replace(/\s+/g, " ").trim(); }

  var NK = null;
  function buildNK() { NK = {}; for (var k in DICT) NK[norm(k)] = DICT[k]; }
  function readLang() { var l = null; try { l = localStorage.getItem(STORE); } catch (e) {} return LANGS.indexOf(l) >= 0 ? l : "en"; }
  function writeLang(l) { try { localStorage.setItem(STORE, l); } catch (e) {} }

  var textNodes = [], attrNodes = [], collected = false;
  function collect() {
    if (collected) return;
    collected = true;
    var w = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT, {
      acceptNode: function (n) {
        var p = n.parentNode;
        if (!p) return NodeFilter.FILTER_REJECT;
        var tag = p.nodeName;
        if (tag === "SCRIPT" || tag === "STYLE" || tag === "NOSCRIPT") return NodeFilter.FILTER_REJECT;
        if (p.closest && p.closest(".lang-switch")) return NodeFilter.FILTER_REJECT;
        if (!n.nodeValue || !n.nodeValue.trim()) return NodeFilter.FILTER_REJECT;
        return NodeFilter.FILTER_ACCEPT;
      }
    });
    var n; while ((n = w.nextNode())) textNodes.push({ node: n, raw: n.nodeValue });
    Array.prototype.forEach.call(document.body.querySelectorAll("[placeholder],[aria-label]"), function (el) {
      if (el.closest && el.closest(".lang-switch")) return;
      var ph = el.getAttribute("placeholder");
      if (ph && ph.trim()) attrNodes.push({ el: el, attr: "placeholder", en: ph });
      var al = el.getAttribute("aria-label");
      if (al && al.trim()) attrNodes.push({ el: el, attr: "aria-label", en: al });
    });
  }

  function look(en, lang) {
    if (lang === "en") return null;
    if (!NK) buildNK();
    var e = NK[norm(en)];
    if (!e) return null;
    var idx = lang === "es" ? 0 : lang === "ru" ? 1 : 2;
    return e[idx] || null;
  }

  function apply(lang) {
    collect();
    textNodes.forEach(function (t) {
      var m = t.raw.match(/^(\s*)([\s\S]*?)(\s*)$/);
      var core = m ? m[2] : t.raw;
      var tr = look(core, lang);
      t.node.nodeValue = (tr !== null && m) ? (m[1] + tr + m[3]) : t.raw;
    });
    attrNodes.forEach(function (a) {
      var tr = look(a.en, lang);
      a.el.setAttribute(a.attr, tr !== null ? tr : a.en);
    });
    Array.prototype.forEach.call(document.querySelectorAll(".lang-switch button"), function (b) {
      b.classList.toggle("is-active", b.getAttribute("data-lang") === lang);
      b.setAttribute("aria-pressed", b.getAttribute("data-lang") === lang ? "true" : "false");
    });
    document.documentElement.setAttribute("lang", lang);
  }

  function setLang(lang) { if (LANGS.indexOf(lang) < 0) lang = "en"; window.CMI18N.lang = lang; writeLang(lang); apply(lang); }
  window.CMI18N = { lang: readLang(), setLang: setLang, apply: apply };

  function init() {
    Array.prototype.forEach.call(document.querySelectorAll(".lang-switch button"), function (b) {
      b.addEventListener("click", function () { setLang(b.getAttribute("data-lang")); });
    });
    apply(window.CMI18N.lang);
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init);
  else init();
})();
