-- Add audio and QR code columns to api_order table
ALTER TABLE api_order 
ADD COLUMN IF NOT EXISTS audio_file_url TEXT,
ADD COLUMN IF NOT EXISTS qr_code_url TEXT,
ADD COLUMN IF NOT EXISTS qr_code_data TEXT;

-- Update existing orders to have empty values for new columns
UPDATE api_order 
SET audio_file_url = '', qr_code_url = '', qr_code_data = ''
WHERE audio_file_url IS NULL OR qr_code_url IS NULL OR qr_code_data IS NULL;
