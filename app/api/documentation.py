"""
API Documentation for CRM System
Comprehensive API documentation generator
"""

import json
from flask import Blueprint, jsonify, render_template

class APIDocumentation:
    """API documentation generator and provider"""
    def __init__(self):
        self.docs = self._generate_api_docs()
    def _generate_api_docs(self):
        # (Stub: Add OpenAPI/Swagger spec generation here)
        return {
            "openapi": "3.0.0",
            "info": {
                "title": "CRM API",
                "version": "1.0.0",
                "description": "Comprehensive API documentation for CRM system."
            },
            "paths": {}
        }
    def get_docs(self):
        return self.docs

# Flask Blueprint for serving API docs
api_docs_bp = Blueprint('api_docs', __name__, url_prefix='/api/docs')

@api_docs_bp.route('/', methods=['GET'])
def serve_api_docs():
    doc = APIDocumentation().get_docs()
    return jsonify(doc) 