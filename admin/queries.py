from auth.supabase_client import get_supabase_client
from catalog import list_components, list_courses, list_terms  # noqa: F401


def add_term(name, start_date, end_date):
    supabase = get_supabase_client()
    supabase.table("terms").insert(
        {"name": name, "start_date": str(start_date), "end_date": str(end_date)}
    ).execute()


def add_course(term_id, name, code, credits):
    supabase = get_supabase_client()
    supabase.table("courses").insert(
        {"term_id": term_id, "name": name, "code": code or None, "credits": credits}
    ).execute()


def add_component(course_id, name, max_marks, weightage_marks):
    supabase = get_supabase_client()
    supabase.table("components").insert(
        {
            "course_id": course_id,
            "name": name,
            "max_marks": max_marks,
            "weightage_marks": weightage_marks,
        }
    ).execute()
