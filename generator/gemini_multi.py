"""
원본 작동 코드를 100% 복제 - 수정 최소화
"""

from google import genai
from io import BytesIO
from PIL import Image
from pathlib import Path
import sys
from typing import List, Tuple, Optional
import time

# 원본 프롬프트 (수정 없음)
BASE_PROMPT = """
[역할/목표]
너는 사진가 겸 리터처다. 내가 제공하는 '참조 이미지'의 피사체 정체성과 핵심 속성을 유지한 상태로, 서로 다른 구도(샷)로 확장 이미지를 생성한다.

[일관성 고정 규칙]
- 얼굴/체형/주요 특징·의상·색감·소품을 참조와 동일하게 유지.
- 헤어스타일·피부톤·질감·문양 일치.

[연출 원칙]
- 각 샷은 카메라 포지션/앵글/렌즈 화각/프레이밍이 명확.
- 현실적인 심도·조명, 과한 왜곡 금지.

[품질/출력]
- 고해상도, 노이즈 최소화, 깨끗한 에지.
- 지정 종횡비 준수. 텍스트/워터마크/로고 금지.
"""

NEGATIVE = """
[금지/네거티브]
- 중복 사지, 손가락 왜상, 관절 왜곡 금지
- 과한 샤픈/노이즈/밴딩/색수차 금지
- 텍스트/워터마크/로고/프레임 금지
- 참조와 불일치하는 헤어·의상 색상 변경 금지
- 배경 글자/표지판 삽입 금지
"""

SHOT_PRESETS = [
    ("closeup", """
    [샷: Close-up]
    - 85mm, 정면, 아이레벨
    - 얼굴 중심, 머리 윗부분 약간 크롭
    - 소프트박스 2점(메인 45°), 배경 단색/bokeh
    - 종횡비: 1:1
    """),
    ("full", """
    [샷: Full Body]
    - 35mm, 아이레벨, 전신 프레이밍
    - 미니멀 스튜디오, 왜곡 최소
    - 종횡비: 3:4
    """),
    ("lowangle", """
    [샷: Low Angle]
    - 24~28mm, 로우앵글, 림라이트 윤곽 강조
    - 과도한 원근 왜곡 금지
    - 종횡비: 9:16
    """),
    ("profile", """
    [샷: Profile]
    - 85mm, 측면 프로필, 아이레벨
    - 주광(윈도우 라이트) + 서브라이트
    - 배경 부드러운 bokeh
    - 종횡비: 4:5
    """),
    ("highangle", """
    [샷: High Angle]
    - 50mm, 하이앵글(위에서 아래로)
    - 부드러운 오버헤드 조명
    - 자연스러운 구도, 과도한 왜곡 금지
    - 종횡비: 4:5
    """),
]


def extract_images(resp) -> List[bytes]:
    """원본 함수 그대로"""
    images = []

    if not getattr(resp, "candidates", None):
        return images

    for cand in resp.candidates:
        parts = getattr(cand.content, "parts", []) or []
        for p in parts:
            inline = getattr(p, "inline_data", None)
            data = getattr(inline, "data", None) if inline else None
            if data:
                images.append(data)

    return images


def init_gemini_client(api_key: str) -> Optional[genai.Client]:
    """API 키를 인자로 받도록 수정된 버전"""
    try:
        client = genai.Client(api_key=api_key)
        print("✅ Gemini 클라이언트 초기화 완료")
        return client
    except Exception as e:
        print(f"❌ Gemini 클라이언트 초기화 실패: {e}")
        return None


def generate_single_shot(
        client: genai.Client,
        reference_image: Image.Image,
        shot_name: str,
        shot_prompt: str,
        output_path: Path,
        retry_count: int = 2
) -> bool:
    """원본 함수 그대로"""
    for attempt in range(retry_count + 1):
        try:
            if attempt > 0:
                print(f"   🔄 재시도 {attempt}/{retry_count}...")
                time.sleep(2)

            # 프롬프트 구성
            contents = [BASE_PROMPT, reference_image, shot_prompt, NEGATIVE]

            # 이미지 생성 요청
            resp = client.models.generate_content(
                model="gemini-2.5-flash-image",
                contents=contents
            )

            # 이미지 추출
            imgs = extract_images(resp)

            if imgs:
                # 이미지 저장
                img = Image.open(BytesIO(imgs[0]))
                output_file = output_path / f"out_{shot_name}.png"
                img.save(output_file, optimize=True)

                print(f"   ✅ 저장 완료: {output_file.name}")
                print(f"      크기: {img.size}, 파일 크기: {output_file.stat().st_size // 1024}KB")
                return True
            else:
                print(f"   ⚠️  이미지 생성 없음 (시도 {attempt + 1}/{retry_count + 1})")

                # 응답 내용 확인
                if hasattr(resp, 'text') and resp.text:
                    print(f"      모델 응답: {resp.text[:150]}...")

                if attempt == retry_count:
                    print(f"   ❌ {shot_name} 생성 실패")
                    print(f"      가능한 원인: API 제한, 모델 제약, 부적절한 콘텐츠 감지")

        except Exception as e:
            print(f"   ❌ 오류 발생 (시도 {attempt + 1}/{retry_count + 1}): {e}")
            if attempt == retry_count:
                return False

    return False


def run_generation(
        api_key: str,
        reference_path: str,
        output_dir: str,
        shots_to_generate: List[str] = None
) -> List[str]:
    """Django view에서 호출하는 함수"""
    
    print("=" * 60)
    print("🎨 Gemini 이미지 생성 시작")
    print("=" * 60)
    print()

    # 1. 클라이언트 초기화
    client = init_gemini_client(api_key)
    if not client:
        return []

    print()

    # 2. 출력 디렉토리 설정
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True, parents=True)
    print(f"📁 출력 디렉토리: {output_path.absolute()}")
    print()

    # 3. 참조 이미지 로드
    try:
        ref_image = Image.open(reference_path)
        print(f"✅ 참조 이미지 로드 완료: {reference_path}")
        print(f"   크기: {ref_image.size}, 모드: {ref_image.mode}")
    except Exception as e:
        print(f"❌ 참조 이미지 로드 실패: {e}")
        return []

    # 4. 생성할 샷 결정
    if shots_to_generate:
        # 선택된 샷만
        shot_list = [(name, prompt) for name, prompt in SHOT_PRESETS 
                     if name in shots_to_generate]
    else:
        # 전체 샷
        shot_list = SHOT_PRESETS

    total_shots = len(shot_list)

    print(f"🎬 총 {total_shots}개의 샷 생성 시작...")
    print("=" * 60)
    print()

    # 5. 각 샷 생성
    success_count = 0
    generated_files = []
    
    for idx, (shot_name, shot_prompt) in enumerate(shot_list, 1):
        print(f"[{idx}/{total_shots}] 🎥 {shot_name.upper()} 샷 생성 중...")

        if generate_single_shot(client, ref_image, shot_name, shot_prompt, output_path):
            success_count += 1
            output_file = output_path / f"out_{shot_name}.png"
            generated_files.append(str(output_file))

        print()

        # API 속도 제한 방지
        if idx < total_shots:
            time.sleep(1)

    # 6. 결과 요약
    print("=" * 60)
    print("✨ 이미지 생성 작업 완료!")
    print(f"   성공: {success_count}/{total_shots}")
    print(f"   실패: {total_shots - success_count}/{total_shots}")
    print(f"   출력 위치: {output_path.absolute()}")
    print("=" * 60)
    
    return generated_files
