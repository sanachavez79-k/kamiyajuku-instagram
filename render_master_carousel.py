import asyncio
from pathlib import Path
from playwright.async_api import async_playwright
from datetime import datetime, timedelta

BASE_DIR = Path(__file__).resolve().parent
ASSETS_DIR = BASE_DIR / "generated_assets"
LOGO_PATH = BASE_DIR / "assets" / "brand_logo_main.png"

# 生徒・活動写真のパス設定（リポジトリ内ポータブル配置）
PHOTO_MONDAY = BASE_DIR / "assets" / "photo_monday.jpg"
PHOTO_WEDNESDAY = BASE_DIR / "assets" / "photo_wednesday.jpg"
PHOTO_FRIDAY = BASE_DIR / "assets" / "photo_friday.jpg"

# 週替わり（Week 1 〜 Week 4）コンテンツプール
WEEKLY_CONTENT_POOL = {
    "LUNES": [
        # Week 1: に vs で
        {
            "pillar": "JLPT文法・重要助詞 (Week 1)",
            "tag_text": "JLPT N5 / N4 GRAMÁTICA ⛩️",
            "bg_primary": "#EEF4EA", "brand_deep": "#1B5E20", "accent_main": "#E8822A", "accent_light": "#DCEBD6",
            "student_photo": PHOTO_MONDAY, "photo_position": "center 20%",
            "title_html": '¿Dices "Tokyo <span style="color: #E8822A; text-decoration: underline;">NI</span>" o "Tokyo <span style="color: #1B5E20; text-decoration: underline;">DE</span>"? 🇯🇵❌',
            "subtitle": "El error con las partículas「に」y「で」que el 90% comete en el JLPT.",
            "hero_left": {"char": "に", "color": "#E8822A", "desc": "Estancia / Destino"},
            "hero_right": {"char": "で", "color": "#1B5E20", "desc": "Acción Activa"},
            "rule1": {"badge": "に (NI)", "badge_bg": "#E8822A", "title": "Lugar de Estancia / Destino", "desc": "Indica DÓNDE está una persona/objeto o a dónde vas.", "ja": '<ruby>東京<rt>とうきょう</rt></ruby><span style="color: #E8822A; font-weight: 900;">に</span> <ruby>住<rt>す</rt></ruby>んでいます。', "es": "Vivo EN Tokio. (Verbo de permanencia)"},
            "rule2": {"badge": "で (DE)", "badge_bg": "#1B5E20", "title": "Lugar de Acción Activa", "desc": "Indica DÓNDE ocurre una actividad o evento dinámico.", "ja": 'レストラン<span style="color: #1B5E20; font-weight: 900;">で</span> <ruby>食<rt>た</rt></ruby>べます。', "es": "Como EN un restaurante. (Verbo de acción)"},
            "q1_ja": '<ruby>図書館<rt>としょかん</rt></ruby>（ &nbsp;&nbsp;&nbsp;&nbsp; ）<ruby>本<rt>ほん</rt></ruby>を <ruby>読<rt>よ</rt></ruby>みます。', "q1_es": "Toshokan ( ) hon o yomimasu. (Leo libros en la biblioteca)",
            "q2_ja": '<ruby>机<rt>つくえ</rt></ruby>の <ruby>上<rt>うえ</rt></ruby>（ &nbsp;&nbsp;&nbsp;&nbsp; ）<ruby>猫<rt>ねこ</rt></ruby>が います。', "q2_es": "Tsukue no ue ( ) neko ga imasu. (Hay un gato sobre la mesa)",
            "a1_text": "Respuesta: で (DE)", "a1_desc": '¡Porque "leer (<ruby>読<rt>よ</rt></ruby>む)" es una <strong>acción activa</strong> en el lugar!',
            "a2_text": "Respuesta: に (NI)", "a2_desc": '¡Porque "estar/haber (いる)" indica <strong>existencia estática / estancia</strong>!',
            "cheat_t1": "¿Hay movimiento / acción activa?", "cheat_b1": '➔ <ruby>食<rt>た</rt></ruby>べる, <ruby>勉強<rt>べんきょう</rt></ruby>する, <ruby>買<rt>か</rt></ruby>う = <strong style="color: #E8822A; font-size: 42px;">で (DE)</strong>',
            "cheat_t2": "¿Es estancia, estar o destino?", "cheat_b2": '➔ <ruby>住<rt>す</rt></ruby>む, いる, ある, <ruby>行<rt>い</rt></ruby>く = <strong style="color: #1B5E20; font-size: 42px;">に (NI)</strong>',
            "dm_keyword": "JLPT", "dm_gift": "<b>Guía PDF gratuita de partículas</b> + <b>Test de Nivel</b>"
        },
        # Week 2: は vs が
        {
            "pillar": "JLPT文法・重要助詞 (Week 2)",
            "tag_text": "JLPT N5 / N4 GRAMÁTICA ⛩️",
            "bg_primary": "#EEF4EA", "brand_deep": "#1B5E20", "accent_main": "#E8822A", "accent_light": "#DCEBD6",
            "student_photo": PHOTO_MONDAY, "photo_position": "center 20%",
            "title_html": '¿Diferencia real entre <span style="color: #E8822A; text-decoration: underline;">WA (は)</span> y <span style="color: #1B5E20; text-decoration: underline;">GA (が)</span>? 🇯🇵🧠',
            "subtitle": "La duda más común explicada con la regla de 'Tema vs Sujeto & Clima'.",
            "hero_left": {"char": "は", "color": "#E8822A", "desc": "Tema Principal"},
            "hero_right": {"char": "が", "color": "#1B5E20", "desc": "Sujeto / Clima y Fenómenos"},
            "rule1": {"badge": "は (WA)", "badge_bg": "#E8822A", "title": "Presenta el Tema ('En cuanto a...')", "desc": "Pone el foco en lo que viene DESPUÉS de la partícula.", "ja": '<ruby>私<rt>わたし</rt></ruby><span style="color: #E8822A; font-weight: 900;">は</span> カルロスです。', "es": "En cuanto a mí, soy Carlos."},
            "rule2": {"badge": "が (GA)", "badge_bg": "#1B5E20", "title": "Sujeto & Fenómenos del Clima / Naturaleza", "desc": "Pone el foco en el sujeto y se usa SIEMPRE para fenómenos del clima y naturaleza.", "ja": '<ruby>雨<rt>あめ</rt></ruby><span style="color: #1B5E20; font-weight: 900;">が</span> <ruby>降<rt>ふ</rt></ruby>る / <ruby>雷<rt>かみなり</rt></ruby><span style="color: #1B5E20; font-weight: 900;">が</span> <ruby>鳴<rt>な</rt></ruby>る', "es": "Llueve / Hay truenos. (Hechos y clima que percibes)"},
            "q1_ja": '<ruby>雨<rt>あめ</rt></ruby>（ &nbsp;&nbsp;&nbsp;&nbsp; ）<ruby>降<rt>ふ</rt></ruby>っています。', "q1_es": "Ame ( ) futte imasu. (Está lloviendo)",
            "q2_ja": '<ruby>今日<rt>きょう</rt></ruby>（ &nbsp;&nbsp;&nbsp;&nbsp; ）いい <ruby>天気<rt>てんき</rt></ruby>ですね。', "q2_es": "Kyou ( ) ii tenki desu ne. (Hoy hace buen tiempo)",
            "a1_text": "Respuesta: が (GA)", "a1_desc": "¡El clima y fenómenos naturales (lluvia, truenos, viento) llevan SIEMPRE が!",
            "a2_text": "Respuesta: は (WA)", "a2_desc": "¡Porque 'Hoy (今日)' es el tema sobre el que estamos hablando!",
            "cheat_t1": "¿Clima o preguntas con 誰 (quién), 何 (qué)?", "cheat_b1": '➔ <ruby>雨<rt>あめ</rt></ruby>が<ruby>降<rt>ふ</rt></ruby>る, <ruby>雷<rt>かみなり</rt></ruby>が<ruby>鳴<rt>な</rt></ruby>る = <strong style="color: #1B5E20; font-size: 38px;">が (GA)</strong>',
            "cheat_t2": "¿Contrastes o temas de conversación?", "cheat_b2": '➔ Siempre llevan <strong style="color: #E8822A; font-size: 38px;">は (WA)</strong>',
            "dm_keyword": "JLPT", "dm_gift": "<b>Guía PDF de Partículas N5/N4</b> + <b>Test de Nivel</b>"
        },
        # Week 3: ために vs ように
        {
            "pillar": "JLPT文法・重要助詞 (Week 3)",
            "tag_text": "JLPT N4 / N3 GRAMÁTICA ⛩️",
            "bg_primary": "#EEF4EA", "brand_deep": "#1B5E20", "accent_main": "#E8822A", "accent_light": "#DCEBD6",
            "student_photo": PHOTO_MONDAY, "photo_position": "center 20%",
            "title_html": '¿"Para hacer": <span style="color: #E8822A; text-decoration: underline;">TAME NI</span> o <span style="color: #1B5E20; text-decoration: underline;">YOU NI</span>? 🇯🇵🎯',
            "subtitle": "Aprende a expresar objetivos y propósitos como un nativo.",
            "hero_left": {"char": "ために", "color": "#E8822A", "desc": "Voluntad Directa"},
            "hero_right": {"char": "ように", "color": "#1B5E20", "desc": "Estado Deseado"},
            "rule1": {"badge": "ために (Tame ni)", "badge_bg": "#E8822A", "title": "Acción Voluntaria y Directa", "desc": "Verbos con control propio (comprar, estudiar, viajar).", "ja": '<ruby>日本<rt>にほん</rt></ruby>へ <ruby>行<rt>い</rt></ruby>く<span style="color: #E8822A; font-weight: 900;">ために</span>、<ruby>貯金<rt>ちょきん</rt></ruby>します。', "es": "Ahorro para ir a Japón. (Acción voluntaria)"},
            "rule2": {"badge": "ように (You ni)", "badge_bg": "#1B5E20", "title": "Estado o Verbo Potencial", "desc": "Para que algo sea posible o no ocurra (poder hablar, no olvidar).", "ja": '<ruby>話<rt>はな</rt></ruby>せる<span style="color: #1B5E20; font-weight: 900;">ように</span>、<ruby>練習<rt>れんしゅう</rt></ruby>します。', "es": "Practico para poder hablar. (Verbo potencial)"},
            "q1_ja": '<ruby>風邪<rt>かぜ</rt></ruby>を ひかない（ &nbsp;&nbsp;&nbsp;&nbsp; ）、マスクを します。', "q1_es": "Kaze o hikanai ( ), masuku o shimasu. (Para no resfriarme...)",
            "q2_ja": '<ruby>家<rt>いえ</rt></ruby>を <ruby>買<rt>か</rt></ruby>う（ &nbsp;&nbsp;&nbsp;&nbsp; ）、<ruby>働<rt>はたら</rt></ruby>きます。', "q2_es": "Ie o kau ( ), hatarakimasu. (Para comprar una casa...)",
            "a1_text": "Respuesta: ように (YOU NI)", "a1_desc": "¡Las formas negativas (〜ない) siempre van con ように!",
            "a2_text": "Respuesta: ために (TAME NI)", "a2_desc": '¡Porque "comprar (買う)" es una acción bajo tu control directo!',
            "cheat_t1": "¿Verbo potencial (できる) o negativo (ない)?", "cheat_b1": '➔ <strong style="color: #1B5E20; font-size: 42px;">ように (YOU NI)</strong>',
            "cheat_t2": "¿Verbo de acción voluntaria directa?", "cheat_b2": '➔ <strong style="color: #E8822A; font-size: 42px;">ために (TAME NI)</strong>',
            "dm_keyword": "JLPT", "dm_gift": "<b>Masterclass PDF de Gramática N4/N3</b> + <b>Test</b>"
        }
    ],
    "MIERCOLES": [
        # Week 1: すみません vs ごめん
        {
            "pillar": "日常会話・リアル表現 (Week 1)",
            "tag_text": "CONVERSACIÓN REAL 💬",
            "bg_primary": "#FFF9E6", "brand_deep": "#B27B00", "accent_main": "#E59800", "accent_light": "#FFEEC2",
            "student_photo": PHOTO_WEDNESDAY, "photo_position": "center 30%",
            "title_html": '¿Cómo pedir perdón en japonés? <span style="color: #B27B00; text-decoration: underline;">すみません</span> vs <span style="color: #E59800; text-decoration: underline;">ごめん</span> 🙇‍♂️✨',
            "subtitle": "Diferencias clave para sonar natural con amigos y en el trabajo.",
            "hero_left": {"char": "すみません", "color": "#B27B00", "desc": "Formal / Cortesía"},
            "hero_right": {"char": "ごめん", "color": "#E59800", "desc": "Casual / Amigos"},
            "rule1": {"badge": "すみません", "badge_bg": "#B27B00", "title": "Cortesía Universal", "desc": "Se usa con desconocidos, superiores o para llamar la atención (¡Disculpe!).", "ja": 'すみません、お<ruby>願<rt>ねが</rt></ruby>いします。', "es": "Disculpe, por favor. (Uso formal y educado)"},
            "rule2": {"badge": "ごめん (ね)", "badge_bg": "#E59800", "title": "Cercano / Casual", "desc": "Solo para amigos cercanos, familia o pareja. ¡Nunca con jefes!", "ja": '<ruby>待<rt>ま</rt></ruby>たせて ごめんね！', "es": "¡Perdón por hacerte esperar! (Entre amigos)"},
            "q1_ja": '（カフェで）「（ &nbsp;&nbsp;&nbsp;&nbsp; ）、お<ruby>水<rt>みず</rt></ruby>を ください。」', "q1_es": "(En una cafetería) ( ) omizu o kudasai. (Disculpe, agua por favor)",
            "q2_ja": '（<ruby>友達<rt>ともだち</rt></ruby>に）「ちょっと <ruby>遅<rt>おく</rt></ruby>れる、（ &nbsp;&nbsp;&nbsp;&nbsp; ）！」', "q2_es": "(A un amigo) Chotto okureru, ( )! (Llego un poco tarde, ¡perdón!)",
            "a1_text": "Respuesta: すみません", "a1_desc": "¡Para llamar al camarero o desconocidos siempre se usa すみません!",
            "a2_text": "Respuesta: ごめん / ごめんね", "a2_desc": "¡Con amigos y personas de confianza se usa la forma casual ごめん!",
            "cheat_t1": "¿En público o con desconocidos?", "cheat_b1": '➔ <strong style="color: #B27B00; font-size: 38px;">すみません</strong>',
            "cheat_t2": "¿Con amigos cercanos o pareja?", "cheat_b2": '➔ <strong style="color: #E59800; font-size: 38px;">ごめん (ね)</strong>',
            "dm_keyword": "JLPT", "dm_gift": "<b>Guía PDF de Conversación Real</b> + <b>Test de Nivel</b>"
        },
        # Week 2: 大丈夫の5つの意味
        {
            "pillar": "日常会話・リアル表現 (Week 2)",
            "tag_text": "CONVERSACIÓN REAL 💬",
            "bg_primary": "#FFF9E6", "brand_deep": "#B27B00", "accent_main": "#E59800", "accent_light": "#FFEEC2",
            "student_photo": PHOTO_WEDNESDAY, "photo_position": "center 30%",
            "title_html": 'Los 4 significados de <span style="color: #B27B00; text-decoration: underline;">だいじょうぶ (大丈夫)</span> 🤯🇯🇵',
            "subtitle": "¿Significa 'Sí', 'No', 'Estoy bien' o 'No te preocupes'?",
            "hero_left": {"char": "OK / Sí", "color": "#B27B00", "desc": "Aceptación"},
            "hero_right": {"char": "No, gracias", "color": "#E59800", "desc": "Rechazo cortés"},
            "rule1": {"badge": "1. 'Estoy bien / Sin problema'", "badge_bg": "#B27B00", "title": "Pregunta de bienestar", "desc": "Cuando alguien te pregunta si te has hecho daño o necesitas ayuda.", "ja": 'A: 大丈夫ですか？ B: はい、<ruby>大丈夫<rt>だいじょうぶ</rt></ruby>です！', "es": "A: ¿Estás bien? B: Sí, no pasa nada."},
            "rule2": {"badge": "2. 'No, gracias' (Rechazo)", "badge_bg": "#E59800", "title": "En tiendas / restaurantes", "desc": "Cuando te ofrecen bolsa o recarga y quieres declinar educadamente.", "ja": 'A: レジ袋は要りますか？ B: あ、<ruby>大丈夫<rt>だいじょうぶ</rt></ruby>です。', "es": "A: ¿Quiere bolsa? B: Ah, estoy bien así (No, gracias)."},
            "q1_ja": '（コンビニで店員に）「レシートは ご利用ですか？」 ➔ いらない時：', "q1_es": "(En el combini: ¿Desea el ticket? ➔ Cuando NO lo quieres:)",
            "q2_ja": '（友達が転んだ時）「痛そう！ （ &nbsp;&nbsp;&nbsp;&nbsp; ）？」', "q2_es": "(Tu amigo se tropieza: ¡Parece que duele! ¿Estás bien?)",
            "a1_text": "Respuesta: あ、大丈夫です (No, gracias)", "a1_desc": "¡Es la forma más natural y educada de decir 'No, gracias' en Japón!",
            "a2_text": "Respuesta: 大丈夫？ (¿Estás bien?)", "a2_desc": "¡Pregunta directa de preocupación hacia un amigo o conocido!",
            "cheat_t1": "¿Quieres decir 'No gracias' en una tienda?", "cheat_b1": '➔ Acompaña con un gesto de mano: <strong style="color: #B27B00; font-size: 36px;">大丈夫です</strong>',
            "cheat_t2": "¿Te preguntan si puedes hacer algo el sábado?", "cheat_b2": '➔ ' + 'Sí, puedo: <strong style="color: #E59800; font-size: 36px;">土曜日、大丈夫！</strong>',
            "dm_keyword": "JLPT", "dm_gift": "<b>Guía PDF de Frases Imprescindibles</b> + <b>Test</b>"
        }
    ],
    "VIERNES": [
        # Week 1: 留学ビザ申請タイムライン
        {
            "pillar": "日本留学・ビザ・文化Tips (Week 1)",
            "tag_text": "ESTUDIAR EN JAPÓN DESDE ESPAÑA ✈️🇪🇸🇯🇵",
            "bg_primary": "#F1F8E9", "brand_deep": "#2E7D32", "accent_main": "#43A047", "accent_light": "#DCEDC8",
            "student_photo": PHOTO_FRIDAY, "photo_position": "center 25%",
            "title_html": '¿Cuándo tramitar tu <span style="color: #2E7D32; text-decoration: underline;">Visado de Estudiante</span> para Japón? ✈️🇪🇸',
            "subtitle": "Cronograma paso a paso si viajas desde España (Madrid / Barcelona).",
            "hero_left": {"char": "6 Meses", "color": "#2E7D32", "desc": "Antes: Trámite COE"},
            "hero_right": {"char": "1-2 Meses", "color": "#43A047", "desc": "Antes: Consulado"},
            "rule1": {"badge": "Paso 1: COE", "badge_bg": "#2E7D32", "title": "Certificado de Elegibilidad", "desc": "La escuela en Japón tramita tu COE en inmigración con 5 a 6 meses de antelación.", "ja": '<ruby>留学<rt>りゅうがく</rt></ruby>ビザの <ruby>申請<rt>しんせい</rt></ruby>スケジュール', "es": "Comienza a preparar tus documentos con 6 meses de antelación."},
            "rule2": {"badge": "Paso 2: Visado", "badge_bg": "#43A047", "title": "Consulado en España", "desc": "Con tu COE, tramitas el visado en el Consulado en Barcelona o Embajada en Madrid (1 semana).", "ja": '<ruby>出発<rt>しゅっぱつ</rt></ruby>の <ruby>準備<rt>しゅっぱつ</rt></ruby>をしよう！', "es": "¡Recoges tu pasaporte visado y listos para volar a Japón!"},
            "q1_ja": 'Q1: ¿Con cuántos meses de antelación debes empezar a preparar tu visado de estudiante?', "q1_es": "(a) 1 mes &nbsp;&nbsp;&nbsp;&nbsp; (b) 6 meses",
            "q2_ja": 'Q2: ¿Dónde se estampa tu visado final una vez tienes el COE en España?', "q2_es": "(a) En el Consulado / Embajada en España &nbsp;&nbsp; (b) En el aeropuerto de Tokio",
            "a1_text": "Respuesta: (b) 6 meses de antelación", "a1_desc": "¡Los trámites con las escuelas japonesas y la inmigración requieren tiempo!",
            "a2_text": "Respuesta: (a) En el Consulado / Embajada en España", "a2_desc": "¡Presentas tu COE en Barcelona o Madrid y te estampan el visado en pocos días!",
            "cheat_t1": "🗓️ Convocatoria de Abril (Primavera)", "cheat_b1": '➔ Documentación lista en: <strong style="color: #2E7D32; font-size: 34px;">Octubre - Noviembre</strong>',
            "cheat_t2": "🍂 Convocatoria de Octubre (Otoño)", "cheat_b2": '➔ Documentación lista en: <strong style="color: #43A047; font-size: 34px;">Abril - Mayo</strong>',
            "dm_keyword": "VISA", "dm_gift": "<b>Guía Completa para Estudiar en Japón desde España</b> + <b>Asesoría Gratuita</b>"
        },
        # Week 2: 生活費と住居事情
        {
            "pillar": "日本留学・ビザ・文化Tips (Week 2)",
            "tag_text": "VIDA & ESTUDIO EN JAPÓN 💴🏠",
            "bg_primary": "#F1F8E9", "brand_deep": "#2E7D32", "accent_main": "#43A047", "accent_light": "#DCEDC8",
            "student_photo": PHOTO_FRIDAY, "photo_position": "center 25%",
            "title_html": '¿Cuánto cuesta vivir como <span style="color: #2E7D32; text-decoration: underline;">Estudiante en Japón</span> al mes? 💴🇯🇵',
            "subtitle": "Presupuesto real de alquiler, comida, transporte y trabajo a tiempo parcial.",
            "hero_left": {"char": "¥120,000", "color": "#2E7D32", "desc": "Gasto mensual medio"},
            "hero_right": {"char": "28 Horas", "color": "#43A047", "desc": "Trabajo permitido/sem"},
            "rule1": {"badge": "Gastos Fijos", "badge_bg": "#2E7D32", "title": "Alquiler y Facturas", "desc": "Residencia de estudiantes o sharehouse: entre ¥45,000 y ¥70,000 al mes.", "ja": '<ruby>生活費<rt>せいかつひ</rt></ruby>の <ruby>目安<rt>めやす</rt></ruby>（シェアハウス・<ruby>寮<rt>りょう</rt></ruby>）', "es": "Alojamiento económico y céntrico para estudiantes."},
            "rule2": {"badge": "Trabajo (Arubaito)", "badge_bg": "#43A047", "title": "Ingresos permitidos", "desc": "Con visa de estudiante puedes trabajar hasta 28 horas/semana (aprox. ¥110,000 - ¥130,000/mes).", "ja": '<ruby>留学生<rt>りゅうがくせい</rt></ruby>の アルバイト', "es": "¡Cubre gran parte de tu manutención trabajando legalmente!"},
            "q1_ja": 'Q1: ¿Cuántas horas a la semana puede trabajar legalmente un estudiante extranjero en Japón?', "q1_es": "(a) 15 horas &nbsp;&nbsp;&nbsp;&nbsp; (b) 28 horas",
            "q2_ja": 'Q2: ¿Cuál es el tipo de alojamiento más económico para empezar en Japón?', "q2_es": "(a) Apartamento individual propio &nbsp;&nbsp; (b) Sharehouse o Residencia de escuela",
            "a1_text": "Respuesta: (b) Hasta 28 horas por semana", "a1_desc": "¡Con el permiso de actividades extra (Shikakugai Katsudou Kyoka) que tramitamos!",
            "a2_text": "Respuesta: (b) Sharehouse o Residencia", "a2_desc": "¡No requiere avalistas ni pagar fianzas elevadas de entrada!",
            "cheat_t1": "💡 Consejo de Kamiya Juku para ahorrar", "cheat_b1": '➔ Cocina en casa y aprovecha los supermercados locales (descuentos nocturnos).',
            "cheat_t2": "💼 ¿Nivel de japonés necesario para trabajar?", "cheat_b2": '➔ Con <strong style="color: #2E7D32; font-size: 34px;">N5-N4</strong> accedes a cafeterías, hoteles y tiendas.',
            "dm_keyword": "VISA", "dm_gift": "<b>Guía de Coste de Vida & Alojamiento en Japón</b> + <b>Asesoría</b>"
        }
    ]
}

