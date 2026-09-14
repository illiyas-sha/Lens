from auth.supabase_client import get_supabase_client


def get_scores_for_components(component_ids):
    if not component_ids:
        return []
    supabase = get_supabase_client()
    return (
        supabase.table("scores")
        .select("component_id, student_id, marks_obtained, max_marks")
        .in_("component_id", component_ids)
        .execute()
        .data
    )
