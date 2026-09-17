CREATE TABLE IF NOT EXISTS system_info (
  id BIGSERIAL PRIMARY KEY,
  key TEXT NOT NULL UNIQUE,
  value JSONB NOT NULL,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

INSERT INTO system_info (key, value) VALUES
('version', '"0.1.0"'::jsonb),
('name', '"Nivy Next AIOS"'::jsonb)
ON CONFLICT (key) DO NOTHING;
