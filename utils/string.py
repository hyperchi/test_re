# -*- coding: utf-8 -*-

def is_valid_id(s):
    try:
        a = float(s)
        return True
    except ValueError as e:
        return False


def is_number(s):
    try:
        a = float(s)
        return True
    except ValueError as e:
        return False

