from models.user_model import User, db
from werkzeug.security import generate_password_hash, check_password_hash


class UserService:
    def add_user(self, form):

        user = User.query.filter_by(email=form.get('email')).first()

        if user:
            return None
        else:
            hash_password = generate_password_hash(form.get('password'),
                                                   method='pbkdf2:sha256',
                                                   salt_length=8)
            new_user = User(
                name=form.get('name'),
                email=form.get('email'),
                password=hash_password
            )

            db.session.add(new_user)
            db.session.commit()
            return new_user

    def login_user(self, password, email):

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                return user

        return None

    def get_user_by_id(self, user_id):
        return User.query.get(user_id)

