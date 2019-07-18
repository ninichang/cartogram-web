import mappackify
import web

for handler in web.cartogram_handlers:

    mappackify.mappackify(handler)