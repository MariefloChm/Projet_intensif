# context_processors.py

def theme_processor(request):
    # Déterminez le thème ici, par exemple en vérifiant la session
    theme = request.session.get('theme', 'light-mode')  # 'light-mode' est la valeur par défaut
    return {'theme': theme}
