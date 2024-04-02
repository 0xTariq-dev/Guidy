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

    user = User(first_name="Dev", last_name="User",
                email="dev_user@gmail.com", password="DevPass",
                resource_type="Books"
                )
    st.new(user)
    st.save()

    print()
    print(st.get(User, user.id))

    user_course = Guidy.CreateCourse("Java", "Medium", 3)
    print("the course from AI")
    print(f"\n+++\n{user_course}\n+++\n")

    course1 = Course(title=user_course['title'], category=user_course['category'],
                description=user_course['description'], length=user_course['length'],
                level=user_course['level'], user_id=user.id
                )
    user.courses.append(course1)
    st.new(course1)
    st.save()

    print("the course from db")
    print(st.get(Course, course1.id))

    print("*****************************")


    print("lessons list from the AI course")
    print(user_course['lessons'])

    print("*****************************")


    lessons = {k: v for k, v in user_course['lessons'].items()}
    [print(f"{k}: {v}") for k, v in user_course.items()]
    print("done done dooooone")
    [print(f"{k}: {v}") for k, v in lessons.items()]
    print("*****************************")

    title = user_course['title']
    # values = list(lessons.values())
    # keys = list(lessons.keys())
    # print(values[0])
    # print(title)
    lessons = list(user_course['lessons'].values())
    for alesson in lessons:

        lesson = Guidy.ExplainLesson(title, lessons[0], "video")
        print(lesson)
        lessonObj = Lesson(title=lesson['title'], description=lesson['description'], course_id=course1.id)
        st.new(lessonObj)
        st.save()


    # lesson1 = json.loads(lesson)
    # print(lesson1)



    print("Done!")
