import psycopg2

regions=['ap-southeast-1','ap-southeast-2','ap-southeast-3','us-east-1','us-east-2','us-west-1','us-west-2','eu-central-1','eu-west-1','eu-west-2','ap-northeast-1','ap-northeast-2','ap-south-1','sa-east-1','ca-central-1']
found=False
for r in regions:
    host = f'aws-0-{r}.pooler.supabase.com'
    try:
        print(f'Testing {host}')
        conn = psycopg2.connect(host=host, port=6543, user='postgres.nretsborzathlvaqxxez', password='3ZzU0iVhaK6WFzp2', dbname='postgres', connect_timeout=3)
        print(f'SUCCESS: {host}')
        found=True
        break
    except Exception as e:
        print(e)
if not found:
    print('FAILED ALL')
