
from shemas.shemas import ProductAdd
import uuid

def session_create(product_add:ProductAdd):
    if product_add.session_id is None:
        session_id = str(uuid.uuid4())
        product_add.response.set_cookie(key="session_id", value=session_id)
        product_add.session_id = session_id
        return {"session_id": session_id}
