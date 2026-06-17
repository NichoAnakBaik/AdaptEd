const { execSync } = require('child_process');

function runCmd(cmd) {
  try {
    console.log(`Running: ${cmd}`);
    execSync(cmd, { stdio: 'inherit' });
  } catch (e) {
    console.log(`Command failed, ignoring.`);
  }
}

runCmd('npx vercel env rm DB_HOST production -y');
runCmd('npx vercel env rm DB_HOST preview -y');
runCmd('npx vercel env rm DB_HOST development -y');
runCmd('npx vercel env add DB_HOST production --value aws-1-ap-south-1.pooler.supabase.com --yes');
runCmd('npx vercel env add DB_HOST preview --value aws-1-ap-south-1.pooler.supabase.com --yes');
runCmd('npx vercel env add DB_HOST development --value aws-1-ap-south-1.pooler.supabase.com --yes');

runCmd('npx vercel env rm DB_PORT production -y');
runCmd('npx vercel env rm DB_PORT preview -y');
runCmd('npx vercel env rm DB_PORT development -y');
runCmd('npx vercel env add DB_PORT production --value 5432 --yes');
runCmd('npx vercel env add DB_PORT preview --value 5432 --yes');
runCmd('npx vercel env add DB_PORT development --value 5432 --yes');

console.log('ALL DONE');
