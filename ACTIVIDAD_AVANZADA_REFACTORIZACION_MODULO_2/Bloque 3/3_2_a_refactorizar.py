# Versión generada por la IA
from dataclasses import dataclass
from typing import Protocol, List
from abc import abstractmethod

class Validator(Protocol):
    @abstractmethod
    def validate(self, value: str) -> bool: ...
    @abstractmethod
    def error_message(self) -> str: ...

@dataclass
class ValidationResult:
    is_valid: bool
    errors: List[str]

class FormValidator:
    def __init__(self, validators: List[Validator]):
        self.validators = validators

    def validate_all(self, value: str) -> ValidationResult:
        errors = [v.error_message() for v in self.validators if not v.validate(value)]
        return ValidationResult(not errors, errors)