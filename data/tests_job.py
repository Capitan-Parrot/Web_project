from requests import get, post, delete

print(get('http://localhost:5000/api/v2/jobs').json())
print(get('http://localhost:5000/api/v2/jobs/2').json())
print(get('http://localhost:5000/api/v2/jobs/9999').json())
print(get('http://localhost:5000/api/v2/jobs/sd').json())
print()
print(post('http://localhost:5000/api/v2/jobs').json())
print(post('http://localhost:5000/api/v2/jobs',
           json={'job': 'swas'}).json())
print(post('http://localhost:5000/api/v2/jobs',
           json={'team_leader': 1,
                 'job': 'cleaning',
                 'work_size': 1,
                 'category': 2}).json())
print()
print(delete('http://localhost:5000/api/v2/jobs/999').json())
print(delete('http://localhost:5000/api/v2/jobs/1').json())