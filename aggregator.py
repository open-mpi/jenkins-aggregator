import time

from celery import Celery
def make_celery(app):
    celery = Celery(app.import_name, broker=app.config['CELERY_BROKER_URL'])
    celery.conf.update(app.config)
    TaskBase = celery.Task
    class ContextTask(TaskBase):
        abstract = True
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)
    celery.Task = ContextTask
    return celery


from flask import Flask, request
flaskapp = Flask(__name__) # note: this variable can't just be named "app", that breaks Celery

flaskapp.config.update( # move to actual config file
    CELERY_BROKER_URL='amqp://guest@localhost', # ?
    CELERY_RESULT_BACKEND='amqp://guest@localhost'
)
celery = make_celery(flaskapp)

shas = {} # use Flask.g or whatever?

@celery.task
def emit(sha):
    # ...
    print "TODO"

@celery.task
def checkTimeout():
    now = time.time()

    for sha in shas.keys():
        if now - shas[sha][0] > 86400: # if the sha is past its 24 hour timeout window
            emit(sha)

@flaskapp.route("/", methods = ["GET", "POST"])
def aggregator():
    if request.method == "POST":
        timestamp = time.time()
        if len(request.form) > 0:
            data = request.form
        else: # figure out how to check for JSON
            data = request.get_json() # add try/catch
        # try/catch all of this
        context = data["context"]
        state = data["state"]
        description = data["description"]
        target = data["target_url"]
        sha = data["sha"]
       
        if not sha in shas:
            shas[sha] = [timestamp, {context: [state, description, target]}] # double check that I'm storing data, not references
        else:
            if state == "pending" and timestamp - shas[sha][0] > 900: # 900 seconds = 15 minutes = pending timeout window
                return "Just received pending status from context \"" + context + "\" outside of pending timeout window."
            if timestamp - shas[sha][0] > 86400: # 86400 seconds = 24 hours = final timeout window
                return "Just received status from context \"" + context + "\" outside of timeout window."
            if not state == "pending":
                if not context in shas[sha][1] or not shas[sha][1][context][0] == "pending": # we're receiving a final status from a context we haven't seen pending
                    return "Just received final status from context \"" + context + "\" without pending status first."
            shas[sha][1][context] = [state, description, target]
       
        # if we're past the pending window and all statuses are now final, emit

        return "Just received a POST request\nsha = " + sha + "\ntime = " + str(timestamp) + "\ntime offset = " + str(timestamp - shas[sha][0]) + "\ndata = " + str(shas[sha][1])
       
    if request.method == "GET":
        return "Just received a GET request"
   
    else: # should never execute
        return "Just received an invalid request"

if __name__ == "__main__":
    flaskapp.run(debug = True)