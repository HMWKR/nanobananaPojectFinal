"""
프로덕션 배포용 설정
Railway/Render 등에서 사용
"""

from .settings import *
import os

# 프로덕션 모드
DEBUG = os.environ.get('DEBUG', 'False') == 'True'

# SECRET_KEY (환경변수에서 가져오기)
SECRET_KEY = os.environ.get('SECRET_KEY', SECRET_KEY)

# ALLOWED_HOSTS
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '*').split(',')

# CSRF
csrf_origins = os.environ.get('CSRF_ORIGINS', '')
if csrf_origins:
    CSRF_TRUSTED_ORIGINS = csrf_origins.split(',')

# WhiteNoise - 정적 파일 서빙
MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# 정적 파일
STATIC_ROOT = BASE_DIR / 'staticfiles'

# 보안 설정 (HTTPS 사용 시)
if not DEBUG:
    SECURE_SSL_REDIRECT = False  # 필요시 True
    SESSION_COOKIE_SECURE = False  # 필요시 True
    CSRF_COOKIE_SECURE = False  # 필요시 True
