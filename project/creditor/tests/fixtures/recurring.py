# -*- coding: utf-8 -*-
import random
import factory.django, factory.fuzzy
from members.models import Member
from creditor.models import TransactionTag, RecurringTransaction
from .tags import TransactionTagFactory


class RecurringTransactionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'creditor.RecurringTransaction'
        django_get_or_create = ('tag', 'owner')

    rtype = factory.fuzzy.FuzzyChoice(RecurringTransaction.RTYPE_READABLE.keys())
    owner = factory.fuzzy.FuzzyChoice(Member.objects.all())
    tag = factory.fuzzy.FuzzyChoice(TransactionTag.objects.all())
    amount = factory.fuzzy.FuzzyInteger(-40, -10, 5)
    start = factory.LazyAttribute(lambda t: factory.fuzzy.FuzzyDate(t.owner.accepted).fuzz())


class MembershipfeeFactory(RecurringTransactionFactory):
    tag = factory.SubFactory(TransactionTagFactory, label='Membership fee', tmatch='1')
    rtype = RecurringTransaction.YEARLY
    amount = -28
    start = factory.LazyAttribute(lambda t: t.owner.accepted)


class KeyholderfeeFactory(RecurringTransactionFactory):
    tag = factory.SubFactory(TransactionTagFactory, label='Keyholder fee', tmatch='2')
    rtype = RecurringTransaction.MONTHLY
    amount = factory.fuzzy.FuzzyInteger(-40, -20, 10)
    owner = factory.fuzzy.FuzzyChoice(Member.objects.filter(access_granted__atype__bit=0)) # TODO: Should we limit this like so ??


def Membershipfee4all(output=False):
    for m in Member.objects.all():
        rt = MembershipfeeFactory(owner=m)
        if output:
            print("Generated RecurringTransaction %s" % rt)
