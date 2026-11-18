from .login import render_login_page
from .dashboard import render_dashboard
from .patients import render_patients_page
from .doctors import render_doctors_page
from .appointments import render_appointments_page
from .history import render_history_page
from .patient_portal import render_patient_dashboard
from .doctor_portal import (
    render_doctor_appointments_page,
    render_doctor_dashboard,
    render_doctor_history_page,
    render_examination_page,
)
from .account import render_account_page
from .accounts_admin import render_accounts_admin_page

__all__ = [
    "render_account_page",
    "render_accounts_admin_page",
    "render_appointments_page",
    "render_dashboard",
    "render_doctor_appointments_page",
    "render_doctor_dashboard",
    "render_doctor_history_page",
    "render_doctors_page",
    "render_examination_page",
    "render_history_page",
    "render_login_page",
    "render_patient_dashboard",
    "render_patients_page",
]
