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

    def is_user_authenticated(self, loggedIn, pk):
        pass


class follow:
    def __init__(self):
        self.followTextText = None

    def user_follow(self, user_pk, following_pk):
        try:
            UserJoin.objects.get(user_id=user_pk, following_id=following_pk).delete()
        except UserJoin.DoesNotExist:
            UserJoin.objects.create(user_id=user_pk, following_id=following_pk)

    def followText(self, user_pk, following_pk):
        try:
            UserJoin.objects.get(user_id=user_pk, following_id=following_pk)
            self.followTextText = "Undo Follow"
        except UserJoin.DoesNotExist:
            self.followTextText = "Follow"
        return self.followTextText


if __name__ == '__main__':
    pass
else:
    authentication = auth()
    followManager = follow()
