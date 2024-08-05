from flask import Blueprint, jsonify
from flask import Response
from flasgger import swag_from
import pandas as pd

bp = Blueprint("data", __name__)


@bp.route('/<type_id>', methods=['GET'])
@swag_from({
    'tags': ['Data'],
    'responses': {
        200: {
            'description': 'A successful response',
            'examples': {
                'application/json': {
                    "type": "string"
                }
            }
        },
        400: {
            'description': 'Invalid type',
            'examples': {
                'application/json': {
                    "type": "Invalid type"
                }
            }
        }
    },
    'parameters': [
        {
            'in': 'path',
            'name': 'type_id',
            'required': True,
            'type': 'string',
            'description': 'Type ID for the name'
        }
    ],
})
def get_data(type_id: str) -> Response | tuple[Response, int]:
    df_types: pd.DataFrame = pd.read_csv('tipos.csv')
    types_info: dict[int, str] = df_types.set_index('id')['nome'].to_dict()

    if type_id.isnumeric() and int(type_id) in types_info:
        return jsonify(
            {
                "type": types_info[int(type_id)]
            }
        )
    else:
        return jsonify(
            {
                "type": "Invalid type"
            },
        ), 400
