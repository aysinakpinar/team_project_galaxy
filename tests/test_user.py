# import pytest
# from models.user import UserModel
# from extension import db
# from tests.factories import create_user

# # def test_create_user(app, database):
# #     with app.app_context():
# #         user = UserModel(
# #             username = "Frank",
# #             password = "password123",
# #             email = "frank@example.com",
# #             location = "London"
# #         )
# #     db.session.add(user)
# #     db.session.commit()
    
# #     saved_user = UserModel.query.filter_by(username = "Frank").first()
# #     assert user.id is not None
# #     assert user.location == "London"
# #     assert user.email == "frank@example.com"



# # def test_create_user2(app, database):
# #     with app.app_context():
# #         user = create_user("Frank", "frank@example.com", 123456780)

# #         saved_user = UserModel.query.filter_by(username="Frank").first()
# #         assert saved_user.id is not None
# #         assert saved_user.phone_number == 123456780
# #         assert saved_user.email == "frank@example.com"


    
# # def test_unique_user_details2(app, database):
# #     with app.app_context():
# #         user = create_user("Frank", "frank@example.com", 123456780)
# #         #verify Frank has been created
# #         assert UserModel.query.filter_by(username = "Frank").first() is not None
# #         # Try creating a user with same email
# #         with pytest.raises(Exception, match="duplicate key value violates unique constraint"):
# #             user = create_user("Arthur", "frank@example.com", 234567890)
# #         db.session.rollback()
# #         # Try creating a user with same username
# #         # with pytest.raises(Exception, match="duplicate key value violates unique constraint"):
# #         #     user3 = UserModel(
# #         #         username = "Frank",
# #         #         password = "password123",
# #         #         email = "alister@example.com",
# #         #         phone_number = 111111111
# #         #     )
# #         #     db.session.add(user3)
# #         #     db.session.commit()
# #         # db.session.rollback()
# #         # # Try creating a user with same phone number
# #         # with pytest.raises(Exception, match="duplicate key value violates unique constraint"):
# #         #     user4 = UserModel(
# #         #         username = "Alister",
# #         #         password = "password123",
# #         #         email = "louis@example.com",
# #         #         phone_number = 123456780
# #         #     )
# #         #     db.session.add(user4)
# #         #     db.session.commit()
# #         # db.session.rollback()
# #         assert UserModel.query.count() == 1, f"Expected 1 user, found {UserModel.query.count()}"