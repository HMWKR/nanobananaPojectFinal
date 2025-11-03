# 🚀 Railway 배포 가이드 (최종 완성판)

## ✅ 모든 설정 완료됨!

이 프로젝트는 Railway 배포를 위해 완벽하게 설정되었습니다.

---

## 📋 배포 순서

### 1️⃣ GitHub 업로드

```bash
git init
git add .
git commit -m "Railway deployment ready"
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git branch -M main
git push -u origin main
```

### 2️⃣ Railway 연결

1. https://railway.app/ 로그인
2. "Start a New Project"
3. "Deploy from GitHub repo"
4. 저장소 선택

### 3️⃣ 환경변수 설정 (Variables 탭)

```
DEBUG=False
SECRET_KEY=django-prod-xyz123abc456def789
ALLOWED_HOSTS=*.railway.app
CSRF_ORIGINS=https://*.railway.app
```

### 4️⃣ 배포 완료!

Railway가 자동으로 배포합니다 (2-5분)

---

## ⚠️ 중요!

**Railway Settings의 Custom Commands는 비워두세요!**
- nixpacks.toml이 자동으로 처리합니다

---

## 🎯 핵심 파일

- ✅ `nixpacks.toml` - Railway 배포 설정
- ✅ `config/settings.py` - 환경변수 지원
- ✅ `requirements.txt` - gunicorn 포함

---

**이제 GitHub에 올리고 Railway에 연결하기만 하면 됩니다!** 🎉
