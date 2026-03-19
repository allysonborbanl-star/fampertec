class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        public_prefixes = ("/admin/", "/static/", "/media/")
        public_paths = {"/", "/login/"}
        if request.path_info in public_paths or request.path_info.startswith(public_prefixes):
            return self.get_response(request)

        if not request.session.get("perfil_id"):
            return redirect("login")

        return self.get_response(request)
