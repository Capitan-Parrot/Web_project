from requests import post, get, delete

print(get('http://localhost:5000/api/jobs').json())  # все работы
print(get('http://localhost:5000/api/jobs/999').json())  # нет такой работы
print(get('http://localhost:5000/api/jobs/2').json())  # с существуюшим id
print(get('http://localhost:5000/api/jobs/swq').json())  # некорректный id
print(get('http://localhost:5000/api/jobs').json())  # все работы


# print(post('http://localhost:5000/api/jobs').json())  # без параметров
# print(post('http://localhost:5000/api/jobs',
#            json={'job': 'swas'}).json())  # не все параметры
# print(post('http://localhost:5000/api/jobs',
#            json={'id': 3,
#                  'team_leader': 3,
#                  'job': 'cleaning',
#                  'work_size': 1,
#                  'category': 1}).json())  # с существуюшим id



# print(get('http://localhost:5000/api/jobs').json())  # все работы
# print(delete('http://localhost:5000/api/jobs/999').json())  # нет такой работы
# print(delete('http://localhost:5000/api/jobs/12').json())  # такая есть
# print(delete('http://localhost:5000/api/jobs/swq').json())  # некорректный id
# print(get('http://localhost:5000/api/jobs').json())  # все работы
