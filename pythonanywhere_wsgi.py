"""
PythonAnywhere WSGI 설정 파일
Web 탭의 WSGI configuration file에 이 내용을 붙여넣으세요
"""

import os
import sys

# ==== 여기를 수정하세요 ====
USERNAME = 'your-username'  # PythonAnywhere 사용자명
PROJECT_NAME = 'gemini_final_v4'
VENV_NAME = 'gemini-env'  # 가상환경 이름
# ==========================

# 프로젝트 경로
path = f'/home/{USERNAME}/{PROJECT_NAME}'
if path not in sys.path:
    sys.path.insert(0, path)

# Django 설정 모듈
os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings'

# 가상환경 활성화 (선택사항 - PythonAnywhere가 자동으로 처리)
# virtualenv = f'/home/{USERNAME}/.virtualenvs/{VENV_NAME}'
# activate_this = os.path.join(virtualenv, 'bin', 'activate_this.py')
# with open(activate_this) as f:
#     exec(f.read(), {'__file__': activate_this})

# Django WSGI application
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
