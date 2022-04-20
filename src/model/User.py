from werkzeug.security import check_password_hash, generate_password_hash
from itsdangerous import TimedSerializer as Serializer, SignatureExpired, BadSignature
import config
from src.controllers import ctrl_users

class User():
    def __init__(self, email, name, password) -> None:
        self.email = email
        self.name = name
        self.password = password

    #Password encryption
    @staticmethod
    def hash_password(self, password):
        self.password = generate_password_hash(password)

    @staticmethod
    #Password resolution
    def verify_password(self, password):
        return check_password_hash(password, self.password)

    #Get token
    @staticmethod
    def generate_auth_token(email):
        print(config.Config.SECRET_KEY)
        s = Serializer('secret')
        return s.dumps({ 'email': email })

    #Resolve the token to confirm the login user identity
    @staticmethod
    def verify_auth_token(token):
        s = Serializer('secret')
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None # valid token, but expired
        except BadSignature:
            return None # invalid token
        return ctrl_users.get_user(data['email'])
