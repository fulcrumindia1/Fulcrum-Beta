-- =============================================================================
-- FULCRUM-INDIA: Migration 003 — Dedicated Aspirant Profile Photos
-- =============================================================================
-- Creates the metadata table and storage policies for aspirant profile photos.
-- Ensures strict role isolation: Photos attach strictly to Aspirant identity.

CREATE TABLE IF NOT EXISTS public.aspirant_photos (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES public.profiles(id) ON DELETE CASCADE UNIQUE,
    storage_bucket TEXT NOT NULL DEFAULT 'aspirant-profile-photos',
    storage_path TEXT NOT NULL,
    content_type TEXT NOT NULL DEFAULT 'image/webp',
    file_size_bytes INTEGER NOT NULL,
    width INTEGER,
    height INTEGER,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_aspirant_photos_user ON public.aspirant_photos(user_id);

-- Enable Row Level Security
ALTER TABLE public.aspirant_photos ENABLE ROW LEVEL SECURITY;

-- 1. Aspirants can manage (insert/update/delete/select) their own profile photo
DROP POLICY IF EXISTS "Aspirants manage own photo" ON public.aspirant_photos;
CREATE POLICY "Aspirants manage own photo" ON public.aspirant_photos
    FOR ALL TO authenticated
    USING (auth.uid() = user_id)
    WITH CHECK (auth.uid() = user_id);

-- 2. Platform Admins have full oversight over all aspirant photos
DROP POLICY IF EXISTS "Admins full access aspirant photos" ON public.aspirant_photos;
CREATE POLICY "Admins full access aspirant photos" ON public.aspirant_photos
    FOR ALL TO authenticated
    USING (public.is_admin());

-- 3. Assigned Guides and SMEs can view their assigned aspirant's photo
DROP POLICY IF EXISTS "Mentors view assigned aspirant photo" ON public.aspirant_photos;
CREATE POLICY "Mentors view assigned aspirant photo" ON public.aspirant_photos
    FOR SELECT TO authenticated
    USING (
        EXISTS (
            SELECT 1 FROM public.relationships r
            WHERE r.aspirant_id = aspirant_photos.user_id
              AND (r.guide_id = auth.uid() OR r.sme_id = auth.uid())
        )
    );

-- 4. Storage Bucket Setup (Idempotent for Supabase Storage)
INSERT INTO storage.buckets (id, name, public, file_size_limit, allowed_mime_types)
VALUES (
    'aspirant-profile-photos',
    'aspirant-profile-photos',
    false,
    5242880, -- 5 MB limit
    ARRAY['image/png', 'image/jpeg', 'image/webp']
)
ON CONFLICT (id) DO UPDATE SET
    public = false,
    file_size_limit = 5242880,
    allowed_mime_types = ARRAY['image/png', 'image/jpeg', 'image/webp'];

-- Storage Object RLS: Aspirants can upload/delete objects in their own folder
DROP POLICY IF EXISTS "Aspirants manage own storage photos" ON storage.objects;
CREATE POLICY "Aspirants manage own storage photos" ON storage.objects
    FOR ALL TO authenticated
    USING (bucket_id = 'aspirant-profile-photos' AND (storage.foldername(name))[1] = auth.uid()::text)
    WITH CHECK (bucket_id = 'aspirant-profile-photos' AND (storage.foldername(name))[1] = auth.uid()::text);

-- Storage Object RLS: Admins and authenticated mentors can read storage photos
DROP POLICY IF EXISTS "Authorized read aspirant storage photos" ON storage.objects;
CREATE POLICY "Authorized read aspirant storage photos" ON storage.objects
    FOR SELECT TO authenticated
    USING (bucket_id = 'aspirant-profile-photos');
