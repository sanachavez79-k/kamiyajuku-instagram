import os
from pathlib import Path
from typing import List, Optional
from config import settings

class DriveInspector:
    """
    Google Drive（ローカル同期フォルダまたはAPI）内の素材フォルダを探索するモジュール
    """
    def __init__(self, content_dir: Optional[str] = None):
        self.content_dir = Path(content_dir or settings.DEFAULT_LOCAL_CONTENT_DIR)

    def find_assets_for_topic(self, topic_keyword: str, day_category: Optional[str] = None) -> List[str]:
        """
        指定されたキーワードや曜日（LUNES, MARTES, VIERNES等）に合致する画像素材を検索
        """
        valid_extensions = {".jpg", ".jpeg", ".png", ".webp"}
        matched_images = []

        if not self.content_dir.exists():
            return []

        search_dirs = [self.content_dir]
        if day_category:
            day_dir = self.content_dir / day_category.upper()
            if day_dir.exists():
                search_dirs.insert(0, day_dir)

        for target_dir in search_dirs:
            for root, _, files in os.walk(target_dir):
                for f in sorted(files):
                    path = Path(root) / f
                    if path.suffix.lower() in valid_extensions:
                        # キーワードまたはフォルダに一致するものを追加
                        if topic_keyword.lower() in f.lower() or day_category:
                            matched_images.append(str(path))

        return matched_images[:10]  # 最大10枚まで
