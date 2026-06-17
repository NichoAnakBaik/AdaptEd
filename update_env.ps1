$ErrorActionPreference = "Continue"

Write-Host "Updating DB_HOST"
npx vercel env rm DB_HOST production -y
npx vercel env rm DB_HOST preview -y
npx vercel env rm DB_HOST development -y
"aws-1-ap-south-1.pooler.supabase.com" | npx vercel env add DB_HOST production preview development

Write-Host "Updating DB_PORT"
npx vercel env rm DB_PORT production -y
npx vercel env rm DB_PORT preview -y
npx vercel env rm DB_PORT development -y
"5432" | npx vercel env add DB_PORT production preview development

Write-Host "Done"
