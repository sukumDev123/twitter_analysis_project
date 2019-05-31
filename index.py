from modules.controllers.twitter_api import TwitterAPI
from modules.controllers.twitter_auth import auth_session

if __name__ == "__main__":
    auth = auth_session()

    api = TwitterAPI(auth)
    name = "nodejs"
    userTimeLines = api.get_user_timeline(name)
    print(userTimeLines)