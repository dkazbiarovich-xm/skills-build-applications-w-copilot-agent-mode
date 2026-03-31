from django.core.management.base import BaseCommand
from octofit_tracker.models import User, Team, Activity, LeaderboardEntry, Workout
from django.db import transaction

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        with transaction.atomic():
            self.stdout.write(self.style.WARNING('Deleting old data...'))
            Activity.objects.all().delete()
            LeaderboardEntry.objects.all().delete()
            Workout.objects.all().delete()
            Team.objects.all().delete()
            User.objects.exclude(is_superuser=True).delete()

            self.stdout.write(self.style.SUCCESS('Creating users...'))
            marvel_heroes = [
                {'username': 'ironman', 'email': 'ironman@marvel.com'},
                {'username': 'captainamerica', 'email': 'cap@marvel.com'},
                {'username': 'spiderman', 'email': 'spiderman@marvel.com'},
            ]
            dc_heroes = [
                {'username': 'batman', 'email': 'batman@dc.com'},
                {'username': 'superman', 'email': 'superman@dc.com'},
                {'username': 'wonderwoman', 'email': 'wonderwoman@dc.com'},
            ]
            marvel_users = [User.objects.create_user(**hero, password='password') for hero in marvel_heroes]
            dc_users = [User.objects.create_user(**hero, password='password') for hero in dc_heroes]

            self.stdout.write(self.style.SUCCESS('Creating teams...'))
            marvel_team = Team.objects.create(name='Marvel')
            marvel_team.members.set(marvel_users)
            dc_team = Team.objects.create(name='DC')
            dc_team.members.set(dc_users)

            self.stdout.write(self.style.SUCCESS('Creating activities...'))
            for user in marvel_users + dc_users:
                Activity.objects.create(
                    user=user,
                    activity_type='Running',
                    duration=30,
                    calories_burned=300,
                    date='2024-01-01',
                    team=marvel_team if user in marvel_users else dc_team
                )

            self.stdout.write(self.style.SUCCESS('Creating leaderboard entries...'))
            for user in marvel_users:
                LeaderboardEntry.objects.create(user=user, team=marvel_team, total_points=100)
            for user in dc_users:
                LeaderboardEntry.objects.create(user=user, team=dc_team, total_points=120)

            self.stdout.write(self.style.SUCCESS('Creating workouts...'))
            w1 = Workout.objects.create(name='Pushups', description='Do 20 pushups', difficulty='Easy')
            w2 = Workout.objects.create(name='Plank', description='Hold plank for 1 min', difficulty='Medium')
            w1.suggested_for.set(marvel_users)
            w2.suggested_for.set(dc_users)

            self.stdout.write(self.style.SUCCESS('Database populated with test data!'))
