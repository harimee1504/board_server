import os
import glob
from ariadne import gql
from ariadne import QueryType, MutationType
import importlib

def load_schemas(graphql_dir):
    """Load and concatenate all .graphql files into a single schema string."""
    schema_parts = []
    for file_path in glob.glob(f"{graphql_dir}/**/*.graphql", recursive=True):
        with open(file_path, 'r') as f:
            schema_parts.append(f.read())
    return gql("\n".join(schema_parts))


def load_resolvers(graphql_dir):
    """Load and aggregate resolvers from queries.py and mutations.py."""
    combined_query_resolvers = {}
    combined_mutation_resolvers = {}

    for dir_path in [os.path.dirname(f) for f in glob.glob(f"{graphql_dir}/**/queries.py", recursive=True)]:
        module_name = os.path.basename(dir_path)
        module_path = f"{graphql_dir.replace('/', '.')}.{module_name}"
        
        try:
            # Import query resolvers
            queries = importlib.import_module(f"{module_path}.queries")
            if hasattr(queries, "resolvers") and isinstance(queries.resolvers, list):
                for resolver in queries.resolvers:
                    if isinstance(resolver._resolvers, dict):
                        combined_query_resolvers.update(resolver._resolvers)
            
            # Import mutation resolvers
            mutations = importlib.import_module(f"{module_path}.mutations")
            if hasattr(mutations, "resolvers") and isinstance(mutations.resolvers, list):
                for resolver in mutations.resolvers:
                    if isinstance(resolver._resolvers, dict):
                        combined_mutation_resolvers.update(resolver._resolvers)

        except ModuleNotFoundError as e:
            print(f"Warning: Could not import resolvers from {module_path}: {e}")

    query = QueryType()
    mutation = MutationType()

    for field, resolver in combined_query_resolvers.items():
        query.set_field(field, resolver)
    for field, resolver in combined_mutation_resolvers.items():
        mutation.set_field(field, resolver)

    return query, mutation


from ariadne import make_executable_schema

def create_schema():
    graphql_dir = "api/graphql"  # Root directory for GraphQL files
    schema_str = load_schemas(graphql_dir)
    query, mutation = load_resolvers(graphql_dir)
    return make_executable_schema(schema_str, query, mutation)