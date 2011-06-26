# -*- coding: utf-8 -*-

"""
legit.models
~~~~~~~~~~~~
"""


class Branch(object):
    """A Git Branch."""

    def __init__(self):
        self.ref = None
        self.name = None
        self.is_remote = False
        self.remote = None

    def __repr__(self):
        return '<branch name="{0}">'.format(self.name)


    @staticmethod
    def new_from_ref(ref):

        branch = Branch()

        branch.ref = ref

        if ref.startswith('refs/heads/'):
            branch.name = ref[11:]

        elif ref.startswith('refs/remotes/'):
            branch.is_remote = True

            base_name = ref.split('/')

            branch.remote = base_name[2]
            branch.name = '/'.join(base_name[3:])
        else:
            # print '!'
            pass

        return branch



class Branches(object):
    """A set of Branches."""

    def __init__(self, branches):
        self.data = branches


    @property
    def published(self):
        return self.data


    @property
    def unpublished(self):
        pass