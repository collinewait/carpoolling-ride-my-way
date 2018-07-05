"""
This module handels requests to urls.
"""
from api.views import RideViews, RequestView
from api.auth.views import RegisterUser, LoginUser

class Urls(object):
    """
    Class to generate urls
    """
    @staticmethod
    def generate_url(app):
        """
         Generates urls on the app context
        :param: app: takes in the app variable
        :return: urls
        """
        ride_view = RideViews.as_view('ride_api')
        app.add_url_rule('/api/v1/rides/', defaults={'ride_id': None},
                         view_func=ride_view, methods=['GET',])

        app.add_url_rule('/api/v1/rides/<int:ride_id>', view_func=ride_view,
                         methods=['GET'])

        app.add_url_rule('/api/v1/rides/', defaults={'ride_id': None},
                         view_func=ride_view, methods=['POST',])

        app.add_url_rule('/api/v1/rides/<int:ride_id>/requests',
                         view_func=ride_view, methods=['POST',])

        app.add_url_rule('/api/v1/auth/signup/', view_func=RegisterUser.as_view('register_user'),
                         methods=["POST",])
        app.add_url_rule('/api/v1/auth/login/', view_func=LoginUser.as_view('login_user'),
                         methods=["POST",])
        app.add_url_rule('/api/v1/users/rides/<int:ride_id>/requests',
                         view_func=RequestView.as_view('all_requests'), methods=["GET",])
