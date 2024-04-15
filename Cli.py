#!/usr/bin/python3
""" console """

import sys
import shlex
import cmd
import re
from models.__init__ import storage
from models.base_model import BaseModel
from models.user import User
from models.course import Course
from models.lesson import Lesson
from models.resource import Resource
from models.review import Review
from datetime import datetime


class GuidyAdmin(cmd.Cmd):
    """Guidy Admin console"""
    prompt = 'GuidyAdmin> ' if sys.__stdin__.isatty() else ''

    classes = {"User": User,
               "Course": Course,
               "Lesson": Lesson,
               "Resource": Resource,
               "Review": Review
               }

    dot_cmds = ['all', 'count', 'show', 'destroy', 'update']

    types = {'rating': int, 'length': int, 'rating': int}

    def cmdloop(self, intro=None):
        while True:
            try:
                super().cmdloop(intro=intro)
                break
            except KeyboardInterrupt:
                print("\nQuitting...")
                return

    def preloop(self):
        """Prints if isatty is false"""
        if not sys.__stdin__.isatty():
            print('GuidyAdmin> ', end='')

    def precmd(self, line):
        storage.reload()
        super().precmd(line)
        return line

    def postcmd(self, stop, line):
        """Prints if isatty is false"""
        self.preloop()
        return stop

    def _ArgParser(self, ObjD):
        """Creates a dictionary from arg list"""
        ArgDict = {}
        for arg in ObjD:
            if '=' not in arg:
                continue
            matches = re.match(r'(\w+)=(.*)', arg)
            if matches:
                # print(matches.groups())
                k, v = matches.groups()
                if k in self.types:
                    v = self.types[k](v)
                else:
                    v = v.replace('_', ' ')
                ArgDict[k] = v
            print(f'{k}: {v}')
        return ArgDict

    def do_create(self, arg):
        """
        Creates a new instance of an object
        [Usage]: create <Object Type> <Attribute1=Value1> <Attribute2=Value2>
        """
        ObjType = shlex.split(arg)
        if len(ObjType) == 0:
            print("** Provide Object Type **")
            return False

        if ObjType[0] in self.classes:
            ArgDict = self._ArgParser(ObjType[1:])
            instance = self.classes[ObjType[0]](**ArgDict)
        else:
            print(f"** Unidentified Type {ObjType[0]} **")
            return False

        instance.save()
        print(instance.id)

    def do_show(self, arg):
        """
        Prints an individual instance of an object
        [Usage]: show <Object Type> <Instance ID>
        """
        ObjD = shlex.split(arg)
        if len(ObjD) == 0:
            print("** Provide Object Type **")
            return False

        if len(ObjD) < 2:
            print("** Provide Object ID **")
            return False

        Type, ID = ObjD[0], ObjD[1]

        if Type not in self.classes:
            print(f"** Unidentified Type {Type}**")
            return False

        k = Type + "." + ID
        print(k)
        print(storage.all().get(k, "** NO Object Found **"))

    def do_destroy(self, arg):
        """
        Deletes an instance based on the class and id
        [Usage]: destroy <Object Type> <Instance ID>
        """
        ObjD = shlex.split(arg)

        if len(ObjD) == 0:
            print("** Object Type Missing **")
            return False

        if len(ObjD) < 2:
            print("** Object ID Missing **")
            return False

        Type, ID = ObjD[0], ObjD[1]

        if Type not in self.classes:
            print(f"** Unidentified Type {Type} **")
            return False

        k = Type + "." + ID
        try:
            storage.delete(storage.all()[k])
            storage.save()
        except KeyError:
            print("** NO Object Found **")

    def do_all(self, arg):
        """
        Prints string representations of instances
        [Usage]: all <Object Type> or all
        """
        Obj = shlex.split(arg)
        Type = Obj[0] if len(Obj) > 0 else ""
        ObjList = []
        ObjDict = {}

        if len(Obj) == 0:
            ObjDict = storage.all()
        elif Type in self.classes:
            ObjDict = storage.all(self.classes[Type])
        else:
            print(f"** Unidentified Type {Type} **")
            return False

        for key in ObjDict:
            ObjList.append(str(ObjDict[key]))

        print("\n" + ",\n\n".join(ObjList) + "\n", end='\n')

    def do_update(self, arg):
        """
        Update an instance based on the class Type, id, attribute & value
        [usage]: update <Object Type> <Instance ID> <Key> <Value>
        """
        ObjD = shlex.split(arg)

        if len(ObjD) == 0:
            print("** Object Type Missing **")
            return

        if len(ObjD) < 3:
            print("** Provide Attribute Name**")
            print(f"{self.do_update.__doc__}")
            return

        if len(ObjD) < 4:
            print("** Provide Attribute Value **")
            print(f"{self.do_update.__doc__}")
            return


        Type, ID = ObjD[0], ObjD[1]
        Key, Value = ObjD[2], ObjD[3] if len(ObjD) > 3 else ""
        Ints = ["rating", "length"]

        if Type not in self.classes:
            print(f"** Unidentified Type {Type} **")
            return

        if len(ObjD) < 2:
            print("** Object ID Missing **")
            return

        Obj = Type + "." + ID
        if Obj not in storage.all():
            print("** NO Object Found **")
            return

        if Key in Ints:
            try:
                Value = int(Value)
            except ValueError:
                Value = 0

        setattr(storage.all()[Obj], Key, Value)
        storage.all()[Obj].save()

    def do_enroll(self, line):
        """Enroll a user in a course"""
        user_id, course_id = shlex.split(line)
        user = storage.get(User, user_id)
        course = storage.get(Course, course_id)
        print(f'Enrolling {user.username} in {course.title}')
        user.courses.append(course)
        storage.save()

    def do_EOF(self, arg):
        """Exits console"""
        print("\nQuitting...")
        return True

    def emptyline(self):
        """ overwriting the emptyline method """
        return False

    def do_quit(self, arg):
        """Quit command to exit the program"""
        print("Quitting...")
        return True


if __name__ == '__main__':
    GuidyAdmin().cmdloop()
