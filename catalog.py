"""Shared read-only lookups for terms/courses/components (used by both the
admin panel and student-facing pages)."""

from auth.supabase_client import get_supabase_client


def list_terms():
    supabase = get_supabase_client()
    return supabase.table("terms").select("*").order("start_date").execute().data


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
