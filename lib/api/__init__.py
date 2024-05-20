from ariadne import load_schema_from_path, make_executable_schema, snake_case_fallback_resolvers

# ##
# Mutations
# ##
from lib.api.mutations.mutations import mutations
from lib.api.mutations.mutations import resolve_deploy_contract
from lib.api.mutations.mutations import resolve_upload_image
from lib.api.mutations.mutations import resolve_add_student
from lib.api.mutations.mutations import resolve_create_account, resolve_send_wei

# 
# Contract administration
mutations.set_field("deployContract", resolve_deploy_contract)

# 
# Image
mutations.set_field("uploadImage", resolve_upload_image)

# Student (Lab2)
mutations.set_field("addStudent", resolve_add_student)

# 
# Account administration
mutations.set_field("createAccount", resolve_create_account)
mutations.set_field("sendWei", resolve_send_wei)



# ##
# Queries
# ##
from lib.api.queries.queries import queries
from lib.api.queries.queries import resolve_get_images, resolve_get_image
from lib.api.queries.queries import resolve_get_students, resolve_can_join
from lib.api.queries.queries import resolve_get_accounts, resolve_get_balance, resolve_check_transaction
from lib.api.queries.queries import resolve_get_current_light_state, resolve_change_light

# 
# Image
queries.set_field("getImages", resolve_get_images)
queries.set_field("getImage", resolve_get_image)

# 
# Students
queries.set_field("getStudents", resolve_get_students)

# 
# Sticks
queries.set_field("canJoin", resolve_can_join)
# queries.set_field("gameEnded", resolve_game_ended)

# 
# Account administration
queries.set_field("getAccounts", resolve_get_accounts)
queries.set_field("getBalance", resolve_get_balance)
queries.set_field("checkTransaction", resolve_check_transaction)


# 
# Semaphore
queries.set_field("getCurrentSemaphoreState", resolve_get_current_light_state)
queries.set_field("changeLight", resolve_change_light)

# ##
# Load schema 
# ##
type_defs = load_schema_from_path("schema.graphql")
schema = make_executable_schema(type_defs, [snake_case_fallback_resolvers, mutations, queries])

