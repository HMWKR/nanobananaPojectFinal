#!/bin/bash
echo "🎨 Gemini 이미지 생성기 v4"
echo ""
pip3 install -r requirements.txt -q
python3 manage.py migrate
echo ""
echo "✅ 준비 완료!"
echo "👉 http://127.0.0.1:8000/"
echo ""
python3 manage.py runserver
