from auth.supabase_client import get_supabase_client


def list_terms():
    supabase = get_supabase_client()
    return supabase.table("terms").select("*").order("start_date").execute().data


def add_term(name, start_date, end_date):
    supabase = get_supabase_client()
    supabase.table("terms").insert(
        {"name": name, "start_date": str(start_date), "end_date": str(end_date)}
    ).execute()


def list_courses(term_id):
    supabase = get_supabase_client()
    return (
        supabase.table("courses")
        .select("*")
        .eq("term_id", term_id)
        .order("name")
        .execute()
        .data
    )


def add_course(term_id, name, code, credits):
    supabase = get_supabase_client()
    supabase.table("courses").insert(
        {"term_id": term_id, "name": name, "code": code or None, "credits": credits}
    ).execute()


def list_components(course_id):
    supabase = get_supabase_client()
    return (
        supabase.table("components")
        .select("*")
        .eq("course_id", course_id)
        .order("name")
        .execute()
        .data
    )


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
