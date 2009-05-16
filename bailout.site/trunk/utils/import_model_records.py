import sys
from utils.logger import Logger


def import_model_records(model, records, log=Logger()):
    """
    Imports a list of dictionaries specified by the 'records'
    parameter into the model specified by the 'model' parameter.
    The 'log' parameter is optional.
    """
    record_count = 0
    for record in records:
        instance = model()
        for field in record:
            setattr(instance, field, record[field])
        try:
            instance.save()
        except Exception:
            # I would prefer catching DatabaseError or IntegrityError
            # instead.  At this point, I am unsure on how to import those,
            # since they vary across database backend types.
            import traceback

            # Display one line of traceback.  This is enough to clue in
            # the user as to what went wrong, but not so much that it is
            # overwhelming.
            traceback.print_exc(1)
            sys.exit(1)
        record_count += 1
    log.info("%s records imported into the '%s' model" % \
        (record_count, model.__name__), 1)
