import json
from dataclasses import dataclass
from typing import Dict, Any

@dataclass
class UserConfig:
    headers: Dict[str, str]
    cookies: Dict[str, str]
    data: Dict[str, Any]
    max_times: int
    token: str

def load_config(config_file: str) -> UserConfig:
    with open(config_file, 'r', encoding='utf-8') as f:
        config = json.load(f)
    return UserConfig(
        headers=config['headers'],
        cookies=config['cookies'],
        data=config['data'],
        max_times=config.get('max_times', 50),
        token=config['token']
    )