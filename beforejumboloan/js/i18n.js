/* Before Jumbo Loan — EN / ES / RU / ZH language support.
   Text-node translation engine. Add "English": ["es","ru","zh"] entries to grow. */
(function () {
  "use strict";
  var LANGS = ["en", "es", "ru", "zh"], STORE = "bjlLang";

  var DICT = {
    /* Navigation + CTAs */
    "Loan Options": ["Opciones de Préstamo", "Кредитные программы", "贷款选项"],
    "Jumbo vs Conforming": ["Jumbo vs Conforme", "Jumbo или конформный", "大额贷款 vs 常规贷款"],
    "Education": ["Educación", "Обучение", "知识中心"],
    "About": ["Acerca de", "О нас", "关于我们"],
    "Contact": ["Contacto", "Контакты", "联系方式"],
    "Start My Scenario": ["Iniciar Mi Escenario", "Начать мой сценарий", "开始我的方案"],
    "Start Application": ["Iniciar Solicitud", "Начать заявку", "开始申请"],
    "Concierge": ["Conserjería", "Консьерж", "礼宾服务"],
    "Send My Scenario": ["Enviar Mi Escenario", "Отправить мой сценарий", "发送我的方案"],
    "Get in touch": ["Póngase en contacto", "Свяжитесь с нами", "联系我们"],

    /* Hero cockpit */
    "Mortgage Strategy Engine": ["Motor de Estrategia Hipotecaria", "Движок ипотечной стратегии", "房贷策略引擎"],
    "The bank may call it jumbo.": ["El banco puede llamarlo jumbo.", "Банк может назвать это jumbo.", "银行可能称之为大额贷款。"],
    "The structure may tell a different story.": ["La estructura puede contar otra historia.", "Но структура может говорить об ином.", "但贷款结构或许另有说法。"],
    "Run the property through county-line, payment, interest-only, buydown, and program-path logic before deciding the structure.": [
      "Analice la propiedad con la lógica de límites por condado, pago, solo interés, reducción de tasa (buydown) y ruta de programa antes de decidir la estructura.",
      "Прогоните объект через логику границ округа, платежа, only-interest, buydown и выбора программы, прежде чем решать структуру.",
      "在决定贷款结构之前，先用县界限额、月供、只付利息、买断利率和项目路径逻辑分析该房产。"
    ],
    "Your Financial Navigator": ["Su Navegador Financiero", "Ваш финансовый навигатор", "您的财务导航"],
    "Your Financial Navigator walks you through every step: the county line, down payment, credit, income, payment strategy, and how conforming vs. jumbo financing fits your scenario — before the bank decides the structure for you.": [
      "Su Navegador Financiero le guía en cada paso: el límite del condado, el pago inicial, el crédito, los ingresos, la estrategia de pago y cómo el financiamiento conforme frente al jumbo encaja en su escenario, antes de que el banco decida la estructura por usted.",
      "Ваш финансовый навигатор проведёт вас через каждый шаг: граница округа, первоначальный взнос, кредит, доход, стратегия платежа и как конформное или jumbo-финансирование подходит вашему сценарию — прежде чем банк решит структуру за вас.",
      "您的财务导航将带您走过每一步：县界限额、首付、信用、收入、月供策略，以及常规贷款与大额贷款如何适配您的情况——在银行替您决定结构之前。"
    ],
    "Talk to a Licensed Mortgage Professional": ["Hable con un Profesional Hipotecario con Licencia", "Свяжитесь с лицензированным ипотечным специалистом", "联系持牌房贷专业人士"],
    "Build your scenario, then send it for a licensed review.": [
      "Cree su escenario y luego envíelo para una revisión con licencia.",
      "Постройте свой сценарий и отправьте его на лицензированную проверку.",
      "构建您的方案，然后提交进行持牌审阅。"
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
  function setLang(lang) { if (LANGS.indexOf(lang) < 0) lang = "en"; window.BJLI18N.lang = lang; writeLang(lang); apply(lang); }
  window.BJLI18N = { lang: readLang(), setLang: setLang, apply: apply };
  function init() {
    Array.prototype.forEach.call(document.querySelectorAll(".lang-switch button"), function (b) {
      b.addEventListener("click", function () { setLang(b.getAttribute("data-lang")); });
    });
    apply(window.BJLI18N.lang);
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init);
  else init();
})();
