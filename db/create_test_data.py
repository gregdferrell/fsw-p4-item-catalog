#
# Story Time App
# Creates test data for the integration tests and development environment setup.
#

import json

import httplib2
import time

if __name__ == "__main__" and __package__ is None:
    from sys import path
    from os.path import dirname as dir

    path.append(dir(path[0]))
    __package__ = "db"


from storytime import story_time_service
from storytime.story_time_db_init import Category, Story, User, db_session


def delete_and_recreate_test_data():
    """
    Deletes and recreates Story Time test data.
    """
    try:
        # Delete all data
        for story in db_session.query(Story):
            story.categories = []
        num_rows_deleted = db_session.query(Story).delete()
        print('Deleted {} stories'.format(num_rows_deleted))
        num_rows_deleted = db_session.query(Category).delete()
        print('Deleted {} categories'.format(num_rows_deleted))
        num_rows_deleted = db_session.query(User).delete()
        print('Deleted {} users'.format(num_rows_deleted))
        db_session.commit()

        # Create test data
        # Users
        user_1 = story_time_service.create_user(
            User(name='gregdferrell', email='gferrell20@gmail.com', active=True))
        num_rows_created = db_session.query(User).count()
        print('Created {} users'.format(num_rows_created))

        # Categories
        cat_scary_id = story_time_service.create_category(Category(label='Scary', description='Eek, scary stories!'))
        cat_funny_id = story_time_service.create_category(Category(label='Funny', description='Funny stories :)'))
        cat_animal_id = story_time_service.create_category(
            Category(label='Animals', description='Stories about Animals'))
        cat_musical_id = story_time_service.create_category(
            Category(label='Musical', description='Musicals'))
        cat_history_id = story_time_service.create_category(
            Category(label='Nonfiction', description='True Stories'))
        cat_scary = story_time_service.get_category_by_id(category_id=cat_scary_id)
        cat_funny = story_time_service.get_category_by_id(category_id=cat_funny_id)
        cat_animal = story_time_service.get_category_by_id(category_id=cat_animal_id)
        cat_musical = story_time_service.get_category_by_id(category_id=cat_musical_id)
        cat_history = story_time_service.get_category_by_id(category_id=cat_history_id)
        num_rows_created = db_session.query(Category).count()
        print('Created {} categories'.format(num_rows_created))

        # Stories
        story_initial = Story(title='Story Time', description='A story about children writing and sharing stories with each other ...',
                          story_text='<REPLACE>',
                          published=True, user_id=user_1,
                          categories=[cat_funny, cat_animal])
        story_zoo_id = story_time_service.create_story(story_initial)

        # Update story text for each story from lipsum generator (every second so we don't hit server too hard)
        url = 'https://lipsum.com/feed/json?what=paras&amount=5&start=yes'
        for story in db_session.query(Story).all():
            h = httplib2.Http()
            json_result = json.loads(str(h.request(url, 'GET')[1], 'utf-8'))
            story.story_text = json_result['feed']['lipsum']
            db_session.add(story)
            db_session.commit()
            time.sleep(1)

        num_rows_created = db_session.query(Story).count()
        print('Created {} stories'.format(num_rows_created))

        db_session.commit()
    except Exception as exc:
        print('Error creating test data:')
        print(exc)
        db_session.rollback()


if __name__ == '__main__':
    delete_and_recreate_test_data()
