from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from djongo import models
from django.db import connection

from bson.objectid import ObjectId

from django.conf import settings

from pymongo import MongoClient

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        # Connect to MongoDB
        client = MongoClient('mongodb://localhost:27017')
        db = client['octofit_db']

        # Clean up collections
        db.users.delete_many({})
        db.teams.delete_many({})
        db.activities.delete_many({})
        db.leaderboard.delete_many({})
        db.workouts.delete_many({})

        # Teams
        marvel_id = ObjectId()
        dc_id = ObjectId()
        teams = [
            {'_id': marvel_id, 'name': 'Marvel'},
            {'_id': dc_id, 'name': 'DC'}
        ]
        db.teams.insert_many(teams)

        # Users (superheroes)
        users = [
            {'name': 'Iron Man', 'email': 'ironman@marvel.com', 'team_id': marvel_id},
            {'name': 'Captain America', 'email': 'cap@marvel.com', 'team_id': marvel_id},
            {'name': 'Spider-Man', 'email': 'spiderman@marvel.com', 'team_id': marvel_id},
            {'name': 'Batman', 'email': 'batman@dc.com', 'team_id': dc_id},
            {'name': 'Superman', 'email': 'superman@dc.com', 'team_id': dc_id},
            {'name': 'Wonder Woman', 'email': 'wonderwoman@dc.com', 'team_id': dc_id},
        ]
        db.users.insert_many(users)

        # Activities
        activities = [
            {'user_email': 'ironman@marvel.com', 'type': 'run', 'distance': 5, 'duration': 30},
            {'user_email': 'cap@marvel.com', 'type': 'cycle', 'distance': 20, 'duration': 60},
            {'user_email': 'spiderman@marvel.com', 'type': 'swim', 'distance': 2, 'duration': 40},
            {'user_email': 'batman@dc.com', 'type': 'run', 'distance': 10, 'duration': 50},
            {'user_email': 'superman@dc.com', 'type': 'fly', 'distance': 100, 'duration': 10},
            {'user_email': 'wonderwoman@dc.com', 'type': 'cycle', 'distance': 15, 'duration': 45},
        ]
        db.activities.insert_many(activities)

        # Workouts
        workouts = [
            {'name': 'Morning Cardio', 'description': 'Cardio session for all'},
            {'name': 'Strength Training', 'description': 'Strength and resistance'},
        ]
        db.workouts.insert_many(workouts)

        # Leaderboard
        leaderboard = [
            {'team_id': marvel_id, 'points': 150},
            {'team_id': dc_id, 'points': 170},
        ]
        db.leaderboard.insert_many(leaderboard)

        # Ensure unique index on email
        db.users.create_index([('email', 1)], unique=True)

        self.stdout.write(self.style.SUCCESS('octofit_db database populated with test data.'))
