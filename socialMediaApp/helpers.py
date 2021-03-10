from .models import UserJoin

class auth:
    def __init__(self):
        self.state = {
            'loggedIn': False,
            'pk': None,
        }

    def getState(self):
        return self.state

    def setState(self, loggedIn, pk):
        state = self.state.copy()
        state['loggedIn'] = loggedIn
        state['pk'] = pk
        self.state = state

class follow:
    def __init__(self):
        self.state = {
            'followText': None,
        }

    def user_follow(self, user_pk, following_pk):
        state = self.state.copy()
        try:
            UserJoin.delete_join(user_pk, following_pk)
            state['followText'] = "Follow"
        except UserJoin.DoesNotExist:
            UserJoin.create_join(user_pk, following_pk)
            state['followText'] = "Undo Follow"




if __name__ == '__main__':
    pass
else:
    authentication = auth()
    followManager = follow()
