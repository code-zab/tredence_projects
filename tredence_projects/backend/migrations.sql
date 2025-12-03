CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE IF NOT EXISTS rooms (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  code TEXT DEFAULT '',
  language VARCHAR(32) DEFAULT 'python',
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT now()
);
