-- =============================================================================
-- FULCRUM-INDIA: Migration 005 — Tighten Aspirant Profile Photo Security & RLS
-- =============================================================================
-- TYPE: Security Hardening (Non-destructive)
-- PURPOSE: Restrict photo storage & metadata reads strictly to the owner, 
--          Platform Admin, and currently authorized active Guides/SMEs with accepted NDA.
-- NOTE: Do not apply to production without explicit administrative approval.

-- 1. Replace overly broad metadata RLS policy on public.aspirant_photos
DROP POLICY IF EXISTS "Mentors view assigned aspirant photo" ON public.aspirant_photos;
CREATE POLICY "Mentors view assigned aspirant photo" ON public.aspirant_photos
    FOR SELECT TO authenticated
    USING (
        EXISTS (
            SELECT 1 FROM public.relationships r
            WHERE r.aspirant_id = aspirant_photos.user_id
              AND r.status = 'active'
              AND (
                  (r.guide_id = auth.uid() OR (r.guide_ids IS NOT NULL AND r.guide_ids ? auth.uid()::text))
                  OR
                  (r.sme_id = auth.uid() OR (r.sme_ids IS NOT NULL AND r.sme_ids ? auth.uid()::text))
              )
              AND EXISTS (
                  SELECT 1 FROM public.user_roles ur
                  WHERE ur.user_id = auth.uid() AND ur.status = 'active'
                    AND ur.role IN ('guide', 'sme')
              )
              AND EXISTS (
                  SELECT 1 FROM public.legal_acceptances la
                  WHERE la.user_id = auth.uid()
                    AND la.status = 'ACCEPTED'
              )
        )
    );

-- 2. Replace overly broad Storage Object RLS policy on storage.objects
DROP POLICY IF EXISTS "Authorized read aspirant storage photos" ON storage.objects;
CREATE POLICY "Authorized read aspirant storage photos" ON storage.objects
    FOR SELECT TO authenticated
    USING (
        bucket_id = 'aspirant-profile-photos'
        AND (
            -- Owner self-access
            (storage.foldername(name))[1] = auth.uid()::text
            OR
            -- Platform Admin full access
            public.is_admin()
            OR
            -- Authorized active Guide or SME with accepted NDA
            EXISTS (
                SELECT 1 FROM public.relationships r
                WHERE r.aspirant_id::text = (storage.foldername(name))[1]
                  AND r.status = 'active'
                  AND (
                      (r.guide_id = auth.uid() OR (r.guide_ids IS NOT NULL AND r.guide_ids ? auth.uid()::text))
                      OR
                      (r.sme_id = auth.uid() OR (r.sme_ids IS NOT NULL AND r.sme_ids ? auth.uid()::text))
                  )
                  AND EXISTS (
                      SELECT 1 FROM public.user_roles ur
                      WHERE ur.user_id = auth.uid() AND ur.status = 'active'
                        AND ur.role IN ('guide', 'sme')
                  )
                  AND EXISTS (
                      SELECT 1 FROM public.legal_acceptances la
                      WHERE la.user_id = auth.uid()
                        AND la.status = 'ACCEPTED'
                  )
            )
        )
    );

-- 3. Reload schema cache
NOTIFY pgrst, 'reload schema';

-- =============================================================================
-- ROLLBACK SCRIPT (Execute if necessary to revert to Migration 003 baseline):
-- =============================================================================
-- DROP POLICY IF EXISTS "Authorized read aspirant storage photos" ON storage.objects;
-- CREATE POLICY "Authorized read aspirant storage photos" ON storage.objects
--     FOR SELECT TO authenticated
--     USING (bucket_id = 'aspirant-profile-photos');
--
-- DROP POLICY IF EXISTS "Mentors view assigned aspirant photo" ON public.aspirant_photos;
-- CREATE POLICY "Mentors view assigned aspirant photo" ON public.aspirant_photos
--     FOR SELECT TO authenticated
--     USING (
--         EXISTS (
--             SELECT 1 FROM public.relationships r
--             WHERE r.aspirant_id = aspirant_photos.user_id
--               AND (r.guide_id = auth.uid() OR r.sme_id = auth.uid())
--         )
--     );
-- NOTIFY pgrst, 'reload schema';

