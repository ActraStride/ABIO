"""
Core Application Errors

Este módulo define los errores base para la aplicación de scraping de Wikipedia.
"""

class ApplicationError(Exception):
    """Excepción base para toda la aplicación."""
    pass

class LoggingSetupError(ApplicationError):
    """Se lanza cuando ocurre un error en la configuración del logging."""
    pass

__all__ = ["ApplicationError", "LoggingSetupError"]
