# 神谷塾（@japones_kamiyajuku）Instagram自動運用マルチエージェントシステム

日本語学校「神谷塾」のInstagram運用（日本語学習者・日本留学希望者の集客、JLPT対策講座の案内）を自律分散型のAIマルチエージェントで自動化するシステムです。

---

## 🛠 システム構成

1. **Supervisor Agent (`agents/supervisor.py`)**
   - パイプライン全体の進行管理および品質検査（QA）
2. **Calendar & Trend Agent (`agents/calendar_trend.py`)**
   - JLPT（7月/12月）日程や日本留学ビザ申請期、曜日テーマに応じた投稿企画・スライド骨子の策定
3. **Copywriter Agent (`agents/copywriter.py`)**
   - スペイン語圏ターゲットに特化したフック、解説、例文、DM誘導CTA（例: `JLPT`, `CLASE`）、ハッシュタグの作成
4. **Design & Drive Inspector Agent (`agents/design_drive.py`)**
   - Google Drive内の写真素材検索、またはPillowによる1080x1350（4:5 縦長推奨）カルーセル画像の自動生成
5. **WhatsApp Approval Agent (`agents/whatsapp_approval.py`)**
   - 管理者のWhatsAppにプレビューを送信し、「承認」または「修正指示」を受信

---

## 🚀 クイックスタート & 実行方法

### 1. 依存ライブラリのインストール
```bash
cd instagram_automation
pip install -r requirements.txt
```

### 2. 環境変数の設定
`.env.example` をコピーして `.env` を作成し、必要なキーを入力します。
```bash
cp .env.example .env
```

### 3. パイプラインのテスト実行
```bash
# 企画・キャプション・カルーセル画像生成のテスト実行（承認シミュレーション付き）
python3 main.py --simulate-approval
```

生成されたカルーセルスライド画像は `generated_assets/` ディレクトリ内に保存されます。

### 4. WhatsApp Webhookサーバーの起動
```bash
python3 webhook_server.py
```
Meta for DevelopersのWhatsApp Webhook設定で、`https://<your-domain>/webhook` を登録すると、実機での承認・修正フローが稼働します。
