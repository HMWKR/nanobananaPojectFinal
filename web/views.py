from pathlib import Path
from django.shortcuts import render
from django.conf import settings
from PIL import Image
from .forms import ImageGenerationForm
from generator.gemini_multi import run_generation


def generate_view(request):
    context = {'form': ImageGenerationForm(), 'images': [], 'error': None}
    
    if request.method != 'POST':
        return render(request, 'web/generate.html', context)
    
    form = ImageGenerationForm(request.POST, request.FILES)
    if not form.is_valid():
        context['form'] = form
        context['error'] = "입력을 확인하세요"
        return render(request, 'web/generate.html', context)
    
    api_key = form.cleaned_data['api_key']
    ref_img = form.cleaned_data['reference_image']
    output_dir = form.cleaned_data['output_dir']
    shots = form.cleaned_data['shots'] or None
    
    # 업로드 저장
    try:
        uploads_dir = Path(settings.MEDIA_ROOT) / 'uploads'
        uploads_dir.mkdir(parents=True, exist_ok=True)
        ref_path = uploads_dir / ref_img.name
        
        with open(ref_path, 'wb+') as f:
            for chunk in ref_img.chunks():
                f.write(chunk)
        
        Image.open(ref_path).verify()
    except Exception as e:
        context['error'] = f"파일 오류: {e}"
        return render(request, 'web/generate.html', context)
    
    # 출력 디렉토리
    out_dir = Path(settings.MEDIA_ROOT) / 'outputs' / output_dir
    out_dir.mkdir(parents=True, exist_ok=True)
    
    # 이미지 생성
    try:
        files = run_generation(
            api_key=api_key,
            reference_path=str(ref_path),
            output_dir=str(out_dir),
            shots_to_generate=shots
        )
        
        if not files:
            context['error'] = "생성 실패\n서버 콘솔 확인"
            return render(request, 'web/generate.html', context)
        
        # URL 변환
        images = []
        for file_path in files:
            rel = Path(file_path).relative_to(settings.MEDIA_ROOT)
            url = f"{settings.MEDIA_URL}{rel}".replace('\\', '/')
            name = Path(file_path).name
            images.append({'url': url, 'name': name})
        
        context['images'] = images
        context['form'] = ImageGenerationForm()
        
    except Exception as e:
        context['error'] = f"오류: {e}"
        import traceback
        traceback.print_exc()
    
    return render(request, 'web/generate.html', context)
