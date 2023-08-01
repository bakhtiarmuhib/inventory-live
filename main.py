import strawberry
from strawberry.tools import create_type
from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter
from mutations.combineMutaion import mutations
from queries.combineQuerie import queries
from fastapi.staticfiles import StaticFiles



# create mutation types
Mutation = create_type("Mutation", mutations)

# create Query tyoe
Query = create_type("Query", queries)

schema = strawberry.federation.Schema(
    query=Query,
    mutation = Mutation
)





graphql_app = GraphQLRouter(schema)

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(graphql_app, prefix="/graphql")


