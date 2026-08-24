import os
from pathlib import Path
from typing import List, Optional
try:
    from PIL import Image, ImageDraw, ImageFont
    HAS_PIL = True
except ImportError:
    HAS_PIL = False

from schemas import InstagramPostPackage, PostVisuals, VisualSlide, PostStatus
from integrations.google_drive import DriveInspector
from config import settings

class DesignDriveAgent:
    """
    画像生成・素材管理エージェント
    Google Driveのフォルダを検査し、素材があれば利用、なければPillowで1080x1350カルーセル画像を自動生成
    """
    def __init__(self):
        self.drive_inspector = DriveInspector()
        self.output_dir = settings.GENERATED_ASSETS_DIR

    def generate_carousel_slide_image(self, post_id: str, slide_index: int, total_slides: int, headline: str, subtitle: str, body: str, is_cta: bool = False) -> str:
        """1080x1350 (Instagram 4:5 縦長推奨比率) の画像をレンダリング"""
        output_path = self.output_dir / f"{post_id}_slide_{slide_index}.jpg"

        if not HAS_PIL:
            # PIL未インストール時のプレースホルダー作成
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(f"KAMIAJUKU SLIDE {slide_index}/{total_slides}\n{headline}\n{subtitle}\n{body}")
            return str(output_path)

        width, height = 1080, 1350
        
        # カラーパレット（神谷塾 公式パンフレット準拠カラー）
        # 背景: 抹茶セージグリーン (#EEF4EA), 濃緑 (#2A5A35), アクセント: オレンジ (#E8822A), カード: 白 (#FFFFFF)
        bg_color = (238, 244, 234) if not is_cta else (28, 61, 36)
        text_color = (28, 40, 29) if not is_cta else (255, 255, 255)
        accent_color = (232, 130, 42) if not is_cta else (249, 178, 51)
        card_bg = (255, 255, 255) if not is_cta else (42, 90, 53)
        brand_green = (42, 90, 53)

        img = Image.new("RGB", (width, height), color=bg_color)
        draw = ImageDraw.Draw(img)

        # 枠線・カード装飾
        margin = 60
        draw.rectangle(
            [(margin, margin), (width - margin, height - margin)],
            fill=card_bg,
            outline=(230, 230, 230) if not is_cta else (60, 75, 120),
            width=3
        )

        # ヘッダーロゴ & スライド番号
        header_text = "KAMIYA JUKU (神谷塾) 🇯🇵"
        draw.text((margin + 40, margin + 40), header_text, fill=accent_color)
        draw.text((width - margin - 120, margin + 40), f"{slide_index}/{total_slides}", fill=(120, 120, 120) if not is_cta else (200, 200, 200))

        # ヘッドライン
        draw.text((margin + 40, margin + 180), headline, fill=text_color)
        
        # サブタイトル
        draw.text((margin + 40, margin + 260), subtitle, fill=accent_color)

        # 本文ブロック
        y_cursor = margin + 380
        for line in body.split("\n"):
            draw.text((margin + 40, y_cursor), line, fill=text_color)
            y_cursor += 50

        # フッター誘導
        footer_text = "Desliza para seguir aprendiendo 👉" if not is_cta else "¡Envía DM a @japones_kamiyajuku! 📩"
        draw.text((margin + 40, height - margin - 80), footer_text, fill=accent_color)

        output_path = self.output_dir / f"{post_id}_slide_{slide_index}.jpg"
        img.save(output_path, "JPEG", quality=95)
        return str(output_path)

    def process_visuals(self, package: InstagramPostPackage, is_story: bool = False) -> InstagramPostPackage:
        topic = package.metadata.topic_summary
        category = package.metadata.category.value
        post_id = package.post_id

        # 1. Google Drive / ローカル素材フォルダの検査
        existing_assets = self.drive_inspector.find_assets_for_topic(topic, day_category=category)
        
        slides: List[VisualSlide] = []
        if is_story or (existing_assets and len(existing_assets) > 0):
            # ストーリーズ画像（9:16）として1枚採用
            target_asset = existing_assets[0] if existing_assets else str(self.output_dir / "story_mock.jpg")
            media_type = "STORIES" if is_story else "CAROUSEL_ALBUM"
            
            if is_story:
                slides.append(VisualSlide(
                    slide_index=1,
                    image_path=target_asset,
                    headline=f"Kamiyajuku Story ({category})",
                    caption_overlay=topic
                ))
            else:
                for idx, path in enumerate(existing_assets[:5], start=1):
                    slides.append(VisualSlide(
                        slide_index=idx,
                        image_path=path,
                        headline=f"Kamiyajuku {category} Event",
                        caption_overlay=topic
                    ))
            source_type = "GOOGLE_DRIVE"
        else:
            # カルーセルスライド画像を自動生成 (4枚構成)
            source_type = "GENERATED"
            media_type = "CAROUSEL_ALBUM"
            slide_configs = [
                {
                    "headline": "¿Cómo decir 'Lo siento'?",
                    "subtitle": "すみません vs ごめんなさい",
                    "body": "Aprende la diferencia crucial\npara no cometer errores en Japón 🇯🇵\n\n・¿Cuándo es formal?\n・¿Cuál sirve para dar gracias?",
                    "is_cta": False
                },
                {
                    "headline": "1. すみません (Sumimasen)",
                    "subtitle": "La palabra 'mágica' en Japón",
                    "body": "✔ Disculpa leve por incomodar\n✔ Agradecimiento por un favor\n✔ Llamar al mesero o pedir paso",
                    "is_cta": False
                },
                {
                    "headline": "2. ごめんなさい (Gomennasai)",
                    "subtitle": "Disculpa cercana y emocional",
                    "body": "✔ Para amigos y familia\n✔ Disculpa sincera de corazón\n❌ ¡No usar con jefes o clientes!",
                    "is_cta": False
                },
                {
                    "headline": "¡Estudia en Japón con nosotros!",
                    "subtitle": "@japones_kamiyajuku",
                    "body": "Ofrecemos:\n• Clases online JLPT N5 - N1\n• Asesoría para visa de estudiante\n• Comunidad internacional\n\n📩 Escribe 'CLASE' o 'JLPT' por DM",
                    "is_cta": True
                }
            ]

            total = len(slide_configs)
            for idx, config in enumerate(slide_configs, start=1):
                img_path = self.generate_carousel_slide_image(
                    post_id=post_id,
                    slide_index=idx,
                    total_slides=total,
                    headline=config["headline"],
                    subtitle=config["subtitle"],
                    body=config["body"],
                    is_cta=config["is_cta"]
                )
                slides.append(VisualSlide(
                    slide_index=idx,
                    image_path=img_path,
                    headline=config["headline"],
                    caption_overlay=config["subtitle"]
                ))

        package.visuals = PostVisuals(
            media_type=media_type,
            source=source_type,
            slides=slides
        )
        package.status = PostStatus.DESIGNED
        package.log(f"DesignDriveAgent: Prepared {len(slides)} items for {media_type} using {source_type}.")
        return package
