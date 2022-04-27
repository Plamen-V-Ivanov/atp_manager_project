import re

from django.core.exceptions import ValidationError

ONLY_LETTERS_FIRST_IS_CAPITAL_VALIDATION_ERROR_MESSAGE = 'Name should contain only letters, first is capital'
ONLY_LETTERS_AND_DOTS_VALIDATION_ERROR_MESSAGE = 'Username should contain only letters and dots as separators'


def validate_only_letters_first_is_capital(value):
    pattern = "^[A-Z][a-z]*$"
    state = bool(re.match(pattern, value))
    if not state:
        raise ValidationError(ONLY_LETTERS_FIRST_IS_CAPITAL_VALIDATION_ERROR_MESSAGE)


def validate_only_letters_and_dots_as_separators(value):
    pattern = "^[a-z][a-z.]*[a-z]$"
    state = bool(re.match(pattern, value))
    if not state:
        raise ValidationError(ONLY_LETTERS_AND_DOTS_VALIDATION_ERROR_MESSAGE)
