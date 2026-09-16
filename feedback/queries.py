from auth.supabase_client import get_supabase_client


def submit_feedback(
    student_id, full_name, email, rating, comments, enhancement_request
):
    supabase = get_supabase_client()
    supabase.table("feedback").insert(
        {
            "student_id": student_id,
            "full_name": full_name,
            "email": email,
            "rating": rating,
            "comments": comments or None,
            "enhancement_request": enhancement_request or None,
        }
    ).execute()
