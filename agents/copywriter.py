from typing import Optional
from schemas import InstagramPostPackage, PostContent, PostStatus
from config import settings

class CopywriterAgent:
    """
    バイリンガル（スペイン語・日本語）コピーライターエージェント
    スペイン語圏の学習者に向けたHook、文法・単語解説、例文、CTA、ハッシュタグを生成
    ※ 重要ルール: 初中級者向けのため、使用する漢字には必ず振り仮名（ルビ / ローマ字）を付与する
    """
    def __init__(self):
        pass

    def write_copy(self, package: InstagramPostPackage, revision_instructions: Optional[str] = None) -> InstagramPostPackage:
        topic = package.metadata.topic_summary
        category = package.metadata.category
        
        # 決定されたCTAトリガーワード
        cta_word = "CLASE" if category != "STUDY_IN_JAPAN" else "ESTUDIO"
        if category == "JLPT":
            cta_word = "JLPT"

        hook_es = "¿Sabías que 'すみません' (Sumimasen) NO solo significa 'lo siento'? 🤔🇯🇵"
        
        body_es = (
            "Muchos estudiantes de japonés usan 'すみません' y 'ごめんなさい' indistintamente, ¡pero tienen matices muy importantes!\n\n"
            "📌 1. すみません (Sumimasen)\n"
            "・Uso 1: Disculpa leve ('Perdón por pasar')\n"
            "・Uso 2: Agradecimiento ('Gracias por la molestia')\n"
            "・Uso 3: Llamar la atención ('¡Disculpe! / Excuse me')\n\n"
            "📌 2. ごめんなさい (Gomennasai)\n"
            "・Una disculpa sincera y personal dirigida a amigos, familiares o personas cercanas.\n"
            "⚠️ ¡Evita usarlo con tu jefe o en un examen de JLPT oral formal!\n\n"
            "💬 ¿Cuál de estas palabras usas más seguido? ¡Cuéntanos en los comentarios!"
        )

        caption_full = (
            f"{hook_es}\n\n"
            f"{body_es}\n\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"🎓 ¡Aprende japonés real y prepara tu viaje a Japón con 神谷塾 (Kamiyajuku)!\n\n"
            f"📩 Envía un DM con la palabra \"{cta_word}\" para recibir:\n"
            f"✅ Información de nuestras clases online en vivo\n"
            f"✅ Guía de becas y visas para estudiar en Japón\n"
            f"✅ Test de nivel gratuito\n\n"
            f"¡Síguenos en @japones_kamiyajuku para más lecciones diarias! 🌸\n"
            f"━━━━━━━━━━━━━━━━━━━━\n\n"
            f"#aprenderjapones #estudiarjapones #idiomajapones #nihongo #jlpt #jlptn5 #jlptn4 #viajarajapon #estudiarenjapon #becasjapon #kamiyajuku #japon"
        )

        hashtags = [
            "#aprenderjapones", "#estudiarjapones", "#idiomajapones", "#nihongo",
            "#jlpt", "#jlptn5", "#jlptn4", "#viajarajapon", "#estudiarenjapon",
            "#becasjapon", "#kamiyajuku", "#japon"
        ]

        if revision_instructions:
            caption_full = f"【修正反映】\n{caption_full}\n\n(※修正指示: {revision_instructions})"

        package.content = PostContent(
            title_ja="「すみません」と「ごめんなさい」の完全使い分け",
            title_es="¿Cómo decir 'Lo siento' correctamente en japonés?",
            caption_full=caption_full,
            hook_es=hook_es,
            body_es=body_es,
            cta_trigger_word=cta_word,
            hashtags=hashtags
        )
        package.status = PostStatus.DRAFTED
        package.log("CopywriterAgent: Generated bilingual Spanish/Japanese caption and DM CTA.")
        return package
