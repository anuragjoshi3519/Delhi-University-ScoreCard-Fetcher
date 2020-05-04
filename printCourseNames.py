with open('Resources/CoursesNames.txt','r',encoding='utf-8') as f:
    courses = f.read()
    [print(course) for course in courses.split('\n')]
