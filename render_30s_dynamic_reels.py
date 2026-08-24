import os
import sys
import asyncio
import cv2
import numpy as np
from pathlib import Path
from playwright.async_api import async_playwright

BASE_DIR = Path(__file__).resolve().parent
ASSETS_DIR = BASE_DIR / "generated_assets"
ASSETS_DIR.mkdir(parents=True, exist_ok=True)

LOGO_PATH = BASE_DIR / "brand_logo_main.png"

# 祭り2025の複数写真素材
MATSURI_DIR = Path("/Users/sanakamiya/Library/CloudStorage/GoogleDrive-kamiyajuku.japones@gmail.com/マイドライブ/インスタグラム/01_ 未処理素材・塾のイベント参加/祭り2025")
PHOTO_M1 = MATSURI_DIR / "DSC01048.JPG" # ひらがなゲーム
PHOTO_M2 = MATSURI_DIR / "DSC01053.JPG" # 生徒と笑顔の対話
PHOTO_M3 = MATSURI_DIR / "DSC01070.JPG" # ブース全体の賑わい
PHOTO_M4 = MATSURI_DIR / "DSC01094.JPG" # 現地参加者との交流

# 北海道留学プログラムの複数写真素材
HOKKAIDO_DIR = Path("/Users/sanakamiya/Library/CloudStorage/GoogleDrive-kamiyajuku.japones@gmail.com/.shortcut-targets-by-id/1uPYf673b3arv-oHAxUHyhCRgV1M6laha/DOWNLOAD｜HOKKAIDO")
PHOTO_H1 = HOKKAIDO_DIR / "Group Lesson 1.JPG" # 教室授業
PHOTO_H2 = HOKKAIDO_DIR / "Communication in Cafe.JPG" # カフェでの交流
PHOTO_H3 = HOKKAIDO_DIR / "Kimono Experience.jpg" # 着物文化体験
PHOTO_H4 = HOKKAIDO_DIR / "Graduation.JPG" # 卒業式・達成感

# 東北大学・正規留学実績の複数写真素材
TOHOKU_DIR = Path("/Users/sanakamiya/Library/CloudStorage/GoogleDrive-kamiyajuku.japones@gmail.com/マイドライブ/インスタグラム/01_ 未処理素材・塾のイベント参加/留学生")
PHOTO_T1 = TOHOKU_DIR / "PHOTO-2025-10-06-15-48-43.jpg" # 東北大学前集合写真
PHOTO_T2 = TOHOKU_DIR / "PHOTO-2025-10-28-10-55-09.jpg" # キャンパス風景

