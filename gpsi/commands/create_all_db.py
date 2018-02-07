from gpsi import db
from gpsi.models import * # noqa

print db.drop_all()
print db.create_all()
