import yaml

def custom_openapi():
    with open("src/docs/openapi.yaml") as file:
        openapi = yaml.load(file, Loader=yaml.FullLoader)
    return openapi
