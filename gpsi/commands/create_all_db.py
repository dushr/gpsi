from gpsi import db
from gpsi.models import *

print db.drop_all()
print db.create_all()