def load_config_from_sheet(day_key="LUNES"):
    """
    投稿アイデア管理シート.xlsx の該当曜日タブ（月曜_JLPT文法 / 水曜_日常会話 / 金曜_日本留学・ビザ）
    からステータスが【READY】になっている最新の行を読み込む
    """
    candidates = [
        BASE_DIR / "投稿アイデア管理シート.xlsx",
        BASE_DIR.parent / "投稿アイデア管理シート.xlsx",
        Path("/Users/sanakamiya/Library/CloudStorage/GoogleDrive-kamiyajuku.japones@gmail.com/マイドライブ/インスタグラム/投稿アイデア管理シート.xlsx")
    ]
    excel_path = None
    for p in candidates:
        if p.exists():
            excel_path = p
            break

    if not excel_path:
        return None

    tab_map = {
        "LUNES": "月曜_JLPT文法",
        "MIERCOLES": "水曜_日常会話",
        "VIERNES": "金曜_日本留学・ビザ"
    }
    target_sheet_name = tab_map.get(day_key, "月曜_JLPT文法")

    try:
        import openpyxl
        wb = openpyxl.load_workbook(excel_path, data_only=True)
        if target_sheet_name not in wb.sheetnames:
            return None

        ws = wb[target_sheet_name]
        ready_row = None
        # 5行目からデータを探索（A: No, B: ステータス, C: テーマ, D: 補足メモ）
        for r in range(5, ws.max_row + 1):
            status = str(ws.cell(row=r, column=2).value or "").strip().upper()
            theme = str(ws.cell(row=r, column=3).value or "").strip()
            memo = str(ws.cell(row=r, column=4).value or "").strip()
            if status == "READY" and theme:
                ready_row = {"theme": theme, "memo": memo, "row_idx": r}
                break

        if not ready_row:
            return None

        theme = ready_row["theme"]
        memo = ready_row["memo"]

        # デフォルトのスタイル設定
        if day_key == "LUNES":
            bg_primary, brand_deep, accent_main, accent_light, photo = "#EEF4EA", "#1B5E20", "#E8822A", "#DCEBD6", PHOTO_MONDAY
            tag_text = "JLPT N5 / N4 GRAMÁTICA ⛩️"
            dm_kw = "JLPT"
            dm_gift = "<b>Guía PDF de Partículas N5/N4</b> + <b>Test de Nivel</b>"
        elif day_key == "MIERCOLES":
            bg_primary, brand_deep, accent_main, accent_light, photo = "#FFFBEB", "#B45309", "#D97706", "#FEF3C7", PHOTO_WEDNESDAY
            tag_text = "JAPONÉS REAL 🇯🇵"
            dm_kw = "JAPONES"
            dm_gift = "<b>Guía de Expresiones Clave para Viajar a Japón</b> + <b>Audio</b>"
        else:
            bg_primary, brand_deep, accent_main, accent_light, photo = "#F0FDF4", "#15803D", "#2E7D32", "#DCFCE7", PHOTO_FRIDAY
            tag_text = "ESTUDIAR EN JAPÓN ✈️"
            dm_kw = "VISA"
            dm_gift = "<b>Guía Completa para Estudiar en Japón desde España</b> + <b>Asesoría</b>"

        # 既存プールの中にマッチするテーマがあればそれをベースに詳細を展開
        pool = WEEKLY_CONTENT_POOL.get(day_key, [])
        for item in pool:
            if any(k in item.get("pillar", "") for k in theme.split()) or any(k in theme for k in ["は", "が", "に", "で", "ため", "よう", "だいじょうぶ", "すみません", "ビザ", "生活費"]):
                # マッチしたテーマを返却
                res = dict(item)
                res["pillar"] = f"{theme}"
                return res

        # 新規テーマの場合：自動構成を組み立て
        return {
            "pillar": f"{theme}",
            "tag_text": tag_text,
            "bg_primary": bg_primary, "brand_deep": brand_deep, "accent_main": accent_main, "accent_light": accent_light,
            "student_photo": photo, "photo_position": "center 20%",
            "title_html": f'Aprende <span style="color: {accent_main}; text-decoration: underline;">{theme}</span> en japonés 🇯🇵🧠',
            "subtitle": f"Consejos y reglas esenciales: {memo}" if memo else "Aprende la regla definitiva en 30 segundos con Kamiya Juku.",
            "hero_left": {"char": "重要", "color": accent_main, "desc": "Regla Clave"},
            "hero_right": {"char": "実践", "color": brand_deep, "desc": "Ejemplo Real"},
            "rule1": {
                "badge": "Punto 1", "badge_bg": accent_main,
                "title": "Regla y Uso Principal", "desc": f"Explicación para {theme}",
                "ja": f"{theme}の 使い方", "es": f"Uso correcto de {theme} en japonés natural."
            },
            "rule2": {
                "badge": "Punto 2", "badge_bg": brand_deep,
                "title": "Consejo y Caso Especial", "desc": memo if memo else "Ten cuidado con los errores más comunes.",
                "ja": f"{memo}" if memo else "自然な 日本語の 表現", "es": "Expresión natural utilizada por nativos."
            },
            "q1_ja": f"¿Cómo se usa {theme}?", "q1_es": "Elige la opción más natural en una conversación.",
            "q2_ja": "¿En qué situación es más adecuado?", "q2_es": "(a) Situación formal &nbsp;&nbsp; (b) Situación informal",
            "a1_text": "Respuesta: ¡Opción correcta!", "a1_desc": f"¡Porque se adapta a la regla de {theme}!",
            "a2_text": "Respuesta: (a) y (b)", "a2_desc": "¡Según el grado de cortesía y contexto!",
            "cheat_t1": f"💡 Regla de oro para {theme}", "cheat_b1": f"➔ {memo}" if memo else "➔ Práctica activa y lectura diaria.",
            "cheat_t2": "💼 ¿Quieres practicar con nativos?", "cheat_b2": "➔ Clases online en grupos reducidos de Kamiya Juku.",
            "dm_keyword": dm_kw,
            "dm_gift": dm_gift
        }

    except Exception as e:
        print(f"⚠️ Excelシート読み込みエラー: {e}")
        return None

