/* West Coast Capital Mortgage — multi-language support (EN / ES / RU)
   Text-node translation engine. Any English source string present in DICT
   is translated everywhere it appears across the site, so shared chrome
   (nav, footer, legal disclaimer, chat) is translated from a single entry.
   Language is stored in localStorage and defaults to "en". */
(function () {
  "use strict";

  var LANGS = ["en", "es", "ru"];
  var STORE = "wccLang";

  /* ---- Dictionary: "English source" : [ "Español", "Русский" ] ----
     Keys must match the page text after whitespace is collapsed/trimmed. */
  var DICT = {
    /* ===== Navigation ===== */
    "Home": ["Inicio", "Главная"],
    "Loan Programs": ["Programas de Préstamo", "Кредитные программы"],
    "🏠 Conventional": ["🏠 Convencional", "🏠 Конвенциональный"],
    "🔑 FHA Loans": ["🔑 Préstamos FHA", "🔑 Кредиты FHA"],
    "🎖️ VA Loans": ["🎖️ Préstamos VA", "🎖️ Кредиты VA"],
    "🌾 USDA Loans": ["🌾 Préstamos USDA", "🌾 Кредиты USDA"],
    "💎 Jumbo Loans": ["💎 Préstamos Jumbo", "💎 Джамбо-кредиты"],
    "📈 Fixed-Rate": ["📈 Tasa Fija", "📈 Фиксированная ставка"],
    "🔁 Refinance": ["🔁 Refinanciamiento", "🔁 Рефинансирование"],
    "🔨 Renovation 203(k)": ["🔨 Renovación 203(k)", "🔨 Реновация 203(k)"],
    "🌅 Reverse Mortgage": ["🌅 Hipoteca Inversa", "🌅 Обратная ипотека"],
    "Calculators": ["Calculadoras", "Калькуляторы"],
    "About": ["Nosotros", "О нас"],
    "Reviews": ["Reseñas", "Отзывы"],
    "Blog": ["Blog", "Блог"],
    "Contact": ["Contacto", "Контакты"],
    "Apply Now": ["Solicitar Ahora", "Подать заявку"],

    /* ===== Footer ===== */
    "Honest guidance. Clear answers. Strong results — for homebuyers and homeowners across California, Florida & Washington.": ["Orientación honesta. Respuestas claras. Resultados sólidos — para compradores y propietarios de vivienda en California, Florida y Washington.", "Честные консультации. Ясные ответы. Надёжные результаты — для покупателей и владельцев жилья в Калифорнии, Флориде и Вашингтоне."],
    "Conventional": ["Convencional", "Конвенциональный"],
    "FHA Loans": ["Préstamos FHA", "Кредиты FHA"],
    "VA Loans": ["Préstamos VA", "Кредиты VA"],
    "USDA Loans": ["Préstamos USDA", "Кредиты USDA"],
    "Jumbo Loans": ["Préstamos Jumbo", "Джамбо-кредиты"],
    "Fixed-Rate": ["Tasa Fija", "Фиксированная ставка"],
    "Company": ["Empresa", "Компания"],
    "About the CEO": ["Sobre el CEO", "О генеральном директоре"],
    "Client Reviews": ["Reseñas de Clientes", "Отзывы клиентов"],
    "Mortgage Blog": ["Blog Hipotecario", "Ипотечный блог"],
    "Contact Us": ["Contáctenos", "Свяжитесь с нами"],
    "Get Started": ["Comenzar", "Начать"],
    "Apply Online": ["Solicitar en Línea", "Подать онлайн"],
    "Free Rate Quote": ["Cotización de Tasa Gratis", "Бесплатный расчёт ставки"],
    "Estimate Payment": ["Estimar Pago", "Рассчитать платёж"],
    "Licensed in CA · FL · WA": ["Con licencia en CA · FL · WA", "Лицензия в CA · FL · WA"],
    "West Coast Capital Mortgage Inc. (NMLS# 2775380) is an Equal Housing Lender. This is not a commitment to lend. All loans are subject to credit approval, income verification, and property appraisal. Rates and programs are subject to change without notice and are shown for illustrative purposes only — actual rates depend on credit profile, loan amount, down payment, occupancy, and property type. Calculator results are estimates and not an offer or guarantee of a loan. Equal Housing Opportunity.": ["West Coast Capital Mortgage Inc. (NMLS# 2775380) es un Prestamista que Ofrece Igualdad de Oportunidades de Vivienda. Esto no constituye un compromiso de préstamo. Todos los préstamos están sujetos a aprobación de crédito, verificación de ingresos y tasación de la propiedad. Las tasas y los programas están sujetos a cambios sin previo aviso y se muestran únicamente con fines ilustrativos — las tasas reales dependen del perfil crediticio, el monto del préstamo, el pago inicial, la ocupación y el tipo de propiedad. Los resultados de las calculadoras son estimaciones y no constituyen una oferta ni una garantía de préstamo. Igualdad de Oportunidades de Vivienda.", "West Coast Capital Mortgage Inc. (NMLS# 2775380) — кредитор, соблюдающий принцип равных возможностей в сфере жилья (Equal Housing Lender). Это не обязательство о предоставлении кредита. Все кредиты предоставляются при условии одобрения кредитоспособности, подтверждения дохода и оценки недвижимости. Ставки и программы могут изменяться без предварительного уведомления и приведены исключительно в иллюстративных целях — фактические ставки зависят от кредитного профиля, суммы кредита, первоначального взноса, типа проживания и типа недвижимости. Результаты калькуляторов являются оценочными и не являются предложением или гарантией кредита. Равные возможности в сфере жилья (Equal Housing Opportunity)."],

    /* ===== Chat widget (static markup) ===== */
    "Mortgage Assistant": ["Asistente Hipotecario", "Ипотечный ассистент"],
    "● Online now": ["● En línea ahora", "● Сейчас в сети"],
    "Today's rates": ["Tasas de hoy", "Ставки сегодня"],
    "FHA loans": ["Préstamos FHA", "Кредиты FHA"],
    "How much can I afford?": ["¿Cuánto puedo pagar?", "Сколько я могу себе позволить?"],
    "Get pre-approved": ["Obtener preaprobación", "Получить предодобрение"],

    /* ===== Shared CTA band ===== */
    "Ready to take the next step?": ["¿Listo para dar el siguiente paso?", "Готовы сделать следующий шаг?"],
    "Get a free, no-obligation rate quote or start your application in minutes. A licensed loan officer will guide you the whole way.": ["Obtenga una cotización de tasa gratuita y sin compromiso, o comience su solicitud en minutos. Un oficial de préstamos con licencia lo guiará en todo momento.", "Получите бесплатный расчёт ставки без обязательств или начните заявку за пару минут. Лицензированный кредитный специалист будет сопровождать вас на каждом шаге."],
    "Call (310) 654-1577": ["Llame al (310) 654-1577", "Позвонить (310) 654-1577"],

    /* ===== Homepage ===== */
    "Licensed in CA · FL · WA · NMLS# 2775380": ["Con licencia en CA · FL · WA · NMLS# 2775380", "Лицензия в CA · FL · WA · NMLS# 2775380"],
    "Home loans done": ["Préstamos hipotecarios hechos", "Ипотека"],
    "the honest way.": ["de forma honesta.", "честным путём."],
    "Whether you're buying your first home, refinancing, or investing — we deliver clear answers, competitive rates, and a team that's with you every step. Backed by 20+ years of lending experience.": ["Ya sea que esté comprando su primera casa, refinanciando o invirtiendo — le ofrecemos respuestas claras, tasas competitivas y un equipo que lo acompaña en cada paso. Respaldado por más de 20 años de experiencia en préstamos.", "Покупаете ли вы первый дом, рефинансируете или инвестируете — мы даём ясные ответы, конкурентные ставки и команду, которая рядом на каждом шаге. Более 20 лет опыта в кредитовании."],
    "Get Pre-Approved": ["Obtener Preaprobación", "Получить предодобрение"],
    "Estimate My Payment": ["Estimar Mi Pago", "Рассчитать платёж"],
    "20+ yrs": ["+20 años", "20+ лет"],
    "Lending experience": ["Experiencia en préstamos", "Опыт кредитования"],
    "$0 down": ["$0 inicial", "$0 взнос"],
    "VA & USDA options": ["Opciones VA y USDA", "Варианты VA и USDA"],
    "3 states": ["3 estados", "3 штата"],
    "Today's Sample Rates": ["Tasas de Muestra de Hoy", "Примерные ставки на сегодня"],
    "● LIVE": ["● EN VIVO", "● ОНЛАЙН"],
    "30-Year Fixed": ["Fija a 30 años", "Фиксированная 30 лет"],
    "15-Year Fixed": ["Fija a 15 años", "Фиксированная 15 лет"],
    "FHA 30-Year": ["FHA a 30 años", "FHA 30 лет"],
    "VA 30-Year": ["VA a 30 años", "VA 30 лет"],
    "Jumbo 30-Year": ["Jumbo a 30 años", "Джамбо 30 лет"],
    "Illustrative rates as of today. Your actual rate depends on credit, down payment & loan type.": ["Tasas ilustrativas de hoy. Su tasa real depende del crédito, el pago inicial y el tipo de préstamo.", "Иллюстративные ставки на сегодня. Ваша фактическая ставка зависит от кредита, первоначального взноса и типа кредита."],
    "Get your real quote →": ["Obtenga su cotización real →", "Получить реальный расчёт →"],
    "Google Reviews": ["Reseñas de Google", "Отзывы Google"],
    "Equal Housing": ["Igualdad de Vivienda", "Равные возможности жилья"],
    "Lender": ["Prestamista", "кредитор"],
    "CA Broker": ["Corredor de CA", "Брокер CA"],
    "since 2009": ["desde 2009", "с 2009"],
    "Find the loan that fits your life": ["Encuentre el préstamo que se ajusta a su vida", "Найдите кредит, подходящий вашей жизни"],
    "Every borrower is different. We match you with the right program — and explain exactly why it works for you.": ["Cada prestatario es diferente. Lo emparejamos con el programa adecuado — y le explicamos exactamente por qué funciona para usted.", "Каждый заёмщик уникален. Мы подберём подходящую программу — и объясним, почему именно она вам подходит."],
    "Flexible terms and competitive rates with as little as 3% down for qualified buyers.": ["Términos flexibles y tasas competitivas con tan solo 3% de pago inicial para compradores calificados.", "Гибкие условия и конкурентные ставки с первоначальным взносом всего от 3% для квалифицированных покупателей."],
    "Explore Conventional →": ["Explorar Convencional →", "Подробнее: Конвенциональный →"],
    "Just 3.5% down and flexible credit — a favorite for first-time buyers.": ["Solo 3.5% de pago inicial y crédito flexible — el favorito de los compradores primerizos.", "Всего 3,5% первоначального взноса и гибкие требования к кредиту — выбор покупателей первого жилья."],
    "Explore FHA Loans →": ["Explorar Préstamos FHA →", "Подробнее: Кредиты FHA →"],
    "$0 down and no PMI for eligible veterans and active-duty service members.": ["$0 de pago inicial y sin PMI para veteranos elegibles y militares en servicio activo.", "$0 первоначального взноса и без PMI для подходящих ветеранов и военнослужащих действительной службы."],
    "Explore VA Loans →": ["Explorar Préstamos VA →", "Подробнее: Кредиты VA →"],
    "$0 down financing for eligible rural and suburban homebuyers.": ["Financiamiento con $0 de pago inicial para compradores elegibles en zonas rurales y suburbanas.", "Финансирование с $0 первоначального взноса для подходящих покупателей в сельской и пригородной местности."],
    "Explore USDA Loans →": ["Explorar Préstamos USDA →", "Подробнее: Кредиты USDA →"],
    "Financing above conforming limits for higher-priced California homes.": ["Financiamiento por encima de los límites conformes para viviendas de mayor precio en California.", "Финансирование сверх соответствующих лимитов для дорогого жилья в Калифорнии."],
    "Explore Jumbo Loans →": ["Explorar Préstamos Jumbo →", "Подробнее: Джамбо-кредиты →"],
    "Lower your rate, shorten your term, or tap into your home's equity.": ["Reduzca su tasa, acorte su plazo o aproveche el valor acumulado de su vivienda.", "Снизьте ставку, сократите срок или используйте капитал вашего дома."],
    "Explore Refinance →": ["Explorar Refinanciamiento →", "Подробнее: Рефинансирование →"],
    "View all loan programs →": ["Ver todos los programas de préstamo →", "Все кредитные программы →"],
    "Why West Coast Capital": ["Por qué West Coast Capital", "Почему West Coast Capital"],
    "Experience you can rely on": ["Experiencia en la que puede confiar", "Опыт, на который можно положиться"],
    "Founded by Anatoliy Kanevsky, a California-licensed broker since 2009 with a career in residential lending dating back to 2004. We've guided thousands of families through one of the most important financial decisions of their lives.": ["Fundada por Anatoliy Kanevsky, corredor con licencia en California desde 2009 y con una carrera en préstamos residenciales que se remonta a 2004. Hemos guiado a miles de familias a través de una de las decisiones financieras más importantes de sus vidas.", "Основана Анатолием Каневским, лицензированным в Калифорнии брокером с 2009 года, с карьерой в жилищном кредитовании с 2004 года. Мы помогли тысячам семей пройти через одно из важнейших финансовых решений в их жизни."],
    "Straight answers, no jargon.": ["Respuestas directas, sin tecnicismos.", "Прямые ответы, без жаргона."],
    "We explain your options clearly so you can decide with confidence.": ["Le explicamos sus opciones con claridad para que pueda decidir con confianza.", "Мы понятно объясняем ваши варианты, чтобы вы могли принять уверенное решение."],
    "Local market expertise.": ["Experiencia en el mercado local.", "Знание местного рынка."],
    "Deep knowledge of California, Florida & Washington housing markets.": ["Amplio conocimiento de los mercados inmobiliarios de California, Florida y Washington.", "Глубокое знание рынков жилья Калифорнии, Флориды и Вашингтона."],
    "Full-lifecycle insight.": ["Visión de ciclo completo.", "Понимание полного цикла."],
    "Our team understands both financing and construction — a rare advantage.": ["Nuestro equipo entiende tanto el financiamiento como la construcción — una ventaja poco común.", "Наша команда разбирается и в финансировании, и в строительстве — редкое преимущество."],
    "Fast, modern process.": ["Proceso rápido y moderno.", "Быстрый, современный процесс."],
    "Apply online in minutes and track everything in one place.": ["Solicite en línea en minutos y siga todo en un solo lugar.", "Подайте заявку онлайн за минуты и отслеживайте всё в одном месте."],
    "Meet our founder →": ["Conozca a nuestro fundador →", "Познакомьтесь с основателем →"],
    "Apply in minutes": ["Solicite en minutos", "Заявка за минуты"],
    "Complete a quick, secure online application — no paperwork pile.": ["Complete una solicitud en línea rápida y segura — sin montañas de papeleo.", "Заполните быструю и безопасную онлайн-заявку — без кипы документов."],
    "Get matched & quoted": ["Reciba opciones y cotización", "Подбор и расчёт"],
    "We compare programs and bring you a personalized rate.": ["Comparamos programas y le ofrecemos una tasa personalizada.", "Мы сравниваем программы и предлагаем персональную ставку."],
    "Close with confidence": ["Cierre con confianza", "Закрытие с уверенностью"],
    "We handle the details and keep you informed to the finish line.": ["Nos encargamos de los detalles y lo mantenemos informado hasta el final.", "Мы берём на себя детали и держим вас в курсе до самого конца."],
    "Tools": ["Herramientas", "Инструменты"],
    "Crunch the numbers in seconds": ["Calcule los números en segundos", "Посчитайте за секунды"],
    "Estimate payments, test a refinance, or see how much home you can afford — instantly.": ["Estime pagos, pruebe un refinanciamiento o vea cuánta casa puede pagar — al instante.", "Оцените платежи, проверьте рефинансирование или узнайте, какой дом вам по карману — мгновенно."],
    "Payment": ["Pago", "Платёж"],
    "Estimate your monthly principal, interest, taxes & insurance.": ["Estime su capital, intereses, impuestos y seguro mensuales.", "Рассчитайте ежемесячный основной долг, проценты, налоги и страховку."],
    "Open →": ["Abrir →", "Открыть →"],
    "See your potential savings and break-even point.": ["Vea sus ahorros potenciales y su punto de equilibrio.", "Узнайте потенциальную экономию и точку окупаемости."],
    "Affordability": ["Capacidad de Pago", "Доступность"],
    "Find a comfortable price range based on your income.": ["Encuentre un rango de precio cómodo según sus ingresos.", "Найдите комфортный ценовой диапазон с учётом ваших доходов."],
    "Compare the long-term cost of renting and owning.": ["Compare el costo a largo plazo de alquilar y de comprar.", "Сравните долгосрочные затраты на аренду и покупку."],
    "Families who trusted us": ["Familias que confiaron en nosotros", "Семьи, которые нам доверились"],
    "\"Helpful service made the whole loan process a positive experience. The loan was amazing for my investment property — I will definitely come back again.\"": ["«Un servicio atento hizo de todo el proceso del préstamo una experiencia positiva. El préstamo fue excelente para mi propiedad de inversión — sin duda volveré.»", "«Внимательный сервис сделал весь процесс кредитования приятным. Кредит на мою инвестиционную недвижимость был отличным — обязательно вернусь снова.»"],
    "Google Reviewer": ["Reseñador de Google", "Отзыв на Google"],
    "Investment Property, Los Angeles": ["Propiedad de Inversión, Los Ángeles", "Инвестиционная недвижимость, Лос-Анджелес"],
    "\"Anatoliy and his team made our first home purchase painless. They explained every step in plain English and got us a great rate.\"": ["«Anatoliy y su equipo hicieron que la compra de nuestra primera casa fuera sencilla. Explicaron cada paso con palabras claras y nos consiguieron una excelente tasa.»", "«Анатолий и его команда сделали покупку нашего первого дома беспроблемной. Они объяснили каждый шаг простым языком и добились для нас отличной ставки.»"],
    "First-Time Buyers, FHA": ["Compradores Primerizos, FHA", "Покупатели первого жилья, FHA"],
    "\"Refinanced and cut my monthly payment significantly. Honest advice and no surprises at closing.\"": ["«Refinancié y reduje significativamente mi pago mensual. Consejos honestos y sin sorpresas en el cierre.»", "«Рефинансировал и значительно снизил ежемесячный платёж. Честные советы и никаких сюрпризов при закрытии.»"],
    "Refinance, Conventional": ["Refinanciamiento, Convencional", "Рефинансирование, Конвенциональный"],
    "Read all reviews →": ["Leer todas las reseñas →", "Читать все отзывы →"],

    /* ===== Breadcrumbs (current page) ===== */
    "/ About": ["/ Nosotros", "/ О нас"],
    "/ Apply Now": ["/ Solicitar Ahora", "/ Подать заявку"],
    "/ Blog": ["/ Blog", "/ Блог"],
    "/ Calculators": ["/ Calculadoras", "/ Калькуляторы"],
    "/ Contact": ["/ Contacto", "/ Контакты"],
    "/ Conventional Mortgage": ["/ Hipoteca Convencional", "/ Конвенциональная ипотека"],
    "/ FHA Home Loan": ["/ Préstamo Hipotecario FHA", "/ Жилищный кредит FHA"],
    "/ Fixed-Rate Mortgage": ["/ Hipoteca de Tasa Fija", "/ Ипотека с фиксированной ставкой"],
    "/ Jumbo Mortgage": ["/ Hipoteca Jumbo", "/ Джамбо-ипотека"],
    "/ Mortgage Refinancing": ["/ Refinanciamiento Hipotecario", "/ Рефинансирование ипотеки"],
    "/ Renovation Mortgage 203(k)": ["/ Hipoteca de Renovación 203(k)", "/ Ипотека на реновацию 203(k)"],
    "/ Reverse Mortgage": ["/ Hipoteca Inversa", "/ Обратная ипотека"],
    "/ Reviews": ["/ Reseñas", "/ Отзывы"],
    "/ USDA Home Loan": ["/ Préstamo Hipotecario USDA", "/ Жилищный кредит USDA"],
    "/ VA Home Loan": ["/ Préstamo Hipotecario VA", "/ Жилищный кредит VA"],

    /* ===== About page ===== */
    "Honest guidance. Clear answers. Strong results.": ["Orientación honesta. Respuestas claras. Resultados sólidos.", "Честные консультации. Ясные ответы. Надёжные результаты."],
    "Meet the team and the founder behind West Coast Capital Mortgage Inc.": ["Conozca al equipo y al fundador detrás de West Coast Capital Mortgage Inc.", "Познакомьтесь с командой и основателем West Coast Capital Mortgage Inc."],
    "Founder & CEO": ["Fundador y CEO", "Основатель и генеральный директор"],
    "California Broker License since July 16, 2009 · NMLS# 2775380": ["Licencia de Corredor de California desde el 16 de julio de 2009 · NMLS# 2775380", "Лицензия брокера Калифорнии с 16 июля 2009 г. · NMLS# 2775380"],
    "Our Story": ["Nuestra Historia", "Наша история"],
    "Two decades of lending, built on trust": ["Dos décadas de préstamos, construidas sobre la confianza", "Два десятилетия кредитования, основанного на доверии"],
    "Anatoliy Kanevsky is the Founder and CEO of West Coast Capital Mortgage Inc., with a career in residential lending that began in 2004 as a loan officer at Finance Connection. From day one, he learned the business from the ground up — working directly with borrowers and guiding families through one of the most important financial decisions of their lives.": ["Anatoliy Kanevsky es el Fundador y CEO de West Coast Capital Mortgage Inc., con una carrera en préstamos residenciales que comenzó en 2004 como oficial de préstamos en Finance Connection. Desde el primer día, aprendió el negocio desde cero — trabajando directamente con los prestatarios y guiando a las familias a través de una de las decisiones financieras más importantes de sus vidas.", "Анатолий Каневский — основатель и генеральный директор West Coast Capital Mortgage Inc. Его карьера в жилищном кредитовании началась в 2004 году с должности кредитного специалиста в Finance Connection. С первого дня он осваивал дело с самых основ — работая напрямую с заёмщиками и помогая семьям принимать одно из важнейших финансовых решений в их жизни."],
    "In 2009 he earned his California Broker License, opening the door to working independently and serving clients at the highest professional level. Over the years his network grew organically through referrals from clients who trusted his straightforward approach.": ["En 2009 obtuvo su Licencia de Corredor de California, abriendo la puerta para trabajar de forma independiente y atender a los clientes al más alto nivel profesional. Con los años, su red creció de forma orgánica gracias a las referencias de clientes que confiaron en su enfoque directo.", "В 2009 году он получил лицензию брокера Калифорнии, что открыло возможность работать самостоятельно и обслуживать клиентов на высшем профессиональном уровне. С годами его сеть росла органически благодаря рекомендациям клиентов, доверявших его прямому подходу."],
    "Alongside his mortgage work, Anatoliy expanded into real estate development as CEO of California Residential Development Partners LLC, specializing in high-end residential construction throughout the Los Angeles area. This dual background — financing and construction — gives him a perspective few professionals possess: he understands the full lifecycle of a property, from financial structuring to the build itself.": ["Además de su trabajo hipotecario, Anatoliy se expandió al desarrollo inmobiliario como CEO de California Residential Development Partners LLC, especializándose en construcción residencial de alta gama en toda el área de Los Ángeles. Esta doble formación — financiamiento y construcción — le brinda una perspectiva que pocos profesionales poseen: comprende el ciclo de vida completo de una propiedad, desde la estructuración financiera hasta la construcción misma.", "Помимо ипотечной деятельности, Анатолий расширил сферу в девелопмент недвижимости как генеральный директор California Residential Development Partners LLC, специализируясь на элитном жилищном строительстве по всему району Лос-Анджелеса. Этот двойной опыт — финансирование и строительство — даёт ему перспективу, которой обладают немногие специалисты: он понимает полный жизненный цикл недвижимости, от финансовой структуры до самой стройки."],
    "Today, under his leadership, West Coast Capital Mortgage Inc. is recognized for integrity, reliability, and a client-focused approach. The mission stays the same:": ["Hoy, bajo su liderazgo, West Coast Capital Mortgage Inc. es reconocida por su integridad, confiabilidad y enfoque centrado en el cliente. La misión sigue siendo la misma:", "Сегодня под его руководством West Coast Capital Mortgage Inc. известна своей честностью, надёжностью и ориентацией на клиента. Миссия остаётся прежней:"],
    "to help people move forward in life.": ["ayudar a las personas a avanzar en la vida.", "помогать людям двигаться вперёд по жизни."],
    "What we value": ["Lo que valoramos", "Наши ценности"],
    "Why clients choose us": ["Por qué los clientes nos eligen", "Почему клиенты выбирают нас"],
    "Integrity first": ["Integridad ante todo", "Честность прежде всего"],
    "Honest guidance and clear answers — we tell you what you need to know, not just what you want to hear.": ["Orientación honesta y respuestas claras — le decimos lo que necesita saber, no solo lo que quiere oír.", "Честные консультации и ясные ответы — мы говорим то, что вам нужно знать, а не только то, что вы хотите услышать."],
    "Unmatched insight": ["Perspectiva inigualable", "Непревзойдённая экспертиза"],
    "Financing plus construction expertise means smarter advice for homeowners and investors alike.": ["La experiencia en financiamiento y construcción significa mejores consejos tanto para propietarios como para inversionistas.", "Опыт в финансировании и строительстве означает более грамотные советы как для домовладельцев, так и для инвесторов."],
    "Strong results": ["Resultados sólidos", "Надёжные результаты"],
    "Competitive rates, a modern process, and a team that's with you to the closing table.": ["Tasas competitivas, un proceso moderno y un equipo que lo acompaña hasta la mesa de cierre.", "Конкурентные ставки, современный процесс и команда, которая рядом с вами вплоть до сделки."],

    /* ===== Apply page ===== */
    "Apply Online in Minutes": ["Solicite en Línea en Minutos", "Подайте заявку онлайн за минуты"],
    "A quick, secure application to get you pre-approved. No obligation — and a licensed loan officer reviews every submission personally.": ["Una solicitud rápida y segura para obtener su preaprobación. Sin compromiso — y un oficial de préstamos con licencia revisa cada solicitud personalmente.", "Быстрая и безопасная заявка для получения предодобрения. Без обязательств — и лицензированный кредитный специалист лично проверяет каждую заявку."],
    "Don't fill this out:": ["No complete esto:", "Не заполняйте это:"],
    "Goal": ["Objetivo", "Цель"],
    "Property": ["Propiedad", "Недвижимость"],
    "About you": ["Sobre usted", "О вас"],
    "Done": ["Listo", "Готово"],
    "What would you like to do?": ["¿Qué le gustaría hacer?", "Что вы хотите сделать?"],
    "Buy a home": ["Comprar una casa", "Купить дом"],
    "Refinance": ["Refinanciar", "Рефинансировать"],
    "Cash-out refinance": ["Refinanciamiento con retiro de efectivo", "Рефинансирование с обналичиванием"],
    "Renovation / 203(k)": ["Renovación / 203(k)", "Реновация / 203(k)"],
    "Which loan type interests you?": ["¿Qué tipo de préstamo le interesa?", "Какой тип кредита вас интересует?"],
    "Not sure yet": ["Aún no estoy seguro", "Пока не уверен"],
    "Jumbo": ["Jumbo", "Джамбо"],
    "Reverse": ["Inversa", "Обратная"],
    "Tell us about the property": ["Cuéntenos sobre la propiedad", "Расскажите о недвижимости"],
    "Property state": ["Estado de la propiedad", "Штат недвижимости"],
    "California": ["California", "Калифорния"],
    "Florida": ["Florida", "Флорида"],
    "Washington": ["Washington", "Вашингтон"],
    "Property type": ["Tipo de propiedad", "Тип недвижимости"],
    "Single-family": ["Unifamiliar", "Односемейный дом"],
    "Condo": ["Condominio", "Кондоминиум"],
    "Townhome": ["Casa adosada", "Таунхаус"],
    "Multi-unit": ["Multifamiliar", "Многоквартирный"],
    "Investment": ["Inversión", "Инвестиционная"],
    "Estimated price / value ($)": ["Precio / valor estimado ($)", "Ориентировочная цена / стоимость ($)"],
    "Down payment / equity ($)": ["Pago inicial / capital ($)", "Первоначальный взнос / капитал ($)"],
    "A little about you": ["Un poco sobre usted", "Немного о вас"],
    "Credit profile": ["Perfil crediticio", "Кредитный профиль"],
    "Excellent (740+)": ["Excelente (740+)", "Отличный (740+)"],
    "Good (680–739)": ["Bueno (680–739)", "Хороший (680–739)"],
    "Fair (620–679)": ["Regular (620–679)", "Средний (620–679)"],
    "Below 620": ["Menos de 620", "Ниже 620"],
    "Not sure": ["No estoy seguro", "Не уверен"],
    "Annual household income ($)": ["Ingreso anual del hogar ($)", "Годовой доход семьи ($)"],
    "Employment": ["Empleo", "Занятость"],
    "W-2 employee": ["Empleado W-2", "Наёмный работник (W-2)"],
    "Self-employed": ["Trabajador independiente", "Самозанятый"],
    "Retired": ["Jubilado", "На пенсии"],
    "Other": ["Otro", "Другое"],
    "First-time buyer?": ["¿Comprador primerizo?", "Покупаете впервые?"],
    "Yes": ["Sí", "Да"],
    "No": ["No", "Нет"],
    "Where can we reach you?": ["¿Dónde podemos contactarlo?", "Как с вами связаться?"],
    "Full name": ["Nombre completo", "Полное имя"],
    "Phone": ["Teléfono", "Телефон"],
    "Email": ["Correo electrónico", "Эл. почта"],
    "Best time to call": ["Mejor hora para llamar", "Удобное время для звонка"],
    "Anytime": ["Cualquier hora", "В любое время"],
    "Morning": ["Mañana", "Утро"],
    "Afternoon": ["Tarde", "День"],
    "Evening": ["Noche", "Вечер"],
    "Anything else we should know? (optional)": ["¿Algo más que debamos saber? (opcional)", "Что-нибудь ещё, что нам следует знать? (необязательно)"],
    "By submitting, you certify the information is complete and correct for the purpose of obtaining mortgage services. We respect your privacy and never sell your data.": ["Al enviar, usted certifica que la información es completa y correcta para el propósito de obtener servicios hipotecarios. Respetamos su privacidad y nunca vendemos sus datos.", "Отправляя форму, вы подтверждаете, что информация полна и верна для целей получения ипотечных услуг. Мы уважаем вашу конфиденциальность и никогда не продаём ваши данные."],
    "Application received!": ["¡Solicitud recibida!", "Заявка получена!"],
    "Thank you. A licensed loan officer from West Coast Capital Mortgage will review your information and reach out shortly. Need to talk now? Call": ["Gracias. Un oficial de préstamos con licencia de West Coast Capital Mortgage revisará su información y se comunicará con usted en breve. ¿Necesita hablar ahora? Llame al", "Спасибо. Лицензированный кредитный специалист West Coast Capital Mortgage рассмотрит вашу информацию и свяжется с вами в ближайшее время. Нужно поговорить сейчас? Позвоните"],
    "Back to home": ["Volver al inicio", "Вернуться на главную"],
    "← Back": ["← Atrás", "← Назад"],
    "Continue": ["Continuar", "Продолжить"],
    "🔒 Your information is encrypted and secure. NMLS# 2775380 · Equal Housing Lender.": ["🔒 Su información está cifrada y segura. NMLS# 2775380 · Prestamista con Igualdad de Vivienda.", "🔒 Ваша информация зашифрована и защищена. NMLS# 2775380 · Кредитор равных возможностей жилья."],

    /* ===== Blog page ===== */
    "The Mortgage Blog": ["El Blog Hipotecario", "Ипотечный блог"],
    "Plain-English guides to help you make smart, confident decisions about your home loan.": ["Guías en lenguaje sencillo para ayudarle a tomar decisiones inteligentes y seguras sobre su préstamo hipotecario.", "Понятные руководства, которые помогут вам принимать разумные и уверенные решения по ипотеке."],
    "First-Time Buyers": ["Compradores Primerizos", "Покупатели первого жилья"],
    "Buying Your First Home in California: A 2026 Roadmap": ["Comprar su primera casa en California: una hoja de ruta para 2026", "Покупка первого дома в Калифорнии: дорожная карта на 2026 год"],
    "From budgeting and credit to closing day, here's a clear, step-by-step path to your first home in today's market.": ["Desde el presupuesto y el crédito hasta el día del cierre, aquí tiene un camino claro y paso a paso hacia su primera casa en el mercado actual.", "От бюджета и кредита до дня закрытия сделки — вот понятный пошаговый путь к вашему первому дому на сегодняшнем рынке."],
    "Read more →": ["Leer más →", "Читать далее →"],
    "FHA vs Conventional: Which Loan Is Right for You?": ["FHA vs Convencional: ¿Cuál préstamo es el adecuado para usted?", "FHA или конвенциональный: какой кредит вам подходит?"],
    "We break down down payments, mortgage insurance, and credit requirements so you can choose with confidence.": ["Desglosamos los pagos iniciales, el seguro hipotecario y los requisitos de crédito para que pueda elegir con confianza.", "Мы разбираем первоначальные взносы, ипотечное страхование и требования к кредиту, чтобы вы могли выбрать уверенно."],
    "Refinancing": ["Refinanciamiento", "Рефинансирование"],
    "Should You Refinance? How to Find Your Break-Even Point": ["¿Debería refinanciar? Cómo encontrar su punto de equilibrio", "Стоит ли рефинансировать? Как найти точку окупаемости"],
    "Refinancing only pays off if you stay past your break-even. Here's how to run the numbers in minutes.": ["El refinanciamiento solo vale la pena si se queda más allá de su punto de equilibrio. Aquí le mostramos cómo calcular los números en minutos.", "Рефинансирование окупается, только если вы остаётесь дольше точки окупаемости. Вот как посчитать за минуты."],
    "VA Loan Benefits Every Veteran Should Know": ["Beneficios del préstamo VA que todo veterano debería conocer", "Преимущества кредита VA, которые должен знать каждый ветеран"],
    "$0 down, no PMI, and a streamline refinance option — make sure you're using every benefit you've earned.": ["$0 de pago inicial, sin PMI y una opción de refinanciamiento simplificado — asegúrese de usar todos los beneficios que ha ganado.", "$0 первоначального взноса, без PMI и опция упрощённого рефинансирования — убедитесь, что используете все заслуженные льготы."],
    "Jumbo Loans Explained for High-Cost California Markets": ["Préstamos Jumbo explicados para los mercados de alto costo de California", "Джамбо-кредиты для дорогих рынков Калифорнии — простыми словами"],
    "When conforming limits won't cut it, here's how jumbo financing works and what it takes to qualify.": ["Cuando los límites conformes no son suficientes, aquí le explicamos cómo funciona el financiamiento jumbo y qué se necesita para calificar.", "Когда соответствующих лимитов недостаточно — вот как работает джамбо-финансирование и что нужно для одобрения."],
    "Home Buying": ["Compra de Vivienda", "Покупка жилья"],
    "How Much House Can You Really Afford?": ["¿Cuánta casa puede pagar realmente?", "Какой дом вы действительно можете себе позволить?"],
    "Lenders use the 43% DTI guideline — but the right payment is the one that fits your life. Here's how to find it.": ["Los prestamistas usan la pauta del 43% de DTI — pero el pago correcto es el que se ajusta a su vida. Aquí le mostramos cómo encontrarlo.", "Кредиторы используют ориентир 43% DTI — но правильный платёж тот, что подходит вашей жизни. Вот как его найти."],
    "Have a question we haven't covered?": ["¿Tiene una pregunta que no hayamos cubierto?", "Есть вопрос, который мы не осветили?"],
    "Ask our AI assistant in the corner, or": ["Pregunte a nuestro asistente de IA en la esquina, o", "Спросите нашего ИИ-ассистента в углу или"],
    "reach out directly": ["contáctenos directamente", "свяжитесь напрямую"],
    "— we're always happy to help.": ["— siempre estamos felices de ayudar.", "— мы всегда рады помочь."],

    /* ===== Calculators page ===== */
    "Mortgage Calculators": ["Calculadoras Hipotecarias", "Ипотечные калькуляторы"],
    "Estimate payments, test a refinance, check affordability, and weigh renting against buying — all updated live as you type.": ["Estime pagos, pruebe un refinanciamiento, verifique su capacidad de pago y compare alquilar con comprar — todo actualizado en vivo mientras escribe.", "Оценивайте платежи, проверяйте рефинансирование, рассчитывайте доступность и сравнивайте аренду с покупкой — всё обновляется в реальном времени по мере ввода."],
    "🧮 Payment": ["🧮 Pago", "🧮 Платёж"],
    "🏡 Affordability": ["🏡 Capacidad de Pago", "🏡 Доступность"],
    "⚖️ Rent vs Buy": ["⚖️ Alquilar vs Comprar", "⚖️ Аренда или покупка"],
    "Purchase payment": ["Pago de compra", "Платёж по покупке"],
    "Home price ($)": ["Precio de la vivienda ($)", "Цена дома ($)"],
    "Down payment (%)": ["Pago inicial (%)", "Первоначальный взнос (%)"],
    "Interest rate (%)": ["Tasa de interés (%)", "Процентная ставка (%)"],
    "Loan term": ["Plazo del préstamo", "Срок кредита"],
    "30 years": ["30 años", "30 лет"],
    "20 years": ["20 años", "20 лет"],
    "15 years": ["15 años", "15 лет"],
    "10 years": ["10 años", "10 лет"],
    "Property tax (%/yr)": ["Impuesto predial (%/año)", "Налог на недвижимость (%/год)"],
    "Home insurance ($/yr)": ["Seguro de vivienda ($/año)", "Страхование жилья ($/год)"],
    "HOA ($/mo)": ["HOA ($/mes)", "HOA ($/мес)"],
    "Estimated monthly payment": ["Pago mensual estimado", "Ориентировочный ежемесячный платёж"],
    "Principal & interest": ["Capital e intereses", "Основной долг и проценты"],
    "Property tax": ["Impuesto predial", "Налог на недвижимость"],
    "Insurance + PMI": ["Seguro + PMI", "Страховка + PMI"],
    "Loan amount": ["Monto del préstamo", "Сумма кредита"],
    "Down payment": ["Pago inicial", "Первоначальный взнос"],
    "Get my real rate →": ["Obtener mi tasa real →", "Узнать мою реальную ставку →"],
    "Refinance savings": ["Ahorros por refinanciamiento", "Экономия от рефинансирования"],
    "Current balance ($)": ["Saldo actual ($)", "Текущий остаток ($)"],
    "Current rate (%)": ["Tasa actual (%)", "Текущая ставка (%)"],
    "New rate (%)": ["Nueva tasa (%)", "Новая ставка (%)"],
    "New term": ["Nuevo plazo", "Новый срок"],
    "Closing costs ($)": ["Costos de cierre ($)", "Расходы на закрытие ($)"],
    "New monthly payment": ["Nuevo pago mensual", "Новый ежемесячный платёж"],
    "Monthly savings": ["Ahorro mensual", "Ежемесячная экономия"],
    "Annual savings": ["Ahorro anual", "Годовая экономия"],
    "Break-even": ["Punto de equilibrio", "Точка окупаемости"],
    "Start refinancing →": ["Comenzar a refinanciar →", "Начать рефинансирование →"],
    "Gross annual income ($)": ["Ingreso anual bruto ($)", "Валовой годовой доход ($)"],
    "Monthly debts ($)": ["Deudas mensuales ($)", "Ежемесячные долги ($)"],
    "Down payment ($)": ["Pago inicial ($)", "Первоначальный взнос ($)"],
    "Estimated home price you can afford": ["Precio de vivienda estimado que puede pagar", "Ориентировочная цена дома, которую вы можете себе позволить"],
    "Max monthly payment": ["Pago mensual máximo", "Максимальный ежемесячный платёж"],
    "Estimated loan amount": ["Monto estimado del préstamo", "Ориентировочная сумма кредита"],
    "Based on 43% DTI": ["Basado en 43% de DTI", "На основе 43% DTI"],
    "guideline": ["pauta", "ориентир"],
    "Get pre-approved →": ["Obtener preaprobación →", "Получить предодобрение →"],
    "Rent vs Buy": ["Alquilar vs Comprar", "Аренда или покупка"],
    "Current monthly rent ($)": ["Alquiler mensual actual ($)", "Текущая ежемесячная аренда ($)"],
    "Years staying": ["Años de permanencia", "Лет проживания"],
    "Annual appreciation (%)": ["Apreciación anual (%)", "Годовой рост стоимости (%)"],
    "Verdict over your time horizon": ["Veredicto en su horizonte de tiempo", "Вывод за ваш период"],
    "Total cost of renting": ["Costo total de alquilar", "Общая стоимость аренды"],
    "Net cost of owning": ["Costo neto de ser propietario", "Чистая стоимость владения"],
    "Est. home equity built": ["Capital acumulado estimado", "Накопленный капитал (оценка)"],
    "Talk to an advisor →": ["Hable con un asesor →", "Поговорить с консультантом →"],
    "Estimates only and not an offer to lend. Actual figures depend on your full financial profile. Contact us at": ["Solo estimaciones y no una oferta de préstamo. Las cifras reales dependen de su perfil financiero completo. Contáctenos al", "Только оценки и не являются предложением кредита. Фактические цифры зависят от вашего полного финансового профиля. Свяжитесь с нами по"],
    "for a precise quote.": ["para una cotización precisa.", "для точного расчёта."],

    /* ===== Contact page ===== */
    "Let's talk about your home loan": ["Hablemos de su préstamo hipotecario", "Поговорим о вашей ипотеке"],
    "Questions about rates, programs, or your application? Reach out and a licensed loan officer will get back to you fast.": ["¿Preguntas sobre tasas, programas o su solicitud? Comuníquese y un oficial de préstamos con licencia le responderá rápidamente.", "Вопросы о ставках, программах или вашей заявке? Свяжитесь с нами, и лицензированный кредитный специалист быстро вам ответит."],
    "Request a free rate quote": ["Solicite una cotización de tasa gratuita", "Запросите бесплатный расчёт ставки"],
    "Fill this out and we'll follow up — usually the same day.": ["Complete esto y nos comunicaremos — generalmente el mismo día.", "Заполните это, и мы свяжемся — обычно в тот же день."],
    "I'm interested in": ["Estoy interesado en", "Меня интересует"],
    "A purchase loan": ["Un préstamo de compra", "Кредит на покупку"],
    "A rate quote": ["Una cotización de tasa", "Расчёт ставки"],
    "General question": ["Pregunta general", "Общий вопрос"],
    "Message": ["Mensaje", "Сообщение"],
    "Send message": ["Enviar mensaje", "Отправить сообщение"],
    "Thanks!": ["¡Gracias!", "Спасибо!"],
    "Your message has been sent. We'll be in touch shortly — or call (310) 654-1577 for immediate help.": ["Su mensaje ha sido enviado. Nos pondremos en contacto en breve — o llame al (310) 654-1577 para ayuda inmediata.", "Ваше сообщение отправлено. Мы скоро свяжемся — или позвоните (310) 654-1577 для немедленной помощи."],
    "Get in touch": ["Póngase en contacto", "Свяжитесь с нами"],
    "We're here to make your home financing simple and clear.": ["Estamos aquí para hacer que el financiamiento de su vivienda sea simple y claro.", "Мы здесь, чтобы сделать финансирование вашего жилья простым и понятным."],
    "📞 Phone": ["📞 Teléfono", "📞 Телефон"],
    "🏢 Office": ["🏢 Oficina", "🏢 Офис"],
    "Los Angeles, California": ["Los Ángeles, California", "Лос-Анджелес, Калифорния"],
    "🌎 Licensed in": ["🌎 Con licencia en", "🌎 Лицензия в"],
    "California · Florida · Washington": ["California · Florida · Washington", "Калифорния · Флорида · Вашингтон"],
    "📋 Licensing": ["📋 Licencias", "📋 Лицензирование"],
    "NMLS# 2775380 · CA Broker since 2009": ["NMLS# 2775380 · Corredor de CA desde 2009", "NMLS# 2775380 · Брокер CA с 2009"],
    "Start an application →": ["Comenzar una solicitud →", "Начать заявку →"],

    /* ===== Conventional page ===== */
    "Conventional Mortgage": ["Hipoteca Convencional", "Конвенциональная ипотека"],
    "Flexible terms and competitive rates with as little as 3% down for qualified buyers in California, Florida and Washington.": ["Términos flexibles y tasas competitivas con tan solo 3% de pago inicial para compradores calificados en California, Florida y Washington.", "Гибкие условия и конкурентные ставки с первоначальным взносом всего от 3% для квалифицированных покупателей в Калифорнии, Флориде и Вашингтоне."],
    "From 3% Down": ["Desde 3% inicial", "От 3% взноса"],
    "Low down-payment options": ["Opciones de pago inicial bajo", "Варианты с низким первоначальным взносом"],
    "No Upfront MI": ["Sin MI inicial", "Без авансового MI"],
    "Unlike FHA loans": ["A diferencia de los préstamos FHA", "В отличие от кредитов FHA"],
    "Any Property": ["Cualquier propiedad", "Любая недвижимость"],
    "Primary, second, investment": ["Principal, segunda, inversión", "Основное, второе, инвестиционное"],
    "Cancel PMI": ["Cancelar PMI", "Отмена PMI"],
    "Once you hit 20% equity": ["Una vez que alcance el 20% de capital", "При достижении 20% капитала"],
    "A conventional mortgage is one that's not guaranteed or insured by the federal government. Instead, these loans are available through private lenders such as banks, credit unions, and mortgage companies — and they remain the most popular financing choice for well-qualified buyers.": ["Una hipoteca convencional es aquella que no está garantizada ni asegurada por el gobierno federal. En cambio, estos préstamos están disponibles a través de prestamistas privados como bancos, cooperativas de crédito y compañías hipotecarias — y siguen siendo la opción de financiamiento más popular para compradores bien calificados.", "Конвенциональная ипотека — это кредит, который не гарантируется и не страхуется федеральным правительством. Такие кредиты предоставляются частными кредиторами — банками, кредитными союзами и ипотечными компаниями — и остаются самым популярным вариантом финансирования для хорошо квалифицированных покупателей."],
    "What is a conventional mortgage?": ["¿Qué es una hipoteca convencional?", "Что такое конвенциональная ипотека?"],
    "Because they aren't government-backed, conventional loans follow guidelines set by Fannie Mae and Freddie Mac. They offer flexible terms, competitive rates, and can be used for primary homes, second homes, and investment properties.": ["Como no están respaldados por el gobierno, los préstamos convencionales siguen las pautas establecidas por Fannie Mae y Freddie Mac. Ofrecen términos flexibles, tasas competitivas y se pueden usar para viviendas principales, segundas viviendas y propiedades de inversión.", "Поскольку они не обеспечены государством, конвенциональные кредиты следуют правилам Fannie Mae и Freddie Mac. Они предлагают гибкие условия, конкурентные ставки и подходят для основного жилья, второго жилья и инвестиционной недвижимости."],
    "Down payments can start as low as 3% for qualifying first-time buyers, though putting 20% down lets you avoid private mortgage insurance (PMI) entirely.": ["Los pagos iniciales pueden comenzar desde tan solo 3% para compradores primerizos que califiquen, aunque dar un 20% de pago inicial le permite evitar por completo el seguro hipotecario privado (PMI).", "Первоначальный взнос может начинаться всего от 3% для квалифицированных покупателей первого жилья, хотя взнос в 20% позволяет полностью избежать частного ипотечного страхования (PMI)."],
    "Conventional mortgage requirements": ["Requisitos para una hipoteca convencional", "Требования для конвенциональной ипотеки"],
    "A credit score of at least 620 (higher scores earn better rates)": ["Un puntaje de crédito de al menos 620 (puntajes más altos obtienen mejores tasas)", "Кредитный рейтинг не менее 620 (более высокий рейтинг — лучшие ставки)"],
    "A down payment of 3%–20% depending on the program": ["Un pago inicial del 3%–20% según el programa", "Первоначальный взнос 3%–20% в зависимости от программы"],
    "A debt-to-income ratio generally at or below 43%": ["Una relación deuda-ingreso generalmente igual o inferior al 43%", "Отношение долга к доходу, как правило, не выше 43%"],
    "Steady, verifiable income and employment history": ["Ingresos e historial laboral estables y verificables", "Стабильный, подтверждаемый доход и трудовой стаж"],
    "Sufficient reserves for some loan amounts": ["Reservas suficientes para algunos montos de préstamo", "Достаточные резервы для некоторых сумм кредита"],
    "Private mortgage insurance (PMI)": ["Seguro hipotecario privado (PMI)", "Частное ипотечное страхование (PMI)"],
    "If your down payment is below 20%, lenders typically require PMI to protect against default. The good news: PMI can be cancelled once you reach 20% equity, lowering your monthly payment over time.": ["Si su pago inicial es inferior al 20%, los prestamistas generalmente requieren PMI para protegerse contra el incumplimiento. La buena noticia: el PMI se puede cancelar una vez que alcance el 20% de capital, reduciendo su pago mensual con el tiempo.", "Если ваш первоначальный взнос меньше 20%, кредиторы обычно требуют PMI для защиты от дефолта. Хорошая новость: PMI можно отменить при достижении 20% капитала, со временем снизив ежемесячный платёж."],
    "Advantages of a conventional loan": ["Ventajas de un préstamo convencional", "Преимущества конвенционального кредита"],
    "Available for primary, secondary, and investment properties": ["Disponible para propiedades principales, secundarias y de inversión", "Доступен для основного, второго и инвестиционного жилья"],
    "No upfront mortgage insurance fee like FHA loans": ["Sin cargo inicial de seguro hipotecario como en los préstamos FHA", "Без авансового взноса за ипотечное страхование, как в кредитах FHA"],
    "PMI can be removed at 20% equity": ["El PMI se puede eliminar al alcanzar el 20% de capital", "PMI можно убрать при 20% капитала"],
    "Competitive rates for strong credit profiles": ["Tasas competitivas para perfiles de crédito sólidos", "Конкурентные ставки для сильного кредитного профиля"],
    "Higher loan limits than FHA in most areas": ["Límites de préstamo más altos que FHA en la mayoría de las áreas", "Более высокие лимиты кредита, чем у FHA, в большинстве районов"],
    "Frequently asked questions": ["Preguntas frecuentes", "Часто задаваемые вопросы"],
    "How much do I need to put down?": ["¿Cuánto necesito dar de pago inicial?", "Какой нужен первоначальный взнос?"],
    "As little as 3% for qualified first-time buyers, but 20% avoids PMI. We'll help you find the sweet spot for your budget.": ["Tan solo 3% para compradores primerizos calificados, pero 20% evita el PMI. Le ayudaremos a encontrar el punto ideal para su presupuesto.", "Всего от 3% для квалифицированных покупателей первого жилья, но 20% избавляет от PMI. Мы поможем найти оптимальный вариант для вашего бюджета."],
    "What credit score do I need?": ["¿Qué puntaje de crédito necesito?", "Какой кредитный рейтинг мне нужен?"],
    "Generally 620 or higher. Stronger scores unlock lower rates — we can review your profile for free.": ["Generalmente 620 o más. Los puntajes más altos desbloquean tasas más bajas — podemos revisar su perfil gratis.", "Как правило, 620 или выше. Более высокий рейтинг открывает более низкие ставки — мы можем бесплатно оценить ваш профиль."],
    "Ready to start?": ["¿Listo para empezar?", "Готовы начать?"],
    "Get pre-approved in minutes.": ["Obtenga su preaprobación en minutos.", "Получите предодобрение за минуты."],

    /* ===== FHA page ===== */
    "FHA Home Loan": ["Préstamo Hipotecario FHA", "Жилищный кредит FHA"],
    "Just 3.5% down and flexible credit requirements — a favorite among first-time homebuyers in Los Angeles and beyond.": ["Solo 3.5% de pago inicial y requisitos de crédito flexibles — el favorito entre los compradores primerizos en Los Ángeles y más allá.", "Всего 3,5% первоначального взноса и гибкие требования к кредиту — фаворит среди покупателей первого жилья в Лос-Анджелесе и за его пределами."],
    "3.5% Down": ["3.5% inicial", "Взнос 3,5%"],
    "Low entry point": ["Punto de entrada bajo", "Низкий порог входа"],
    "580 Score": ["Puntaje 580", "Рейтинг 580"],
    "Flexible credit": ["Crédito flexible", "Гибкие требования к кредиту"],
    "Gift Funds OK": ["Fondos de regalo OK", "Подаренные средства — ОК"],
    "For down payment": ["Para el pago inicial", "Для первоначального взноса"],
    "First-Timers": ["Primerizos", "Покупатели впервые"],
    "Most popular choice": ["La opción más popular", "Самый популярный выбор"],
    "FHA home loans are insured by the Federal Housing Administration and provided by FHA-approved lenders. With low down payments and forgiving credit guidelines, they're one of the most accessible paths to homeownership — especially for first-time buyers.": ["Los préstamos hipotecarios FHA están asegurados por la Administración Federal de Vivienda y otorgados por prestamistas aprobados por FHA. Con pagos iniciales bajos y pautas de crédito flexibles, son uno de los caminos más accesibles hacia la propiedad de vivienda — especialmente para compradores primerizos.", "Жилищные кредиты FHA застрахованы Федеральной жилищной администрацией и предоставляются одобренными FHA кредиторами. Благодаря низкому первоначальному взносу и мягким требованиям к кредиту это один из самых доступных путей к собственному жилью — особенно для покупателей первого жилья."],
    "What is an FHA home loan?": ["¿Qué es un préstamo hipotecario FHA?", "Что такое жилищный кредит FHA?"],
    "FHA loans come with fixed terms of 15 or 30 years and are a popular choice among first-time homebuyers as well as buyers with less-than-perfect credit. Because the government insures the loan, lenders can offer more flexible qualification standards.": ["Los préstamos FHA vienen con plazos fijos de 15 o 30 años y son una opción popular entre compradores primerizos, así como compradores con un crédito no perfecto. Como el gobierno asegura el préstamo, los prestamistas pueden ofrecer estándares de calificación más flexibles.", "Кредиты FHA имеют фиксированные сроки 15 или 30 лет и популярны как среди покупателей первого жилья, так и среди заёмщиков с неидеальной кредитной историей. Поскольку кредит страхует государство, кредиторы могут предлагать более гибкие требования к одобрению."],
    "Mortgage insurance premiums (MIP)": ["Primas de seguro hipotecario (MIP)", "Взносы по ипотечному страхованию (MIP)"],
    "FHA loans require both an upfront mortgage insurance premium and an annual premium paid monthly. This insurance is what allows the low down payment and flexible credit — factor it into your monthly cost when comparing to conventional financing.": ["Los préstamos FHA requieren tanto una prima inicial de seguro hipotecario como una prima anual pagada mensualmente. Este seguro es lo que permite el bajo pago inicial y el crédito flexible — considérelo en su costo mensual al compararlo con el financiamiento convencional.", "Кредиты FHA требуют как авансового взноса по ипотечному страхованию, так и ежегодного взноса, уплачиваемого ежемесячно. Именно эта страховка позволяет низкий первоначальный взнос и гибкие требования к кредиту — учитывайте её в ежемесячных расходах при сравнении с конвенциональным финансированием."],
    "How to qualify for an FHA loan": ["Cómo calificar para un préstamo FHA", "Как получить одобрение по кредиту FHA"],
    "A credit score as low as 580 with 3.5% down (or 500–579 with 10% down)": ["Un puntaje de crédito desde 580 con 3.5% de pago inicial (o 500–579 con 10% de pago inicial)", "Кредитный рейтинг от 580 при взносе 3,5% (или 500–579 при взносе 10%)"],
    "A debt-to-income ratio typically up to 43% (sometimes higher with compensating factors)": ["Una relación deuda-ingreso típicamente de hasta 43% (a veces más con factores compensatorios)", "Отношение долга к доходу обычно до 43% (иногда выше при компенсирующих факторах)"],
    "Steady employment and verifiable income": ["Empleo estable e ingresos verificables", "Стабильная занятость и подтверждаемый доход"],
    "The home must be your primary residence": ["La vivienda debe ser su residencia principal", "Жильё должно быть вашим основным местом проживания"],
    "The property must meet FHA minimum standards": ["La propiedad debe cumplir con los estándares mínimos de FHA", "Недвижимость должна соответствовать минимальным стандартам FHA"],
    "Advantages of FHA loans": ["Ventajas de los préstamos FHA", "Преимущества кредитов FHA"],
    "Down payments as low as 3.5%": ["Pagos iniciales desde 3.5%", "Первоначальный взнос от 3,5%"],
    "Flexible credit requirements": ["Requisitos de crédito flexibles", "Гибкие требования к кредиту"],
    "Gift funds allowed for the down payment": ["Se permiten fondos de regalo para el pago inicial", "Для первоначального взноса допускаются подаренные средства"],
    "Assumable by a future buyer": ["Transferible a un futuro comprador", "Может быть переоформлен на будущего покупателя"],
    "Great for first-time buyers": ["Excelente para compradores primerizos", "Отлично подходит для покупателей первого жилья"],
    "Can I use gift money for my down payment?": ["¿Puedo usar dinero de regalo para mi pago inicial?", "Можно ли использовать подаренные деньги для первоначального взноса?"],
    "Yes — FHA allows your entire down payment to come from an eligible gift, such as from family.": ["Sí — FHA permite que todo su pago inicial provenga de un regalo elegible, como de un familiar.", "Да — FHA разрешает, чтобы весь первоначальный взнос был получен в виде подходящего подарка, например от семьи."],
    "Is FHA only for first-time buyers?": ["¿Es FHA solo para compradores primerizos?", "Только ли для покупателей первого жилья предназначен FHA?"],
    "No. While popular with first-timers, FHA loans are available to any qualified buyer purchasing a primary residence.": ["No. Aunque son populares entre los primerizos, los préstamos FHA están disponibles para cualquier comprador calificado que adquiera una residencia principal.", "Нет. Хотя они популярны у покупателей первого жилья, кредиты FHA доступны любому квалифицированному покупателю основного жилья."],

    /* ===== Fixed-Rate page ===== */
    "Fixed-Rate Mortgage": ["Hipoteca de Tasa Fija", "Ипотека с фиксированной ставкой"],
    "Predictable payments that never change — the most popular financing for buyers who value stability.": ["Pagos predecibles que nunca cambian — el financiamiento más popular para compradores que valoran la estabilidad.", "Предсказуемые платежи, которые никогда не меняются — самое популярное финансирование для тех, кто ценит стабильность."],
    "Locked Rate": ["Tasa Fija", "Зафиксированная ставка"],
    "Never changes": ["Nunca cambia", "Никогда не меняется"],
    "Rate Protection": ["Protección de Tasa", "Защита ставки"],
    "Beat future hikes": ["Anticipe futuras alzas", "Защита от будущих повышений"],
    "Easy Budgeting": ["Presupuesto Fácil", "Простое планирование бюджета"],
    "Same payment": ["Mismo pago", "Один и тот же платёж"],
    "10–30 Yrs": ["10–30 años", "10–30 лет"],
    "Choose your term": ["Elija su plazo", "Выберите срок"],
    "A fixed-rate mortgage has an interest rate that stays the same for the entire life of the loan. Your principal-and-interest payment never changes, which is exactly why it's the most popular type of home financing — it offers predictability you can plan your life around.": ["Una hipoteca de tasa fija tiene una tasa de interés que permanece igual durante toda la vida del préstamo. Su pago de capital e intereses nunca cambia, que es exactamente por lo que es el tipo de financiamiento de vivienda más popular — ofrece una previsibilidad en torno a la cual puede planificar su vida.", "У ипотеки с фиксированной ставкой процентная ставка остаётся неизменной на протяжении всего срока кредита. Ваш платёж по основному долгу и процентам никогда не меняется — именно поэтому это самый популярный вид жилищного финансирования: он даёт предсказуемость, вокруг которой можно планировать жизнь."],
    "What is a fixed-rate mortgage?": ["¿Qué es una hipoteca de tasa fija?", "Что такое ипотека с фиксированной ставкой?"],
    "With a fixed rate, market swings don't touch your monthly principal and interest. Whether rates rise or fall, your payment is locked, making budgeting simple for the long haul.": ["Con una tasa fija, las fluctuaciones del mercado no afectan su capital e intereses mensuales. Ya sea que las tasas suban o bajen, su pago está fijo, lo que simplifica la planificación a largo plazo.", "При фиксированной ставке колебания рынка не влияют на ваш ежемесячный платёж по основному долгу и процентам. Растут ставки или падают — ваш платёж зафиксирован, что упрощает долгосрочное планирование бюджета."],
    "Types of fixed-rate mortgages": ["Tipos de hipotecas de tasa fija", "Виды ипотеки с фиксированной ставкой"],
    "30-year fixed — the lowest monthly payment, most popular": ["Fija a 30 años — el pago mensual más bajo, la más popular", "Фиксированная 30 лет — самый низкий ежемесячный платёж, самая популярная"],
    "20-year fixed — a middle ground on term and interest": ["Fija a 20 años — un punto medio en plazo e intereses", "Фиксированная 20 лет — золотая середина по сроку и процентам"],
    "15-year fixed — higher payment, far less interest paid overall": ["Fija a 15 años — pago más alto, mucho menos interés pagado en total", "Фиксированная 15 лет — выше платёж, но гораздо меньше процентов в итоге"],
    "10-year fixed — fastest payoff for aggressive savers": ["Fija a 10 años — el pago más rápido para ahorradores agresivos", "Фиксированная 10 лет — самое быстрое погашение для активных накопителей"],
    "Advantages of a fixed-rate mortgage": ["Ventajas de una hipoteca de tasa fija", "Преимущества ипотеки с фиксированной ставкой"],
    "Payment stability for the life of the loan": ["Estabilidad de pago durante toda la vida del préstamo", "Стабильность платежа на весь срок кредита"],
    "Protection from rising interest rates": ["Protección contra el aumento de las tasas de interés", "Защита от роста процентных ставок"],
    "Easy, predictable budgeting": ["Presupuesto fácil y predecible", "Простое и предсказуемое планирование бюджета"],
    "Simple to understand": ["Fácil de entender", "Просто понять"],
    "Drawbacks to consider": ["Desventajas a considerar", "Недостатки, которые стоит учесть"],
    "Fixed rates can start slightly higher than the initial rate on an adjustable-rate mortgage. If you plan to move or refinance within a few years, an ARM may save money short-term — we'll help you weigh it.": ["Las tasas fijas pueden comenzar ligeramente más altas que la tasa inicial de una hipoteca de tasa ajustable. Si planea mudarse o refinanciar dentro de unos años, una ARM podría ahorrarle dinero a corto plazo — le ayudaremos a evaluarlo.", "Фиксированные ставки могут стартовать чуть выше начальной ставки по ипотеке с переменной ставкой. Если вы планируете переехать или рефинансировать в течение нескольких лет, ARM может сэкономить деньги в краткосрочной перспективе — мы поможем взвесить варианты."],
    "Which term is right for me?": ["¿Qué plazo es el adecuado para mí?", "Какой срок мне подходит?"],
    "If you want the lowest payment, go 30-year. If you want to pay less interest and own sooner, consider 15-year. We'll model both.": ["Si quiere el pago más bajo, elija 30 años. Si quiere pagar menos intereses y ser propietario antes, considere 15 años. Modelaremos ambos.", "Если хотите самый низкий платёж — выбирайте 30 лет. Если хотите платить меньше процентов и быстрее стать владельцем — рассмотрите 15 лет. Мы рассчитаем оба варианта."],
    "Can I pay it off early?": ["¿Puedo pagarla anticipadamente?", "Можно ли погасить досрочно?"],
    "Yes — our fixed-rate loans have no prepayment penalty, so extra payments shorten your loan and save interest.": ["Sí — nuestros préstamos de tasa fija no tienen penalización por pago anticipado, por lo que los pagos adicionales acortan su préstamo y ahorran intereses.", "Да — по нашим кредитам с фиксированной ставкой нет штрафа за досрочное погашение, поэтому дополнительные платежи сокращают срок кредита и экономят на процентах."],

    /* ===== Jumbo page ===== */
    "Jumbo Mortgage": ["Hipoteca Jumbo", "Джамбо-ипотека"],
    "Financing above conforming loan limits — ideal for higher-priced homes across California, Florida and Washington.": ["Financiamiento por encima de los límites de préstamo conformes — ideal para viviendas de mayor precio en California, Florida y Washington.", "Финансирование сверх соответствующих лимитов кредита — идеально для дорогого жилья в Калифорнии, Флориде и Вашингтоне."],
    "High Limits": ["Límites Altos", "Высокие лимиты"],
    "Above conforming": ["Por encima de lo conforme", "Сверх соответствующих лимитов"],
    "Luxury Homes": ["Viviendas de Lujo", "Элитное жильё"],
    "High-cost areas": ["Áreas de alto costo", "Дорогие районы"],
    "Fixed or ARM": ["Fija o ARM", "Фиксированная или ARM"],
    "Flexible structures": ["Estructuras flexibles", "Гибкие структуры"],
    "Competitive": ["Competitiva", "Конкурентная"],
    "Great rates for strong files": ["Excelentes tasas para perfiles sólidos", "Отличные ставки для сильных заявок"],
    "A jumbo home loan is financing that exceeds the limits set by the Federal Housing Finance Agency. Although they're non-conforming, jumbo loans still follow Consumer Financial Protection Bureau guidelines and are essential for purchasing higher-priced properties.": ["Un préstamo hipotecario jumbo es un financiamiento que excede los límites establecidos por la Agencia Federal de Financiamiento de Vivienda. Aunque son no conformes, los préstamos jumbo aún siguen las pautas de la Oficina de Protección Financiera del Consumidor y son esenciales para comprar propiedades de mayor precio.", "Джамбо-кредит — это финансирование, превышающее лимиты, установленные Федеральным агентством жилищного финансирования (FHFA). Хотя они являются несоответствующими, джамбо-кредиты по-прежнему следуют правилам Бюро финансовой защиты потребителей и необходимы для покупки более дорогой недвижимости."],
    "What is a jumbo mortgage?": ["¿Qué es una hipoteca jumbo?", "Что такое джамбо-ипотека?"],
    "When a home's price exceeds the conforming loan limit for your county, a jumbo loan bridges the gap. These loans let qualified buyers finance luxury and high-cost-area homes that conventional limits won't cover.": ["Cuando el precio de una vivienda excede el límite de préstamo conforme de su condado, un préstamo jumbo cubre la diferencia. Estos préstamos permiten a los compradores calificados financiar viviendas de lujo y en áreas de alto costo que los límites convencionales no cubren.", "Когда цена дома превышает соответствующий лимит кредита для вашего округа, джамбо-кредит покрывает разницу. Такие кредиты позволяют квалифицированным покупателям финансировать элитное жильё и дома в дорогих районах, которые не покрывают конвенциональные лимиты."],
    "Jumbo vs conforming loan limits": ["Límites de préstamo jumbo vs conformes", "Джамбо против соответствующих лимитов кредита"],
    "Conforming limits are set annually and vary by county. Loans above that threshold are 'jumbo.' In high-cost California markets, jumbo financing is common for primary homes — not just luxury estates.": ["Los límites conformes se establecen anualmente y varían según el condado. Los préstamos por encima de ese umbral son 'jumbo'. En los mercados de alto costo de California, el financiamiento jumbo es común para viviendas principales — no solo para propiedades de lujo.", "Соответствующие лимиты устанавливаются ежегодно и различаются по округам. Кредиты выше этого порога называются «джамбо». На дорогих рынках Калифорнии джамбо-финансирование распространено и для основного жилья — не только для элитных особняков."],
    "How to qualify for a jumbo mortgage": ["Cómo calificar para una hipoteca jumbo", "Как получить одобрение по джамбо-ипотеке"],
    "A strong credit score, generally 700 or higher": ["Un puntaje de crédito sólido, generalmente 700 o más", "Высокий кредитный рейтинг, как правило, 700 или выше"],
    "A larger down payment (often 10–20%+)": ["Un pago inicial mayor (a menudo 10–20%+)", "Более крупный первоначальный взнос (часто 10–20%+)"],
    "Significant cash reserves": ["Reservas de efectivo significativas", "Значительные денежные резервы"],
    "A low debt-to-income ratio": ["Una relación deuda-ingreso baja", "Низкое отношение долга к доходу"],
    "Full documentation of income and assets": ["Documentación completa de ingresos y activos", "Полная документация по доходам и активам"],
    "Benefits of a jumbo mortgage": ["Beneficios de una hipoteca jumbo", "Преимущества джамбо-ипотеки"],
    "Finance high-value properties in a single loan": ["Financie propiedades de alto valor en un solo préstamo", "Финансируйте дорогую недвижимость одним кредитом"],
    "Competitive rates for strong borrowers": ["Tasas competitivas para prestatarios sólidos", "Конкурентные ставки для надёжных заёмщиков"],
    "Fixed and adjustable options": ["Opciones fijas y ajustables", "Фиксированные и переменные варианты"],
    "Available for primary, second, and investment homes": ["Disponible para viviendas principales, segundas y de inversión", "Доступно для основного, второго и инвестиционного жилья"],
    "How much can I borrow?": ["¿Cuánto puedo pedir prestado?", "Сколько я могу занять?"],
    "Jumbo loan amounts can run well into the millions depending on your profile. Let's review what you'd qualify for.": ["Los montos de préstamos jumbo pueden llegar a varios millones según su perfil. Revisemos para cuánto calificaría.", "Суммы джамбо-кредитов могут достигать миллионов в зависимости от вашего профиля. Давайте посмотрим, на что вы можете претендовать."],
    "Are jumbo rates higher?": ["¿Son más altas las tasas jumbo?", "Выше ли ставки по джамбо-кредитам?"],
    "Not necessarily — for strong borrowers, jumbo rates are often very competitive with conforming loans.": ["No necesariamente — para prestatarios sólidos, las tasas jumbo suelen ser muy competitivas con las de los préstamos conformes.", "Не обязательно — для надёжных заёмщиков ставки по джамбо-кредитам часто вполне конкурентны со ставками по соответствующим кредитам."],

    /* ===== Refinance page ===== */
    "Mortgage Refinancing": ["Refinanciamiento Hipotecario", "Рефинансирование ипотеки"],
    "Lower your rate, shorten your term, or tap your home's equity by replacing your current loan with a better one.": ["Reduzca su tasa, acorte su plazo o aproveche el valor acumulado de su vivienda reemplazando su préstamo actual por uno mejor.", "Снизьте ставку, сократите срок или используйте капитал дома, заменив текущий кредит на более выгодный."],
    "Lower Rate": ["Tasa Más Baja", "Ниже ставка"],
    "Cut your payment": ["Reduzca su pago", "Снизьте платёж"],
    "Shorter Term": ["Plazo Más Corto", "Короче срок"],
    "Pay off sooner": ["Pague antes", "Погасите быстрее"],
    "Cash Out": ["Retiro de Efectivo", "Обналичивание"],
    "Use your equity": ["Use su capital", "Используйте капитал"],
    "FHA/VA Streamline": ["Simplificado FHA/VA", "Упрощённое FHA/VA"],
    "Fast & simple": ["Rápido y simple", "Быстро и просто"],
    "When you refinance, you replace your current home loan with a new one. Like your original mortgage, refinancing requires an application, underwriting, and closing — but the payoff can be a lower rate, a shorter term, or cash from your equity.": ["Cuando refinancia, reemplaza su préstamo hipotecario actual por uno nuevo. Al igual que su hipoteca original, el refinanciamiento requiere una solicitud, suscripción y cierre — pero la recompensa puede ser una tasa más baja, un plazo más corto o efectivo de su capital.", "При рефинансировании вы заменяете текущий жилищный кредит новым. Как и при первоначальной ипотеке, рефинансирование требует заявки, андеррайтинга и закрытия сделки — но в результате вы можете получить более низкую ставку, более короткий срок или наличные из капитала."],
    "The refinancing process": ["El proceso de refinanciamiento", "Процесс рефинансирования"],
    "You file an application, go through underwriting, and close on the new loan — which pays off and replaces the old one. We make each step clear and handle the heavy lifting so it's far simpler than your first mortgage felt.": ["Usted presenta una solicitud, pasa por la suscripción y cierra el nuevo préstamo — que paga y reemplaza el anterior. Aclaramos cada paso y nos encargamos del trabajo pesado para que sea mucho más simple de lo que sintió su primera hipoteca.", "Вы подаёте заявку, проходите андеррайтинг и закрываете новый кредит — который погашает и заменяет старый. Мы делаем каждый шаг понятным и берём на себя основную работу, так что это намного проще, чем ваша первая ипотека."],
    "Reasons to refinance": ["Razones para refinanciar", "Причины для рефинансирования"],
    "Lower your interest rate and monthly payment": ["Reducir su tasa de interés y pago mensual", "Снизить процентную ставку и ежемесячный платёж"],
    "Shorten your loan term to pay off faster": ["Acortar el plazo de su préstamo para pagar más rápido", "Сократить срок кредита для более быстрого погашения"],
    "Switch from an adjustable to a fixed rate": ["Cambiar de una tasa ajustable a una fija", "Перейти с переменной ставки на фиксированную"],
    "Take cash out for renovations or debt consolidation": ["Obtener efectivo para renovaciones o consolidación de deudas", "Получить наличные на ремонт или консолидацию долгов"],
    "Remove mortgage insurance once you have equity": ["Eliminar el seguro hipotecario una vez que tenga capital", "Убрать ипотечное страхование при наличии капитала"],
    "Types of refinancing": ["Tipos de refinanciamiento", "Виды рефинансирования"],
    "Rate-and-term refinance — change your rate, term, or both": ["Refinanciamiento de tasa y plazo — cambie su tasa, plazo o ambos", "Рефинансирование ставки и срока — измените ставку, срок или оба"],
    "Cash-out refinance — borrow against your equity": ["Refinanciamiento con retiro de efectivo — pida prestado contra su capital", "Рефинансирование с обналичиванием — займ под капитал дома"],
    "Streamline refinance — simplified process for FHA and VA loans": ["Refinanciamiento simplificado — proceso simplificado para préstamos FHA y VA", "Упрощённое рефинансирование — упрощённый процесс для кредитов FHA и VA"],
    "Is it worth it?": ["¿Vale la pena?", "Стоит ли это того?"],
    "The key is your break-even point — when monthly savings cover your closing costs. Use our refinance calculator to see your number, then let us confirm it with a real quote.": ["La clave es su punto de equilibrio — cuando los ahorros mensuales cubren sus costos de cierre. Use nuestra calculadora de refinanciamiento para ver su número, luego permítanos confirmarlo con una cotización real.", "Главное — ваша точка окупаемости, когда ежемесячная экономия покрывает расходы на закрытие сделки. Воспользуйтесь нашим калькулятором рефинансирования, чтобы увидеть свою цифру, а затем мы подтвердим её реальным расчётом."],
    "When should I refinance?": ["¿Cuándo debería refinanciar?", "Когда стоит рефинансировать?"],
    "Often when rates drop at least 0.5–1% below your current rate, or when your goals change. We'll run the math with you for free.": ["A menudo cuando las tasas bajan al menos 0.5–1% por debajo de su tasa actual, o cuando cambian sus objetivos. Haremos los cálculos con usted gratis.", "Обычно когда ставки падают как минимум на 0,5–1% ниже вашей текущей ставки или когда меняются ваши цели. Мы бесплатно сделаем расчёты вместе с вами."],
    "How long does it take?": ["¿Cuánto tiempo toma?", "Сколько времени это занимает?"],
    "Most refinances close in roughly 30 days. Streamline options for FHA/VA can be faster.": ["La mayoría de los refinanciamientos se cierran en aproximadamente 30 días. Las opciones simplificadas para FHA/VA pueden ser más rápidas.", "Большинство рефинансирований закрываются примерно за 30 дней. Упрощённые варианты для FHA/VA могут быть быстрее."],

    /* ===== Renovation 203(k) page ===== */
    "Renovation Mortgage 203(k)": ["Hipoteca de Renovación 203(k)", "Ипотека на реновацию 203(k)"],
    "Buy or refinance a home that needs work and roll the renovation costs into a single FHA-insured loan.": ["Compre o refinancie una vivienda que necesita arreglos e incluya los costos de renovación en un solo préstamo asegurado por FHA.", "Купите или рефинансируйте дом, требующий ремонта, и включите расходы на реновацию в один кредит, застрахованный FHA."],
    "Buy + Renovate": ["Comprar + Renovar", "Покупка + Ремонт"],
    "One loan": ["Un solo préstamo", "Один кредит"],
    "Fixer-Uppers": ["Casas para Remodelar", "Дома под ремонт"],
    "Turn into dream homes": ["Conviértalas en la casa de sus sueños", "Превратите в дом мечты"],
    "FHA-backed": ["Respaldado por FHA", "Под гарантией FHA"],
    "Funds in Escrow": ["Fondos en Depósito", "Средства на эскроу-счёте"],
    "Released as you go": ["Liberados a medida que avanza", "Выдаются по мере выполнения работ"],
    "With a 203(k) loan, you can buy or refinance a home that needs repairs and fold the renovation costs right into your mortgage. Because these loans are insured by the Federal Housing Administration, they often come with more lenient qualification requirements than other renovation financing.": ["Con un préstamo 203(k), puede comprar o refinanciar una vivienda que necesita reparaciones e incorporar los costos de renovación directamente en su hipoteca. Como estos préstamos están asegurados por la Administración Federal de Vivienda, a menudo tienen requisitos de calificación más flexibles que otros financiamientos de renovación.", "С кредитом 203(k) вы можете купить или рефинансировать дом, нуждающийся в ремонте, и включить расходы на реновацию прямо в ипотеку. Поскольку эти кредиты застрахованы Федеральной жилищной администрацией, они часто имеют более мягкие требования к одобрению, чем другие виды финансирования ремонта."],
    "What is a 203(k) renovation mortgage?": ["¿Qué es una hipoteca de renovación 203(k)?", "Что такое ипотека на реновацию 203(k)?"],
    "Instead of juggling a purchase loan plus a separate construction loan, the 203(k) combines the home price and the renovation budget into one FHA-insured mortgage with one monthly payment.": ["En lugar de manejar un préstamo de compra más un préstamo de construcción por separado, el 203(k) combina el precio de la vivienda y el presupuesto de renovación en una sola hipoteca asegurada por FHA con un solo pago mensual.", "Вместо того чтобы совмещать кредит на покупку и отдельный строительный кредит, 203(k) объединяет цену дома и бюджет на реновацию в одну застрахованную FHA ипотеку с одним ежемесячным платежом."],
    "Limited vs standard 203(k)": ["203(k) limitado vs estándar", "Ограниченный против стандартного 203(k)"],
    "Limited 203(k) — for smaller projects up to a set cost cap; ideal for cosmetic updates and minor repairs": ["203(k) limitado — para proyectos más pequeños hasta un límite de costo establecido; ideal para mejoras cosméticas y reparaciones menores", "Ограниченный 203(k) — для небольших проектов в пределах установленного лимита; идеален для косметических обновлений и мелкого ремонта"],
    "Standard 203(k) — for major renovations, structural work, and larger budgets, with a HUD consultant involved": ["203(k) estándar — para renovaciones mayores, trabajos estructurales y presupuestos más grandes, con la participación de un consultor de HUD", "Стандартный 203(k) — для крупных реноваций, конструктивных работ и больших бюджетов, с участием консультанта HUD"],
    "How to qualify for a 203(k)": ["Cómo calificar para un 203(k)", "Как получить одобрение по 203(k)"],
    "Meet FHA credit and down-payment guidelines (as low as 3.5% down)": ["Cumplir con las pautas de crédito y pago inicial de FHA (desde 3.5% de pago inicial)", "Соответствовать требованиям FHA по кредиту и первоначальному взносу (от 3,5%)"],
    "Renovation plans and contractor bids are required": ["Se requieren planes de renovación y presupuestos de contratistas", "Требуются планы реновации и сметы подрядчиков"],
    "The property must meet FHA standards after the work": ["La propiedad debe cumplir con los estándares de FHA después del trabajo", "После работ недвижимость должна соответствовать стандартам FHA"],
    "The 203(k) process": ["El proceso 203(k)", "Процесс 203(k)"],
    "You get approved based on the home's projected after-renovation value, choose licensed contractors, and the renovation funds are held in escrow and released as work is completed. We coordinate the moving parts with you.": ["Usted obtiene la aprobación según el valor proyectado de la vivienda después de la renovación, elige contratistas con licencia, y los fondos de renovación se mantienen en depósito y se liberan a medida que se completa el trabajo. Coordinamos todos los detalles con usted.", "Вы получаете одобрение на основе прогнозируемой стоимости дома после реновации, выбираете лицензированных подрядчиков, а средства на ремонт хранятся на эскроу-счёте и выдаются по мере выполнения работ. Мы координируем все этапы вместе с вами."],
    "Can I buy a fixer-upper with this?": ["¿Puedo comprar una casa para remodelar con esto?", "Можно ли с этим купить дом под ремонт?"],
    "Yes — that's exactly what it's for. You finance the purchase and the repairs together.": ["Sí — para eso es exactamente. Financia la compra y las reparaciones juntas.", "Да — именно для этого он и предназначен. Вы финансируете покупку и ремонт вместе."],
    "How much can I borrow for renovations?": ["¿Cuánto puedo pedir prestado para renovaciones?", "Сколько я могу занять на реновацию?"],
    "It depends on the loan type and the home's after-repair value. We'll size the right program for your project.": ["Depende del tipo de préstamo y del valor de la vivienda después de las reparaciones. Dimensionaremos el programa adecuado para su proyecto.", "Это зависит от типа кредита и стоимости дома после ремонта. Мы подберём подходящую программу для вашего проекта."],

    /* ===== Reverse page ===== */
    "Reverse Mortgage": ["Hipoteca Inversa", "Обратная ипотека"],
    "For homeowners 62+ — convert a portion of your home equity into cash without monthly mortgage payments.": ["Para propietarios de 62 años o más — convierta una parte del capital de su vivienda en efectivo sin pagos hipotecarios mensuales.", "Для домовладельцев 62+ — превратите часть капитала вашего дома в наличные без ежемесячных ипотечных платежей."],
    "Age 62+": ["62 años o más", "Возраст 62+"],
    "For older homeowners": ["Para propietarios mayores", "Для пожилых домовладельцев"],
    "No Monthly Pmt": ["Sin pago mensual", "Без ежемесячного платежа"],
    "Required": ["Requerido", "Обязательно"],
    "Stay Home": ["Quédese en Casa", "Оставайтесь дома"],
    "Keep your title": ["Conserve su título", "Сохраните право собственности"],
    "Flexible Payout": ["Pago Flexible", "Гибкие выплаты"],
    "Lump, monthly, or LOC": ["Suma global, mensual o línea de crédito", "Единовременно, ежемесячно или кредитная линия"],
    "A reverse mortgage is a type of loan where a homeowner withdraws a portion of their home equity but doesn't have to repay the loan until they leave the house. It's designed to help older homeowners turn equity into usable funds while staying in their home.": ["Una hipoteca inversa es un tipo de préstamo en el que un propietario retira una parte del capital de su vivienda pero no tiene que pagar el préstamo hasta que abandone la casa. Está diseñada para ayudar a los propietarios mayores a convertir el capital en fondos utilizables mientras permanecen en su hogar.", "Обратная ипотека — это вид кредита, при котором домовладелец снимает часть капитала своего дома, но не обязан погашать кредит, пока не покинет дом. Она создана, чтобы помочь пожилым домовладельцам превратить капитал в доступные средства, оставаясь в своём доме."],
    "What is a reverse mortgage?": ["¿Qué es una hipoteca inversa?", "Что такое обратная ипотека?"],
    "With a reverse mortgage, the lender pays you — not the other way around. The loan balance is repaid when you sell the home, move out permanently, or pass away. You retain ownership and continue paying property taxes, insurance, and upkeep.": ["Con una hipoteca inversa, el prestamista le paga a usted — no al revés. El saldo del préstamo se paga cuando vende la vivienda, se muda permanentemente o fallece. Usted conserva la propiedad y continúa pagando los impuestos prediales, el seguro y el mantenimiento.", "При обратной ипотеке кредитор платит вам — а не наоборот. Остаток кредита погашается, когда вы продаёте дом, окончательно съезжаете или уходите из жизни. Вы сохраняете право собственности и продолжаете оплачивать налоги на недвижимость, страховку и содержание."],
    "How to qualify for a reverse mortgage": ["Cómo calificar para una hipoteca inversa", "Как получить одобрение по обратной ипотеке"],
    "Be at least 62 years old": ["Tener al menos 62 años", "Быть не моложе 62 лет"],
    "Own the home outright or have significant equity": ["Ser dueño de la vivienda por completo o tener un capital significativo", "Владеть домом полностью или иметь значительный капитал"],
    "Live in the home as your primary residence": ["Vivir en la casa como su residencia principal", "Проживать в доме как в основном месте жительства"],
    "Stay current on property taxes, insurance, and maintenance": ["Estar al día con los impuestos prediales, el seguro y el mantenimiento", "Своевременно оплачивать налоги на недвижимость, страховку и содержание"],
    "Complete a required HUD counseling session": ["Completar una sesión de asesoramiento requerida por HUD", "Пройти обязательную консультацию HUD"],
    "Ways to receive your proceeds": ["Formas de recibir sus fondos", "Способы получения средств"],
    "A lump sum at closing": ["Una suma global al cierre", "Единовременная сумма при закрытии"],
    "Fixed monthly payments": ["Pagos mensuales fijos", "Фиксированные ежемесячные выплаты"],
    "A line of credit you draw from as needed": ["Una línea de crédito de la que dispone según sea necesario", "Кредитная линия, из которой вы берёте средства по мере необходимости"],
    "A combination of these options": ["Una combinación de estas opciones", "Комбинация этих вариантов"],
    "Benefits of a reverse mortgage": ["Beneficios de una hipoteca inversa", "Преимущества обратной ипотеки"],
    "No monthly mortgage payments required": ["No se requieren pagos hipotecarios mensuales", "Не требуется ежемесячных ипотечных платежей"],
    "Stay in your home": ["Permanezca en su hogar", "Оставайтесь в своём доме"],
    "Funds are generally tax-free (consult a tax advisor)": ["Los fondos generalmente están libres de impuestos (consulte a un asesor fiscal)", "Средства, как правило, не облагаются налогом (проконсультируйтесь с налоговым консультантом)"],
    "Flexible ways to receive money": ["Formas flexibles de recibir dinero", "Гибкие способы получения денег"],
    "Do I still own my home?": ["¿Sigo siendo dueño de mi casa?", "Останусь ли я владельцем дома?"],
    "Yes. You keep title to your home. The loan is repaid when you sell, move out, or pass away.": ["Sí. Usted conserva el título de su vivienda. El préstamo se paga cuando vende, se muda o fallece.", "Да. Вы сохраняете право собственности на дом. Кредит погашается, когда вы продаёте, съезжаете или уходите из жизни."],
    "Is counseling required?": ["¿Se requiere asesoramiento?", "Обязательна ли консультация?"],
    "Yes — HUD requires independent counseling to make sure a reverse mortgage is right for you. We'll point you to an approved counselor.": ["Sí — HUD requiere asesoramiento independiente para asegurarse de que una hipoteca inversa sea adecuada para usted. Le indicaremos un asesor aprobado.", "Да — HUD требует независимой консультации, чтобы убедиться, что обратная ипотека вам подходит. Мы направим вас к одобренному консультанту."],

    /* ===== Reviews page ===== */
    "What our clients say": ["Lo que dicen nuestros clientes", "Что говорят наши клиенты"],
    "Real experiences from families and investors we've helped finance their futures.": ["Experiencias reales de familias e inversionistas a quienes hemos ayudado a financiar su futuro.", "Реальные истории семей и инвесторов, которым мы помогли профинансировать их будущее."],
    "Rated 5.0 by our clients": ["Calificados con 5.0 por nuestros clientes", "Оценка 5.0 от наших клиентов"],
    "We're proud of the relationships we've built. Here's what people say about working with us.": ["Estamos orgullosos de las relaciones que hemos construido. Esto es lo que dice la gente sobre trabajar con nosotros.", "Мы гордимся построенными отношениями. Вот что люди говорят о работе с нами."],
    "Investment Property": ["Propiedad de Inversión", "Инвестиционная недвижимость"],
    "\"Anatoliy and his team made our first home purchase painless. They explained every step in plain English and got us a great rate on our FHA loan.\"": ["«Anatoliy y su equipo hicieron que la compra de nuestra primera casa fuera sencilla. Explicaron cada paso con palabras claras y nos consiguieron una excelente tasa en nuestro préstamo FHA.»", "«Анатолий и его команда сделали покупку нашего первого дома беспроблемной. Они объяснили каждый шаг простым языком и добились отличной ставки по нашему кредиту FHA.»"],
    "\"Refinanced and cut my monthly payment significantly. Honest advice and no surprises at closing — exactly what you want.\"": ["«Refinancié y reduje significativamente mi pago mensual. Consejos honestos y sin sorpresas en el cierre — exactamente lo que uno quiere.»", "«Рефинансировал и значительно снизил ежемесячный платёж. Честные советы и никаких сюрпризов при закрытии — именно то, что нужно.»"],
    "\"As a veteran, the VA loan process can be confusing. They handled my Certificate of Eligibility and got me into my home with $0 down.\"": ["«Como veterano, el proceso del préstamo VA puede ser confuso. Gestionaron mi Certificado de Elegibilidad y me ayudaron a entrar en mi casa con $0 de pago inicial.»", "«Как ветерану, процесс кредита VA может казаться запутанным. Они оформили мой сертификат соответствия и помогли въехать в дом с $0 первоначального взноса.»"],
    "VA Loan": ["Préstamo VA", "Кредит VA"],
    "\"We needed a jumbo loan for our LA home and they made a complex process feel simple. Responsive and professional throughout.\"": ["«Necesitábamos un préstamo jumbo para nuestra casa en Los Ángeles e hicieron que un proceso complejo se sintiera simple. Atentos y profesionales en todo momento.»", "«Нам нужен был джамбо-кредит для дома в Лос-Анджелесе, и они сделали сложный процесс простым. Отзывчивы и профессиональны на всём пути.»"],
    "Jumbo Loan": ["Préstamo Jumbo", "Джамбо-кредит"],
    "\"Great experience from start to finish. Quick communication, fair rate, and they actually answered the phone when I called.\"": ["«Gran experiencia de principio a fin. Comunicación rápida, tasa justa y de verdad contestaron el teléfono cuando llamé.»", "«Отличный опыт от начала до конца. Быстрая связь, справедливая ставка, и они действительно отвечали на звонки.»"],
    "Worked with us?": ["¿Trabajó con nosotros?", "Работали с нами?"],
    "We'd love to hear about your experience — and so would future homebuyers.": ["Nos encantaría conocer su experiencia — y a los futuros compradores también.", "Мы будем рады услышать о вашем опыте — как и будущие покупатели жилья."],
    "Leave us a Google review →": ["Déjenos una reseña en Google →", "Оставьте отзыв на Google →"],

    /* ===== USDA page ===== */
    "USDA Home Loan": ["Préstamo Hipotecario USDA", "Жилищный кредит USDA"],
    "$0 down financing for eligible rural and suburban homebuyers, backed by the U.S. Department of Agriculture.": ["Financiamiento con $0 de pago inicial para compradores elegibles en zonas rurales y suburbanas, respaldado por el Departamento de Agricultura de EE. UU.", "Финансирование с $0 первоначального взноса для подходящих покупателей в сельской и пригородной местности, при поддержке Министерства сельского хозяйства США."],
    "$0 Down": ["$0 inicial", "$0 взнос"],
    "100% financing": ["Financiamiento del 100%", "100% финансирование"],
    "Location-Based": ["Según la ubicación", "По местоположению"],
    "Rural & suburban": ["Rural y suburbano", "Сельская и пригородная зона"],
    "Low MI": ["MI bajo", "Низкий MI"],
    "Cheaper than FHA": ["Más barato que FHA", "Дешевле, чем FHA"],
    "Income Limits": ["Límites de Ingreso", "Лимиты дохода"],
    "Built for affordability": ["Diseñado para la asequibilidad", "Создан для доступности"],
    "USDA loans make purchasing a home more affordable for buyers in eligible rural and many suburban areas. The U.S. Department of Agriculture backs these loans much like the VA backs loans for veterans — meaning $0 down and lower costs for those who qualify.": ["Los préstamos USDA hacen que comprar una vivienda sea más asequible para compradores en zonas rurales elegibles y muchas áreas suburbanas. El Departamento de Agricultura de EE. UU. respalda estos préstamos de manera similar a como el VA respalda los préstamos para veteranos — lo que significa $0 de pago inicial y costos más bajos para quienes califican.", "Кредиты USDA делают покупку жилья доступнее для покупателей в подходящих сельских и многих пригородных районах. Министерство сельского хозяйства США поддерживает эти кредиты подобно тому, как VA поддерживает кредиты для ветеранов — то есть $0 первоначального взноса и меньшие расходы для тех, кто соответствует требованиям."],
    "What is a USDA home mortgage?": ["¿Qué es una hipoteca de vivienda USDA?", "Что такое жилищная ипотека USDA?"],
    "With government backing, USDA loans offer 100% financing and reduced mortgage insurance compared to other low-down-payment options. Eligibility is based on the property's location and your household income.": ["Con respaldo del gobierno, los préstamos USDA ofrecen financiamiento del 100% y un seguro hipotecario reducido en comparación con otras opciones de bajo pago inicial. La elegibilidad se basa en la ubicación de la propiedad y el ingreso de su hogar.", "При государственной поддержке кредиты USDA предлагают 100% финансирование и сниженное ипотечное страхование по сравнению с другими вариантами с низким первоначальным взносом. Право на участие зависит от местоположения недвижимости и дохода вашей семьи."],
    "How to qualify for a USDA loan": ["Cómo calificar para un préstamo USDA", "Как получить одобрение по кредиту USDA"],
    "The property must be in a USDA-eligible area": ["La propiedad debe estar en un área elegible para USDA", "Недвижимость должна находиться в зоне, подходящей для USDA"],
    "Household income must fall within local limits": ["El ingreso del hogar debe estar dentro de los límites locales", "Доход семьи должен укладываться в местные лимиты"],
    "A credit score around 640 is typically preferred": ["Generalmente se prefiere un puntaje de crédito alrededor de 640", "Обычно предпочтителен кредитный рейтинг около 640"],
    "Types of USDA programs": ["Tipos de programas USDA", "Виды программ USDA"],
    "Guaranteed Loans for moderate-income buyers through approved lenders": ["Préstamos Garantizados para compradores de ingresos moderados a través de prestamistas aprobados", "Гарантированные кредиты для покупателей со средним доходом через одобренных кредиторов"],
    "Direct Loans for low- and very-low-income applicants": ["Préstamos Directos para solicitantes de ingresos bajos y muy bajos", "Прямые кредиты для заявителей с низким и очень низким доходом"],
    "Home Improvement Loans and grants for eligible repairs": ["Préstamos y subvenciones para mejoras del hogar para reparaciones elegibles", "Кредиты и гранты на улучшение жилья для подходящего ремонта"],
    "Benefits of a USDA loan": ["Beneficios de un préstamo USDA", "Преимущества кредита USDA"],
    "$0 down payment": ["$0 de pago inicial", "$0 первоначального взноса"],
    "Lower mortgage insurance than FHA": ["Seguro hipotecario más bajo que FHA", "Ипотечное страхование ниже, чем у FHA"],
    "Competitive fixed rates": ["Tasas fijas competitivas", "Конкурентные фиксированные ставки"],
    "Flexible credit guidelines": ["Pautas de crédito flexibles", "Гибкие требования к кредиту"],
    "How do I know if a home qualifies?": ["¿Cómo sé si una vivienda califica?", "Как узнать, подходит ли дом?"],
    "Eligibility is location-based — we can check any address against USDA maps for you in seconds.": ["La elegibilidad se basa en la ubicación — podemos verificar cualquier dirección en los mapas de USDA en segundos.", "Право на участие зависит от местоположения — мы можем проверить любой адрес по картам USDA за секунды."],
    "Are there income limits?": ["¿Hay límites de ingreso?", "Есть ли лимиты по доходу?"],
    "Yes, limits vary by county and household size. We'll confirm whether you qualify.": ["Sí, los límites varían según el condado y el tamaño del hogar. Confirmaremos si usted califica.", "Да, лимиты различаются по округам и размеру семьи. Мы подтвердим, подходите ли вы."],

    /* ===== VA page ===== */
    "VA Home Loan": ["Préstamo Hipotecario VA", "Жилищный кредит VA"],
    "$0 down and no PMI for eligible veterans, active-duty service members, and their families.": ["$0 de pago inicial y sin PMI para veteranos elegibles, militares en servicio activo y sus familias.", "$0 первоначального взноса и без PMI для подходящих ветеранов, военнослужащих действительной службы и их семей."],
    "For eligible vets": ["Para veteranos elegibles", "Для подходящих ветеранов"],
    "No PMI": ["Sin PMI", "Без PMI"],
    "Ever": ["Nunca", "Никогда"],
    "Low Costs": ["Costos Bajos", "Низкие расходы"],
    "Limited closing costs": ["Costos de cierre limitados", "Ограниченные расходы на закрытие"],
    "Streamline Refi": ["Refi Simplificado", "Упрощённое рефи"],
    "Easy IRRRL option": ["Opción IRRRL fácil", "Простой вариант IRRRL"],
    "VA home loans are guaranteed by the U.S. Department of Veterans Affairs. Created in 1944, the program has helped more than 24 million veterans, active-duty members, and their families purchase or refinance a home — often with no down payment at all.": ["Los préstamos hipotecarios VA están garantizados por el Departamento de Asuntos de Veteranos de EE. UU. Creado en 1944, el programa ha ayudado a más de 24 millones de veteranos, militares en servicio activo y sus familias a comprar o refinanciar una vivienda — a menudo sin ningún pago inicial.", "Жилищные кредиты VA гарантируются Министерством по делам ветеранов США. Программа, созданная в 1944 году, помогла более чем 24 миллионам ветеранов, военнослужащих действительной службы и их семьям купить или рефинансировать жильё — часто вообще без первоначального взноса."],
    "What is a VA home loan?": ["¿Qué es un préstamo hipotecario VA?", "Что такое жилищный кредит VA?"],
    "VA loans are among the most powerful benefits available to those who served. The VA guarantees a portion of the loan, allowing approved lenders to offer $0 down financing with no private mortgage insurance and competitive rates.": ["Los préstamos VA están entre los beneficios más poderosos disponibles para quienes sirvieron. El VA garantiza una parte del préstamo, lo que permite a los prestamistas aprobados ofrecer financiamiento con $0 de pago inicial, sin seguro hipotecario privado y con tasas competitivas.", "Кредиты VA — одна из самых мощных льгот, доступных тем, кто служил. VA гарантирует часть кредита, что позволяет одобренным кредиторам предлагать финансирование с $0 первоначального взноса, без частного ипотечного страхования и с конкурентными ставками."],
    "How to qualify for a VA loan": ["Cómo calificar para un préstamo VA", "Как получить одобрение по кредиту VA"],
    "A valid Certificate of Eligibility (COE) based on your service": ["Un Certificado de Elegibilidad (COE) válido según su servicio", "Действующий сертификат соответствия (COE) на основе вашей службы"],
    "Sufficient income to cover the mortgage and living expenses": ["Ingresos suficientes para cubrir la hipoteca y los gastos de vida", "Достаточный доход для покрытия ипотеки и расходов на жизнь"],
    "A satisfactory credit profile (no strict VA minimum, though lenders set their own)": ["Un perfil crediticio satisfactorio (sin un mínimo estricto del VA, aunque los prestamistas establecen el suyo)", "Удовлетворительный кредитный профиль (у VA нет строгого минимума, хотя кредиторы устанавливают свой)"],
    "Types of VA loans": ["Tipos de préstamos VA", "Виды кредитов VA"],
    "VA purchase loans for buying a primary home": ["Préstamos de compra VA para adquirir una vivienda principal", "Кредиты VA на покупку основного жилья"],
    "VA Interest Rate Reduction Refinance Loans (IRRRL / streamline)": ["Préstamos de Refinanciamiento con Reducción de Tasa de Interés del VA (IRRRL / simplificado)", "Кредиты рефинансирования VA со снижением процентной ставки (IRRRL / упрощённое)"],
    "VA cash-out refinances to tap equity": ["Refinanciamientos VA con retiro de efectivo para aprovechar el capital", "Рефинансирование VA с обналичиванием для использования капитала"],
    "Loans for energy-efficient improvements": ["Préstamos para mejoras de eficiencia energética", "Кредиты на энергоэффективные улучшения"],
    "Benefits of a VA loan": ["Beneficios de un préstamo VA", "Преимущества кредита VA"],
    "$0 down payment for eligible borrowers": ["$0 de pago inicial para prestatarios elegibles", "$0 первоначального взноса для подходящих заёмщиков"],
    "No private mortgage insurance": ["Sin seguro hipotecario privado", "Без частного ипотечного страхования"],
    "Competitive interest rates": ["Tasas de interés competitivas", "Конкурентные процентные ставки"],
    "No prepayment penalty": ["Sin penalización por pago anticipado", "Без штрафа за досрочное погашение"],
    "Do I need a down payment?": ["¿Necesito un pago inicial?", "Нужен ли первоначальный взнос?"],
    "Most eligible borrowers can finance 100% of the purchase price with $0 down.": ["La mayoría de los prestatarios elegibles pueden financiar el 100% del precio de compra con $0 de pago inicial.", "Большинство подходящих заёмщиков могут профинансировать 100% стоимости покупки с $0 первоначального взноса."],
    "How do I get my Certificate of Eligibility?": ["¿Cómo obtengo mi Certificado de Elegibilidad?", "Как получить сертификат соответствия?"],
    "We help you request your COE as part of the application — it confirms your VA loan entitlement based on your service.": ["Le ayudamos a solicitar su COE como parte de la solicitud — confirma su derecho al préstamo VA según su servicio.", "Мы помогаем запросить ваш COE в рамках заявки — он подтверждает ваше право на кредит VA на основе службы."]
  };

  /* ---- Strings used by scripts (chat replies, wizard buttons, calculator verdicts) ---- */
  var UI = {
    chatGreeting: {
      en: "👋 Hi! I'm your West Coast Capital Mortgage assistant. Ask me about rates, loan programs, or getting pre-approved.",
      es: "👋 ¡Hola! Soy su asistente de West Coast Capital Mortgage. Pregúnteme sobre tasas, programas de préstamo o cómo obtener la preaprobación.",
      ru: "👋 Здравствуйте! Я ваш ассистент West Coast Capital Mortgage. Спросите меня о ставках, кредитных программах или предодобрении."
    },
    rates: {
      en: "Today's sample rates: 30-yr fixed ~6.49%, 15-yr ~5.74%, FHA ~6.13%. Rates change daily and depend on your credit, down payment, and loan type. Want a personalized quote? I can have a loan officer reach out — just share your name and phone, or call (310) 654-1577.",
      es: "Tasas de muestra de hoy: fija a 30 años ~6.49%, 15 años ~5.74%, FHA ~6.13%. Las tasas cambian a diario y dependen de su crédito, pago inicial y tipo de préstamo. ¿Desea una cotización personalizada? Puedo pedir que un oficial de préstamos lo contacte — comparta su nombre y teléfono, o llame al (310) 654-1577.",
      ru: "Примерные ставки на сегодня: фиксированная 30 лет ~6,49%, 15 лет ~5,74%, FHA ~6,13%. Ставки меняются ежедневно и зависят от вашего кредита, первоначального взноса и типа кредита. Хотите персональный расчёт? Я могу попросить кредитного специалиста связаться с вами — укажите имя и телефон или позвоните (310) 654-1577."
    },
    fha: {
      en: "FHA loans are great for first-time buyers — as little as 3.5% down and flexible credit requirements. They do carry mortgage insurance. Want me to start a quick pre-qualification?",
      es: "Los préstamos FHA son excelentes para compradores primerizos — desde 3.5% de pago inicial y requisitos de crédito flexibles. Sí incluyen seguro hipotecario. ¿Quiere que inicie una precalificación rápida?",
      ru: "Кредиты FHA отлично подходят для покупателей первого жилья — от 3,5% первоначального взноса и гибкие требования к кредиту. Они включают ипотечное страхование. Хотите, я начну быструю предварительную квалификацию?"
    },
    va: {
      en: "VA loans offer $0 down for eligible veterans and active-duty service members, with no PMI. You'll need a Certificate of Eligibility. Shall I connect you with our VA specialist?",
      es: "Los préstamos VA ofrecen $0 de pago inicial para veteranos elegibles y militares en servicio activo, sin PMI. Necesitará un Certificado de Elegibilidad. ¿Lo conecto con nuestro especialista en VA?",
      ru: "Кредиты VA предлагают $0 первоначального взноса для подходящих ветеранов и военнослужащих действительной службы, без PMI. Вам понадобится сертификат соответствия. Соединить вас с нашим специалистом по VA?"
    },
    jumbo: {
      en: "Jumbo loans finance amounts above the conforming limit — ideal for higher-priced LA properties. They typically need stronger credit and reserves. I can outline what you'd qualify for.",
      es: "Los préstamos jumbo financian montos por encima del límite conforme — ideales para propiedades de mayor precio en Los Ángeles. Suelen requerir mejor crédito y reservas. Puedo describir para cuánto calificaría.",
      ru: "Джамбо-кредиты финансируют суммы сверх соответствующего лимита — идеально для дорогой недвижимости в Лос-Анджелесе. Обычно требуют более высокого кредита и резервов. Я могу описать, на что вы можете претендовать."
    },
    down: {
      en: "Down payments range from 0% (VA/USDA) to 3.5% (FHA) to 3–20% (conventional). Less than 20% usually adds mortgage insurance. Tell me the price range and I'll estimate it.",
      es: "Los pagos iniciales van desde 0% (VA/USDA) hasta 3.5% (FHA) y 3–20% (convencional). Menos del 20% generalmente agrega seguro hipotecario. Dígame el rango de precio y lo estimaré.",
      ru: "Первоначальные взносы варьируются от 0% (VA/USDA) до 3,5% (FHA) и 3–20% (конвенциональный). Менее 20% обычно добавляет ипотечное страхование. Назовите ценовой диапазон, и я сделаю оценку."
    },
    refi: {
      en: "Refinancing can lower your rate, shorten your term, or tap equity. The break-even is when your monthly savings cover closing costs. Try our refinance calculator, or I can run the numbers with you.",
      es: "El refinanciamiento puede reducir su tasa, acortar su plazo o aprovechar el capital. El punto de equilibrio es cuando sus ahorros mensuales cubren los costos de cierre. Pruebe nuestra calculadora de refinanciamiento, o puedo calcular los números con usted.",
      ru: "Рефинансирование может снизить ставку, сократить срок или использовать капитал. Точка окупаемости — когда ежемесячная экономия покрывает расходы на закрытие. Попробуйте наш калькулятор рефинансирования, или я могу посчитать вместе с вами."
    },
    credit: {
      en: "Minimums vary: FHA from ~580, conventional ~620, jumbo ~700+. Even with lower scores there are options. Want me to flag this for a loan officer review?",
      es: "Los mínimos varían: FHA desde ~580, convencional ~620, jumbo ~700+. Incluso con puntajes más bajos hay opciones. ¿Quiere que lo marque para una revisión de un oficial de préstamos?",
      ru: "Минимумы различаются: FHA от ~580, конвенциональный ~620, джамбо ~700+. Даже с более низким рейтингом есть варианты. Хотите, я отмечу это для рассмотрения кредитным специалистом?"
    },
    prequal: {
      en: "Great — getting pre-approved takes about 10 minutes. Head to our Apply page, or share your name, phone, and the loan type you're after and I'll pass it to our team.",
      es: "Excelente — obtener la preaprobación toma unos 10 minutos. Vaya a nuestra página de Solicitud, o comparta su nombre, teléfono y el tipo de préstamo que busca y lo enviaré a nuestro equipo.",
      ru: "Отлично — предодобрение занимает около 10 минут. Перейдите на нашу страницу заявки или укажите имя, телефон и интересующий тип кредита, и я передам это нашей команде."
    },
    contact: {
      en: "You can reach West Coast Capital Mortgage at (310) 654-1577, or leave your name and number here and a licensed loan officer will call you back shortly.",
      es: "Puede comunicarse con West Coast Capital Mortgage al (310) 654-1577, o deje su nombre y número aquí y un oficial de préstamos con licencia le devolverá la llamada en breve.",
      ru: "Вы можете связаться с West Coast Capital Mortgage по телефону (310) 654-1577 или оставить здесь имя и номер, и лицензированный кредитный специалист вскоре перезвонит вам."
    },
    hello: {
      en: "Hi! I'm the West Coast Capital Mortgage assistant. I can help with rates, loan programs (FHA, VA, USDA, Jumbo, Conventional), down payments, and getting pre-approved. What are you looking into?",
      es: "¡Hola! Soy el asistente de West Coast Capital Mortgage. Puedo ayudar con tasas, programas de préstamo (FHA, VA, USDA, Jumbo, Convencional), pagos iniciales y obtener la preaprobación. ¿Qué está buscando?",
      ru: "Здравствуйте! Я ассистент West Coast Capital Mortgage. Я могу помочь со ставками, кредитными программами (FHA, VA, USDA, Джамбо, Конвенциональный), первоначальными взносами и предодобрением. Что вас интересует?"
    },
    usda: {
      en: "USDA loans offer $0 down for eligible rural and some suburban areas, with low mortgage insurance. Eligibility depends on location and income. Want me to check if your area qualifies?",
      es: "Los préstamos USDA ofrecen $0 de pago inicial para zonas rurales elegibles y algunas suburbanas, con seguro hipotecario bajo. La elegibilidad depende de la ubicación y los ingresos. ¿Quiere que verifique si su área califica?",
      ru: "Кредиты USDA предлагают $0 первоначального взноса для подходящих сельских и некоторых пригородных районов с низким ипотечным страхованием. Право на участие зависит от местоположения и дохода. Хотите, я проверю, подходит ли ваш район?"
    },
    reverse: {
      en: "Reverse mortgages let homeowners 62+ convert equity into cash without monthly payments. They're worth discussing carefully — I can connect you with our specialist.",
      es: "Las hipotecas inversas permiten a los propietarios de 62 años o más convertir el capital en efectivo sin pagos mensuales. Vale la pena discutirlas con cuidado — puedo conectarlo con nuestro especialista.",
      ru: "Обратная ипотека позволяет домовладельцам 62+ превращать капитал в наличные без ежемесячных платежей. Их стоит обсудить внимательно — я могу соединить вас с нашим специалистом."
    },
    botDefault: {
      en: "That's a great question. A licensed loan officer can give you the most accurate answer. Call (310) 654-1577, or share your name and phone and we'll reach out. Meanwhile, you can also start an application or try our calculators.",
      es: "Esa es una excelente pregunta. Un oficial de préstamos con licencia puede darle la respuesta más precisa. Llame al (310) 654-1577, o comparta su nombre y teléfono y nos comunicaremos. Mientras tanto, también puede iniciar una solicitud o probar nuestras calculadoras.",
      ru: "Отличный вопрос. Лицензированный кредитный специалист даст вам самый точный ответ. Позвоните (310) 654-1577 или оставьте имя и телефон, и мы свяжемся. А пока вы также можете начать заявку или воспользоваться нашими калькуляторами."
    },
    wizSubmit: { en: "Submit application", es: "Enviar solicitud", ru: "Отправить заявку" },
    wizContinue: { en: "Continue", es: "Continuar", ru: "Продолжить" },
    buyWins: { en: "Buying wins", es: "Comprar gana", ru: "Покупка выгоднее" },
    rentWins: { en: "Renting wins", es: "Alquilar gana", ru: "Аренда выгоднее" },
    moSuffix: { en: " mo", es: " mes", ru: " мес" }
  };

  /* ---- Engine ---- */
  function norm(s) { return s.replace(/\s+/g, " ").trim(); }

  function readLang() {
    var l = null;
    try { l = localStorage.getItem(STORE); } catch (e) {}
    return LANGS.indexOf(l) >= 0 ? l : "en";
  }
  function writeLang(l) { try { localStorage.setItem(STORE, l); } catch (e) {} }

  var textNodes = [];   // { node, raw }
  var attrNodes = [];   // { el, attr, en }
  var collected = false;
  var onChange = [];

  function collect() {
    if (collected || !document.body) return;
    collected = true;
    var walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT, {
      acceptNode: function (node) {
        var p = node.parentNode;
        if (!p) return NodeFilter.FILTER_REJECT;
        var tag = p.nodeName;
        if (tag === "SCRIPT" || tag === "STYLE" || tag === "NOSCRIPT") return NodeFilter.FILTER_REJECT;
        if (p.closest && p.closest(".lang-switch")) return NodeFilter.FILTER_REJECT;
        if (p.classList && p.classList.contains("year")) return NodeFilter.FILTER_REJECT;
        if (!node.nodeValue || !node.nodeValue.trim()) return NodeFilter.FILTER_REJECT;
        return NodeFilter.FILTER_ACCEPT;
      }
    });
    var n;
    while ((n = walker.nextNode())) textNodes.push({ node: n, raw: n.nodeValue });

    var els = document.body.querySelectorAll("[placeholder],[aria-label]");
    Array.prototype.forEach.call(els, function (el) {
      if (el.closest && el.closest(".lang-switch")) return;
      if (el.hasAttribute("placeholder")) attrNodes.push({ el: el, attr: "placeholder", en: el.getAttribute("placeholder") });
      if (el.hasAttribute("aria-label")) attrNodes.push({ el: el, attr: "aria-label", en: el.getAttribute("aria-label") });
    });
  }

  function lookup(en, lang) {
    if (lang === "en") return null;
    var e = DICT[norm(en)];
    if (!e) return null;
    return lang === "es" ? e[0] : e[1];
  }

  function apply(lang) {
    collect();
    document.documentElement.lang = lang;
    textNodes.forEach(function (t) {
      var m = t.raw.match(/^(\s*)([\s\S]*?)(\s*)$/);
      var tr = lookup(m[2], lang);
      t.node.nodeValue = (tr !== null) ? (m[1] + tr + m[3]) : t.raw;
    });
    attrNodes.forEach(function (a) {
      var tr = lookup(a.en, lang);
      a.el.setAttribute(a.attr, tr !== null ? tr : a.en);
    });
    var btns = document.querySelectorAll(".lang-switch button");
    Array.prototype.forEach.call(btns, function (b) {
      b.classList.toggle("active", b.getAttribute("data-lang") === lang);
    });
    Array.prototype.forEach.call(document.querySelectorAll(".year"), function (el) {
      el.textContent = new Date().getFullYear();
    });
    onChange.forEach(function (fn) { try { fn(lang); } catch (e) {} });
  }

  function setLang(lang) {
    if (LANGS.indexOf(lang) < 0) lang = "en";
    I18N.lang = lang;
    writeLang(lang);
    apply(lang);
  }

  var I18N = {
    lang: readLang(),
    setLang: setLang,
    apply: apply,
    t: function (key) {
      var e = UI[key];
      return e ? (e[I18N.lang] || e.en) : "";
    },
    onChange: function (fn) { onChange.push(fn); }
  };
  window.I18N = I18N;

  function init() {
    var btns = document.querySelectorAll(".lang-switch button");
    Array.prototype.forEach.call(btns, function (b) {
      b.addEventListener("click", function () { setLang(b.getAttribute("data-lang")); });
    });
    apply(I18N.lang);
  }

  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init);
  else init();
})();
