from ariadne import load_schema_from_path, make_executable_schema, snake_case_fallback_resolvers
from lib.api.mutations.mutations import mutations, resolve_upload_image
from lib.api.queries.queries import queries, resolve_get_images, resolve_get_image

mutations.set_field("uploadImage", resolve_upload_image)

queries.set_field("getImages", resolve_get_images)
queries.set_field("getImage", resolve_get_image)

type_defs = load_schema_from_path("schema.graphql")
schema = make_executable_schema(type_defs, [snake_case_fallback_resolvers, mutations, queries])

