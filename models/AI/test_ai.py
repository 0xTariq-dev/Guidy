from AI_service import Guidy
import sys, os
script_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(script_dir, os.pardir))
grand_parent_dir = os.path.abspath(os.path.join(parent_dir, os.pardir))
sys.path.append(parent_dir)
sys.path.append(grand_parent_dir)
from models import storage as st
from models.base_model import BaseModel, Base
from models.user import User
from models.course import Course
from models.lesson import Lesson
from models.resource import Resource
from models.review import Review



if __name__ == "__main__":
    print(sys.path)
    user_course = Guidy.CreateCourse("Java", "Medium", 5)
    print(f"+++\n{user_course}+++\n")
    user = User(first_name="Fake", last_name="User",
                email="Fake@gmail.com", password="FakePass",
                resource_type="Books"
                )
    st.new(user)
    st.save()
    print()
    print(user.to_dict())
    print()
    print(st.get(User, user.id))
    course1 = Course(title=user_course['title'], category=user_course['category'],
                description=user_course['description'], length=user_course['length'],
                level=user_course['level'], user_id=user.id
                )
    user.courses.append(course1)
    st.new(course1)
    st.save()
    print()
    print(course1.to_dict())
    print()
    print(st.get(Course, course1.id))
    # print(Course['lessons'])
    # print(course_json)
    # with open('course.json', 'w') as f:
    #     f.write(str(Course))

    # lessons = {k: v for k, v in Course['lessons'].items()}
    # [print(f"{k}: {v}") for k, v in Course.items() if k != 'lessons']
    # [print(f"{k}: {v}") for k, v in lessons.items()]

    # title = Course['title']
    # values = list(lessons.values())
    # keys = list(lessons.keys())
    # print(values[0])
    # print(title)
    # lessons = list(Course['lessons'].values())
    # lesson = Guidy.ExplainLesson(Course['category'], lessons[0], "video")
    # print(lesson)
    # print(lesson.description)
    # [print(resource) for resource in lesson['resources']]
    # display(HTML(lesson['description']))
    # lesson1 = json.loads(lesson)
    # print(lesson1)
    # with open('lesson1.json', 'w') as f:
        # json.dump(lesson1, f)

    # [print(f"{k}: {v}") for k, v in lesson1.items() if k != 'resources']
    # [print(f"{k}: {v}") for k, v in lesson1['resources'].items()]

    # print("Done!")
