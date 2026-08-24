from datetime import datetime
from typing import Optional
from schemas import (
    InstagramPostPackage, PostMetadata, PostCategory, TargetLevel, 
    PostPlan, SlidePlan, PostStatus
)

class CalendarTrendAgent:
    """
    企画・カレンダー連動・トレンドリサーチエージェント
    JLPT（7月/12月）や日本留学の年間スケジュール、曜日テーマに合わせて投稿を企画
    """
    def __init__(self):
        self.day_mapping = {
            0: ("LUNES", PostCategory.JLPT, TargetLevel.N5, "文法・基礎フレーズ徹底解説"),
            1: ("MARTES", PostCategory.STUDY_IN_JAPAN, TargetLevel.VISA_SEEKER, "日本留学・ビザ申請・生活ガイド"),
            2: ("MIERCOLES", PostCategory.PRACTICAL_JAPANESE, TargetLevel.N4, "アニメや日常で使えるリアル日本語"),
            3: ("JUEVES", PostCategory.JLPT, TargetLevel.N3, "間違えやすい類義語・JLPT対策ポイント"),
            4: ("VIERNES", PostCategory.EVENT_COMMUNITY, TargetLevel.ALL, "週末カルチャー・受講生の成果・交流イベント"),
            5: ("SABADO", PostCategory.PRACTICAL_JAPANESE, TargetLevel.ALL, "漢字・カタカナ言葉のトリビア"),
            6: ("DOMINGO", PostCategory.STUDY_IN_JAPAN, TargetLevel.VISA_SEEKER, "来週の目標・留学カウンセリング案内")
        }

    def plan_post(self, specific_theme: Optional[str] = None, target_date: Optional[datetime] = None) -> InstagramPostPackage:
        now = target_date or datetime.now()
        day_of_week = now.weekday()
        day_tag, category, level, default_topic = self.day_mapping.get(
            day_of_week, 
            ("LUNES", PostCategory.JLPT, TargetLevel.N5, "文法解説")
        )

        topic = specific_theme or default_topic
        post_id = f"KMY_{now.strftime('%Y%m%d_%H%M%S')}"

        # テーマに応じたスライド構成案
        slides_outline = [
            SlidePlan(
                slide_index=1,
                headline="¿Cómo decir 'Lo siento' correctamente en japonés? 🙇‍♂️",
                body_text_ja="「すみません」と「ごめんなさい」の違い",
                body_text_es="No siempre significan lo mismo. Descubre cómo usarlos sin sonar descortés.",
                notes_for_designer="表紙。インパクトのあるタイトルと対比デザイン"
            ),
            SlidePlan(
                slide_index=2,
                headline="1. すみません (Sumimasen)",
                body_text_ja="軽い謝罪、感謝（ありがとう）、呼びかけ（Excuse me）に使えます。",
                body_text_es="Es el más versátil: sirve para disculparse, agradecer o llamar la atención de alguien.",
                notes_for_designer="使用例と例文をカード形式で配置"
            ),
            SlidePlan(
                slide_index=3,
                headline="2. ごめんなさい (Gomennasai)",
                body_text_ja="親しい人への心からの謝罪。ビジネスや目上の人には使いません。",
                body_text_es="Disculpa más personal y cercana. ¡Cuidado! No se usa en situaciones formales de trabajo.",
                notes_for_designer="注意点マーク（⚠️）とポイントを強調"
            ),
            SlidePlan(
                slide_index=4,
                headline="¡Aprende japonés real con Kamiyajuku! 🇯🇵",
                body_text_ja="神谷塾で一緒に日本語と日本留学の夢を叶えましょう！",
                body_text_es="Envía 'CLASE' por DM para tu clase de prueba gratis o info sobre visas de estudio.",
                notes_for_designer="最終スライド（CTA）。神谷塾ロゴとDM誘導"
            )
        ]

        metadata = PostMetadata(
            category=category,
            target_level=level,
            goal="LEAD_DM",
            topic_summary=topic
        )

        package = InstagramPostPackage(
            post_id=post_id,
            created_at=now,
            status=PostStatus.PLANNING,
            metadata=metadata
        )
        package.log(f"CalendarTrendAgent: Planned topic '{topic}' under category {category} (Day: {day_tag})")
        return package
