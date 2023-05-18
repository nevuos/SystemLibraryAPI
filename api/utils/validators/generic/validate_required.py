from typing import Any, Callable, Dict, List, Tuple
from functools import wraps
from flask import jsonify, request


def validate_required_fields(fields: List[str]) -> Callable[[Callable[..., Tuple[Any, int]]], Callable[..., Tuple[Any, int]]]:
    def decorator(func: Callable[..., Tuple[Any, int]]) -> Callable[..., Tuple[Any, int]]:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Tuple[Any, int]:
            data = request.get_json(force=True, silent=True)
            if not data:
                return jsonify({'error': 'Nenhum dado foi fornecido.'}), 400

            missing_fields = [
                field for field in fields if field not in data or data[field] is None]
            if missing_fields:
                return jsonify({'error': 'Campos obrigatórios ausentes ou vazios: {}'.format(', '.join(missing_fields))}), 400

            return func(*args, **kwargs)
        return wrapper
    return decorator
