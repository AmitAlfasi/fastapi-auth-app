"""
OpenAPI/Swagger UI customization module for FastAPI application.
This module provides functionality to customize the OpenAPI schema and Swagger UI
to support JWT Bearer token authentication and improve API documentation.
"""

from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi

def custom_openapi(app: FastAPI):
    """
    Customize Swagger UI to support JWT Bearer token authentication.
    
    This function modifies the OpenAPI schema to:
    1. Add JWT Bearer token security scheme
    2. Apply security requirements globally to all routes
    3. Set up proper API documentation metadata
    
    Args:
        app (FastAPI): FastAPI application instance
        
    Returns:
        dict: The customized OpenAPI schema
        
    Note:
        The function caches the schema in app.openapi_schema after first generation
    """
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title="FastAPI Auth App",
        version="1.0.0",
        description="JWT-based Authentication with Swagger support",
        routes=app.routes,
    )

    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT"
        }
    }

    for path in openapi_schema["paths"].values():
        for method in path.values():
            method["security"] = [{"BearerAuth": []}]

    app.openapi_schema = openapi_schema
    return app.openapi_schema
