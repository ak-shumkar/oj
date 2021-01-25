from .models import ContestRating, Contest


class Elo:
    def __init__(self, contest_id):
        self.contest_id = contest_id
        self.ratings = ContestRating.objects.get(contest_id=contest_id)
        # self.contest =
