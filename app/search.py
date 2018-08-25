# -*- coding: utf-8 -*-
# -*- author: Jiangtao -*-

"""search module"""


from flask import current_app
from app import db


def add_to_index(index, model):
    """add to index with model"""
    if not current_app.elasticsearch:
        return
    payload = {}
    for field in model.__searchable__:
        payload[field] = getattr(model, field)
    current_app.elasticsearch.index(index=index, doc_type=index, id=model.id, body=payload)


def remove_from_index(index, model):
    """remove from index with model"""
    if not current_app.elasticsearch:
        return
    current_app.elasticsearch.delete(index=index, doc_type=index, id=model.id)


def query_index(index, query, page, per_page):
    """query index with page & per_page
    :return tuple(model.ids, total)
    """
    if not current_app.elasticsearch:
        return [], 0
    body = {
        "query": {"multi_match": {"query": query, "fields": ['*']}},
        "from": (page - 1) * per_page,
        "size": per_page,
    }
    search = current_app.elasticsearch.search(index=index, doc_type=index, body=body)
    ids = [int(hit['_id']) for hit in search['hits']['hits']]
    return ids, search['hits']['total']


class SearchableMixin:
    """mixin for searchable"""
    @classmethod
    def search(cls, expression, page, per_page):
        """convert result ids from es search to sqlalchemy objs with order of ids"""
        ids, total = query_index(cls.__tablename__, expression, page, per_page)
        if total == 0:
            return cls.query.filter_by(id=0), 0
        when = []
        for _i, _id in enumerate(ids):
            when.append((_id, _i))
        return cls.query.filter(cls.id.in_(ids)).order_by(db.case(when, value=cls.id)), total

    @classmethod
    def before_commit(cls, session):
        """handler before sqlalchemy session commit"""
        session._changes = {
            "add": list(session.new),
            "update": list(session.dirty),
            "delete": list(session.deleted)
        }

    @classmethod
    def after_commit(cls, session):
        """handler after sqlalchemy session commit"""
        for obj in session._changes["add"]:
            if isinstance(obj, SearchableMixin):
                add_to_index(obj.__tablename__, obj)
        for obj in session._changes["update"]:
            if isinstance(obj, SearchableMixin):
                add_to_index(obj.__tablename__, obj)
        for obj in session._changes["delete"]:
            if isinstance(obj, SearchableMixin):
                remove_from_index(obj.__tablename__, obj)
        session._changes = None

    @classmethod
    def reindex(cls):
        """reindex all sqlalchemy objs of the given table"""
        for obj in cls.query:
            add_to_index(obj.__tablename__, obj)