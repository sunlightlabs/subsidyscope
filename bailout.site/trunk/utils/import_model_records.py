import sys
from utils.logger import Logger
# from django.core.exceptions import ValidationError

# from django. import IntegrityError

def import_model_records(model, records, log=Logger()):
    record_count = 0
    for record in records:
        instance = model()
        for field in record:
            setattr(instance, field, record[field])
        try:
            instance.save()
        except Exception:
            # It would be better to catch DatabaseError or IntegrityError
            # instead!  However, I am not sure how to import those, since
            # they vary across database backend types.
            import traceback
            traceback.print_exc(1)
            sys.exit(1)
        record_count += 1
    log.info("%s records imported into %s" % \
        (record_count, model.__name__), 1)
