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
PHOTO_MATSURI = Path("/Users/sanakamiya/Library/CloudStorage/GoogleDrive-kamiyajuku.japones@gmail.com/マイドライブ/インスタグラム/01_ 未処理素材・塾のイベント参加/祭り2025/DSC01048.JPG")
PHOTO_STUDENTS = Path("/Users/sanakamiya/Library/CloudStorage/GoogleDrive-kamiyajuku.japones@gmail.com/マイドライブ/インスタグラム/01_ 未処理素材・塾のイベント参加/留学生/PHOTO-2025-10-06-15-48-43.jpg")
PHOTO_HOKKAIDO = Path("/Users/sanakamiya/Library/CloudStorage/GoogleDrive-kamiyajuku.japones@gmail.com/.shortcut-targets-by-id/1uPYf673b3arv-oHAxUHyhCRgV1M6laha/DOWNLOAD｜HOKKAIDO/Group Lesson 1.JPG")

# ========================================================
# 1. バルセロナ祭り・コミュニティ特化リール (1080x1920 / 9:16)
# ========================================================
def generate_matsuri_reel_html():
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
  .main-title {{ font-size: 52px; font-weight: 900; line-height: 1.25; color: #1A202C; }}
  .sub-title {{ font-size: 28px; font-weight: 700; color: #4A5568; margin-top: 10px; }}
</style>
</head>
<body>
  <!-- Scene 1: イベント風景 (0-5s) -->
  <div class="scene active" id="scene-1">
    <div class="reel-header">
      <div class="logo-box"><img src="file://{LOGO_PATH}"><span>KAMIYA JUKU 神谷塾</span></div>
      <div style="font-size: 24px; font-weight: 900; color: #E59800;">🇪🇸 MATSURI BARCELONA</div>
    </div>
    <div class="photo-frame"><img src="file://{PHOTO_MATSURI}" style="object-position: center 30%;"></div>
    <div class="text-card">
      <div class="badge-tag">COMUNIDAD & EVENTOS ⛩️</div>
      <div class="main-title">Aprende Japonés Real<br>con <span style="color: #B27B00;">Profesores Nativos</span></div>
      <div class="sub-title">Cultura, eventos en directo y clases en grupos reducidos.</div>
    </div>
  </div>

  <!-- Scene 2: CTA (5-10s) -->
  <div class="scene" id="scene-2">
    <div class="reel-header">
      <div class="logo-box"><img src="file://{LOGO_PATH}"><span>KAMIYA JUKU 神谷塾</span></div>
      <div style="font-size: 24px; font-weight: 900; color: #B27B00;">🎁 GUÍA GRATUITA</div>
    </div>
    <div class="text-card" style="padding: 60px 48px; margin: auto 0;">
      <div style="font-size: 80px; margin-bottom: 12px;">⛩️🇪🇸</div>
      <h1 style="font-size: 52px; font-weight: 900; color: #B27B00;">¿Quieres hablar japonés con fluidez?</h1>
      <p style="font-size: 26px; color: #4A5568; font-weight: 700; margin: 16px 0;">Únete a la academia de referencia en España.</p>
      <div style="background: linear-gradient(135deg, #B27B00 0%, #E59800 100%); color:#FFF; border-radius: 28px; padding: 36px; margin: 26px 0;">
        <p style="font-size: 22px; font-weight: 800; letter-spacing: 1px;">ENVÍA UN DM CON LA PALABRA</p>
        <div style="font-size: 68px; font-weight: 900; color: #FFF; margin: 6px 0;">"JLPT"</div>
        <p style="font-size: 22px; font-weight: 700;">y recibe nuestra <b>Guía PDF gratuita + Test de Nivel</b></p>
      </div>
      <div style="font-size: 26px; font-weight: 800; color: #B27B00;">📱 WhatsApp: +34 682 054 654</div>
    </div>
    <div style="text-align: center; font-size: 26px; font-weight: 800; color: #718096;">⛩️ @japones_kamiyajuku · Barcelona & Online</div>
  </div>
  <script>function setScene(idx){{ document.querySelectorAll('.scene').forEach((s, i) => s.classList.toggle('active', i === idx)); }}</script>
</body>
</html>"""

# ========================================================
# 2. 北海道留学プログラム特化リール (1080x1920 / 9:16)
# ========================================================
def generate_hokkaido_reel_html():
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
  .main-title {{ font-size: 52px; font-weight: 900; line-height: 1.25; color: #1A202C; }}
  .sub-title {{ font-size: 28px; font-weight: 700; color: #4A5568; margin-top: 10px; }}
</style>
</head>
<body>
  <!-- Scene 1: 北海道教室 (0-5s) -->
  <div class="scene active" id="scene-1">
    <div class="reel-header">
      <div class="logo-box"><img src="file://{LOGO_PATH}"><span>KAMIYA JUKU 神谷塾</span></div>
      <div style="font-size: 24px; font-weight: 900; color: #43A047;">✈️ ESTUDIAR EN JAPÓN</div>
    </div>
    <div class="photo-frame"><img src="file://{PHOTO_HOKKAIDO}" style="object-position: center 25%;"></div>
    <div class="text-card">
      <div class="badge-tag">PROGRAMA HOKKAIDO ❄️🌸</div>
      <div class="main-title">Estudia en Japón<br>con <span style="color: #2E7D32;">Escuelas Oficiales</span></div>
      <div class="sub-title">Aprende con inmersión total y acompañamiento desde España.</div>
    </div>
  </div>

  <!-- Scene 2: CTA (5-10s) -->
  <div class="scene" id="scene-2">
    <div class="reel-header">
      <div class="logo-box"><img src="file://{LOGO_PATH}"><span>KAMIYA JUKU 神谷塾</span></div>
      <div style="font-size: 24px; font-weight: 900; color: #2E7D32;">✈️ ASESORÍA GRATUITA</div>
    </div>
    <div class="text-card" style="padding: 60px 48px; margin: auto 0;">
      <div style="font-size: 80px; margin-bottom: 12px;">✈️🇯🇵</div>
      <h1 style="font-size: 52px; font-weight: 900; color: #2E7D32;">¿Quieres estudiar en Japón en 2026/2027?</h1>
      <p style="font-size: 26px; color: #4A5568; font-weight: 700; margin: 16px 0;">Tramitamos tu visado, escuela y alojamiento.</p>
      <div style="background: linear-gradient(135deg, #1B5E20 0%, #2E7D32 100%); color:#FFF; border-radius: 28px; padding: 36px; margin: 26px 0;">
        <p style="font-size: 22px; font-weight: 800; letter-spacing: 1px;">ENVÍA UN DM CON LA PALABRA</p>
        <div style="font-size: 68px; font-weight: 900; color: #F9B233; margin: 6px 0;">"VISA"</div>
        <p style="font-size: 22px; font-weight: 700;">y recibe la <b>Guía de Visados + Asesoría Gratuita</b></p>
      </div>
      <div style="font-size: 26px; font-weight: 800; color: #2E7D32;">📱 WhatsApp: +34 682 054 654</div>
    </div>
    <div style="text-align: center; font-size: 26px; font-weight: 800; color: #718096;">⛩️ @japones_kamiyajuku · Barcelona & Online</div>
  </div>
  <script>function setScene(idx){{ document.querySelectorAll('.scene').forEach((s, i) => s.classList.toggle('active', i === idx)); }}</script>
</body>
</html>"""

# ========================================================
# 3. 東北大学 正規留学＆合格実績特化リール (1080x1920 / 9:16)
# ========================================================
def generate_tohoku_success_reel_html():
    return f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<style>
  @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@700;800;900&family=Noto+Sans+JP:wght@700;900&display=swap');
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{ width: 1080px; height: 1920px; background-color: #EEF4EA; font-family: 'Montserrat', 'Noto Sans JP', sans-serif; overflow: hidden; }}
  .scene {{ display: none; width: 1080px; height: 1920px; padding: 90px 70px; flex-direction: column; justify-content: space-between; }}
  .scene.active {{ display: flex; }}
  .reel-header {{ display: flex; justify-content: space-between; align-items: center; background: rgba(255,255,255,0.95); padding: 20px 34px; border-radius: 40px; box-shadow: 0 10px 30px rgba(0,0,0,0.08); }}
  .logo-box {{ display: flex; align-items: center; gap: 14px; font-size: 28px; font-weight: 900; color: #1B5E20; }}
  .logo-box img {{ width: 52px; height: 52px; object-fit: contain; }}
  .photo-frame {{ width: 100%; height: 980px; border-radius: 36px; overflow: hidden; box-shadow: 0 20px 50px rgba(0,0,0,0.14); border: 4px solid #FFFFFF; }}
  .photo-frame img {{ width: 100%; height: 100%; object-fit: cover; }}
  .text-card {{ background: #FFFFFF; border-radius: 32px; padding: 44px; box-shadow: 0 16px 40px rgba(0,0,0,0.08); text-align: center; border-top: 12px solid #1B5E20; }}
  .badge-tag {{ display: inline-block; background: #1B5E20; color: #FFF; font-size: 22px; font-weight: 900; padding: 8px 24px; border-radius: 20px; margin-bottom: 14px; }}
  .main-title {{ font-size: 52px; font-weight: 900; line-height: 1.25; color: #1A202C; }}
  .sub-title {{ font-size: 28px; font-weight: 700; color: #4A5568; margin-top: 10px; }}
</style>
</head>
<body>
  <!-- Scene 1: 東北大学留学生グループ (0-5s) -->
  <div class="scene active" id="scene-1">
    <div class="reel-header">
      <div class="logo-box"><img src="file://{LOGO_PATH}"><span>KAMIYA JUKU 神谷塾</span></div>
      <div style="font-size: 24px; font-weight: 900; color: #1B5E20;">🎓 CASOS DE ÉXITO</div>
    </div>
    <div class="photo-frame"><img src="file://{PHOTO_STUDENTS}" style="object-position: center 20%;"></div>
    <div class="text-card">
      <div class="badge-tag">TOHOKU UNIVERSITY 🇯🇵</div>
      <div class="main-title">De España a la<br><span style="color: #1B5E20;">Universidad en Japón</span></div>
      <div class="sub-title">Nuestros alumnos logran su ingreso con la preparación integral de Kamiya Juku.</div>
    </div>
  </div>

  <!-- Scene 2: CTA (5-10s) -->
  <div class="scene" id="scene-2">
    <div class="reel-header">
      <div class="logo-box"><img src="file://{LOGO_PATH}"><span>KAMIYA JUKU 神谷塾</span></div>
      <div style="font-size: 24px; font-weight: 900; color: #1B5E20;">🎓 ASESORÍA OFICIAL</div>
    </div>
    <div class="text-card" style="padding: 60px 48px; margin: auto 0;">
      <div style="font-size: 80px; margin-bottom: 12px;">🎓✈️</div>
      <h1 style="font-size: 50px; font-weight: 900; color: #1B5E20;">Consigue tu plaza universitaria en Japón</h1>
      <p style="font-size: 26px; color: #4A5568; font-weight: 700; margin: 16px 0;">Preparación académica, exámenes de admisión y visados.</p>
      <div style="background: linear-gradient(135deg, #1B5E20 0%, #2E7D32 100%); color:#FFF; border-radius: 28px; padding: 36px; margin: 26px 0;">
        <p style="font-size: 22px; font-weight: 800; letter-spacing: 1px;">ENVÍA UN DM CON LA PALABRA</p>
        <div style="font-size: 68px; font-weight: 900; color: #F9B233; margin: 6px 0;">"VISA"</div>
        <p style="font-size: 22px; font-weight: 700;">para agendar tu <b>Asesoría Gratuita Online</b></p>
      </div>
      <div style="font-size: 26px; font-weight: 800; color: #1B5E20;">📱 WhatsApp: +34 682 054 654</div>
    </div>
    <div style="text-align: center; font-size: 26px; font-weight: 800; color: #718096;">⛩️ @japones_kamiyajuku · Barcelona & Online</div>
  </div>
  <script>function setScene(idx){{ document.querySelectorAll('.scene').forEach((s, i) => s.classList.toggle('active', i === idx)); }}</script>
</body>
</html>"""

# ========================================================
# 4. 15秒 週間文法クイズリール (1080x1920 / 9:16)
# ========================================================
def generate_weekly_quiz_reel_html():
    return f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<style>
  @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@700;800;900&family=Noto+Sans+JP:wght@700;900&display=swap');
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{ width: 1080px; height: 1920px; background-color: #FFF9E6; font-family: 'Montserrat', 'Noto Sans JP', sans-serif; overflow: hidden; }}
  .scene {{ display: none; width: 1080px; height: 1920px; padding: 100px 70px; flex-direction: column; justify-content: space-between; }}
  .scene.active {{ display: flex; }}
  .reel-header {{ display: flex; justify-content: space-between; align-items: center; background: #FFFFFF; padding: 20px 34px; border-radius: 40px; box-shadow: 0 10px 30px rgba(0,0,0,0.08); }}
  .logo-box {{ display: flex; align-items: center; gap: 14px; font-size: 28px; font-weight: 900; color: #B27B00; }}
  .logo-box img {{ width: 52px; height: 52px; object-fit: contain; }}
  ruby {{ ruby-position: over; }}
  rt {{ font-size: 0.5em; color: #B27B00; font-weight: 800; }}
  .quiz-card {{ background: #FFFFFF; border-radius: 36px; padding: 60px 48px; box-shadow: 0 20px 50px rgba(0,0,0,0.08); text-align: center; border-top: 14px solid #B27B00; margin: auto 0; }}
  .countdown-number {{ font-size: 140px; font-weight: 900; color: #E8822A; margin: 20px 0; }}
</style>
</head>
<body>
  <!-- Scene 1: 出題 (0-4s) -->
  <div class="scene active" id="scene-1">
    <div class="reel-header">
      <div class="logo-box"><img src="file://{LOGO_PATH}"><span>KAMIYA JUKU 神谷塾</span></div>
      <div style="font-size: 24px; font-weight: 900; color: #B27B00;">MINI QUIZ JLPT ✍️</div>
    </div>
    <div class="quiz-card">
      <div style="display:inline-block; background:#B27B00; color:#FFF; font-size:24px; font-weight:900; padding:8px 24px; border-radius:20px; margin-bottom:24px;">¿に (NI) o で (DE)?</div>
      <h1 style="font-size: 58px; font-weight: 900; color: #1A202C; line-height: 1.3; margin-bottom: 30px;">¿Cuál es la partícula correcta? 🇯🇵</h1>
      <div style="background: #F8FAF7; padding: 36px; border-radius: 24px; font-size: 46px; font-weight: 900; color: #B27B00; border: 2px solid rgba(0,0,0,0.06);">
        <ruby>図書館<rt>としょかん</rt></ruby>（ ❓ ）<ruby>本<rt>ほん</rt></ruby>を <ruby>読<rt>よ</rt></ruby>みます。
      </div>
      <p style="font-size: 28px; color: #718096; font-weight: 700; margin-top: 20px;">(Leo libros en la biblioteca)</p>
    </div>
    <div style="text-align: center; font-size: 28px; font-weight: 800; color: #B27B00;">🤔 ¡Piénsalo en 3 segundos! 👇</div>
  </div>

  <!-- Scene 2: カウントダウン (4-7s) -->
  <div class="scene" id="scene-2">
    <div class="reel-header">
      <div class="logo-box"><img src="file://{LOGO_PATH}"><span>KAMIYA JUKU 神谷塾</span></div>
      <div style="font-size: 24px; font-weight: 900; color: #E8822A;">⏳ TIEMPO...</div>
    </div>
    <div class="quiz-card" style="border-top-color: #E8822A;">
      <div style="font-size: 32px; font-weight: 800; color: #718096;">¿Tienes tu respuesta?</div>
      <div class="countdown-number">3... 2... 1...</div>
      <div style="font-size: 36px; font-weight: 900; color: #1A202C;">¿Elegiste に (NI) o で (DE)?</div>
    </div>
    <div style="text-align: center; font-size: 28px; font-weight: 800; color: #E8822A;">👉 ¡La respuesta correcta es...!</div>
  </div>

  <!-- Scene 3: 正解と解説 (7-11s) -->
  <div class="scene" id="scene-3">
    <div class="reel-header">
      <div class="logo-box"><img src="file://{LOGO_PATH}"><span>KAMIYA JUKU 神谷塾</span></div>
      <div style="font-size: 24px; font-weight: 900; color: #1B5E20;">✅ RESPUESTA</div>
    </div>
    <div class="quiz-card" style="border-top-color: #1B5E20;">
      <div style="font-size: 70px; margin-bottom: 10px;">🎉</div>
      <div style="font-size: 54px; font-weight: 900; color: #1B5E20; margin-bottom: 20px;">¡Respuesta: で (DE)!</div>
      <div style="background: #EEF4EA; padding: 30px; border-radius: 20px; font-size: 38px; font-weight: 900; color: #1B5E20;">
        <ruby>図書館<rt>としょかん</rt></ruby> <strong style="color: #E8822A; text-decoration: underline;">で</strong> <ruby>本<rt>ほん</rt></ruby>を <ruby>読<rt>よ</rt></ruby>みます。
      </div>
      <p style="font-size: 28px; font-weight: 700; color: #2D3748; margin-top: 24px; line-height: 1.4;">
        ¡Porque "leer (<ruby>読<rt>よ</rt></ruby>む)" es una <strong>acción activa</strong> que realizas en el lugar!
      </p>
    </div>
    <div style="text-align: center; font-size: 26px; font-weight: 800; color: #1B5E20;">🧠 Acción activa = で (DE) · Estancia fija = に (NI)</div>
  </div>

  <!-- Scene 4: CTA (11-14s) -->
  <div class="scene" id="scene-4">
    <div class="reel-header">
      <div class="logo-box"><img src="file://{LOGO_PATH}"><span>KAMIYA JUKU 神谷塾</span></div>
      <div style="font-size: 24px; font-weight: 900; color: #B27B00;">🎁 GUÍA PDF</div>
    </div>
    <div class="quiz-card" style="border-top-color: #E8822A;">
      <h2 style="font-size: 48px; font-weight: 900; color: #B27B00; margin-bottom: 16px;">¿Acertaste la respuesta? 💬</h2>
      <p style="font-size: 26px; color: #4A5568; font-weight: 700;">Deja tu comentario o guarda este reel para repasar.</p>
      <div style="background: linear-gradient(135deg, #1B5E20 0%, #2E7D32 100%); color:#FFF; border-radius: 24px; padding: 32px; margin: 26px 0;">
        <p style="font-size: 20px; font-weight: 800; color: #E2E8F0;">ENVÍA UN DM CON LA PALABRA</p>
        <div style="font-size: 60px; font-weight: 900; color: #F9B233; margin: 6px 0;">"JLPT"</div>
        <p style="font-size: 20px; font-weight: 700;">y te enviamos nuestra <b>Guía PDF Gratuita de Partículas</b></p>
      </div>
      <div style="font-size: 24px; font-weight: 800; color: #B27B00;">📱 WhatsApp: +34 682 054 654</div>
    </div>
    <div style="text-align: center; font-size: 26px; font-weight: 800; color: #718096;">⛩️ @japones_kamiyajuku · Barcelona & Online</div>
  </div>
  <script>function setScene(idx){{ document.querySelectorAll('.scene').forEach((s, i) => s.classList.toggle('active', i === idx)); }}</script>
</body>
</html>"""

async def render_reel(html_generator, output_filename, scene_durations):
    html_code = html_generator()
    temp_html = ASSETS_DIR / f"temp_{output_filename}.html"
    with open(temp_html, "w", encoding="utf-8") as f:
        f.write(html_code)

    output_path = str(ASSETS_DIR / output_filename)
    fps = 30
    total_seconds = sum(scene_durations)

    width, height = 1080, 1920
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video_writer = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    print(f"🎬 リール動画レンダリング開始: {output_filename}")

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
    print(f"✅ 生成完了: {output_filename} ({total_seconds}秒)")
    return output_path

if __name__ == "__main__":
    print("🚀 個別特化リール動画 4本を一括生成中...")
    asyncio.run(render_reel(generate_matsuri_reel_html, "kamiyajuku_reel_matsuri.mp4", [5, 5]))
    asyncio.run(render_reel(generate_hokkaido_reel_html, "kamiyajuku_reel_hokkaido.mp4", [5, 5]))
    asyncio.run(render_reel(generate_tohoku_success_reel_html, "kamiyajuku_reel_tohoku_success.mp4", [5, 5]))
    asyncio.run(render_reel(generate_weekly_quiz_reel_html, "kamiyajuku_reel_weekly_quiz.mp4", [4, 3, 4, 3]))
    print("🎉 全4本のリール動画生成が完了しました！")
