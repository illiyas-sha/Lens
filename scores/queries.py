from auth.supabase_client import get_supabase_client


def get_existing_score(component_id, student_id):
    supabase = get_supabase_client()
    result = (
        supabase.table("scores")
        .select("*")
        .eq("component_id", component_id)
        .eq("student_id", student_id)
        .execute()
    )
    return result.data[0] if result.data else None


def submit_score(component_id, student_id, marks_obtained, max_marks):
    supabase = get_supabase_client()
    supabase.table("scores").upsert(
        {
            "component_id": component_id,
            "student_id": student_id,
            "marks_obtained": marks_obtained,
            "max_marks": max_marks,
        },
        on_conflict="component_id,student_id",
    ).execute()
