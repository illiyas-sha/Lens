-- Lens DB schema (Supabase/Postgres)
-- Reference copy of what's deployed in the Supabase project's SQL Editor.
-- Keep this in sync manually whenever the schema changes.

create table terms (
  id bigint generated always as identity primary key,
  name text not null,
  start_date date,
  end_date date,
  created_at timestamptz not null default now()
);

create table courses (
  id bigint generated always as identity primary key,
  term_id bigint not null references terms(id) on delete cascade,
  name text not null,
  code text,
  credits numeric,
  created_at timestamptz not null default now()
);

create table components (
  id bigint generated always as identity primary key,
  course_id bigint not null references courses(id) on delete cascade,
  name text not null,
  max_marks numeric not null check (max_marks > 0),
  weightage_marks numeric,
  created_at timestamptz not null default now()
);

comment on column components.weightage_marks is
  'Marks this component contributes to the course total (its converted/scaled max), not a percentage. E.g. raw max_marks=30 scaled to weightage_marks=15.';

create extension if not exists pgcrypto;

-- Custom auth (not Supabase Auth): email + bcrypt password_hash live here
-- directly. The app uses the service_role key server-side and enforces
-- access control in application code instead of RLS/auth.uid().
create table students (
  id uuid primary key default gen_random_uuid(),
  full_name text not null,
  nick_name text,
  section text,
  email text not null unique,
  password_hash text not null,
  is_admin boolean not null default false,
  created_at timestamptz not null default now()
);

create table scores (
  id bigint generated always as identity primary key,
  component_id bigint not null references components(id) on delete cascade,
  student_id uuid not null references students(id) on delete cascade,
  marks_obtained numeric not null check (marks_obtained >= 0),
  max_marks numeric not null check (max_marks > 0),
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  unique (component_id, student_id),
  check (marks_obtained <= max_marks)
);
