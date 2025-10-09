
import os
import json
import hashlib
from pathlib import Path

class Config:
    def __init__(self, name, folder):
        self.name = name
        self.folder = folder
        self.base_dir = Path(os.getenv("APPDATA")) / folder
        self.base_dir.mkdir(parents=True, exist_ok=True)
        self.file_path = self.base_dir / f"{name}.json"
        self.hash_path = self.base_dir / f"{name}.hash"

    def _calculate_hash(self, data):
        encoded = json.dumps(data, sort_keys=True).encode("utf-8")
        return hashlib.sha256(encoded).hexdigest()

    def save(self, data):
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        h = self._calculate_hash(data)
        with open(self.hash_path, "w", encoding="utf-8") as f:
            f.write(h)

    def load(self):
        if not self.file_path.exists():
            return None
        with open(self.file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        if not self.verify(data):
            raise ValueError("Config file integrity check failed")
        return data

    def verify(self, data=None):
        if not self.hash_path.exists() or not self.file_path.exists():
            return False
        if data is None:
            with open(self.file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
        current_hash = self._calculate_hash(data)
        with open(self.hash_path, "r", encoding="utf-8") as f:
            stored_hash = f.read().strip()
        return current_hash == stored_hash

    def exists(self):
        return self.file_path.exists()

    def delete(self):
        if self.file_path.exists():
            self.file_path.unlink()
        if self.hash_path.exists():
            self.hash_path.unlink()

    @classmethod
    def list_configs(cls, folder):
        base_dir = Path(os.getenv("APPDATA")) / folder
        if not base_dir.exists():
            return []
        return [f.stem for f in base_dir.glob("*.json")]
