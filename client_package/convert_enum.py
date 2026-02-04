import sys

from game.common.enums import *


def main(args: list[str]):
    if len(args) < 2:
        print('convert_enum.py <o|object|a|action> <enum_value>')
        return

    enum_type = args[0]
    enum_class: type[ObjectType] | type[ActionType]
    if enum_type in {'o', 'object'}:
        enum_class = ObjectType
    elif enum_type in {'a', 'action'}:
        enum_class = ActionType
    else:
        print(f'invalid enum type "{enum_type}"; must be o/object/a/action')
        return

    for v in args[1:]:
        if not v.isdigit():
            continue
        print(enum_class(int(v)))

if __name__ == '__main__':
    main(sys.argv[1:])