# ========================================================
# 1. バルセロナ祭り 30秒マルチ写真リール (全5シーン・30秒)
# ========================================================
def generate_matsuri_30s_reel_html():
    return f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<style>
  @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@700;800;900&family=Noto+Sans+JP:wght@700;900&display=swap');
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{ width: 1080px; height: 1920px; background-color: #FFF9E6; font-family: 'Montserrat', 'Noto Sans JP', sans-serif; overflow: hidden; }}
  .scene {{ display: none; width: 1080px; height: 1920px; padding: 90px 70px; flex-direction: column; justify-content: space-between; }}
  .scene.active {{ display: flex; }}
  
  .reel-header {{ display: flex; justify-content: space-between; align-items: center; background: rgba(255,255,255,0.95); padding: 20px 34px; border-radius: 40px; box-shadow: 0 10px 30px rgba(0,0,0,0.08); }}
  .logo-box {{ display: flex; align-items: center; gap: 14px; font-size: 28px; font-weight: 900; color: #B27B00; }}
  .logo-box img {{ width: 52px; height: 52px; object-fit: contain; }}
  
  .photo-frame {{ width: 100%; height: 980px; border-radius: 36px; overflow: hidden; box-shadow: 0 20px 50px rgba(0,0,0,0.14); border: 4px solid #FFFFFF; }}
  .photo-frame img {{ width: 100%; height: 100%; object-fit: cover; }}
  
  .text-card {{ background: #FFFFFF; border-radius: 32px; padding: 44px; box-shadow: 0 16px 40px rgba(0,0,0,0.08); text-align: center; border-top: 12px solid #B27B00; }}
  .badge-tag {{ display: inline-block; background: #B27B00; color: #FFF; font-size: 22px; font-weight: 900; padding: 8px 24px; border-radius: 20px; margin-bottom: 14px; }}
  .main-title {{ font-size: 50px; font-weight: 900; line-height: 1.25; color: #1A202C; }}
  .sub-title {{ font-size: 28px; font-weight: 700; color: #4A5568; margin-top: 10px; }}
</style>
</head>
<body>
  <!-- Scene 1: 写真1 (0-6s) -->
  <div class="scene active" id="scene-1">
    <div class="reel-header">
      <div class="logo-box"><img src="file://{LOGO_PATH}"><span>KAMIYA JUKU 神谷塾</span></div>
      <div style="font-size: 24px; font-weight: 900; color: #E59800;">🇪🇸 MATSURI BARCELONA</div>
    </div>
    <div class="photo-frame"><img src="file://{PHOTO_M1}" style="object-position: center 30%;"></div>
    <div class="text-card">
      <div class="badge-tag">COMUNIDAD EN ESPAÑA ⛩️</div>
      <div class="main-title">Aprende Japonés Real<br>con <span style="color: #B27B00;">Profesores Nativos</span></div>
      <div class="sub-title">Eventos culturales, juegos de kanji y práctica viva.</div>
    </div>
  </div>

  <!-- Scene 2: 写真2 (6-12s) -->
  <div class="scene" id="scene-2">
    <div class="reel-header">
      <div class="logo-box"><img src="file://{LOGO_PATH}"><span>KAMIYA JUKU 神谷塾</span></div>
      <div style="font-size: 24px; font-weight: 900; color: #B27B00;">💬 AMBIENTE CERCANO</div>
    </div>
    <div class="photo-frame"><img src="file://{PHOTO_M2}" style="object-position: center 25%;"></div>
    <div class="text-card" style="border-top-color: #E8822A;">
      <div class="badge-tag" style="background: #E8822A;">SIN MIEDO A EQUIVOCARTE 🌸</div>
      <div class="main-title">Aprende a tu Ritmo en<br><span style="color: #E8822A;">Grupos Reducidos & Online</span></div>
      <div class="sub-title">Un espacio donde cada alumno recibe atención personalizada.</div>
    </div>
  </div>

  <!-- Scene 3: 写真3 (12-18s) -->
  <div class="scene" id="scene-3">
    <div class="reel-header">
      <div class="logo-box"><img src="file://{LOGO_PATH}"><span>KAMIYA JUKU 神谷塾</span></div>
      <div style="font-size: 24px; font-weight: 900; color: #1B5E20;">🎌 PASIÓN POR JAPÓN</div>
    </div>
    <div class="photo-frame"><img src="file://{PHOTO_M3}" style="object-position: center 35%;"></div>
    <div class="text-card" style="border-top-color: #1B5E20;">
      <div class="badge-tag" style="background: #1B5E20;">MÉTODO DINÁMICO 💡</div>
      <div class="main-title">De Cero a Hablar con<br><span style="color: #1B5E20;">Seguridad y Confianza</span></div>
      <div class="sub-title">Gramática clara, pronunciación real y cultura japonesa.</div>
    </div>
  </div>

  <!-- Scene 4: 写真4 (18-24s) -->
  <div class="scene" id="scene-4">
    <div class="reel-header">
      <div class="logo-box"><img src="file://{LOGO_PATH}"><span>KAMIYA JUKU 神谷塾</span></div>
      <div style="font-size: 24px; font-weight: 900; color: #B27B00;">🇯🇵 COMUNIDAD KAMIYA JUKU</div>
    </div>
    <div class="photo-frame"><img src="file://{PHOTO_M4}" style="object-position: center 20%;"></div>
    <div class="text-card">
      <div class="badge-tag">BARCELONA & ONLINE 🌍</div>
      <div class="main-title">Conecta con Personas<br>que <span style="color: #B27B00;">comparten tu pasión</span></div>
      <div class="sub-title">Clases para todos los niveles: N5, N4, N3 y conversación.</div>
    </div>
  </div>

  <!-- Scene 5: CTA (24-30s) -->
  <div class="scene" id="scene-5">
    <div class="reel-header">
      <div class="logo-box"><img src="file://{LOGO_PATH}"><span>KAMIYA JUKU 神谷塾</span></div>
      <div style="font-size: 24px; font-weight: 900; color: #B27B00;">🎁 REGALO EXCLUSIVO</div>
    </div>
    <div class="text-card" style="padding: 60px 48px; margin: auto 0;">
      <div style="font-size: 80px; margin-bottom: 12px;">⛩️🇪🇸</div>
      <h1 style="font-size: 50px; font-weight: 900; color: #B27B00; line-height: 1.2;">
        ¡Empieza hoy tu camino con el japonés!
      </h1>
      <p style="font-size: 26px; color: #4A5568; font-weight: 700; margin: 16px 0;">
        Aprende con nosotros en clases online y grupos reducidos.
      </p>
      <div style="background: linear-gradient(135deg, #B27B00 0%, #E59800 100%); color:#FFF; border-radius: 28px; padding: 36px; margin: 26px 0;">
        <p style="font-size: 22px; font-weight: 800; letter-spacing: 1px;">ENVÍA UN DM CON LA PALABRA</p>
        <div style="font-size: 72px; font-weight: 900; color: #FFF; margin: 6px 0;">"JLPT"</div>
        <p style="font-size: 22px; font-weight: 700;">y recibe nuestra <b>Guía PDF Gratuita + Test de Nivel</b></p>
      </div>
      <div style="font-size: 26px; font-weight: 800; color: #B27B00;">📱 WhatsApp: +34 682 054 654</div>
    </div>
    <div style="text-align: center; font-size: 26px; font-weight: 800; color: #718096;">⛩️ @japones_kamiyajuku · Barcelona & Online</div>
  </div>

  <script>function setScene(idx){{ document.querySelectorAll('.scene').forEach((s, i) => s.classList.toggle('active', i === idx)); }}</script>
</body>
</html>"""

# ========================================================
# 2. 北海道留学プログラム 30秒マルチ写真リール (全5シーン・30秒)
# ========================================================
def generate_hokkaido_30s_reel_html():
    return f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<style>
  @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@700;800;900&family=Noto+Sans+JP:wght@700;900&display=swap');
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{ width: 1080px; height: 1920px; background-color: #F1F8E9; font-family: 'Montserrat', 'Noto Sans JP', sans-serif; overflow: hidden; }}
  .scene {{ display: none; width: 1080px; height: 1920px; padding: 90px 70px; flex-direction: column; justify-content: space-between; }}
  .scene.active {{ display: flex; }}
  .reel-header {{ display: flex; justify-content: space-between; align-items: center; background: rgba(255,255,255,0.95); padding: 20px 34px; border-radius: 40px; box-shadow: 0 10px 30px rgba(0,0,0,0.08); }}
  .logo-box {{ display: flex; align-items: center; gap: 14px; font-size: 28px; font-weight: 900; color: #2E7D32; }}
  .logo-box img {{ width: 52px; height: 52px; object-fit: contain; }}
  .photo-frame {{ width: 100%; height: 980px; border-radius: 36px; overflow: hidden; box-shadow: 0 20px 50px rgba(0,0,0,0.14); border: 4px solid #FFFFFF; }}
  .photo-frame img {{ width: 100%; height: 100%; object-fit: cover; }}
  .text-card {{ background: #FFFFFF; border-radius: 32px; padding: 44px; box-shadow: 0 16px 40px rgba(0,0,0,0.08); text-align: center; border-top: 12px solid #2E7D32; }}
  .badge-tag {{ display: inline-block; background: #2E7D32; color: #FFF; font-size: 22px; font-weight: 900; padding: 8px 24px; border-radius: 20px; margin-bottom: 14px; }}
  .main-title {{ font-size: 50px; font-weight: 900; line-height: 1.25; color: #1A202C; }}
  .sub-title {{ font-size: 28px; font-weight: 700; color: #4A5568; margin-top: 10px; }}
</style>
</head>
<body>
  <!-- Scene 1: 教室授業 (0-6s) -->
  <div class="scene active" id="scene-1">
    <div class="reel-header">
      <div class="logo-box"><img src="file://{LOGO_PATH}"><span>KAMIYA JUKU 神谷塾</span></div>
      <div style="font-size: 24px; font-weight: 900; color: #43A047;">✈️ ESTUDIAR EN JAPÓN</div>
    </div>
    <div class="photo-frame"><img src="file://{PHOTO_H1}" style="object-position: center 25%;"></div>
    <div class="text-card">
      <div class="badge-tag">PROGRAMA HOKKAIDO ❄️🌸</div>
      <div class="main-title">Estudia Japonés en Japón<br>con <span style="color: #2E7D32;">Escuelas Oficiales</span></div>
      <div class="sub-title">Aprende con inmersión total en un entorno seguro y acogedor.</div>
    </div>
  </div>

  <!-- Scene 2: カフェ交流 (6-12s) -->
  <div class="scene" id="scene-2">
    <div class="reel-header">
      <div class="logo-box"><img src="file://{LOGO_PATH}"><span>KAMIYA JUKU 神谷塾</span></div>
      <div style="font-size: 24px; font-weight: 900; color: #2E7D32;">☕ VIDA EN JAPÓN</div>
    </div>
    <div class="photo-frame"><img src="file://{PHOTO_H2}" style="object-position: center 30%;"></div>
    <div class="text-card" style="border-top-color: #43A047;">
      <div class="badge-tag" style="background: #43A047;">CONVERSACIÓN REAL 💬</div>
      <div class="main-title">Practica con Japoneses<br><span style="color: #43A047;">fuera del aula cada día</span></div>
      <div class="sub-title">Actividades en cafeterías, intercambios y vida estudiantil.</div>
    </div>
  </div>

  <!-- Scene 3: 着物文化体験 (12-18s) -->
  <div class="scene" id="scene-3">
    <div class="reel-header">
      <div class="logo-box"><img src="file://{LOGO_PATH}"><span>KAMIYA JUKU 神谷塾</span></div>
      <div style="font-size: 24px; font-weight: 900; color: #1B5E20;">👘 CULTURA TRADICIONAL</div>
    </div>
    <div class="photo-frame"><img src="file://{PHOTO_H3}" style="object-position: center 20%;"></div>
    <div class="text-card" style="border-top-color: #1B5E20;">
      <div class="badge-tag" style="background: #1B5E20;">EXPERIENCIA COMPLETA 🇯🇵</div>
      <div class="main-title">Vive las Tradiciones:<br><span style="color: #1B5E20;">Kimono, Festivales y Viajes</span></div>
      <div class="sub-title">No solo estudias el idioma, vives la cultura japonesa en primera persona.</div>
    </div>
  </div>

  <!-- Scene 4: 卒業式・達成感 (18-24s) -->
  <div class="scene" id="scene-4">
    <div class="reel-header">
      <div class="logo-box"><img src="file://{LOGO_PATH}"><span>KAMIYA JUKU 神谷塾</span></div>
      <div style="font-size: 24px; font-weight: 900; color: #2E7D32;">🎓 ALCANZA TU META</div>
    </div>
    <div class="photo-frame"><img src="file://{PHOTO_H4}" style="object-position: center 25%;"></div>
    <div class="text-card">
      <div class="badge-tag">ACOMPAÑAMIENTO TOTAL 🤝</div>
      <div class="main-title">Te Guiamos Desde España<br><span style="color: #2E7D32;">hasta tu graduación</span></div>
      <div class="sub-title">Gestión de visados, búsqueda de escuela, alojamiento y soporte.</div>
    </div>
  </div>

  <!-- Scene 5: CTA (24-30s) -->
  <div class="scene" id="scene-5">
    <div class="reel-header">
      <div class="logo-box"><img src="file://{LOGO_PATH}"><span>KAMIYA JUKU 神谷塾</span></div>
      <div style="font-size: 24px; font-weight: 900; color: #2E7D32;">✈️ ASESORÍA GRATUITA</div>
    </div>
    <div class="text-card" style="padding: 60px 48px; margin: auto 0;">
      <div style="font-size: 80px; margin-bottom: 12px;">✈️🌸</div>
      <h1 style="font-size: 50px; font-weight: 900; color: #2E7D32; line-height: 1.2;">
        ¿Quieres estudiar en Japón en 2026/2027?
      </h1>
      <p style="font-size: 26px; color: #4A5568; font-weight: 700; margin: 16px 0;">
        Abierta la convocatoria para los cursos oficiales.
      </p>
      <div style="background: linear-gradient(135deg, #1B5E20 0%, #2E7D32 100%); color:#FFF; border-radius: 28px; padding: 36px; margin: 26px 0;">
        <p style="font-size: 22px; font-weight: 800; letter-spacing: 1px;">ENVÍA UN DM CON LA PALABRA</p>
        <div style="font-size: 72px; font-weight: 900; color: #F9B233; margin: 6px 0;">"VISA"</div>
        <p style="font-size: 22px; font-weight: 700;">y recibe la <b>Guía de Visados + Asesoría Gratuita</b></p>
      </div>
      <div style="font-size: 26px; font-weight: 800; color: #2E7D32;">📱 WhatsApp: +34 682 054 654</div>
    </div>
    <div style="text-align: center; font-size: 26px; font-weight: 800; color: #718096;">⛩️ @japones_kamiyajuku · Barcelona & Online</div>
  </div>

  <script>function setScene(idx){{ document.querySelectorAll('.scene').forEach((s, i) => s.classList.toggle('active', i === idx)); }}</script>
</body>
</html>"""

async def render_30s_reel(html_generator, output_filename):
    html_code = html_generator()
    temp_html = ASSETS_DIR / f"temp_{output_filename}.html"
    with open(temp_html, "w", encoding="utf-8") as f:
        f.write(html_code)

    output_path = str(ASSETS_DIR / output_filename)
    fps = 30
    scene_durations = [6, 6, 6, 6, 6] # 5シーン × 6秒 = 30秒
    total_seconds = sum(scene_durations)

    width, height = 1080, 1920
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video_writer = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    print(f"🎬 30秒リール動画レンダリング開始: {output_filename} (30秒・5シーン)")

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={"width": width, "height": height}, device_scale_factor=1)
        await page.goto(f"file://{temp_html.resolve()}", wait_until="networkidle")

        frame_idx = 0
        for s_idx, duration in enumerate(scene_durations):
            await page.evaluate(f"setScene({s_idx})")
            await asyncio.sleep(0.05)

            screenshot_bytes = await page.screenshot(type="jpeg", quality=95)
            nparr = np.frombuffer(screenshot_bytes, np.uint8)
            img_frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

            num_frames = duration * fps
            for _ in range(num_frames):
                video_writer.write(img_frame)
                frame_idx += 1

        await browser.close()

    video_writer.release()
    print(f"✅ 生成完了: {output_filename} ({total_seconds}秒 / {frame_idx}フレーム)")
    return output_path

if __name__ == "__main__":
    print("🚀 30秒マルチ写真リール動画を一括生成中...")
    asyncio.run(render_30s_reel(generate_matsuri_30s_reel_html, "kamiyajuku_reel_matsuri_30s.mp4"))
    asyncio.run(render_30s_reel(generate_hokkaido_30s_reel_html, "kamiyajuku_reel_hokkaido_30s.mp4"))
    print("🎉 30秒リール動画の生成が完了しました！")
