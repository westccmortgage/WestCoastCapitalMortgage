/* K West Mortgage — EN / ES / RU / ZH language support.
   Text-node translation engine. Add "English": ["es","ru","zh"] entries to grow. */
(function () {
  "use strict";
  var LANGS = ["en", "es", "ru", "zh"], STORE = "kwLang";

  var DICT = {
    /* Navigation + CTAs */
    "Concierge": ["Conserjería", "Консьерж", "礼宾服务"],
    "Loan Programs": ["Programas de Préstamo", "Кредитные программы", "贷款项目"],
    "How It Works": ["Cómo Funciona", "Как это работает", "运作方式"],
    "Education": ["Educación", "Обучение", "知识中心"],
    "About": ["Acerca de", "О нас", "关于我们"],
    "Contact": ["Contacto", "Контакты", "联系方式"],
    "Start My Scenario": ["Iniciar Mi Escenario", "Начать мой сценарий", "开始我的方案"],
    "Compare": ["Comparar", "Сравнить", "比较"],
    "Review My Scenario": ["Revisar Mi Escenario", "Проверить мой сценарий", "审阅我的方案"],
    "Review My Key West Scenario": ["Revisar Mi Escenario de Key West", "Проверить мой сценарий Key West", "审阅我的Key West方案"],
    "Talk to a Mortgage Professional": ["Hablar con un Profesional Hipotecario", "Связаться с ипотечным специалистом", "联系房贷专家"],
    "Conforming": ["Conforme", "Конформные", "常规贷款"],
    "Loan Options": ["Opciones de Préstamo", "Кредитные программы", "贷款选项"],

    /* Hero */
    "Key West Mortgage Concierge": ["Conserjería Hipotecaria de Key West", "Ипотечный консьерж Key West", "Key West房贷礼宾服务"],
    "Key West Mortgage Guidance": ["Orientación Hipotecaria de Key West", "Ипотечное сопровождение Key West", "Key West房贷指导"],
    "Starts Here": ["Comienza Aquí", "начинается здесь", "从这里开始"],
    "Start with your situation — purchase, refinance, lower payment, investment property, self-employed income, or a difficult Key West loan scenario. Answer a few simple questions and we'll help organize your Monroe County mortgage path before connecting you with a licensed mortgage professional.": [
      "Comience con su situación: compra, refinanciamiento, pago más bajo, propiedad de inversión, ingresos por cuenta propia o un escenario de préstamo difícil en Key West. Responda unas preguntas sencillas y le ayudaremos a organizar su camino hipotecario en el condado de Monroe antes de conectarlo con un profesional hipotecario con licencia.",
      "Начните со своей ситуации — покупка, рефинансирование, снижение платежа, инвестиционная недвижимость, доход самозанятого или сложный кредитный сценарий в Key West. Ответьте на несколько простых вопросов, и мы поможем организовать ваш ипотечный путь в округе Monroe, прежде чем связать вас с лицензированным ипотечным специалистом.",
      "从您的情况开始——购房、再融资、降低月供、投资房产、自雇收入，或复杂的Key West贷款情形。回答几个简单的问题，我们将帮助您理清Monroe县的房贷方案，然后为您对接持牌房贷专业人士。"
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
    ]
  };

  function tt(s) { return s.replace(/[‘’]/g, "'").replace(/[“”]/g, '"').replace(/[–—]/g, "-"); }
  function norm(s) { return tt(s).replace(/\s+/g, " ").trim(); }
  var NK = null;
  function buildNK() { NK = {}; for (var k in DICT) NK[norm(k)] = DICT[k]; }
  function readLang() { var l = null; try { l = localStorage.getItem(STORE); } catch (e) {} return LANGS.indexOf(l) >= 0 ? l : "en"; }
  function writeLang(l) { try { localStorage.setItem(STORE, l); } catch (e) {} }

  var textNodes = [], attrNodes = [], collected = false;
  function collect() {
    if (collected) return; collected = true;
    var w = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT, {
      acceptNode: function (n) {
        var p = n.parentNode; if (!p) return NodeFilter.FILTER_REJECT;
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
      var ph = el.getAttribute("placeholder"); if (ph && ph.trim()) attrNodes.push({ el: el, attr: "placeholder", en: ph });
      var al = el.getAttribute("aria-label"); if (al && al.trim()) attrNodes.push({ el: el, attr: "aria-label", en: al });
    });
  }
  function look(en, lang) {
    if (lang === "en") return null; if (!NK) buildNK();
    var e = NK[norm(en)]; if (!e) return null;
    var idx = lang === "es" ? 0 : lang === "ru" ? 1 : 2; return e[idx] || null;
  }
  function apply(lang) {
    collect();
    textNodes.forEach(function (t) {
      var m = t.raw.match(/^(\s*)([\s\S]*?)(\s*)$/);
      var core = m ? m[2] : t.raw; var tr = look(core, lang);
      t.node.nodeValue = (tr !== null && m) ? (m[1] + tr + m[3]) : t.raw;
    });
    attrNodes.forEach(function (a) { var tr = look(a.en, lang); a.el.setAttribute(a.attr, tr !== null ? tr : a.en); });
    Array.prototype.forEach.call(document.querySelectorAll(".lang-switch button"), function (b) {
      b.classList.toggle("is-active", b.getAttribute("data-lang") === lang);
      b.setAttribute("aria-pressed", b.getAttribute("data-lang") === lang ? "true" : "false");
    });
    document.documentElement.setAttribute("lang", lang);
  }
  function setLang(lang) { if (LANGS.indexOf(lang) < 0) lang = "en"; window.KWI18N.lang = lang; writeLang(lang); apply(lang); }
  window.KWI18N = { lang: readLang(), setLang: setLang, apply: apply };
  function init() {
    Array.prototype.forEach.call(document.querySelectorAll(".lang-switch button"), function (b) {
      b.addEventListener("click", function () { setLang(b.getAttribute("data-lang")); });
    });
    apply(window.KWI18N.lang);
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init);
  else init();
})();
