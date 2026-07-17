import os
from io import BytesIO
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
from fastapi import HTTPException
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from schemas.certificate_schema import CertificateCreate
import repositories.certificate_repo as certificate_repo
import repositories.course_repo as course_repo
from fastapi.responses import StreamingResponse

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATE_PATH = os.path.join(BASE_DIR, "assets", "certificate_template.png")
FONT_PATH = os.path.join(BASE_DIR, "assets", "Roboto-Black.ttf")


def create_certificate(
    session: Session, user_id: int, course_id: int, certificate_in: CertificateCreate
):
    course = course_repo.get_course_by_id(session, course_id)
    if not course:
        raise HTTPException(404, "course not found with this ID")
    return certificate_repo.add_certificate(session, user_id, course_id, certificate_in)


def __draw_certificate_pdf(
    student_name: str, course_title: str, verification_code: str
) -> BytesIO:
    if not os.path.exists(TEMPLATE_PATH):
        raise HTTPException(
            500, "Certificate background template image missing from server assets."
        )

    img = Image.open(TEMPLATE_PATH).convert("RGB")
    W, H = img.size
    draw = ImageDraw.Draw(img)
    base_size = min(W, H)

    name_font_size = int(base_size * 0.06)
    course_font_size = int(base_size * 0.035)
    footer_font_size = int(base_size * 0.025)
    name_font_size = max(name_font_size, 30)
    course_font_size = max(course_font_size, 18)
    footer_font_size = max(footer_font_size, 14)

    try:
        name_font = ImageFont.truetype(FONT_PATH, name_font_size)
        course_font = ImageFont.truetype(FONT_PATH, course_font_size)
        footer_font = ImageFont.truetype(FONT_PATH, footer_font_size)
    except IOError:
        name_font = ImageFont.load_default()
        course_font = ImageFont.load_default()
        footer_font = ImageFont.load_default()

    current_date = datetime.now().strftime("%B %d, %Y")

    date_text = f"Date: {current_date}"
    code_text = f"Verify Code: {verification_code}"

    name_width = draw.textlength(student_name, font=name_font)
    course_width = draw.textlength(course_title, font=course_font)
    date_width = draw.textlength(date_text, font=footer_font)
    code_width = draw.textlength(code_text, font=footer_font)

    max_width = W * 0.85

    while name_width > max_width and name_font_size > 20:
        name_font_size -= 2
        name_font = ImageFont.truetype(FONT_PATH, name_font_size)
        name_width = draw.textlength(student_name, font=name_font)

    while course_width > max_width and course_font_size > 12:
        course_font_size -= 2
        course_font = ImageFont.truetype(FONT_PATH, course_font_size)
        course_width = draw.textlength(course_title, font=course_font)

    max_footer_width = W * 0.40
    while (
        date_width > max_footer_width or code_width > max_footer_width
    ) and footer_font_size > 10:
        footer_font_size -= 1
        footer_font = ImageFont.truetype(FONT_PATH, footer_font_size)
        date_width = draw.textlength(date_text, font=footer_font)
        code_width = draw.textlength(code_text, font=footer_font)

    name_y = int(H * 0.45)
    course_y = int(H * 0.55)
    footer_y = int(H * 0.78)

    # Draw Student Name (centered)
    name_x = (W - name_width) / 2
    draw.text((name_x, name_y), student_name, fill=(0, 0, 0), font=name_font)

    # Draw Course Title (centered)
    course_x = (W - course_width) / 2
    draw.text((course_x, course_y), course_title, fill=(0, 0, 0), font=course_font)

    # Draw Date (left side)
    date_x = (W * 0.30) - (date_width / 2)
    draw.text((date_x, footer_y), date_text, fill=(50, 50, 50), font=footer_font)

    # Draw Verification Code (right side)
    code_x = (W * 0.70) - (code_width / 2)
    draw.text((code_x, footer_y), code_text, fill=(50, 50, 50), font=footer_font)

    # Save to buffer
    pdf_buffer = BytesIO()
    img.save(pdf_buffer, format="PDF", resolution=100.0)
    pdf_buffer.seek(0)

    return pdf_buffer


def download_certificate(
    session: Session, user_id: int, student_username: str, course_id: int
):
    course = course_repo.get_course_by_id(session, course_id)
    if not course:
        raise HTTPException(404, "course not found")
    certificate_data = certificate_repo.get_user_course_certificate(
        session, user_id, course_id
    )
    if not certificate_data:
        raise HTTPException(400, "certificate not issued yet. complete course first")
    certificate_user_id = {c.user_id for c in certificate_data}
    if certificate_user_id != user_id:
        raise HTTPException(
            403, "you are not allowed to download someone else's certificate"
        )

    verification_code = {c.verification_code for c in certificate_data}

    pdf_file = __draw_certificate_pdf(student_username, course.title, verification_code)

    # 3. Stream it natively to browser as an attachment download
    return StreamingResponse(
        pdf_file,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f"attachment; filename=Certificate-{course_id}.pdf"
        },
    )


def verify_certificate_by_code(session: Session, verification_code: int):
    details = certificate_repo.verify_certificate_by_code(session, verification_code)
    if not details:
        raise HTTPException(404, "no certificate found")
    return details
