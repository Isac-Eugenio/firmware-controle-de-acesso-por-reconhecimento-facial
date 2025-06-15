sobre o erro - AttributeError: module 'bcrypt' has no attribute '__about__':
    substitua a linha do erro em bcrypt.py "version = _bcrypt.__about__.__version__ " por 
    "version = getattr(_bcrypt, "__version__", None)"
