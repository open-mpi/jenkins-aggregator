from django.db import models

class Commit(models.Model):
    pullID = models.IntegerField()
    sha = models.CharField(max_length = 200) # TODO more accurate max length?
    triggerTime = models.DateTimeField() # time of triggering event (e.g., commit, "bot:retest" comment) on GitHub
    # note: Django automatically creates Commit.resultset_set because ResultSet has a ForeignKey relation back to Commit
    # TODO add URL back to GitHub thread
    
    def __unicode__(self):
        return "TODO" # TODO how to put Fields (esp. DateTimeField) into formatted string? How many characters from pullID and sha to include?
        
    def passed(self):
        p = True
        for result in self.resultset_set.all(): 
            if result.passed == False:
                p = False
                # TODO break loop, since continuing is unnecessary?
        return p
    
    
class ResultSet(models.Model):
    commit = models.ForeignKey(Commit)
    sourceID = models.CharField(max_length = 200) # TODO "
    timeReceived = models.DateTimeField()
    passed = models.BooleanField(default = False) # TODO should this be a method instead?
    # autogenerated: testresult_set
    # TODO add optional URL to institutional Jenkins site?
    rawResults = models.FileField() # TODO make private (how do in Python?) Is FileField best storage object available?
    
    def __unicode__(self):
        return "TODO" # TODO sourceID + timeReceived?
        
    
class TestResult(models.Model):
    resultSet = models.ForeignKey(ResultSet)
    passed = models.BooleanField()
    skipped = models.BooleanField()
    description = models.CharField(max_length = 200) # TODO "
    output = models.CharField(max_length = 200) # TODO "
    
    def __unicode__(self):
        return "TODO" # description or some placeholder if description is missing?
