from .models import *
from .exceptions import *
from django.db.models import *


def create_group(user_id, name, member_ids):
    user_ids=list(User.objects.values_list("id",flat=True))
    member_ids=set(member_ids)
    if user_id not in user_ids:
        raise InvalidUserException
    if not name:
        raise InvalidGroupNameException
    for member_id in member_ids:
        if member_id not in user_ids:
            raise InvalidMemberException
    if user_id in member_ids:
        member_ids.remove(user_id)
    group=Group.objects.create(name=name)
    memberships=[
        Membership(group=group,member_id=member_id,is_admin=False)
        for member_id in member_ids
    ]
    memberships.append(Membership(group=group,member_id=user_id,is_admin=True))
    Membership.objects.bulk_create(memberships)
    return group.id


def add_member_to_group(user_id, new_member_id, group_id):
    user_ids=list(User.objects.values_list("id",flat=True))
    if user_id not in user_ids:
        raise InvalidUserException
    if new_member_id not in user_ids:
            raise InvalidMemberException
    group=Group.objects.filter(id=group_id)
    if not group:
            raise InvalidGroupException
    member_ids=list(group[0].members.values_list("id",flat=True))
    if user_id not in member_ids:
        raise UserNotInGroupException
    queryset=Membership.objects.filter(Q(group_id=group_id)&Q(is_admin=True)&Q(member_id=user_id))

    if not queryset:
        raise UserIsNotAdminException

    if new_member_id not in member_ids:
        queryset=Membership.objects.create(group_id=group_id,is_admin=False,member_id=new_member_id)

def remove_member_from_group(user_id, member_id, group_id):
    user_ids=list(User.objects.values_list("id",flat=True))
    if user_id not in user_ids:
        raise InvalidUserException
    if member_id not in user_ids:
            raise InvalidMemberException
    group=Group.objects.filter(id=group_id)
    if not group:
            raise InvalidGroupException
    member_ids=list(group[0].members.values_list("id",flat=True))
    if user_id not in member_ids :
        raise UserNotInGroupException
    if member_id not in member_ids:
        raise MemberNotInGroupException
    queryset=Membership.objects.filter(Q(group_id=group_id)&Q(is_admin=True)&Q(member_id=user_id))

    if not queryset:
        raise UserIsNotAdminException
    group[0].members.clear()

def make_member_as_admin(user_id, member_id, group_id):
    user_ids=list(User.objects.values_list("id",flat=True))
    if user_id not in user_ids:
        raise InvalidUserException
    if member_id not in user_ids:
            raise InvalidMemberException
    group=Group.objects.filter(id=group_id)
    if not group:
            raise InvalidGroupException
    member_ids=list(group[0].members.values_list("id",flat=True))
    if user_id not in member_ids :
        raise UserNotInGroupException
    if member_id not in member_ids:
        raise MemberNotInGroupException


    if not queryset:
        raise UserIsNotAdminException
    queryset[0].is_admin=True
    queryset[0].save()


def create_post(user_id, post_content, group_id=None):
    user_ids=list(User.objects.values_list("id",flat=True))
    if user_id not in user_ids:
        raise InvalidUserException
    if not post_content:
        raise InvalidPostContent
    if group_id==None:
        Post.objects.create(content=post_content,posted_by_id=user_id)
    else:
        group=Group.objects.filter(id=group_id)
        if not group:
            raise InvalidGroupException
        member_ids=list(group[0].members.values_list("id",flat=True))
        if user_id not in member_ids :
            raise UserNotInGroupException
        Post.objects.create(content=post_content,posted_by_id=user_id,group_id=group_id)


def get_group_feed(user_id, group_id, offset, limit):
    pass


def get_posts_with_more_comments_than_reactions():
    pass