def get_current_week_config(day_key="LUNES", target_date=None):
    """
    1. 投稿アイデア管理シート.csv に READY な行があればそれを最優先で読み込み
    2. なければ週番号（日付）に基づいて自動的にプールから選択
    """
    sheet_config = load_config_from_sheet(day_key)
    if sheet_config:
        return sheet_config

    pool = WEEKLY_CONTENT_POOL.get(day_key, WEEKLY_CONTENT_POOL["LUNES"])
    
    if target_date is None:
        now = datetime.now()
        if now.weekday() in [6, 1, 3] and now.hour >= 20:
            target_date = now + timedelta(days=1)
        else:
            target_date = now

    current_week_num = target_date.isocalendar()[1]
    week_index = (current_week_num - 34) % len(pool)
    return pool[week_index]

DAY_CONFIGS = {
    day: get_current_week_config(day)
    for day in ["LUNES", "MIERCOLES", "VIERNES"]
}

def generate_master_day_html(day_key="LUNES", target_date=None):
    c = get_current_week_config(day_key, target_date=target_date)
    
    html = f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<style>
  @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@500;700;800;900&family=Noto+Sans+JP:wght@500;700;900&display=swap');

  :root {{
    --bg-primary: {c['bg_primary']};
    --bg-card: #FFFFFF;
    --brand-deep: {c['brand_deep']};
    --accent-main: {c['accent_main']};
    --accent-light: {c['accent_light']};
    --text-main: #1A202C;
    --text-muted: #4A5568;
    --card-shadow: 0 16px 36px rgba(0, 0, 0, 0.06);
    --border-radius: 32px;
  }}

  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{ background-color: #333; font-family: 'Montserrat', 'Noto Sans JP', sans-serif; }}

  .slide {{
    width: 1080px; height: 1350px;
    background-color: var(--bg-primary);
    position: relative;
    padding: 75px 70px;
    display: flex; flex-direction: column; justify-content: space-between;
    overflow: hidden;
  }}

  /* ヘッダー */
  .slide-header {{
    display: flex; justify-content: space-between; align-items: center;
    border-bottom: 2px solid rgba(0,0,0,0.08); padding-bottom: 22px;
  }}
  .logo-badge {{
    display: flex; align-items: center; gap: 14px;
    font-weight: 900; font-size: 28px; color: var(--brand-deep);
  }}
  .logo-badge img {{ width: 50px; height: 50px; object-fit: contain; }}
  .slide-counter {{
    background: #FFFFFF; border: 1px solid rgba(0,0,0,0.08);
    padding: 8px 24px; border-radius: 20px;
    font-size: 24px; font-weight: 900; color: var(--brand-deep);
  }}

  /* フッター */
  .slide-footer {{
    display: flex; justify-content: space-between; align-items: center;
    border-top: 2px solid rgba(0,0,0,0.08); padding-top: 22px;
    font-size: 24px; font-weight: 700; color: var(--text-muted);
  }}
  .swipe-cta {{
    display: flex; align-items: center; gap: 12px;
    color: var(--brand-deep); font-weight: 800; font-size: 26px;
  }}

  /* ルビ（ふりがな） */
  ruby {{ ruby-position: over; }}
  rt {{ font-size: 0.52em; color: var(--brand-deep); font-weight: 800; transform: translateY(-3px); }}

  /* タグバッジ */
  .tag-chip {{
    display: inline-block; background: var(--brand-deep);
    color: #FFF; font-size: 22px; font-weight: 900;
    padding: 10px 24px; border-radius: 14px; margin-bottom: 24px; letter-spacing: 0.5px;
  }}

  /* 表紙の対比ヒーローボックス */
  .cover-hero-box {{
    margin-top: 40px; background: #FFF; border-radius: var(--border-radius);
    padding: 44px; display: flex; justify-content: space-around; align-items: center;
    box-shadow: var(--card-shadow); border: 2px solid rgba(0,0,0,0.06);
  }}
  .hero-item {{ text-align: center; }}
  .hero-char {{ font-size: { '76px' if len(c['hero_left']['char']) > 3 else '110px' }; font-weight: 900; line-height: 1; margin-bottom: 12px; }}
  .hero-vs {{ font-size: 40px; font-weight: 900; color: var(--accent-main); }}

  /* ルールカード */
  .rule-card {{
    background: #FFF; border-radius: 28px; padding: 38px 44px;
    box-shadow: var(--card-shadow); border-left: 14px solid var(--accent-main);
    margin-bottom: 28px;
  }}
  .rule-card.rule-second {{ border-left-color: var(--brand-deep); }}
  .rule-badge {{
    font-size: 30px; font-weight: 900; color: #FFF;
    background: var(--accent-main); padding: 6px 20px; border-radius: 12px;
  }}
  .rule-second .rule-badge {{ background: var(--brand-deep); }}
  .example-box {{
    background: #F8FAF7; border-radius: 18px; padding: 20px 26px;
    margin-top: 16px; border: 1px solid rgba(0,0,0,0.06);
  }}
  .example-ja {{ font-size: 38px; font-weight: 800; color: var(--text-main); margin-bottom: 8px; }}
  .example-es {{ font-size: 26px; font-weight: 600; color: var(--text-muted); }}

  /* クイズカード */
  .quiz-card {{
    background: #FFF; border-radius: 28px; padding: 40px;
    margin-bottom: 24px; box-shadow: var(--card-shadow);
    border: 1px solid rgba(0,0,0,0.06);
  }}

  /* 最終スライド（生徒写真＋連絡先CTA） */
  .cta-student-card {{
    background: #FFFFFF; border-radius: var(--border-radius);
    padding: 34px 40px; box-shadow: var(--card-shadow);
    border: 2px solid rgba(0,0,0,0.06);
  }}
  .student-photo-banner {{
    width: 100%; height: 260px; border-radius: 20px;
    object-fit: cover; object-position: {c['photo_position']};
    margin-bottom: 22px; box-shadow: 0 8px 20px rgba(0,0,0,0.12);
  }}
  .contact-badge-box {{
    display: flex; justify-content: space-around; background: #F8FAF7;
    border-radius: 16px; padding: 18px 20px; margin-top: 18px;
    font-size: 21px; font-weight: 800; color: var(--text-main);
  }}
</style>
</head>
<body>

  <!-- ==================== Slide 1: 表紙 ==================== -->
  <div class="slide" id="slide-1">
    <div class="slide-header">
      <div class="logo-badge">
        <img src="file://{LOGO_PATH}">
        <span>KAMIYA JUKU <small style="font-size: 18px; font-weight: normal; color: #718096;">神谷塾</small></span>
      </div>
      <div class="slide-counter">1 / 6</div>
    </div>
    
    <div>
      <div class="tag-chip">{c['tag_text']}</div>
      <h1 style="font-size: 60px; font-weight: 900; line-height: 1.18; color: var(--text-main); margin-bottom: 18px;">
        {c['title_html']}
      </h1>
      <p style="font-size: 32px; font-weight: 700; color: var(--text-muted); line-height: 1.4;">
        {c['subtitle']}
      </p>

      <div class="cover-hero-box">
        <div class="hero-item">
          <div class="hero-char" style="color: {c['hero_left']['color']};">{c['hero_left']['char']}</div>
          <div style="font-size: 26px; font-weight: 800; color: var(--text-muted);">{c['hero_left']['desc']}</div>
        </div>
        <div class="hero-vs">VS</div>
        <div class="hero-item">
          <div class="hero-char" style="color: {c['hero_right']['color']};">{c['hero_right']['char']}</div>
          <div style="font-size: 26px; font-weight: 800; color: var(--text-muted);">{c['hero_right']['desc']}</div>
        </div>
      </div>
    </div>

    <div class="slide-footer">
      <div>@japones_kamiyajuku</div>
      <div class="swipe-cta">Desliza para ver la regla 👉</div>
    </div>
  </div>

  <!-- ==================== Slide 2: ルール解説 ==================== -->
  <div class="slide" id="slide-2">
    <div class="slide-header">
      <div class="logo-badge">
        <img src="file://{LOGO_PATH}">
        <span>KAMIYA JUKU <small style="font-size: 18px; font-weight: normal; color: #718096;">神谷塾</small></span>
      </div>
      <div class="slide-counter">2 / 6</div>
    </div>

    <div>
      <div class="rule-card">
        <div style="display: flex; align-items: center; gap: 16px; margin-bottom: 12px;">
          <div class="rule-badge" style="background: {c['rule1']['badge_bg']};">{c['rule1']['badge']}</div>
          <div style="font-size: 32px; font-weight: 900; color: var(--text-main);">{c['rule1']['title']}</div>
        </div>
        <p style="font-size: 26px; color: var(--text-muted); font-weight: 600;">{c['rule1']['desc']}</p>
        <div class="example-box">
          <div class="example-ja">{c['rule1']['ja']}</div>
          <div class="example-es">{c['rule1']['es']}</div>
        </div>
      </div>

      <div class="rule-card rule-second">
        <div style="display: flex; align-items: center; gap: 16px; margin-bottom: 12px;">
          <div class="rule-badge" style="background: {c['rule2']['badge_bg']};">{c['rule2']['badge']}</div>
          <div style="font-size: 32px; font-weight: 900; color: var(--text-main);">{c['rule2']['title']}</div>
        </div>
        <p style="font-size: 26px; color: var(--text-muted); font-weight: 600;">{c['rule2']['desc']}</p>
        <div class="example-box">
          <div class="example-ja">{c['rule2']['ja']}</div>
          <div class="example-es">{c['rule2']['es']}</div>
        </div>
      </div>
    </div>

    <div class="slide-footer">
      <div>@japones_kamiyajuku</div>
      <div class="swipe-cta">¡Ponte a prueba en el quiz! 👉</div>
    </div>
  </div>

  <!-- ==================== Slide 3: クイズ問題 ==================== -->
  <div class="slide" id="slide-3">
    <div class="slide-header">
      <div class="logo-badge">
        <img src="file://{LOGO_PATH}">
        <span>KAMIYA JUKU <small style="font-size: 18px; font-weight: normal; color: #718096;">神谷塾</small></span>
      </div>
      <div class="slide-counter">3 / 6</div>
    </div>

    <div>
      <div class="tag-chip">MINI QUIZ 神谷塾</div>
      <h2 style="font-size: 42px; font-weight: 900; color: var(--brand-deep); margin-bottom: 28px;">
        ¿Cuál es la opción correcta? 🤔✍️
      </h2>
      
      <div class="quiz-card" style="padding: 42px 38px;">
        <div style="font-size: 36px; font-weight: 900; color: var(--brand-deep); margin-bottom: 12px;">
          ❓ <strong>Q1:</strong> {c['q1_ja']}
        </div>
        <p style="font-size: 24px; color: var(--text-muted); font-weight: 600;">{c['q1_es']}</p>
      </div>

      <div class="quiz-card" style="padding: 42px 38px;">
        <div style="font-size: 36px; font-weight: 900; color: var(--brand-deep); margin-bottom: 12px;">
          ❓ <strong>Q2:</strong> {c['q2_ja']}
        </div>
        <p style="font-size: 24px; color: var(--text-muted); font-weight: 600;">{c['q2_es']}</p>
      </div>
    </div>

    <div class="slide-footer">
      <div>@japones_kamiyajuku</div>
      <div class="swipe-cta">🤔 ¿Tienes tu respuesta? ¡Desliza! 👉</div>
    </div>
  </div>

  <!-- ==================== Slide 4: 解答と解説 ==================== -->
  <div class="slide" id="slide-4">
    <div class="slide-header">
      <div class="logo-badge">
        <img src="file://{LOGO_PATH}">
        <span>KAMIYA JUKU <small style="font-size: 18px; font-weight: normal; color: #718096;">神谷塾</small></span>
      </div>
      <div class="slide-counter">4 / 6</div>
    </div>

    <div>
      <div class="tag-chip">RESPUESTAS & EXPLICACIÓN</div>
      
      <div class="quiz-card" style="border-left: 14px solid var(--brand-deep);">
        <div style="font-size: 28px; font-weight: 800; color: var(--text-muted); margin-bottom: 10px;">
          Q1: {c['q1_ja']}
        </div>
        <div style="background: {c['accent_light']}; padding: 20px 24px; border-radius: 16px;">
          <div style="font-size: 30px; font-weight: 900; color: var(--brand-deep);">✅ {c['a1_text']}</div>
          <div style="font-size: 24px; color: var(--brand-deep); font-weight: 700; margin-top: 6px;">
            {c['a1_desc']}
          </div>
        </div>
      </div>

      <div class="quiz-card" style="border-left: 14px solid var(--accent-main); margin-top: 24px;">
        <div style="font-size: 28px; font-weight: 800; color: var(--text-muted); margin-bottom: 10px;">
          Q2: {c['q2_ja']}
        </div>
        <div style="background: #FFF4E8; padding: 20px 24px; border-radius: 16px;">
          <div style="font-size: 30px; font-weight: 900; color: #C05621;">✅ {c['a2_text']}</div>
          <div style="font-size: 24px; color: #7B341E; font-weight: 700; margin-top: 6px;">
            {c['a2_desc']}
          </div>
        </div>
      </div>
    </div>

    <div class="slide-footer">
      <div>@japones_kamiyajuku</div>
      <div class="swipe-cta">Resumen rápido para memorizar 👉</div>
    </div>
  </div>

  <!-- ==================== Slide 5: チートシート ==================== -->
  <div class="slide" id="slide-5">
    <div class="slide-header">
      <div class="logo-badge">
        <img src="file://{LOGO_PATH}">
        <span>KAMIYA JUKU <small style="font-size: 18px; font-weight: normal; color: #718096;">神谷塾</small></span>
      </div>
      <div class="slide-counter">5 / 6</div>
    </div>

    <div class="quiz-card" style="padding: 48px;">
      <h2 style="font-size: 44px; font-weight: 900; color: var(--brand-deep); margin-bottom: 28px;">
        🧠 Truco Rápido de Kamiya Juku:
      </h2>
      
      <div style="display: flex; flex-direction: column; gap: 28px; font-size: 26px;">
        <div style="background: #FFF9F2; padding: 28px; border-radius: 20px; border-left: 12px solid var(--accent-main);">
          <strong style="font-size: 28px;">{c['cheat_t1']}</strong><br>
          {c['cheat_b1']}
        </div>

        <div style="background: #F4FAF2; padding: 28px; border-radius: 20px; border-left: 12px solid var(--brand-deep);">
          <strong style="font-size: 28px;">{c['cheat_t2']}</strong><br>
          {c['cheat_b2']}
        </div>
      </div>
    </div>

    <div class="slide-footer">
      <div>@japones_kamiyajuku</div>
      <div class="swipe-cta">¡Regalo exclusivo en el siguiente! 👉</div>
    </div>
  </div>

  <!-- ==================== Slide 6: 生徒写真＋WhatsApp/メール連絡先CTA ==================== -->
  <div class="slide" id="slide-6">
    <div class="slide-header">
      <div class="logo-badge">
        <img src="file://{LOGO_PATH}">
        <span>KAMIYA JUKU <small style="font-size: 18px; font-weight: normal; color: #718096;">神谷塾</small></span>
      </div>
      <div class="slide-counter">6 / 6</div>
    </div>

    <div class="cta-student-card">
      <img class="student-photo-banner" src="file://{c['student_photo']}" alt="Estudiantes de Kamiya Juku">
      
      <div style="text-align: center;">
        <h2 style="font-size: 38px; font-weight: 900; color: var(--brand-deep); margin-bottom: 10px;">
          ¿Quieres dominar el japonés este año? 🎓🇯🇵
        </h2>
        <p style="font-size: 23px; color: var(--text-muted); font-weight: 600; margin-bottom: 16px;">
          Aprende con profesores nativos en clases particulares online & grupos reducidos.
        </p>

        <div style="background: {c['bg_primary']}; border: 2px solid var(--brand-deep); border-radius: 20px; padding: 20px; margin-bottom: 16px;">
          <p style="font-size: 19px; font-weight: 800; color: var(--brand-deep); letter-spacing: 1px;">ENVÍA UN DM CON LA PALABRA</p>
          <div style="font-size: 52px; font-weight: 900; color: var(--accent-main); margin: 4px 0;">"{c['dm_keyword']}"</div>
          <p style="font-size: 19px; color: var(--text-muted); font-weight: 700;">y recibe nuestra {c['dm_gift']}</p>
        </div>

        <div class="contact-badge-box">
          <div>📱 WhatsApp: <b>+34 682 054 654</b></div>
          <div>✉️ Email: <b>info@kamiyajuku.com</b></div>
        </div>
      </div>
    </div>

    <div class="slide-footer">
      <div>@japones_kamiyajuku</div>
      <div style="color: var(--brand-deep); font-weight: 800;">¡Síguenos y guarda este post! 🔖</div>
    </div>
  </div>

</body>
</html>
"""
    return html

async def render_day_carousel(day_key="LUNES"):
    html_code = generate_master_day_html(day_key)
    temp_html = ASSETS_DIR / f"temp_master_{day_key}.html"
    with open(temp_html, "w", encoding="utf-8") as f:
        f.write(html_code)

    output_paths = []
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={"width": 1080, "height": 1350}, device_scale_factor=2)
        await page.goto(f"file://{temp_html.resolve()}", wait_until="networkidle")

        for i in range(1, 7):
            el = await page.query_selector(f"#slide-{i}")
            if el:
                out_p = str(ASSETS_DIR / f"master_slide_{day_key}_{i}.jpg")
                await el.screenshot(path=out_p, type="jpeg", quality=95)
                output_paths.append(out_p)
        await browser.close()
    return output_paths

if __name__ == "__main__":
    for d in ["LUNES", "MIERCOLES", "VIERNES"]:
        print(f"🚀 【{d}】カルーセル生成中...")
        slides = asyncio.run(render_day_carousel(d))
        print(f"✅ 【{d}】完了: {len(slides)} 枚")
