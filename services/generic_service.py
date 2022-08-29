from redis_om import JsonModel
from lib.service_error_handler import service_error_handler

class GenericService:
    def __init__(self, model: JsonModel, formatter = None) -> None:
        self.Model = model
        if not formatter:
            self.format_model = lambda model: model.dict() 
        else:
            self.format_model = formatter 

    @service_error_handler
    def get_all(self, limit: int = 10):
        # models_found = [self.format_model(self.Model.get(pk)) for pk in self.Model.all_pks()]
        models_pks = self.Model.all_pks()
        if not models_pks:
            raise Exception("No models to show")
        models_found = [self.format_model(self.Model.get(pk)) for pk in models_pks]
        return (models_found[:limit], None)
    
    @service_error_handler
    def get_by_pk(self, pk: str):
        return (self.format_model(self.Model.get(pk)), None)

    @service_error_handler
    def delete_by_pk(self, pk: str):
        model = self.Model.get(pk)
        self.Model.delete(pk)
        return (self.format_model(model), None)