from bson.objectid import ObjectId

from db import db

cards_collection = db.cards


def get_clear_card_item(card):
    """ Mongo has inconvenient format of id:
    '_id': ObjectId("60fbd0c0588d65e6872dc118")
    function get card object taken from mongo
    and returns card object with pretty id:
    'id': '60fbd0c0588d65e6872dc118'
    """
    card['id'] = str(card['_id'])
    card.pop('_id')
    return card


def get_all_cards(username):
    cards_cursor = cards_collection.find({
        'original_word': {'$exists': True},
        'username': username,
    })
    all_cards = list(cards_cursor)
    all_cards = [get_clear_card_item(card) for card in all_cards]
    return all_cards


def insert_card(original_word, translated_word, username):
    card = {
        'original_word': original_word,
        'translated_word': translated_word,
        'username': username,
        'pile_name': 'default',
    }
    inserted_card = cards_collection.insert_one(card)
    return str(inserted_card.inserted_id)


def update_card(id, original_word, translated_word):
    id = {'_id': ObjectId(id)}
    card = {
        '$set': {
            'original_word': original_word,
            'translated_word': translated_word,
        }
    }
    cards_collection.update_one(id, card)
    return {'result': 'ok'}


def delete_card(id):
    cards_collection.delete_one({'_id': ObjectId(id)})
    return {'result': 'ok'}


def move_card_to_pile(card_id, pile_name):
    cards_collection.update_one(
        {'_id': ObjectId(card_id)},
        {
            '$set': {'pile_name': pile_name},
        }
    )
    return {'result': 'ok'}
