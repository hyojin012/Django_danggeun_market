import os
import uuid
import mimetypes

from supabase import create_client

# os.getenv로 가져온 값 뒤에 있을지 모를 공백이나 줄바꿈(\n)을 .strip()으로 완전히 제거합니다.
SUPABASE_URL = os.getenv("SUPABASE_URL", "").strip()
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY", "").strip()

# 만약 키 값에 한글이 섞여 들어왔다면 터미널에 경고를 띄웁니다.
if not SUPABASE_KEY.isascii():
    print("⚠️ 경고: .env 파일의 SUPABASE_SERVICE_ROLE_KEY에 한글이나 비-ASCII 문자가 포함되어 있습니다!")

BUCKET_NAME = "product-images"

supabase = create_client(
    SUPABASE_URL,
    SUPABASE_KEY
)

def upload_product_image(uploaded_file, user_id):
    extension = (
        uploaded_file.name
        .split(".")[-1]
        .lower()
    )

    file_name = (
        f"{uuid.uuid4().hex}.{extension}"
    )

    file_path = (
        f"products/{user_id}/{file_name}"
    )

    content_type, _ = mimetypes.guess_type(uploaded_file.name)
    if not content_type or not content_type.isascii():
        content_type = getattr(uploaded_file, 'content_type', 'application/octet-stream')
        content_type = content_type.encode('ascii', 'ignore').decode('ascii')

    supabase.storage.from_(
        BUCKET_NAME
    ).upload(
        path=file_path,
        file=uploaded_file.read(),
        file_options={
            "content-type": content_type,
            "upsert": False,
        }
    )

    return (
        supabase.storage
        .from_(BUCKET_NAME)
        .get_public_url(file_path)
    )
