import unittest

from show.models import ShowContributor, Credit, Show

class ShowTestCase(unittest.TestCase):
    
    def test_get_primary_contributors(self):
        # create a show with some credits
        show = Show(title="title")
        show.save()
        contributor1 = ShowContributor(title="title")
        contributor1.save()
        contributor2 = ShowContributor(title="title")
        contributor2.save()
        contributor3 = ShowContributor(title="title")
        contributor3.save()
        Credit(show=show, contributor=contributor1, role=2).save()
        Credit(show=show, contributor=contributor2, role=10).save()
        Credit(show=show, contributor=contributor3, role=2).save()


        # result should only contain contributors with highest role. can contain multiples with 
        # highest role is not neccessarily 1
        primary_contributors = show.get_primary_contributors()
        self.failUnless(contributor1 in primary_contributors)
        self.failUnless(contributor3 in primary_contributors)
        self.failIf(contributor2 in primary_contributors)
    
    
    def test_is_contributor_name_in_title(self):
        # create a show with some credits
        show = Show(title="The Contributor Title Show")
        show.save()
        matching_contributor = ShowContributor(title="       ConTRIbutoR Title            ")
        matching_contributor.save()
        nonmatching_contributor = ShowContributor(title="  Foo Bar   ")
        nonmatching_contributor.save()

        # ignore case and leading/trailing whitespace. match on title
        self.failUnless(show.is_contributor_title_in_title(matching_contributor))
        
        # check for failure
        self.failIf(show.is_contributor_title_in_title(nonmatching_contributor))
