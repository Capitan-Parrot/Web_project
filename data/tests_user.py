from requests import get, post, delete

print(get('http://localhost:5000/api/v2/users').json())
print(get('http://localhost:5000/api/v2/users/2').json())
print(get('http://localhost:5000/api/v2/users/9999').json())
print(get('http://localhost:5000/api/v2/users/sd').json())

print(post('http://localhost:5000/api/v2/users').json())
print(post('http://localhost:5000/api/v2/users',
           json={'name': 'swas'}).json())
print(post('http://localhost:5000/api/v2/users',
           json={'surname': 'Ivan',
                 'name': 'Susanin',
                 'age': 25,
                 'position': 'captain_2',
                 'speciality': 'research engineer',
                 'address': 'Moon',
                 'email': '12@mars.org'}).json())

print(delete('http://localhost:5000/api/v2/users/999').json())
print(delete('http://localhost:5000/api/v2/users/1').json())