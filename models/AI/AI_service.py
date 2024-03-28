from openai import OpenAI
from os import getenv
from dotenv import load_dotenv
import json
from IPython.display import display, HTML

load_dotenv()


class Guidy:
    """GuidedCourse class"""

    client = OpenAI(api_key=getenv('OPENAI_API_KEY2'))

    def CreateCourse(CourseSubject, CourseLevel, NumberOfLessons, type=None):
        """Create a course based on user input"""
        completion = Guidy.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": """You are an experinced mentor, 
                 your job is to create course in any subject and level,
                 return lessons titles only,
                 make your response as Json object in the following format:
                 {"title": "Course Title",
                  "category": "Course Category",
                  "description": "Course Description",
                  "length": "lesson count as integer",
                  "level": "Course Level",
                  "lessons": {"Lesson number": "Title",...}}"""
                  },
                {"role": "user",
                 "content": f"""I need a course on {CourseSubject}, 
                 {CourseLevel} level, 
                 {NumberOfLessons} lessons"""}
            ]
        )

        dict = json.loads(completion.choices[0].message.content)
        js = completion.choices[0].message.content
        return js if type == 'json' else dict

    def ExplainLesson(CourseSubject, LessonTitle, ResourcesType, type=None):
        """Create a course based on user input"""
        completion = Guidy.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system",
                 "content": f"""You are a young friendly mentor, your job is
                 to explain in min of 1000 word a lesson about {LessonTitle} in 
                 {CourseSubject} with many examples and provide {ResourcesType}
                 link based on the type the user prefers if possible, if you 
                 couldn't find any resources, you can provide any type of 
                 resources you think is useful but ensure the links works,
                 return your explaination as a single HTML div element nested
                 inside a JSON object structured as follows:
                 {{
                     "title": "{LessonTitle}",
                     "description": "Lesson explanation with a link",
                     "resources": {{
                         "Resource name": "Resource link",
                         # make your priority to find a working links from any type 
                         # than finding the type the user asked for, avoid youtube
                         # short links as they expire.
                         ...}}
                 }},
                 and ensure key names are the same."""
                },
                {"role": "user", "content": f"Explain {LessonTitle} in {CourseSubject} course, provide {ResourcesType} resources if possible"}
            ],
                max_tokens=2000,
                n=1,
                temperature=0.1
        )

        dict = json.loads(completion.choices[0].message.content)
        js = completion.choices[0].message.content
        return js if type == 'json' else dict
