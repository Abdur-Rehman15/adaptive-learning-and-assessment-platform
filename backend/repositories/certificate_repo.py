from sqlmodel import Session, select, func
from models.certificate_model import Certificate


def add_certificate(
    session: Session, user_id: int, course_id: int, certificate_in: Certificate
):
    db_certificate = Certificate(
        issued_at=certificate_in.issued_at,
        verification_code=certificate_in.verification_code,
        user_id=user_id,
        course_id=course_id,
    )
    session.add(db_certificate)
    session.commit()
    session.refresh(db_certificate)
    return db_certificate


def get_user_course_certificate(session: Session, user_id: int, course_id: int):
    return session.exec(
        select(Certificate).where(
            Certificate.user_id == user_id, Certificate.course_id == course_id
        )
    ).all()


def verify_certificate_by_code(session: Session, verification_code: int):
    return session.exec(
        select(Certificate).where(Certificate.verification_code == verification_code)
    ).first()
