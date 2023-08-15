#!/usr/bin/python3

""" Define HBnB Console """
import cmd
from models.base_model import BaseModel
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from models.user import User
import models
import json


class HBNBCommand(cmd.Cmd):
    """
    Command-line interpreter for the HBNB application.
    Supports creating, showing, updating, deleting, and listing instances.
    """

    prompt = "(hbnb) "
    __classes = {
        "BaseModel",
        "User",
        "State",
        "City",
        "Place",
        "Amenity",
        "Review"
    }

    def default(self, line):
        """Catch commands if nothing else matches then."""
        # print("DEF:::", line)
        self._precmd(line)

    def _precmd(self, line):
        """Intercepts commands to test for class.syntax()"""
        # print("PRECMD:::", line)
        match = re.search(r"^(\w*)\.(\w+)(?:\(([^)]*)\))$", line)
        if not match:
            return line
        classname = match.group(1)
        method = match.group(2)
        args = match.group(3)
        match_uid_and_args = re.search('^"([^"]*)"(?:, (.*))?$', args)
        if match_uid_and_args:
            uid = match_uid_and_args.group(1)
            attr_or_dict = match_uid_and_args.group(2)
        else:
            uid = args
            attr_or_dict = False

        attr_and_value = ""
        if method == "update" and attr_or_dict:
            match_dict = re.search('^({.*})$', attr_or_dict)
            if match_dict:
                self.update_dict(classname, uid, match_dict.group(1))
                return ""
            match_attr_and_value = re.search(
                '^(?:"([^"]*)")?(?:, (.*))?$', attr_or_dict)
            if match_attr_and_value:
                attr_and_value = (match_attr_and_value.group(
                    1) or "") + " " + (match_attr_and_value.group(2) or "")
        command = method + " " + classname + " " + uid + " " + attr_and_value
        self.onecmd(command)
        return command 

    def do_quit(self, arg):
        """
        Quit command to exit the program
        """
        return True

    def do_EOF(self, arg):
        """
        Exit the program gracefully using Ctrl+D (EOF)
        """
        print("")  # Print a newline before exiting
        return True

    def emptyline(self):
        """
        Do nothing on an empty line
        """
        pass

    def do_create(self, arg):
        """
        Creates a new instance of BaseModel, State,
        City, Amenity, Place, Review, or User,
        saves it (to the JSON file) and prints the id.
        Usage: create <class name>
        """
        if not arg:
            print("** class name missing **")
        elif arg not in BaseModel.__subclasses__():
            print("** class doesn't exist **")
        else:
            new_instance = BaseModel()
            if arg == "State":
                new_instance = State()
            elif arg == "City":
                new_instance = City()
            elif arg == "Amenity":
                new_instance = Amenity()
            elif arg == "Place":
                new_instance = Place()
            elif arg == "Review":
                new_instance = Review()
            elif arg == "User":
                new_instance = User()
            new_instance.save()
            print(new_instance.id)

    def do_show(self, arg):
        """
        Prints string representation of an instance based on class name and id
        Usage: show <class name> <id>
        """
        args = arg.split()
        if not args:
            print("** class name missing **")
        elif args[0] not in BaseModel.__subclasses__():
            print("** class doesn't exist **")
        elif len(args) < 2:
            print("** instance id missing **")
        else:
            obj_key = "{}.{}".format(args[0], args[1])
            if obj_key in storage.all():
                print(storage.all()[obj_key])
            else:
                print("** no instance found **")

    def do_destroy(self, arg):
        """
        Deletes an instance based on the class name
        and id (save the change into the JSON file).
        Usage: destroy <class name> <id>
        """
        args = arg.split()
        if not args:
            print("** class name missing **")
        elif args[0] not in BaseModel.__subclasses__():
            print("** class doesn't exist **")
        elif len(args) < 2:
            print("** instance id missing **")
        else:
            obj_key = "{}.{}".format(args[0], args[1])
            if obj_key in storage.all():
                storage.all().pop(obj_key)
                storage.save()
            else:
                print("** no instance found **")

    def do_all(self, arg):
        """
        Prints all string representation of all instances
        based or not on the class name.
        Usage: all or all <class name>
        """
        args = line.split()
        all_objs = models.storage.all()
        if not args:
            print([str(value) for value in all_objs.values()])
        elif args[0] in self.__classes:
            print(
                [str(value)
                 for key, value in all_objs.items()
                 if key.split(".")[0] == args[0]]
            )
        else:
            print("** class doesn't exist **")

    def parse(self, line):
        """
        Parse command line arguments
        """
        return line.split()
        
    def do_update(self, arg):
        """
        Updates an instance based on the class name and
        id by adding or updating attribute.
        Usage: update <class name> <id> <attribute name> "<attribute value>"
        """
        args = arg.split()
        if not args:
            print("** class name missing **")
        elif args[0] not in BaseModel.__subclasses__():
            print("** class doesn't exist **")
        elif len(args) < 2:
            print("** instance id missing **")
        else:
            obj_key = "{}.{}".format(args[0], args[1])
            if obj_key in storage.all():
                if len(args) < 3:
                    print("** attribute name missing **")
                elif len(args) < 4:
                    print("** value missing **")
                else:
                    obj = storage.all()[obj_key]
                    attr_name = args[2]
                    attr_value = args[3]
                    setattr(obj, attr_name, attr_value)
                    obj.save()
            else:
                print("** no instance found **")


if __name__ == '__main__':
    HBNBCommand().cmdloop()
