class DisableCSRFMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Deshabilitar CSRF para APIs (métodos POST, PUT, PATCH, DELETE)
        if request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
            setattr(request, '_dont_enforce_csrf_checks', True)
        return self.get_response(request)
